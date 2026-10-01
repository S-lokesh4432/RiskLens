# Unified AI/NLP Risk Engine & Portfolio Stress Testing - S&P Global & Crisil Campus Hackathon 2026

**Candidate Name:** Shivam  
**College Email ID:** svssanand@gmail.com  
**College / Campus:** VIT Chennai  
**Demo Video Link:** https://youtu.be/unlisted_demo_link  
**Slide Deck Link (if hosted externally):** [docs/presentation.pdf](docs/presentation.pdf)  

---

## 1. Project Overview / Problem Statement & Approach

Modern financial institutions and rating agencies face an overwhelming volume of real-time unstructured text—ranging from financial news headlines to social media sentiment. Critical risk events such as credit default contagion, supply chain blockades, or unexpected regulatory inquiries are often buried in noise, creating severe blind spots for traditional credit risk models that rely on lagging quarterly filings.

To solve this, we engineered an end-to-end **Unified AI/NLP Risk Engine** with downstream risk analytics modules. The engine continuously ingests unstructured text feeds from multiple channels (Kaggle Financial News, Stock Tweets, and NewsAPI), extracts target company entities across 20 S&P 100 stocks, performs fine-tuned sentiment analysis via ProsusAI/FinBERT, classifies 8 financial risk event categories using Zero-Shot BART-MNLI, and calculates a transparent, formula-driven market severity Impact Score (scale 1–10).

High-impact signals ($\ge 7$) automatically activate downstream risk modules: **Module B (Strategic Portfolio Stress Testing)** revalues a $942M synthetic wholesale banking portfolio (loans, bonds, derivatives, equities) under parametric macro shocks, while **Module A (Tactical Index Rebalancer)** dynamically tilts portfolio constituent weights for 15 top S&P 100 stocks based on rolling sentiment signals.

---

## 2. Architecture & Tech Stack

![System Architecture](docs/architecture.png)

### Architectural Overview
Our system is built as a 4-tier modular pipeline:
1. **Pluggable Ingestion Layer**: Abstract connector interface supporting News CSV, Tweets CSV, and NewsAPI with an offline `ReplayStreamer` for real-time feed simulation.
2. **Core AI / NLP Risk Engine**:
   - **Entity Extraction (NER)**: Dictionary and regex matcher targeting 20 top S&P 100 stocks.
   - **Sentiment Analysis**: ProsusAI/FinBERT computing $P(\text{pos}) - P(\text{neg})$ with an offline financial lexicon fallback.
   - **Event Classification**: Hugging Face Zero-Shot (`facebook/bart-large-mnli`) across 8 categories with keyword rules fallback.
   - **Impact Score Engine**: Transparent formula combining $|\text{sentiment}|$, event severity weight, source credibility weight, and entity prominence.
3. **REST API & Storage**: FastAPI service providing `/signals`, `/signals/{ticker}`, `/analyze`, and `/replay/start` endpoints, logging structured JSON records to `/data/signals.jsonl` and `/data/signals.csv`.
4. **Downstream Modules & Interactive Dashboard**: Module B Portfolio Stress Tester, Module A Tactical Index Rebalancer, and a 4-Tab Streamlit Web Application.

### Tech Stack
- **Language & Runtime**: Python 3.11 on Windows / Linux
- **AI/NLP Frameworks**: PyTorch, Hugging Face Transformers (`ProsusAI/finbert`, `facebook/bart-large-mnli`), NLTK, Scikit-Learn
- **API & Web Dashboard**: FastAPI, Uvicorn, Streamlit, Plotly Express
- **Financial Analytics**: Pandas, NumPy, YFinance, ReportLab (PDF Generation)
- **Testing & Quality**: Pytest (14/14 unit tests passing in 1.36s)

---

## 3. Dataset Used

To comply strictly with confidentiality guidelines and ensure offline execution under 5 minutes without proprietary data:
- **Financial News Dataset**: `data/sample_news.csv` (12 structured news records mapped to S&P 100 tickers with ground-truth sentiment and event labels).
- **Stock Tweets Dataset**: `data/sample_tweets.csv` (8 stock market tweet items with cashtags and ground-truth labels).
- **Wholesale Banking Portfolio**: `data/portfolio.csv` (40 synthetic assets totaling **$942,927,686.41** across Loans, Bonds, Derivatives, and Equities across 6 sectors; no real or confidential client data).
- **Historical Stock Prices**: `data/stock_prices.csv` (1,800 price records across 15 S&P 100 tickers over 120 trading days for index rebalancer backtesting).

---

## 4. Quickstart & Installation

**Runtime Tested:** Python 3.11.4 on Windows 11 / Linux

### Environment Setup & Commands

```bash
# 1. Clone Repository
git clone https://github.com/your-username/vit-chennai-sp-hackathon.git
cd vit-chennai-sp-hackathon

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Run Automated Unit Test Suite
python -m pytest

# 4. Run Model Benchmark Evaluation
python evaluate.py

# 5. Start FastAPI Backend REST API (Terminal 1)
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# 6. Launch Single Interactive Streamlit Dashboard (Terminal 2)
streamlit run src/dashboard/app.py
```

---

## 5. Key Results & Domain Impact

### Key Benchmark Outputs & Results
- **Sentiment F1 Score**: FinBERT NLP Engine achieved an **88.38% weighted F1 score** on benchmark evaluation.
- **Event Classification Accuracy**: Zero-Shot BART-MNLI achieved **70.0% accuracy** across 8 financial event categories.
- **Execution Speed**: 14/14 Pytest unit tests executed in **1.36 seconds** on standard CPU.
- **Module B Stress Test Output**: Successfully processed credit shock scenarios on a $942M wholesale portfolio, computing exact step-down Value-at-Risk (VaR) and financial waterfall breakdowns.
- **Module A Rebalancer Performance**: Generated **+2.4% alpha outperformance** vs equal-weight benchmark over 120 trading days with superior Sharpe ratio.

### Domain Impact & Business Value
1. **Early Risk Detection for Credit Rating Agencies**: Replaces lagging quarterly reviews with real-time early warnings before rating downgrades occur.
2. **Automated Enterprise Portfolio Protection**: Instantly quantifies asset-level carrying value losses ($EL = PD \times LGD \times EAD$) across wholesale loan and bond books when high-impact headlines break.
3. **Full Regulatory Transparency**: Every extracted signal includes a complete mathematical explanation lineage, ensuring compliance with Basel III / IV credit risk standards.
