"""
FastAPI application entry point.

Personalized Email Campaign Generator with A/B Testing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.config import settings
from app.models.schemas import HealthResponse
from app.api.routes import router as api_router

# ── App Initialization ──────────────────────────────────────────────
app = FastAPI(
    title="Personalized Email Campaign Generator",
    description=(
        "GenAI system that generates personalized marketing email variants, "
        "runs simulated A/B tests, and iteratively improves generation "
        "using LangGraph."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Middleware & Monitoring ───────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)


# ── Health Check ─────────────────────────────────────────────────────
@app.get("/api/v1/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check if the service is running."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        environment=settings.app_env,
    )


# ── Startup Event ────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print(f"🚀 Email Campaign Generator starting in {settings.app_env} mode")
    print(f"📊 MLflow tracking: {settings.mlflow_tracking_uri}")
    print(f"🤖 LLM provider: {settings.llm_provider} ({settings.llm_model})")


# ── API Routes (Linked in Phase 5&6) ────────────────────────────
app.include_router(api_router, prefix="/api/v1")
