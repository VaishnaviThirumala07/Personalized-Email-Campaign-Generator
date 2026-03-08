# 📧 Personalized Email Campaign Generator

### Agentic Marketing with LangGraph, Bayesian A/B Testing & MLOps

A production-grade GenAI system that automates the generation, testing, and optimization of marketing emails. Unlike static templates, this system uses a **multi-agent loop** to learn which copy resonates best with specific customer segments and iteratively improves its own prompts.

## 🚀 The Architecture

The core logic is powered by **LangGraph**, treating the campaign optimization as a stateful, cyclical process:

1. **Segment Analysis:** Ingests synthetic CRM data to understand customer personas.
2. **Variant Generation:** Uses **Few-Shot Prompting** (referenced from the Enron Email Dataset) to generate tailored variants.
3. **Simulated A/B Testing:** A "User Proxy" agent simulates engagement metrics (CTR/Open Rates).
4. **Bayesian Evaluation:** A statistical node determines the winning variant.
5. **Prompt Evolution:** The winning copy is used to refine the prompt for the next generation.

## 🛠️ Tech Stack

* **Orchestration:** LangGraph, LangChain
* **GenAI Models:** Gemini
* **Data Engineering:** DVC (Data Version Control), Pandas
* **API & Deployment:** FastAPI, Docker, GitHub Actions
* **MLOps:** MLflow (Experiment Tracking), Prometheus & Grafana (Monitoring)

## 📁 Project Structure

```text
├── app/                    # FastAPI REST API
├── langgraph_pipeline/     # Agentic Workflow (Nodes, State, Graph)
├── data/                   # Tracked by DVC (Enron snippets, CRM profiles)
├── prompts/                # Versioned Prompt Templates
├── monitoring/             # Grafana Dashboards & Prometheus Config
├── tests/                  # CI/CD Quality Gate Tests
└── mlflow_logs/            # Local MLflow Tracking

```

## ⚡ Key Features

* **Persona-Conditioned Generation:** Styles emails based on age, interests, and purchase history.
* **Bayesian Optimization:** Moves beyond simple A/B testing to understand the probability of a variant's success.
* **Automated MLOps Pipeline:** * **MLflow:** Logs prompt versions and CTR performance.
* **Grafana:** Visualizes variant win-rates across different segments in real-time.


* **Style Injection:** Uses the Enron dataset to maintain professional, human-like correspondence styles.

* **MLflow UI:** `http://localhost:5000`
* **Grafana Dashboard:** `http://localhost:3000`

---

**Would you like me to generate the `docker-compose.yml` file to help you spin up the MLflow, Prometheus, and FastAPI services simultaneously?**
