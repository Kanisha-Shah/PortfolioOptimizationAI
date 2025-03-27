from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)  # <-- Add this
    risk_tolerance = Column(String, default="medium")
    goals = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    holdings = relationship("Holding", back_populates="owner", cascade="all, delete-orphan")

class Holding(Base):
    __tablename__ = "holdings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String, index=True)
    quantity = Column(Float)
    purchase_price = Column(Float)
    purchase_date = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="holdings")