from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.core.logging import logger

from app.api.v1 import (
    auth, users, contacts, sos, location,
    tracking, safety, checkins, guides,
    incidents, reports, evidence, assistant
)
from app.websocket import sos_tracking

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing AlertX2 database tables...")
    await init_db()
    logger.info("AlertX2 API engine online.")
    yield
    logger.info("AlertX2 shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    description="AlertX2 Mission-Critical Personal Safety & Emergency Response Engine",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 Mounts
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["Users & Profiles"])
app.include_router(contacts.router, prefix=f"{settings.API_V1_PREFIX}/contacts", tags=["Emergency Contacts"])
app.include_router(sos.router, prefix=f"{settings.API_V1_PREFIX}/sos", tags=["SOS Dispatch"])
app.include_router(location.router, prefix=f"{settings.API_V1_PREFIX}/location", tags=["Location Telemetry"])
app.include_router(tracking.router, prefix=f"{settings.API_V1_PREFIX}/tracking", tags=["Public Live Tracking"])
app.include_router(safety.router, prefix=f"{settings.API_V1_PREFIX}/safety", tags=["Safety Timers"])
app.include_router(checkins.router, prefix=f"{settings.API_V1_PREFIX}/checkins", tags=["Safety Check-ins"])
app.include_router(guides.router, prefix=f"{settings.API_V1_PREFIX}/guides", tags=["Emergency Guides"])
app.include_router(incidents.router, prefix=f"{settings.API_V1_PREFIX}/incidents", tags=["Incident History"])
app.include_router(reports.router, prefix=f"{settings.API_V1_PREFIX}/reports", tags=["Community Incident Reports"])
app.include_router(evidence.router, prefix=f"{settings.API_V1_PREFIX}/evidence", tags=["Evidence Vault"])
app.include_router(assistant.router, prefix=f"{settings.API_V1_PREFIX}/assistant", tags=["AI Safety Assistant"])

# WebSocket Mounts
app.include_router(sos_tracking.router, tags=["WebSockets"])

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "2.0.0",
        "environment": settings.ENVIRONMENT
    }
