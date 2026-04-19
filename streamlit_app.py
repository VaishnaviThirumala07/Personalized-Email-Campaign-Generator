"""
Streamlit Demo Interface — Personalized Email Campaign Generator.

A rich interactive UI that demonstrates the full LangGraph-powered
A/B testing pipeline: Segment → Generate → Simulate → Evaluate → Update.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
from datetime import datetime

# ── Page Configuration ─────────────────────────────────────────────
st.set_page_config(
    page_title="Email Campaign Generator",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS for Premium Design ──────────────────────────────────
st.markdown(
    """
<style>
    /* ── Global ─────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hero Section ──────────────────────── */
    .hero-container {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border-radius: 20px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 60%);
        animation: pulse-glow 4s ease-in-out infinite;
    }
    @keyframes pulse-glow {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.03em;
        margin-bottom: 0.3rem;
        position: relative;
        z-index: 1;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #a5b4fc;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }

    /* ── Metric Cards ──────────────────────── */
    .metric-card {
        background: linear-gradient(145deg, #1e1b4b 0%, #312e81 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.7);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.2);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }

    /* ── Email Preview Card ────────────────── */
    .email-card {
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .email-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15);
    }
    .email-card.winner {
        border-color: rgba(52, 211, 153, 0.6);
        background: linear-gradient(145deg, #064e3b 0%, #0f172a 100%);
    }
    .email-subject {
        font-size: 1.15rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }
    .email-body {
        font-size: 0.9rem;
        color: #94a3b8;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    .variant-badge {
        display: inline-block;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.2rem 0.75rem;
        border-radius: 20px;
        margin-bottom: 0.75rem;
        letter-spacing: 0.05em;
    }
    .variant-badge.winner-badge {
        background: linear-gradient(135deg, #10b981, #059669);
    }

    /* ── Pipeline Status ───────────────────── */
    .pipeline-step {
        background: rgba(30, 27, 75, 0.5);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .pipeline-step.active {
        border-color: rgba(99, 102, 241, 0.6);
        background: rgba(99, 102, 241, 0.1);
    }
    .pipeline-step.done {
        border-color: rgba(52, 211, 153, 0.5);
        background: rgba(52, 211, 153, 0.05);
    }
    .step-icon {
        font-size: 1.2rem;
    }
    .step-text {
        color: #e2e8f0;
        font-weight: 500;
        font-size: 0.9rem;
    }

    /* ── Sidebar Styling ───────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }

    /* ── General Improvements ──────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 20px;
    }
    div[data-testid="stExpander"] {
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ── Helper Functions ───────────────────────────────────────────────
def get_segment_config():
    """Get segment configurations with display info."""
    return {
        "young_professional": {
            "icon": "💼",
            "label": "Young Professional",
            "desc": "Tech-savvy, career-focused, ages 22-35",
        },
        "parent": {
            "icon": "👨‍👩‍👧‍👦",
            "label": "Parent",
            "desc": "Family-oriented, value-conscious",
        },
        "retiree": {
            "icon": "🏖️",
            "label": "Retiree",
            "desc": "Quality-focused, detail-oriented",
        },
        "student": {
            "icon": "🎓",
            "label": "Student",
            "desc": "Budget-conscious, trend-aware",
        },
        "executive": {
            "icon": "👔",
            "label": "Executive",
            "desc": "Time-pressed, ROI-focused",
        },
    }


def load_benchmarks():
    """Load segment benchmarks for display."""
    try:
        df = pd.read_csv("data/processed/benchmarks.csv")
        return df
    except Exception:
        return pd.DataFrame(
            {
                "segment": [
                    "young_professional",
                    "parent",
                    "retiree",
                    "student",
                    "executive",
                ],
                "base_open_rate": [0.35, 0.28, 0.42, 0.22, 0.38],
                "base_ctr": [0.08, 0.05, 0.10, 0.04, 0.07],
            }
        )


def run_demo_pipeline(profile: dict, campaign_goal: str, max_iterations: int):
    """
    Run the LangGraph pipeline and yield intermediate states for live display.
    Falls back to a simulated demo if the LLM is not configured.
    """
    try:
        from langgraph_pipeline.graph import build_campaign_graph

        graph = build_campaign_graph()
        initial_state = {
            "customer_profile": profile,
            "segment": profile.get("segment", "young_professional"),
            "campaign_goal": campaign_goal,
            "variants": [],
            "simulation_results": [],
            "winner": None,
            "winner_confidence": 0.0,
            "is_winner_determined": False,
            "iteration": 0,
            "max_iterations": max_iterations,
            "prompt_history": [],
            "error": None,
        }

        results = {"steps": [], "final_state": None}

        for output in graph.stream(initial_state, {"recursion_limit": 20}):
            for node_name, state in output.items():
                results["steps"].append(
                    {
                        "node": node_name,
                        "state": state,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        results["final_state"] = initial_state | {
            s["node"]: s["state"] for s in results["steps"]
        }

        # Actually merge properly
        merged = dict(initial_state)
        for step in results["steps"]:
            merged.update(step["state"])
        results["final_state"] = merged

        return results

    except Exception as e:
        # Fallback: simulated demo so the UI always works
        return run_simulated_pipeline(profile, campaign_goal, max_iterations, str(e))


def run_simulated_pipeline(
    profile: dict, campaign_goal: str, max_iterations: int, error_context: str = ""
):
    """Simulated pipeline for demo purposes when LLM is unavailable."""
    from scipy.stats import beta as beta_dist

    segment = profile.get("segment", "young_professional")
    name = profile.get("name", "Customer")

    steps = []
    all_iteration_data = []

    for iteration in range(1, max_iterations + 1):
        # Step 1: Segment
        steps.append(
            {
                "node": "segment",
                "state": {
                    "segment": segment,
                    "campaign_goal": campaign_goal,
                    "iteration": iteration - 1,
                },
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Step 2: Generate Variants
        variants = [
            {
                "variant_id": "A",
                "subject": f"🔥 {name}, don't miss this exclusive deal!",
                "body": (
                    f"Hi {name},\n\n"
                    f"As a valued {segment.replace('_', ' ')}, we've hand-picked something special for you.\n\n"
                    f"Our latest collection is designed with your interests in mind. "
                    f"Act now — this offer is available for a limited time only!\n\n"
                    f"Best regards,\nThe Campaign Team"
                ),
                "style_notes": "Urgency-driven with FOMO psychological trigger",
            },
            {
                "variant_id": "B",
                "subject": f"Hey {name}, we thought you'd love this ✨",
                "body": (
                    f"Hello {name},\n\n"
                    f"We noticed you've been exploring some great products lately. "
                    f"Here's something we think fits your style perfectly.\n\n"
                    f"Take your time — great things are worth the wait. "
                    f"Click below to discover what's new.\n\n"
                    f"Cheers,\nThe Campaign Team"
                ),
                "style_notes": "Curiosity-driven with personalization trigger",
            },
        ]

        steps.append(
            {
                "node": "generate_variants",
                "state": {"variants": variants, "iteration": iteration},
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Step 3: Simulate
        benchmarks = load_benchmarks()
        seg_data = benchmarks[benchmarks["segment"] == segment]
        base_ctr = float(seg_data["base_ctr"].iloc[0]) if len(seg_data) > 0 else 0.06
        base_open = (
            float(seg_data["base_open_rate"].iloc[0]) if len(seg_data) > 0 else 0.30
        )

        n = 1000
        sim_results = []
        for v in variants:
            ctr_mu = np.clip(np.random.normal(base_ctr, 0.015), 0.01, 0.99)
            open_mu = np.clip(np.random.normal(base_open, 0.05), 0.05, 0.99)
            num_opens = np.random.binomial(n, open_mu)
            num_clicks = np.random.binomial(n, ctr_mu)
            sim_results.append(
                {
                    "variant_id": v["variant_id"],
                    "open_rate": round(num_opens / n, 4),
                    "ctr": round(num_clicks / n, 4),
                    "conversion_rate": round(
                        np.random.uniform(0.01, 0.15) * (num_clicks / n), 4
                    ),
                    "num_recipients": n,
                    "num_opens": int(num_opens),
                    "num_clicks": int(num_clicks),
                }
            )

        steps.append(
            {
                "node": "simulate",
                "state": {"simulation_results": sim_results},
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Step 4: Evaluate (Bayesian)
        res_a, res_b = sim_results[0], sim_results[1]
        alpha_a = 1 + res_a["num_clicks"]
        beta_a = 1 + (n - res_a["num_clicks"])
        alpha_b = 1 + res_b["num_clicks"]
        beta_b = 1 + (n - res_b["num_clicks"])

        samples = 100000
        sa = beta_dist.rvs(alpha_a, beta_a, size=samples)
        sb = beta_dist.rvs(alpha_b, beta_b, size=samples)
        prob_a = float(np.mean(sa > sb))

        winner = None
        confidence = 0.0
        is_determined = False

        if prob_a > 0.95:
            winner = variants[0]
            confidence = prob_a
            is_determined = True
        elif (1 - prob_a) > 0.95:
            winner = variants[1]
            confidence = 1 - prob_a
            is_determined = True

        steps.append(
            {
                "node": "evaluate",
                "state": {
                    "winner": winner,
                    "winner_confidence": confidence,
                    "is_winner_determined": is_determined,
                },
                "timestamp": datetime.now().isoformat(),
            }
        )

        all_iteration_data.append(
            {
                "iteration": iteration,
                "variants": variants,
                "sim_results": sim_results,
                "winner": winner,
                "confidence": confidence,
                "is_determined": is_determined,
            }
        )

        if is_determined:
            # Update prompt step
            steps.append(
                {
                    "node": "update_prompt",
                    "state": {
                        "prompt_history": [
                            {
                                "iteration": iteration,
                                "system_prompt": f"Winner used: {winner['style_notes']}",
                                "winning_variant_id": winner["variant_id"],
                            }
                        ]
                    },
                    "timestamp": datetime.now().isoformat(),
                }
            )
            break

    # Build final merged state
    merged = {
        "customer_profile": profile,
        "segment": segment,
        "campaign_goal": campaign_goal,
        "iteration": all_iteration_data[-1]["iteration"] if all_iteration_data else 0,
        "max_iterations": max_iterations,
        "variants": all_iteration_data[-1]["variants"] if all_iteration_data else [],
        "simulation_results": (
            all_iteration_data[-1]["sim_results"] if all_iteration_data else []
        ),
        "winner": all_iteration_data[-1]["winner"] if all_iteration_data else None,
        "winner_confidence": (
            all_iteration_data[-1]["confidence"] if all_iteration_data else 0
        ),
        "is_winner_determined": (
            all_iteration_data[-1]["is_determined"] if all_iteration_data else False
        ),
    }

    return {
        "steps": steps,
        "final_state": merged,
        "iteration_data": all_iteration_data,
        "demo_mode": True,
        "error_context": error_context,
    }


# ── MAIN UI ────────────────────────────────────────────────────────


def main():
    # ── Hero Section ───────────────────────────────────────────────
    st.markdown(
        """
    <div class="hero-container">
        <div class="hero-title">📧 Personalized Email Campaign Generator</div>
        <div class="hero-subtitle">
            GenAI-powered A/B testing with LangGraph · Bayesian evaluation · Iterative prompt optimization
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Sidebar: Customer Profile Builder ──────────────────────────
    with st.sidebar:
        st.markdown("### 🎯 Customer Profile")
        st.markdown("---")

        segments = get_segment_config()
        segment_options = {f"{v['icon']} {v['label']}": k for k, v in segments.items()}

        selected_display = st.selectbox(
            "Customer Segment",
            options=list(segment_options.keys()),
            index=0,
            help="Select the target customer segment",
        )
        selected_segment = segment_options[selected_display]

        st.caption(segments[selected_segment]["desc"])

        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("Name", value="Alex Mercer")
        with col2:
            customer_age = st.number_input("Age", min_value=13, max_value=120, value=28)

        interests = st.multiselect(
            "Interests",
            [
                "Technology",
                "Fitness",
                "Travel",
                "Food",
                "Fashion",
                "Gaming",
                "Books",
                "Music",
                "Finance",
                "Health",
            ],
            default=["Technology", "Fitness"],
        )

        preferred_tone = st.select_slider(
            "Preferred Tone",
            options=["formal", "friendly", "casual"],
            value="casual",
        )

        engagement_score = st.slider(
            "Engagement Score",
            min_value=0.0,
            max_value=1.0,
            value=0.85,
            step=0.05,
            help="Historical engagement score (0 = low, 1 = high)",
        )

        st.markdown("---")
        st.markdown("### ⚙️ Campaign Settings")

        campaign_goal = st.text_input(
            "Campaign Goal",
            value="Sell smart fitness watch",
            help="What product/action are you promoting?",
        )

        max_iterations = st.slider(
            "Max Iterations",
            min_value=1,
            max_value=5,
            value=3,
            help="Maximum A/B optimization loops before termination",
        )

        st.markdown("---")

        # Build the profile dict
        customer_profile = {
            "customer_id": f"cust_{hash(customer_name) % 10000:04d}",
            "name": customer_name,
            "age": customer_age,
            "segment": selected_segment,
            "interests": [i.lower() for i in interests],
            "purchase_history": {
                "avg_order_value": 150,
                "frequency": "monthly",
            },
            "preferred_tone": preferred_tone,
            "engagement_score": engagement_score,
        }

        run_pipeline = st.button(
            "🚀 Run Campaign Pipeline",
            use_container_width=True,
            type="primary",
        )

    # ── Main Content Area ──────────────────────────────────────────
    if run_pipeline:
        # Execute pipeline with progress
        progress_container = st.container()
        with progress_container:
            col_prog1, col_prog2 = st.columns([3, 1])
            with col_prog1:
                progress_bar = st.progress(0, text="Starting pipeline...")
            with col_prog2:
                status_display = st.empty()

        pipeline_steps = [
            ("🔍", "Segmenting customer..."),
            ("✍️", "Generating email variants..."),
            ("🧪", "Running A/B simulation..."),
            ("📊", "Bayesian evaluation..."),
            ("🔄", "Updating prompts..."),
        ]

        for i, (icon, desc) in enumerate(pipeline_steps):
            progress_bar.progress((i + 1) / len(pipeline_steps), text=f"{icon} {desc}")
            status_display.markdown(
                f"<div style='text-align:center; color:#818cf8; font-weight:600;'>{icon}</div>",
                unsafe_allow_html=True,
            )
            time.sleep(0.5)

        # Actually run the pipeline
        results = run_demo_pipeline(customer_profile, campaign_goal, max_iterations)

        progress_bar.progress(1.0, text="✅ Pipeline complete!")
        status_display.markdown(
            "<div style='text-align:center; color:#34d399; font-weight:600;'>✅</div>",
            unsafe_allow_html=True,
        )

        if results.get("demo_mode"):
            st.info(
                "🎭 **Demo Mode** — Running with simulated LLM responses. "
                "Configure a valid API key in `.env` to use actual LLM generation.",
                icon="ℹ️",
            )

        # Store results in session state for tab persistence
        st.session_state["results"] = results
        st.session_state["profile"] = customer_profile

    # ── Display Results ────────────────────────────────────────────
    if "results" in st.session_state:
        results = st.session_state["results"]
        final = results["final_state"]

        # ── Top Metrics Row ────────────────────────────────────────
        st.markdown("### 📊 Campaign Results")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-value">{final.get("iteration", 0)}</div>
                <div class="metric-label">Iterations Run</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with m2:
            winner_text = "✅ Yes" if final.get("is_winner_determined") else "❌ No"
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-value">{winner_text}</div>
                <div class="metric-label">Winner Found</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with m3:
            conf = final.get("winner_confidence", 0) * 100
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-value">{conf:.1f}%</div>
                <div class="metric-label">Bayesian Confidence</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with m4:
            segment_display = get_segment_config().get(
                final.get("segment", ""),
                {"icon": "🎯", "label": final.get("segment", "")},
            )
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-value">{segment_display["icon"]}</div>
                <div class="metric-label">{segment_display["label"]}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Tabs ───────────────────────────────────────────────────
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📧 Email Variants",
                "📈 A/B Test Results",
                "🔬 Pipeline Trace",
                "📋 Raw State",
            ]
        )

        with tab1:
            render_email_variants(final)

        with tab2:
            render_ab_results(results)

        with tab3:
            render_pipeline_trace(results)

        with tab4:
            render_raw_state(final)

    else:
        # ── Welcome / Landing State ────────────────────────────────
        render_welcome_state()


def render_email_variants(final: dict):
    """Render the email variant cards."""
    variants = final.get("variants", [])
    winner = final.get("winner")
    sim_results = final.get("simulation_results", [])

    if not variants:
        st.warning("No variants generated.")
        return

    cols = st.columns(len(variants))
    for i, (v, col) in enumerate(zip(variants, cols)):
        with col:
            is_winner = winner and winner.get("variant_id") == v.get("variant_id")
            badge_class = "variant-badge winner-badge" if is_winner else "variant-badge"
            card_class = "email-card winner" if is_winner else "email-card"
            badge_text = (
                f"🏆 WINNER — Variant {v.get('variant_id', '?')}"
                if is_winner
                else f"Variant {v.get('variant_id', '?')}"
            )

            # Get simulation data for this variant
            sim_data = next(
                (s for s in sim_results if s.get("variant_id") == v.get("variant_id")),
                {},
            )

            st.markdown(
                f"""
            <div class="{card_class}">
                <span class="{badge_class}">{badge_text}</span>
                <div class="email-subject">📬 {v.get("subject", "No Subject")}</div>
                <div class="email-body">{v.get("body", "No body content")}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Mini metrics under each card
            if sim_data:
                mc1, mc2, mc3 = st.columns(3)
                mc1.metric(
                    "Open Rate",
                    f"{sim_data.get('open_rate', 0) * 100:.1f}%",
                )
                mc2.metric(
                    "CTR",
                    f"{sim_data.get('ctr', 0) * 100:.2f}%",
                )
                mc3.metric(
                    "Clicks",
                    f"{sim_data.get('num_clicks', 0):,}",
                )

            # Style notes expander
            with st.expander(f"🎨 Style Notes — Variant {v.get('variant_id', '?')}"):
                st.markdown(
                    f"**Psychological Approach:** {v.get('style_notes', 'N/A')}"
                )


def render_ab_results(results: dict):
    """Render the A/B test comparison charts."""
    final = results["final_state"]
    sim_results = final.get("simulation_results", [])

    if not sim_results:
        st.warning("No simulation results available.")
        return

    # ── CTR Comparison Bar Chart ───────────────────────────────────
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        df_sim = pd.DataFrame(sim_results)
        fig_ctr = go.Figure()

        colors = ["#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd"]
        for i, row in df_sim.iterrows():
            is_winner = (final.get("winner", {}) or {}).get("variant_id") == row[
                "variant_id"
            ]
            fig_ctr.add_trace(
                go.Bar(
                    x=[f"Variant {row['variant_id']}"],
                    y=[row["ctr"] * 100],
                    name=f"Variant {row['variant_id']}",
                    marker_color="#10b981" if is_winner else colors[i % len(colors)],
                    marker_line_width=2,
                    marker_line_color=(
                        "#34d399" if is_winner else "rgba(99,102,241,0.3)"
                    ),
                    text=[f"{row['ctr'] * 100:.2f}%"],
                    textposition="outside",
                    textfont=dict(size=14, color="white"),
                )
            )

        fig_ctr.update_layout(
            title=dict(
                text="Click-Through Rate Comparison",
                font=dict(size=16, color="#e2e8f0"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(
                title="CTR (%)",
                gridcolor="rgba(99,102,241,0.1)",
                color="#94a3b8",
            ),
            xaxis=dict(color="#94a3b8"),
            showlegend=False,
            height=400,
            margin=dict(t=50, b=50),
        )
        st.plotly_chart(fig_ctr, use_container_width=True)

    with col_chart2:
        # ── Open Rate Comparison ───────────────────────────────────
        fig_open = go.Figure()

        for i, row in df_sim.iterrows():
            is_winner = (final.get("winner", {}) or {}).get("variant_id") == row[
                "variant_id"
            ]
            fig_open.add_trace(
                go.Bar(
                    x=[f"Variant {row['variant_id']}"],
                    y=[row["open_rate"] * 100],
                    name=f"Variant {row['variant_id']}",
                    marker_color="#10b981" if is_winner else colors[i % len(colors)],
                    marker_line_width=2,
                    marker_line_color=(
                        "#34d399" if is_winner else "rgba(99,102,241,0.3)"
                    ),
                    text=[f"{row['open_rate'] * 100:.1f}%"],
                    textposition="outside",
                    textfont=dict(size=14, color="white"),
                )
            )

        fig_open.update_layout(
            title=dict(
                text="Open Rate Comparison",
                font=dict(size=16, color="#e2e8f0"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(
                title="Open Rate (%)",
                gridcolor="rgba(99,102,241,0.1)",
                color="#94a3b8",
            ),
            xaxis=dict(color="#94a3b8"),
            showlegend=False,
            height=400,
            margin=dict(t=50, b=50),
        )
        st.plotly_chart(fig_open, use_container_width=True)

    # ── Bayesian Posterior Visualization ────────────────────────────
    st.markdown("#### 🔬 Bayesian Posterior Distribution")

    if len(sim_results) >= 2:
        from scipy.stats import beta as beta_dist

        res_a, res_b = sim_results[0], sim_results[1]
        n = res_a["num_recipients"]

        alpha_a = 1 + res_a["num_clicks"]
        beta_a = 1 + (n - res_a["num_clicks"])
        alpha_b = 1 + res_b["num_clicks"]
        beta_b = 1 + (n - res_b["num_clicks"])

        x = np.linspace(0, 0.2, 500)
        pdf_a = beta_dist.pdf(x, alpha_a, beta_a)
        pdf_b = beta_dist.pdf(x, alpha_b, beta_b)

        fig_posterior = go.Figure()
        fig_posterior.add_trace(
            go.Scatter(
                x=x * 100,
                y=pdf_a,
                mode="lines",
                name=f"Variant A (CTR ≈ {res_a['ctr'] * 100:.2f}%)",
                line=dict(color="#6366f1", width=3),
                fill="tozeroy",
                fillcolor="rgba(99,102,241,0.15)",
            )
        )
        fig_posterior.add_trace(
            go.Scatter(
                x=x * 100,
                y=pdf_b,
                mode="lines",
                name=f"Variant B (CTR ≈ {res_b['ctr'] * 100:.2f}%)",
                line=dict(color="#f97316", width=3),
                fill="tozeroy",
                fillcolor="rgba(249,115,22,0.15)",
            )
        )

        fig_posterior.update_layout(
            title=dict(
                text="Posterior Distributions of CTR (Beta-Binomial)",
                font=dict(size=16, color="#e2e8f0"),
            ),
            xaxis=dict(
                title="CTR (%)",
                gridcolor="rgba(99,102,241,0.1)",
                color="#94a3b8",
            ),
            yaxis=dict(
                title="Probability Density",
                gridcolor="rgba(99,102,241,0.1)",
                color="#94a3b8",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                font=dict(color="#e2e8f0"),
                bgcolor="rgba(0,0,0,0.3)",
                bordercolor="rgba(99,102,241,0.3)",
            ),
            height=400,
            margin=dict(t=50, b=50),
        )
        st.plotly_chart(fig_posterior, use_container_width=True)

    # ── Full Metrics Table ─────────────────────────────────────────
    st.markdown("#### 📋 Detailed Simulation Metrics")
    df_display = pd.DataFrame(sim_results)
    df_display.columns = [col.replace("_", " ").title() for col in df_display.columns]
    st.dataframe(
        df_display.style.format(
            {
                "Open Rate": "{:.2%}",
                "Ctr": "{:.2%}",
                "Conversion Rate": "{:.4%}",
            }
        ),
        use_container_width=True,
    )


def render_pipeline_trace(results: dict):
    """Render the pipeline execution trace."""
    steps = results.get("steps", [])

    if not steps:
        st.warning("No pipeline trace available.")
        return

    st.markdown("#### 🔄 LangGraph Execution Flow")

    node_icons = {
        "segment": "🔍",
        "generate_variants": "✍️",
        "simulate": "🧪",
        "evaluate": "📊",
        "update_prompt": "🔄",
    }

    # Graph visualization
    nodes_order = [
        "segment",
        "generate_variants",
        "simulate",
        "evaluate",
        "update_prompt",
    ]
    executed = [s["node"] for s in steps]

    for node in nodes_order:
        icon = node_icons.get(node, "⬜")
        is_done = node in executed
        status_class = "done" if is_done else ""
        status_icon = "✅" if is_done else "⬜"

        st.markdown(
            f"""
        <div class="pipeline-step {status_class}">
            <span class="step-icon">{status_icon}</span>
            <span class="step-text">{icon} {node.replace("_", " ").title()}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Detailed step log
    st.markdown("#### 📜 Step-by-Step Log")

    for i, step in enumerate(steps):
        node = step["node"]
        icon = node_icons.get(node, "⬜")
        with st.expander(
            f"Step {i + 1}: {icon} {node.replace('_', ' ').title()}", expanded=(i == 0)
        ):
            st.json(step["state"])


def render_raw_state(final: dict):
    """Render the raw pipeline state for debugging."""
    st.markdown("#### 🔧 Final Pipeline State (JSON)")
    st.json(final)


def render_welcome_state():
    """Render the welcome / empty state with architecture overview."""

    st.markdown("### 🏗️ Architecture Overview")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
        This application demonstrates a **GenAI-powered email campaign optimization system** 
        built with modern MLOps tooling:

        | Component | Technology | Purpose |
        |-----------|-----------|---------|
        | 🧠 **LLM Engine** | Google Gemini / OpenAI / Anthropic | Email variant generation |
        | 🔄 **Orchestration** | LangGraph | Multi-step state machine pipeline |
        | 📊 **Evaluation** | Bayesian A/B Testing (Beta-Binomial) | Statistical winner selection |
        | 🚀 **API** | FastAPI | RESTful service layer |
        | 📈 **Tracking** | MLflow | Experiment metrics & artifacts |
        | 🐳 **Deployment** | Docker Compose | Full-stack orchestration |
        | 🔁 **CI/CD** | GitHub Actions | Lint → Test → Build pipeline |
        | 📦 **Data** | DVC | Versioned datasets & benchmarks |
        """
        )

    with col2:
        st.markdown("#### Pipeline Flow")
        st.code(
            """
Customer Profile
    │
    ▼
┌─────────────┐
│   Segment   │
└─────┬───────┘
      ▼
┌─────────────┐
│  Generate   │
│  Variants   │
└─────┬───────┘
      ▼
┌─────────────┐
│  Simulate   │
│  A/B Test   │
└─────┬───────┘
      ▼
┌─────────────┐
│  Evaluate   │◄──┐
│  (Bayesian) │   │
└─────┬───────┘   │
      │  No Winner│
      ▼           │
  Winner? ────────┘
      │ Yes
      ▼
┌─────────────┐
│   Update    │
│   Prompts   │
└─────────────┘
            """,
            language=None,
        )

    # ── Segment Benchmarks ─────────────────────────────────────────
    st.markdown("### 📊 Segment Performance Benchmarks")

    df = load_benchmarks()
    if not df.empty:
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df["segment"].str.replace("_", " ").str.title(),
                y=df["base_open_rate"] * 100,
                name="Open Rate",
                marker_color="#6366f1",
                text=[f"{v * 100:.0f}%" for v in df["base_open_rate"]],
                textposition="outside",
                textfont=dict(color="white"),
            )
        )
        fig.add_trace(
            go.Bar(
                x=df["segment"].str.replace("_", " ").str.title(),
                y=df["base_ctr"] * 100,
                name="CTR",
                marker_color="#8b5cf6",
                text=[f"{v * 100:.0f}%" for v in df["base_ctr"]],
                textposition="outside",
                textfont=dict(color="white"),
            )
        )
        fig.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="#94a3b8"),
            yaxis=dict(
                title="Rate (%)",
                gridcolor="rgba(99,102,241,0.1)",
                color="#94a3b8",
            ),
            legend=dict(
                font=dict(color="#e2e8f0"),
                bgcolor="rgba(0,0,0,0.3)",
            ),
            height=350,
            margin=dict(t=30, b=50),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
    ---
    <div style="text-align: center; color: #64748b; font-size: 0.85rem;">
        👈 Configure a customer profile in the sidebar and click <b>Run Campaign Pipeline</b> to start
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
