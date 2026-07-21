import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Allow running from either repo root (backend.main:app) or backend dir (main:app).
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from backend.config import get_settings
from backend.api.routes import router
from backend.db.session import init_db
from backend.utils.logging import logger

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Energem backend...")
    try:
        init_db()
        logger.info("Database tables initialized")
    except Exception as e:
        logger.warning(f"Database init skipped: {e}")
    logger.info(f"Groq model configured: {settings.groq_model}")
    yield
    logger.info("Shutting down Energem backend...")


app = FastAPI(
    title="Energem",
    description="Energy Supply Chain Resilience System — Real-time disruption forecasting and procurement recommendations for India",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "app": "Energem",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "landing": "/api/landing",
            "corridors_status": "/api/corridors/status",
            "dashboard": "/api/dashboard",
            "risk": "/api/risk",
            "signals": "/api/signals",
            "signals_latest": "/api/signals/latest",
            "signals_refresh": "/api/signals/refresh",
            "scenario": "/api/scenario",
            "recommend": "/api/recommend",
            "market": "/api/market",
            "sanctions": "/api/sanctions",
            "news": "/api/news",
            "escalation": "/api/escalation",
            "escalation_assess": "/api/escalation/assess",
            "resilience": "/api/resilience",
            "resilience_assess": "/api/resilience/assess",
            "geospatial": "/api/geospatial",
            "compare": "/api/compare",
            "simulate": "/api/scenarios/simulate",
            "procurement_recommendations": "/api/procurement/recommendations",
            "procurement_authorize": "/api/procurement/authorize",
            "procurement_export_pptx": "/api/procurement/export/pptx",
            "dashboard_export_pdf": "/api/dashboard/export/pdf",
            "historical_comparison": "/api/signals/{signal_id}/historical-comparison",
        },
    }
