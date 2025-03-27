from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.session import init_db
from api.auth import router as auth_router
from api.routes import router as api_router

app = FastAPI(
    title="Portfolio AI Optimization",
    description="API for the Portfolio AI Optimization project with Authentication",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(api_router, prefix="/api", tags=["Main"])

@app.get("/")
def root():
    return {"message": "Welcome to the Portfolio AI Optimization API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)