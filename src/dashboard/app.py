import sys
import os

# Dynamically add project root directory to sys.path for Streamlit
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import datetime

# Import custom engine components
from src.ingestion.schemas import RawTextItem, StructuredRiskSignal
from src.ingestion.replay import ReplayStreamer
from src.engine.pipeline import RiskPipeline
from src.engine.logger import SignalLogger
from src.engine.evaluator import ModelEvaluator
from src.modules.stress_testing.engine import StressTestEngine
from src.modules.rebalancer.backtest import IndexBacktester

# Page Configuration & Custom CSS
st.set_page_config(
    page_title="S&P Global & Crisil AI Risk Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    /* Dark glassmorphism & corporate S&P theme */
    .stApp {
        background: linear-gradient(135deg, #0b132b 0%, #1c2541 50%, #0b132b 100%);
        color: #ffffff;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 18px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-val {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00b4d8;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #a0aab2;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .trigger-badge {
        background: linear-gradient(90deg, #d90429 0%, #ef233c 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(239, 35, 60, 0.4);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        color: #e0e6ed;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0077b6 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize pipeline cache
@st.cache_resource
def get_pipeline():
    return RiskPipeline(use_finbert=True, use_zeroshot=True)

pipeline = get_pipeline()

# Header
st.title("🛡️ Unified AI/NLP Risk Engine & Portfolio Analytics")
st.caption("S&P Global & Crisil Campus Hackathon 2026 Submission | Candidate ID: vit-chennai_s&p")

# Sidebar Controls
st.sidebar.header("⚙️ System Controls")
ingestion_mode = st.sidebar.radio("Ingestion Source Mode", ["REPLAY (Offline CSV Stream)", "LIVE (NewsAPI Feed)"])

if st.sidebar.button("🔄 Execute Ingestion Feed Batch"):
    mode_arg = "LIVE" if "LIVE" in ingestion_mode else "REPLAY"
    streamer = ReplayStreamer(mode=mode_arg)
    items = streamer.get_all_items()
    count = 0
    for item in items:
        sig = pipeline.process_item(item)
        SignalLogger.log_signal(sig)
        count += 1
    st.sidebar.success(f"Processed {count} items into signal store!")

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Key Specs")
st.sidebar.markdown("- **Sentiment Model**: ProsusAI/FinBERT")
st.sidebar.markdown("- **Zero-Shot Classifier**: HF BART-MNLI")
st.sidebar.markdown("- **Portfolio**: Wholesale Banking ($942M)")
st.sidebar.markdown("- **Index**: 15 S&P 100 Constituent Stocks")

# Main Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🛰️ Live Signal Feed", 
    "🔥 Module B: Stress Test", 
    "📈 Module A: Rebalancer", 
    "🧪 Model Evaluation"
])

# ==========================================
# TAB 1: LIVE SIGNAL FEED
# ==========================================
with tab1:
    st.subheader("Real-Time Multi-Source Risk Signal Extraction")
    
    signals = SignalLogger.get_all_signals()
    if not signals:
        # Load sample replay if empty
        streamer = ReplayStreamer(mode="REPLAY")
        for item in streamer.get_all_items():
            sig = pipeline.process_item(item)
            SignalLogger.log_signal(sig)
        signals = SignalLogger.get_all_signals()

    df_sig = pd.DataFrame(signals)

    # Top KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{len(df_sig)}</div><div class="metric-label">Signals Extracted</div></div>', unsafe_allow_html=True)
    with c2:
        high_imp = len(df_sig[df_sig["impact_score"] >= 7]) if "impact_score" in df_sig else 0
        st.markdown(f'<div class="metric-card"><div class="metric-val">{high_imp}</div><div class="metric-label">High Impact Signals (≥7)</div></div>', unsafe_allow_html=True)
    with c3:
        avg_sent = df_sig["sentiment_score"].mean() if "sentiment_score" in df_sig else 0.0
        st.markdown(f'<div class="metric-card"><div class="metric-val">{avg_sent:+.2f}</div><div class="metric-label">Avg Market Sentiment</div></div>', unsafe_allow_html=True)
    with c4:
        top_ticker = df_sig[df_sig["company"] != "GENERAL"]["company"].mode()[0] if not df_sig[df_sig["company"] != "GENERAL"].empty else "NVDA"
        st.markdown(f'<div class="metric-card"><div class="metric-val">{top_ticker}</div><div class="metric-label">Most Mentioned Entity</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Filters
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        search_txt = st.text_input("🔍 Search Text / Ticker", "")
    with col_f2:
        selected_source = st.multiselect("Source Filter", ["news", "twitter"], default=["news", "twitter"])
    with col_f3:
        all_events = list(df_sig["event_type"].unique()) if "event_type" in df_sig else []
        selected_events = st.multiselect("Event Type Filter", all_events, default=all_events)
    with col_f4:
        min_impact = st.slider("Min Impact Score", 1, 10, 1)

    # Filter Dataframe
    filtered_df = df_sig.copy()
    if search_txt:
        filtered_df = filtered_df[
            filtered_df["text"].str.contains(search_txt, case=False, na=False) | 
            filtered_df["company"].str.contains(search_txt, case=False, na=False)
        ]
    if selected_source:
        filtered_df = filtered_df[filtered_df["source"].isin(selected_source)]
    if selected_events:
        filtered_df = filtered_df[filtered_df["event_type"].isin(selected_events)]
    filtered_df = filtered_df[filtered_df["impact_score"] >= min_impact]

    st.dataframe(
        filtered_df[["timestamp", "source", "company", "event_type", "sentiment_score", "impact_score", "confidence", "text"]],
        use_container_width=True,
        height=320
    )

    st.markdown("---")
    st.subheader("🧪 Live Interactive NLP Analyzer Sandbox")
    user_text = st.text_area("Enter custom financial news article or social media text to analyze in real-time:", 
                             "JPMorgan Chase announces unexpected $1.5B credit loss provision due to commercial real estate debt defaults.")
    user_source = st.selectbox("Source Type", ["news", "twitter"])
    
    if st.button("🚀 Analyze Text with NLP Risk Engine"):
        raw = RawTextItem(
            id="SANDBOX-01",
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            source=user_source,
            text=user_text
        )
        res_sig = pipeline.process_item(raw)
        
        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.metric("Extracted Entity", res_sig.company)
        sc2.metric("FinBERT Sentiment Score", f"{res_sig.sentiment_score:+.4f}")
        sc3.metric("Predicted Event Category", res_sig.event_type)
        sc4.metric("Calculated Impact Score", f"{res_sig.impact_score} / 10")
        
        st.info(f"💡 **Explanation & Model Lineage**: {res_sig.explanation}")


# ==========================================
# TAB 2: MODULE B STRESS TEST
# ==========================================
with tab2:
    st.subheader("Module B: Strategic Portfolio Stress Testing")
    
    signals = SignalLogger.get_all_signals()
    # Adverse high-impact signals: sentiment <= -0.3 and impact >= 7
    adverse_signals = [s for s in signals if s.get("impact_score", 0) >= 7 and s.get("sentiment_score", 0.0) <= -0.3]
    
    if adverse_signals:
        sig_options = [f"[{s['event_type']}] Impact: {s['impact_score']}/10 | Sent: {s['sentiment_score']:+.2f} | {s['company']} | {s['text'][:60]}..." for s in adverse_signals]
        selected_option = st.selectbox("Select Triggering Adverse Risk Signal for Stress Test Simulation:", sig_options)
        selected_sig_idx = sig_options.index(selected_option)
        active_signal = StructuredRiskSignal(**adverse_signals[selected_sig_idx])
    else:
        # High impact adverse default fallback signal
        active_signal = StructuredRiskSignal(
            id="SIG-ADVERSE-01",
            timestamp="2026-03-02 09:00:00",
            source="news",
            text="A major midstream energy contractor defaulted on $500 million in senior debt obligations, triggering credit default contagion risks across banking syndicates.",
            company="CVX",
            sentiment_score=-0.91,
            event_type="Credit Event",
            impact_score=9,
            confidence=0.92,
            explanation="Severe credit default contagion shock"
        )
        st.info("ℹ️ Displaying default Adverse Credit Event signal for stress testing demo.")

    # Run Stress Engine
    stress_engine = StressTestEngine()
    stress_res = stress_engine.run_stress_test(active_signal)

    # Trigger Banner
    if stress_res["triggered"]:
        st.markdown(f'<div class="trigger-badge">⚡ {stress_res["trigger_message"]}</div>', unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Stress Trigger Not Activated: {stress_res['trigger_message']}")
    
    summary = stress_res["summary"]
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Baseline Portfolio Value", f"${summary['baseline_total_usd']/1e6:,.2f}M")
    mc2.metric("Stressed Portfolio Value", f"${summary['stressed_total_usd']/1e6:,.2f}M")
    mc3.metric("Total Stress Portfolio Loss", f"${summary['total_loss_usd']/1e6:,.2f}M", delta=f"-{summary['loss_pct']*100:.2f}%", delta_color="inverse")
    mc4.metric("Parametric 99% VaR Estimate", f"${summary['var_99_estimate_usd']/1e6:,.2f}M")

    st.markdown("---")

    # Waterfall Chart
    col_w1, col_w2 = st.columns([6, 4])
    with col_w1:
        st.subheader("Financial Loss Waterfall (Baseline → Asset Class Losses → Stressed)")
        ac_summary = stress_res.get("by_asset_class", {})
        
        loan_loss = ac_summary.get("Loan", {}).get("loss_usd", abs(ac_summary.get("Loan", {}).get("pnl_usd", 0.0)))
        bond_loss = ac_summary.get("Bond", {}).get("loss_usd", abs(ac_summary.get("Bond", {}).get("pnl_usd", 0.0)))
        deriv_loss = ac_summary.get("Derivative", {}).get("loss_usd", abs(ac_summary.get("Derivative", {}).get("pnl_usd", 0.0)))
        eq_loss = ac_summary.get("Equity", {}).get("loss_usd", abs(ac_summary.get("Equity", {}).get("pnl_usd", 0.0)))
        
        measures = ["absolute", "relative", "relative", "relative", "relative", "total"]
        x_vals = ["Baseline", "Loan Loss", "Bond Loss", "Deriv Loss", "Equity Loss", "Stressed"]
        y_vals = [
            summary['baseline_total_usd'] / 1e6,
            -loan_loss / 1e6,
            -bond_loss / 1e6,
            -deriv_loss / 1e6,
            -eq_loss / 1e6,
            summary['stressed_total_usd'] / 1e6
        ]

        text_vals = [
            f"${summary['baseline_total_usd']/1e6:.1f}M",
            f"-${loan_loss/1e6:.1f}M",
            f"-${bond_loss/1e6:.1f}M",
            f"-${deriv_loss/1e6:.1f}M",
            f"-${eq_loss/1e6:.1f}M",
            f"${summary['stressed_total_usd']/1e6:.1f}M"
        ]

        fig_wf = go.Figure(go.Waterfall(
            name = "Portfolio Valuation ($M)",
            orientation = "v",
            measure = measures,
            x = x_vals,
            textposition = "outside",
            text = text_vals,
            y = y_vals,
            connector = {"line":{"color":"rgb(180, 180, 180)"}},
            decreasing = {"marker":{"color":"#ef233c"}},
            increasing = {"marker":{"color":"#2a9d8f"}},
            totals = {"marker":{"color":"#0077b6"}}
        ))
        fig_wf.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            height=380,
            yaxis=dict(title="Portfolio Value ($ Millions)", showgrid=True, gridcolor="rgba(255,255,255,0.1)")
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    with col_w2:
        st.subheader("Loss Breakdown by Sector")
        sec_summary = stress_res.get("by_sector", {})
        sec_rows = []
        for k, v in sec_summary.items():
            l_val = v.get("loss_usd", abs(v.get("pnl_usd", 0.0)))
            if l_val > 0:
                sec_rows.append({"sector": k, "loss_usd": l_val / 1e6})
                
        sec_df = pd.DataFrame(sec_rows)
        if not sec_df.empty:
            fig_pie = px.pie(
                sec_df,
                names="sector",
                values="loss_usd",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.RdBu,
                title="Sector Loss Allocation ($ Millions)"
            )
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white", height=380)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No sector losses recorded.")

    # Detailed Asset Breakdown Table
    st.subheader("Detailed Asset Revaluation Ledger ($)")
    df_assets = pd.DataFrame(stress_res["detailed_assets"])
    if "loss_usd" not in df_assets.columns and "baseline_value_usd" in df_assets.columns:
        df_assets["loss_usd"] = df_assets["baseline_value_usd"] - df_assets["stressed_value_usd"]
    
    display_cols = [c for c in ["asset_id", "asset_name", "asset_class", "sector", "ticker", "baseline_value_usd", "stressed_value_usd", "loss_usd", "pnl_pct"] if c in df_assets.columns]
    st.dataframe(
        df_assets[display_cols],
        use_container_width=True,
        height=300
    )


# ==========================================
# TAB 3: MODULE A REBALANCER
# ==========================================
with tab3:
    st.subheader("Module A: Tactical Index Rebalancer (15 S&P 100 Stocks)")
    
    # Run Rebalancer Backtest
    backtester = IndexBacktester()
    bt_res = backtester.run_backtest()
    bt_sum = bt_res["summary"]

    rc1, rc2, rc3, rc4 = st.columns(4)
    rc1.metric("Strategy Cumulative Return", f"{bt_sum['strategy_return_pct']:+.2f}%")
    rc2.metric("Benchmark (Equal Weight)", f"{bt_sum['benchmark_return_pct']:+.2f}%")
    rc3.metric("Alpha Outperformance", f"{bt_sum['alpha_outperformance_pct']:+.2f}%", delta=f"{bt_sum['alpha_outperformance_pct']:+.2f}%")
    rc4.metric("Strategy Sharpe Ratio", f"{bt_sum['strategy_sharpe']:.2f}")

    st.markdown("---")

    col_b1, col_b2 = st.columns([6, 4])
    with col_b1:
        st.subheader("Cumulative Portfolio Performance vs Equal Weight Benchmark")
        df_ts = pd.DataFrame({
            "Date": bt_res["timeline"]["dates"],
            "Sentiment Tilted Strategy": bt_res["timeline"]["strategy_cum_returns"],
            "Equal Weight Benchmark": bt_res["timeline"]["benchmark_cum_returns"]
        }).set_index("Date")
        
        fig_ts = px.line(df_ts, labels={"value": "Cumulative Return (%)"}, color_discrete_map={"Sentiment Tilted Strategy": "#00b4d8", "Equal Weight Benchmark": "#ffb703"})
        fig_ts.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white", height=380)
        st.plotly_chart(fig_ts, use_container_width=True)

    with col_b2:
        st.subheader("Constituent Sentiment & Weight Allocation")
        df_weights = pd.DataFrame([
            {"ticker": t, "weight_pct": bt_res["constituent_weights"][t]*100, "sentiment": bt_res["sentiment_scores"][t]}
            for t in bt_res["tickers"]
        ])
        fig_bar = px.bar(df_weights, x="ticker", y="weight_pct", color="sentiment", color_continuous_scale="RdYlGn",
                         labels={"weight_pct": "Tilted Weight (%)", "ticker": "Ticker"})
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white", height=380)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Index Weight Comparison Table")
    df_weights["equal_weight_pct"] = round(100.0 / len(df_weights), 2)
    df_weights["tilt_delta_pct"] = round(df_weights["weight_pct"] - df_weights["equal_weight_pct"], 2)
    st.dataframe(df_weights, use_container_width=True)


# ==========================================
# TAB 4: MODEL EVALUATION
# ==========================================
with tab4:
    st.subheader("Model Evaluation & Benchmark Comparison")
    
    eval_path = "data/eval_results.json"
    if not os.path.exists(eval_path):
        evaluator = ModelEvaluator()
        eval_res = evaluator.run_evaluation()
    else:
        with open(eval_path, "r", encoding="utf-8") as f:
            eval_res = json.load(f)

    ec1, ec2, ec3, ec4 = st.columns(4)
    ec1.metric("Total Evaluation Samples", eval_res.get("total_samples", 20))
    ec2.metric("FinBERT Sentiment F1 Score", f"{eval_res['finbert_engine']['f1_score']:.4f}")
    ec3.metric("VADER Baseline F1 Score", f"{eval_res['vader_baseline']['f1_score']:.4f}")
    ec4.metric("Zero-Shot Event Accuracy", f"{eval_res['event_classifier']['accuracy']*100:.1f}%")

    st.markdown("---")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.subheader("Sentiment Classification Performance Comparison")
        df_comp = pd.DataFrame([
            {"Metric": "Accuracy", "FinBERT Engine": eval_res['finbert_engine']['accuracy'], "VADER Baseline": eval_res['vader_baseline']['accuracy']},
            {"Metric": "Precision", "FinBERT Engine": eval_res['finbert_engine']['precision'], "VADER Baseline": eval_res['vader_baseline']['precision']},
            {"Metric": "Recall", "FinBERT Engine": eval_res['finbert_engine']['recall'], "VADER Baseline": eval_res['vader_baseline']['recall']},
            {"Metric": "F1 Score", "FinBERT Engine": eval_res['finbert_engine']['f1_score'], "VADER Baseline": eval_res['vader_baseline']['f1_score']}
        ]).set_index("Metric")
        
        fig_comp = px.bar(df_comp, barmode="group", color_discrete_sequence=["#00b4d8", "#e63946"])
        fig_comp.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white", height=320)
        st.plotly_chart(fig_comp, use_container_width=True)

    with col_e2:
        st.subheader("Impact Score Formula Validation")
        st.markdown("""
        **Formula Specification**:
        $$\\text{Impact Score} = \\min\\left(10, \\max\\left(1, \\text{round}\\left(10 \\times |\\text{sentiment}| \\times w_{\\text{event}} \\times w_{\\text{source}} \\times w_{\\text{entity}}\\right)\\right)\\right)$$
        
        - **$w_{\\text{event}}$ Severity**: Geopolitical (1.25), Credit Event (1.30), Regulatory (1.15), Macro (1.15)
        - **$w_{\\text{source}}$ Credibility**: News (1.00), Twitter (0.85)
        - **$w_{\\text{entity}}$ Prominence**: Identified S&P Ticker (1.00), General (0.80)
        """)
        
        # Sample Distribution Chart
        sig_data = SignalLogger.get_all_signals()
        if sig_data:
            df_s = pd.DataFrame(sig_data)
            fig_hist = px.histogram(df_s, x="impact_score", nbins=10, title="Impact Score Distribution across Feed",
                                    color_discrete_sequence=["#2a9d8f"])
            fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white", height=240)
            st.plotly_chart(fig_hist, use_container_width=True)
