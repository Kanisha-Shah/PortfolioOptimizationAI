from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import datetime
import os
import tempfile

from database.session import SessionLocal
from database.models import User, Holding
from agents.orchestrator import PipelineOrchestrator  # New import

router = APIRouter()
load_dotenv()

class HoldingSchema(BaseModel):
    symbol: str
    quantity: float
    purchase_price: float

class UserSchema(BaseModel):
    name: str
    risk_tolerance: Optional[str] = "medium"
    goals: Optional[str] = None
    holdings: List[HoldingSchema] = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/user", response_model=UserSchema)
def create_or_update_user(user: UserSchema, db: Session = Depends(get_db)):
    # Check if the user already exists
    db_user = db.query(User).filter(User.name == user.name).first()
    if db_user:
        db_user.risk_tolerance = user.risk_tolerance
        db_user.goals = user.goals
        db.query(Holding).filter(Holding.user_id == db_user.id).delete()
        for holding in user.holdings:
            db_holding = Holding(
                user_id=db_user.id,
                symbol=holding.symbol,
                quantity=holding.quantity,
                purchase_price=holding.purchase_price
            )
            db.add(db_holding)
        db.commit()
        db.refresh(db_user)
        return user
    else:
        new_user = User(
            name=user.name,
            risk_tolerance=user.risk_tolerance,
            goals=user.goals
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        for holding in user.holdings:
            db_holding = Holding(
                user_id=new_user.id,
                symbol=holding.symbol,
                quantity=holding.quantity,
                purchase_price=holding.purchase_price
            )
            db.add(db_holding)
        db.commit()
        return user

@router.get("/user/{name}", response_model=UserSchema)
def get_user(name: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == name).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    holdings = [
        HoldingSchema(
            symbol=holding.symbol,
            quantity=holding.quantity,
            purchase_price=holding.purchase_price
        )
        for holding in db_user.holdings
    ]
    return UserSchema(
        name=db_user.name,
        risk_tolerance=db_user.risk_tolerance,
        goals=db_user.goals,
        holdings=holdings
    )

@router.post("/run-pipeline")
def run_pipeline(user: UserSchema, db: Session = Depends(get_db)):
    """
    Executes the full pipeline:
      1. Creates/updates the user and holdings in the DB.
      2. Runs portfolio analysis (fetching current prices and computing profit/loss).
      3. Runs portfolio optimization via an LLM.
      4. Generates a one‑page PDF report.
    """
    # Create or update the user record (using the same function as /user endpoint)
    create_or_update_user(user, db)
    
    # Prepare holdings data from the user input
    holdings = []
    for h in user.holdings:
        holdings.append({
            "symbol": h.symbol,
            "quantity": h.quantity,
            "purchase_price": h.purchase_price
        })
    
    # Initialize the orchestrator (which internally connects all agents)
    openai_api_key = os.getenv("OPENAI_API_KEY")
    orchestrator = PipelineOrchestrator(openai_api_key=openai_api_key)
    
    # Run the pipeline to generate PDF bytes
    pdf_bytes = orchestrator.run_pipeline(holdings, user.risk_tolerance)
    
    # Create "Reports" folder if it doesn't exist
    reports_folder = "Reports"
    os.makedirs(reports_folder, exist_ok=True)
    
    # Build filename: Username_Report_YYYYMMDD.pdf
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"{user.name}_Report_{today_str}.pdf"
    file_path = os.path.join(reports_folder, filename)
    
    # Write PDF bytes to file
    with open(file_path, "wb") as f:
        f.write(pdf_bytes)

    return FileResponse(file_path, media_type="application/pdf", filename=filename)