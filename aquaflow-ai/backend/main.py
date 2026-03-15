"""
AquaFlow AI — FastAPI Backend Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.routes import sensors, anomalies, alerts, reports
from backend.utils.database import init_db
from backend.utils.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="AquaFlow AI API",
    description="Intelligent water pipeline monitoring and anomaly detection",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensors.router, prefix="/api/sensors", tags=["Sensors"])
app.include_router(anomalies.router, prefix="/api/anomalies", tags=["Anomalies"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "service": "AquaFlow AI", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}
