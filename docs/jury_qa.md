# Jury Technical Q&A Guide
**S&P Global & Crisil Campus Hackathon 2026**
**Project:** Unified AI/NLP Risk Engine & Portfolio Stress Testing

---

### Q1: Why did you choose ProsusAI/FinBERT over standard VADER or general BERT for sentiment analysis?
**Answer:**
> Standard VADER and general-domain BERT models struggle with financial language nuance. For example, words like *"liability"*, *"debt"*, or *"cost contraction"* carry specific domain meanings that general sentiment analyzers misclassify as purely neutral or negative. 
> `ProsusAI/finbert` is fine-tuned specifically on financial corpora (MD&A sections, analyst reports, earnings call transcripts). It computes probabilities $P(\text{positive})$, $P(\text{negative})$, and $P(\text{neutral})$, allowing us to calculate a continuous sentiment score $P(\text{pos}) - P(\text{neg}) \in [-1.0, 1.0]$. 
> Furthermore, to satisfy the hackathon requirement of running offline in under 5 minutes on CPU, we implemented a calibrated continuous lexicon analyzer ($S = \tanh(\Delta \times 0.6)$) that guarantees zero runtime errors even without GPU acceleration.

---

### Q2: Why did you use Zero-Shot Classification (BART-MNLI) instead of training a custom supervised classifier for event types?
**Answer:**
> Training a supervised classifier for 8 specialized financial risk categories (Geopolitical, Credit Event, Macroeconomic, Regulatory, etc.) requires thousands of hand-annotated training samples which introduces label bias and high maintenance overhead. 
> Hugging Face's Zero-Shot classification (`facebook/bart-large-mnli`) leverages Natural Language Inference (NLI) premise-hypothesis pairs to evaluate candidate labels directly without Task-Specific Fine-Tuning. This allows our engine to dynamically support new risk categories by modifying label definitions without re-training models. We also backed this with keyword fallback rules for instant CPU execution.

---

### Q3: How is the Impact Score calculated, and how did you validate its formula?
**Answer:**
> The Impact Score (integer 1–10) predicts market severity using a transparent, multi-factor deterministic formula:
> $$\text{Impact} = \min\left(10, \max\left(1, \text{round}\left(10 \times |\text{sentiment}| \times w_{\text{event}} \times w_{\text{source}} \times w_{\text{entity}}\right)\right)\right)$$
> - **$|\text{sentiment}|$**: Absolute sentiment magnitude $[0, 1]$.
> - **$w_{\text{event}}$**: Event severity weight (Credit Event: 1.30, Geopolitical: 1.25, Regulatory: 1.15, Macro: 1.15, Earnings: 0.95, Product Launch: 0.85).
> - **$w_{\text{source}}$**: Source credibility weight (News: 1.00, Twitter: 0.85).
> - **$w_{\text{entity}}$**: Entity prominence weight (Identified S&P 100 Ticker: 1.00, General: 0.80).
> 
> **Validation:** We validated this formula against benchmark news items, ensuring high-severity news (e.g., credit defaults, geopolitical blockades) consistently trigger impact scores $\ge 7$, matching credit risk committee expectations.

---

### Q4: How is the baseline Value-at-Risk (VaR) calculated, and how does Module B revalue portfolio assets during a stress event?
**Answer:**
> **1. Baseline 99% 10-Day VaR Calculation:**
> Baseline VaR is calculated independently on the portfolio before news events occur, using a parametric 99% confidence z-score ($z = 2.326$) scaled over a 10-day horizon ($\sqrt{10/252}$):
> $$\text{VaR}_{99} = \sum_{i} V_i \times \sigma_i \times 2.326 \times \sqrt{\frac{10}{252}}$$
> Where annual volatility assumptions ($\sigma_i$) are: Equities = 20%, Derivatives = 25%, Bonds = 6%, Loans = 3% (representing an undiversified upper bound assuming $\rho = 1$).
>
> **2. Stress Test Asset Revaluation:**
> During an adverse stress event, Module B applies CCAR-style shocks amplified by a Sector Sensitivity Matrix ($\text{SECTOR\_MULT}$) and company exposure multipliers:
> - **Bonds**: Revalued using a 2nd-order Taylor Series expansion incorporating Modified Duration and Convexity under a combined yield shock ($\Delta y = \text{Rate Shift} + \text{Credit Spread Widening}$):
>   $$\Delta P = P_0 \times \left( -\text{ModDuration} \times \Delta y + \frac{1}{2} \times \text{Convexity} \times (\Delta y)^2 \right)$$
> - **Wholesale Loans**: Revalued by calculating post-shock Credit Expected Loss ($EL = PD \times LGD \times EAD$). Additive PD expansion ($PD_{\text{stressed}} = PD_0 \times (1.0 + X \cdot |\text{sentiment}|)$) and LGD bumps reduce loan carrying values.
> - **Derivatives**: Revalued via Delta sensitivity ($\Delta V = \text{Notional} \times \text{Delta} \times \Delta S/S_0$).
> - **Equities**: Shocked by sector-amplified equity drops ($\Delta S/S_0$).

---

### Q5: How does Module A (Index Rebalancer) prevent excessive portfolio turnover during volatile sentiment swings?
**Answer:**
> In tactical index rebalancing, unconstrained sentiment tilting causes high transaction costs due to frequent portfolio re-allocation. Module A solves this by implementing three strict risk controls:
> 1. **Boundary Caps**: Minimum weight $w_{\text{min}} = 2.0\%$ (prevents divestment of valid index constituents) and maximum weight $w_{\text{max}} = 15.0\%$ (prevents over-concentration).
> 2. **Step Turnover Cap**: Maximum step turnover constraint ($\sum |w_{i,t} - w_{i,t-1}| \le 10\%$).
> 3. **Exponential Sentiment Decay**: Smoothes sentiment spikes across rolling windows to filter out temporary market noise.

---

### Q6: What assumptions and simplifications were made, and how would this scale at S&P Global / Crisil?
**Answer:**
> **Assumptions & Simplifications:**
> 1. Bond yield shocks sum benchmark rate shifts and credit spread widening into a single yield shock ($\Delta y$) as an illustrative simplification.
> 2. Stress scenario parameters represent illustrative CCAR-style shocks; in production, regulators (Fed CCAR / EBA) provide calibrated macro scenarios.
> 3. Baseline VaR represents an undiversified upper bound ($\rho = 1$) for transparent real-time calculation.
>
> **Enterprise Scaling:**
> 1. **Ingestion**: Scaled using Apache Kafka / AWS Kinesis topics handling tens of thousands of unstructured text feeds per second.
> 2. **Inference**: Deployed as containerized microservices on Kubernetes (EKS) with GPU inference endpoints (Triton Inference Server / Hugging Face TEI) for sub-50ms FinBERT response times.
> 3. **Storage**: Risk signals streamed into TimescaleDB / Snowflake for real-time risk dashboarding and regulatory audit compliance.
