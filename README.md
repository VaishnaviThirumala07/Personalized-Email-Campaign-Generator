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
| **LLM Provider** | OpenAI / Anthropic |
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
- OpenAI or Anthropic API key

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

---

## 📁 Project Structure

```
ResumeProject/
├── app/                        # FastAPI application
│   ├── api/                    # REST API routes
│   ├── core/config.py          # Settings (Pydantic BaseSettings)
│   ├── models/schemas.py       # Request/response Pydantic models
│   └── main.py                 # FastAPI entry point
├── langgraph_pipeline/         # LangGraph workflow
│   ├── nodes/                  # Individual graph nodes
│   │   ├── segment.py          # Customer segmentation
│   │   ├── generate.py         # LLM email variant generation
│   │   ├── simulate.py         # A/B test simulation
│   │   ├── evaluate.py         # Bayesian evaluation
│   │   └── update_prompt.py    # Prompt evolution
│   ├── state.py                # Graph state definition
│   └── graph.py                # Graph construction
├── data/                       # Datasets (DVC-tracked)
│   ├── raw/                    # Raw Enron emails
│   ├── processed/              # Cleaned data + CRM profiles
│   └── scripts/                # Data processing scripts
├── prompts/                    # Prompt templates & few-shot examples
├── tests/                      # Test suite
├── monitoring/                 # Prometheus + Grafana configs
├── .github/workflows/ci.yml    # GitHub Actions CI
├── Dockerfile                  # Container image
├── docker-compose.yml          # Full stack orchestration
├── dvc.yaml                    # DVC pipeline definition
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/generate` | Customer profile → best personalized email |
| `POST` | `/api/v1/campaign/run` | Run full A/B optimization for a segment |
| `GET` | `/api/v1/campaign/results/{segment}` | Segment-wise performance report |
| `GET` | `/api/v1/health` | Health check |

---

## 📄 License

This project is for educational and portfolio purposes.
