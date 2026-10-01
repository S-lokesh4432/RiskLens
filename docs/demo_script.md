# Demo Video Script (5–8 Minutes)
**S&P Global & Crisil Campus Hackathon 2026**
**Project Title:** Unified AI/NLP Risk Engine & Portfolio Stress Testing
**Candidate Name:** Shivam (Candidate ID: vit-chennai_s&p)

---

## 🎬 Video Overview & Timestamp Timeline

| Segment | Duration | Topic | Screen Visual | Speaker Script Summary |
|---------|----------|-------|---------------|------------------------|
| **1. Intro** | 0:00 – 0:45 (45s) | Problem & Core Architecture | Slide Deck / Architecture Diagram (`docs/architecture.png`) | Introduce problem: Financial institutions struggle with unstructured risk text. Explain our 4-tier solution: Ingestion → NLP Risk Engine → REST API → Stress Testing & Rebalancer. |
| **2. Setup & Run** | 0:45 – 1:30 (45s) | Quickstart Terminal Execution | Terminal / PowerShell | Show git clone, pip install, running `evaluate.py` (showing 14/14 tests passing), starting FastAPI backend (`uvicorn src.api.main:app`), and launching Streamlit dashboard (`streamlit run src/dashboard/app.py`). |
| **3. Live Signal Feed** | 1:30 – 3:00 (1.5m) | Tab 1: NLP Signal Extraction | Streamlit Tab 1 | Demonstrate multi-source signal feed table (News + Twitter). Filter by entity (e.g. `NVDA`, `JPM`). Use Interactive Text Sandbox to analyze custom news headline in real-time, showing FinBERT sentiment, Zero-shot event tag, and Impact Score formula output. |
| **4. Module B Stress Test** | 3:00 – 4:30 (1.5m) | Tab 2: Portfolio Stress Testing | Streamlit Tab 2 | Show automated trigger notification when impact score > 7. Walk through before/after financial waterfall chart on $942M wholesale banking portfolio. Explain bond Duration/Convexity math, loan Expected Loss ($EL = PD \times LGD \times EAD$), and derivative Delta shock. |
| **5. Module A Rebalancer** | 4:30 – 5:45 (1.1m) | Tab 3: Index Rebalancer | Streamlit Tab 3 | Walkthrough 15 S&P 100 constituent index. Show sentiment-tilted weight allocation (min 2%, max 15%, turnover cap). Highlight historical backtest line chart demonstrating +2.4% alpha outperformance vs equal-weight benchmark. |
| **6. Model Evaluation** | 5:45 – 6:30 (45s) | Tab 4: Benchmark Metrics | Streamlit Tab 4 | Show FinBERT 88.38% F1 score comparison vs VADER baseline, zero-shot event accuracy, and impact score distribution across the feed. |
| **7. Outro & Impact** | 6:30 – 7:00 (30s) | Summary & Closing | Slide 6 / Camera | Summarize domain impact for credit risk monitoring, regulatory transparency, and portfolio protection. Thank the jury. |

---

## 🎙️ Detailed Word-for-Word Voiceover Script

### Section 1: Intro (0:00 – 0:45)
> "Hello members of the jury panel! My name is Shivam, representing VIT Chennai for the S&P Global & Crisil Campus Hackathon 2026. 
> Today, commercial banks and rating agencies process millions of unstructured text items daily—from financial news headlines to market chatter on social media. Crucial risk signals like credit default contagion, supply chain bottlenecks, or sudden regulatory inquiries are often buried until quarterly reviews.
> To solve this, I built a **Unified AI/NLP Risk Engine** with downstream risk management modules. As shown in our system architecture, the engine ingests multi-source feeds, extracts target entities across 20 S&P 100 stocks, scores sentiment using ProsusAI/FinBERT, classifies 8 risk event types using Zero-Shot BART-MNLI, and calculates a transparent market severity Impact Score from 1 to 10."

### Section 2: Quickstart & Local Setup (0:45 – 1:30)
> "Let's start from a fresh terminal environment as specified in our README Quickstart:
> First, we run `pip install -r requirements.txt`. 
> Next, let's execute `python -m pytest` to run our automated test suite. As you can see, all 14 unit tests across the engine, API, stress testing, and rebalancer pass cleanly in under 1.5 seconds!
> Now, we start our FastAPI REST service on port 8000 using `uvicorn src.api.main:app`, and launch our interactive dashboard using `streamlit run src/dashboard/app.py`."

### Section 3: Live Signal Feed Walkthrough (1:30 – 3:00)
> "Switching to our Streamlit dashboard, Tab 1 displays our **Live Signal Feed**. 
> The engine continuously processes feeds from Kaggle Financial News, Stock Tweets datasets, and NewsAPI live streams.
> Notice our search and filter controls—we can instantly filter signals by company ticker like NVIDIA or JPMorgan, by source channel, or by minimum impact score.
> Below, our **Live Interactive Sandbox** allows risk analysts to input custom unstructured text. For example: *'JPMorgan Chase announces unexpected $1.5B credit loss provision due to commercial real estate debt defaults.'*
> Clicking 'Analyze Text', the engine instantly identifies entity `JPM`, computes a negative sentiment score of -0.75 via FinBERT, classifies the event as a `Credit Event`, and calculates a high Impact Score of 8 out of 10, providing full mathematical explanation lineage!"

### Section 4: Module B Strategic Portfolio Stress Testing (3:00 – 4:30)
> "Moving to Tab 2, we demonstrate **Module B: Strategic Portfolio Stress Testing**.
> We generated a synthetic wholesale banking portfolio of $942 Million across Loans, Bonds, Derivatives, and Equities across 6 key sectors.
> When a signal's impact score exceeds our configured threshold of 7, our automated trigger activates!
> Here, a high-impact Credit Event signal triggers our financial scenario engine. 
> Our financial valuation models revalue each asset:
> - Bonds use a 2nd-order Taylor expansion with Modified Duration and Convexity under rate/spread shocks.
> - Loans evaluate post-shock Expected Loss ($EL = PD \times LGD \times EAD$), shifting carrying values.
> - Derivatives apply Delta sensitivity approximations.
> Our waterfall chart shows the exact step-down from our $942M baseline to asset class losses, giving risk officers immediate Value-at-Risk (VaR) estimates."

### Section 5: Module A Tactical Index Rebalancer (4:30 – 5:45)
> "In Tab 3, we show **Module A: Tactical Index Rebalancer**.
> We mock an index of 15 top S&P 100 constituent stocks starting with equal weights (6.67% each).
> Using exponential rolling sentiment decay, our rebalancer tilts weights toward positive sentiment assets while enforcing a minimum weight of 2%, a maximum cap of 15%, and a 10% step turnover limit.
> In our historical backtest chart over 120 trading days, our sentiment-tilted strategy generated **+2.4% alpha outperformance** over the equal-weight benchmark with a superior Sharpe ratio!"

### Section 6: Model Evaluation & Conclusion (5:45 – 7:00)
> "Finally, in Tab 4, we provide quantitative evaluation benchmarks against ground-truth labels. 
> Our FinBERT engine achieved an **88.38% weighted F1 score**, outperforming traditional VADER baselines, while our Zero-Shot event classifier achieved 70% accuracy on domain categories.
> In conclusion, this solution bridges the gap between raw unstructured market text and actionable wholesale portfolio risk management. Thank you for your time!"
