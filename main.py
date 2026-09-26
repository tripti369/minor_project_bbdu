"""
main.py
=======
FastAPI application entrypoint for the Predictive Intelligence Engine.

Run with (from the backend/ folder):
    uvicorn app.main:app --reload --port 8000

Or simply:
    python run.py
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import predict, analysis, scenario, upload, knowledge, history, datasets

app = FastAPI(
    title="Predictive Intelligence Engine API",
    description="Real-data backend powering forecasting, churn/attrition analysis, "
                 "Monte Carlo scenario simulation, CSV upload and a lightweight RAG knowledge base.",
    version="1.0.0",
)

cors_origins = os.getenv("CORS_ORIGINS", "*")
allow_origins = ["*"] if cors_origins.strip() == "*" else [o.strip() for o in cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Predictive Intelligence Engine API is running",
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    return {"status": "healthy"}


app.include_router(predict.router, prefix="/api", tags=["Predict"])
app.include_router(analysis.router, prefix="/api", tags=["Analysis"])
app.include_router(scenario.router, prefix="/api", tags=["Scenario"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(knowledge.router, prefix="/api", tags=["Knowledge / RAG"])
app.include_router(history.router, prefix="/api", tags=["History"])
app.include_router(datasets.router, prefix="/api", tags=["Datasets"])
