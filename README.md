# Personalized Email Campaign Generator with A/B Testing

>  A GenAI system that generates personalized marketing email variants, runs simulated A/B tests, learns which copy performs better per customer segment, and iteratively improves generation using LangGraph.

---

## 🏗️ Architecture

```
Customer Profile → [Segment] → [Generate Variants] → [Simulate A/B] → [Evaluate] → [Update Prompt]
                                       ↑                                    │
                                       └──── Loop (if no winner) ──────────┘
```

### Tech Stack

| Layer | Technology |
|---|---|
| **LLM Orchestration** | LangGraph, LangChain |
| **LLM Provider** | Gemini |
| **API** | FastAPI |
| **MLOps** | MLflow, DVC |
| **Monitoring** | Prometheus, Grafana |
| **Deployment** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional, for full stack)
- Gemini API key

### 1. Clone & Setup

```bash
git clone <repo-url>
cd ResumeProject
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API docs.

### 4. Run with Docker Compose (Full Stack)

```bash
docker-compose up --build
```

This starts:
- **API** at `http://localhost:8000`
- **MLflow** at `http://localhost:5000`
- **Prometheus** at `http://localhost:9090`
- **Grafana** at `http://localhost:3000` (admin/admin)

### 5. Run Tests

```bash
pytest tests/ -v
```

## 📊 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/generate` | Customer profile → best personalized email |
| `POST` | `/api/v1/campaign/run` | Run full A/B optimization for a segment |
| `GET` | `/api/v1/campaign/results/{segment}` | Segment-wise performance report |
| `GET` | `/api/v1/health` | Health check |

---
