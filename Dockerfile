# ============================================
# Dockerfile — Personalized Email Campaign Generator
# ============================================

# ── Stage 1: Base ──────────────────────────────────
FROM python:3.11-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ── Stage 2: Dependencies ─────────────────────────
FROM base as dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Stage 3: Application ──────────────────────────
FROM dependencies as application

# Copy application code
COPY app/ app/
COPY langgraph_pipeline/ langgraph_pipeline/
COPY prompts/ prompts/
COPY data/processed/ data/processed/
COPY monitoring/ monitoring/

# Expose ports
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
