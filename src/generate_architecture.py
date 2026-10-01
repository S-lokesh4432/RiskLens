"""
Architecture Diagram Visualizer & High-Res PNG Generator.
Outputs: docs/architecture.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("docs", exist_ok=True)

fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
ax.set_facecolor("#0b132b")
fig.patch.set_facecolor("#0b132b")

# Outer Box Styling
box_style = dict(boxstyle="round,pad=0.5", fc="#1c2541", ec="#00b4d8", lw=2)
header_style = dict(color="#00b4d8", fontsize=14, fontweight="bold", ha="center")
sub_style = dict(color="#e0e6ed", fontsize=10, ha="center")

# Layer 1: Ingestion
ax.text(0.5, 0.92, "1. PLUGGABLE DATA INGESTION LAYER", **header_style)
rect1 = patches.Rectangle((0.05, 0.80), 0.90, 0.10, linewidth=2, edgecolor="#00b4d8", facecolor="#1c2541")
ax.add_patch(rect1)
ax.text(0.20, 0.85, "News CSV Connector\n(Kaggle Financial News)", **sub_style)
ax.text(0.50, 0.85, "Tweets CSV Connector\n(Stock Tweets Feed)", **sub_style)
ax.text(0.80, 0.85, "NewsAPI Live Connector\n(Fallback to Replay)", **sub_style)

# Arrow 1
ax.annotate('', xy=(0.5, 0.74), xytext=(0.5, 0.80),
            arrowprops=dict(facecolor='#00b4d8', edgecolor='#00b4d8', width=2, headwidth=8))

# Layer 2: Core NLP Risk Engine
ax.text(0.5, 0.72, "2. CORE AI / NLP RISK ENGINE", **header_style)
rect2 = patches.Rectangle((0.05, 0.48), 0.90, 0.22, linewidth=2, edgecolor="#7209b7", facecolor="#1c2541")
ax.add_patch(rect2)
ax.text(0.20, 0.60, "Entity Extraction NER\n(20 S&P 100 Tickers)", **sub_style)
ax.text(0.40, 0.60, "FinBERT Sentiment\n(ProsusAI/finbert)\nP(pos) - P(neg)", **sub_style)
ax.text(0.60, 0.60, "Zero-Shot Classifier\n(BART-MNLI)\n8 Event Categories", **sub_style)
ax.text(0.82, 0.60, "Impact Calculator\nFormula: 1-10 Score\nEvent + Source + Entity", **sub_style)

# Arrow 2
ax.annotate('', xy=(0.5, 0.42), xytext=(0.5, 0.48),
            arrowprops=dict(facecolor='#7209b7', edgecolor='#7209b7', width=2, headwidth=8))

# Layer 3: REST API & Persistence
ax.text(0.5, 0.40, "3. FASTAPI REST SERVICE & PERSISTENCE LAYER", **header_style)
rect3 = patches.Rectangle((0.05, 0.28), 0.90, 0.10, linewidth=2, edgecolor="#4cc9f0", facecolor="#1c2541")
ax.add_patch(rect3)
ax.text(0.25, 0.33, "FastAPI Endpoints\nGET /signals | GET /signals/{ticker}\nPOST /analyze | POST /replay/start", **sub_style)
ax.text(0.75, 0.33, "Signal Logger Storage\ndata/signals.jsonl\ndata/signals.csv", **sub_style)

# Arrow 3
ax.annotate('', xy=(0.5, 0.22), xytext=(0.5, 0.28),
            arrowprops=dict(facecolor='#4cc9f0', edgecolor='#4cc9f0', width=2, headwidth=8))

# Layer 4: Downstream Analytics & Dashboard
ax.text(0.5, 0.20, "4. DOWNSTREAM ANALYTICS MODULES & DASHBOARD", **header_style)
rect4 = patches.Rectangle((0.05, 0.04), 0.90, 0.14, linewidth=2, edgecolor="#4361ee", facecolor="#1c2541")
ax.add_patch(rect4)
ax.text(0.22, 0.10, "Module B: Portfolio Stress Test\n($942M Wholesale Banking)\nValuation & Shocks", **sub_style)
ax.text(0.50, 0.10, "Streamlit 4-Tab App\nLive Feed | Stress Test\nRebalancer | Model Eval", **sub_style)
ax.text(0.78, 0.10, "Module A: Tactical Rebalancer\n(15 S&P 100 Index)\nSentiment Tilt & Backtest", **sub_style)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

plt.title("Unified AI/NLP Risk Engine System Architecture\nS&P Global & Crisil Campus Hackathon 2026", color="#ffffff", fontsize=16, pad=20, fontweight="bold")
plt.tight_layout()
plt.savefig("docs/architecture.png", dpi=300, bbox_inches="tight")
print("Saved high-res architecture diagram to docs/architecture.png")
