"""
Synthetic Data Generator for S&P Global & Crisil Campus Hackathon 2026.
Generates:
1. sample_news.csv (Unstructured news feed with ground-truth labels for eval)
2. sample_tweets.csv (Social media feed with ground-truth labels for eval)
3. portfolio.csv (Wholesale banking portfolio: Loans, Bonds, Derivatives, Equities)
4. stock_prices.csv (Historical price data for 15 S&P 100 tickers for rebalancing)
"""

import os
import pandas as pd
import numpy as np
import datetime

os.makedirs("data", exist_ok=True)
np.random.seed(42)

# --- 1. SAMPLE NEWS DATASET ---
news_items = [
    {
        "timestamp": "2026-03-01 09:15:00",
        "source": "news",
        "headline": "Federal Reserve signals potential rate hikes amid persistent inflation concerns",
        "text": "The Federal Reserve hinted at maintaining higher interest rates for longer as core inflation data remains stickier than anticipated. Markets expect tightening credit conditions across wholesale banking sectors.",
        "company": "JPM",
        "ground_truth_sentiment": "negative",
        "ground_truth_sentiment_score": -0.75,
        "ground_truth_event": "Macroeconomic"
    },
    {
        "timestamp": "2026-03-01 10:30:00",
        "source": "news",
        "headline": "NVIDIA unveils next-gen AI superchip architecture with 3x efficiency gains",
        "text": "NVIDIA announced its groundbreaking new Blackwell Ultra AI architecture at its annual tech summit, promising unprecedented compute power and major corporate data center adoption.",
        "company": "NVDA",
        "ground_truth_sentiment": "positive",
        "ground_truth_sentiment_score": 0.88,
        "ground_truth_event": "Product Launch"
    },
    {
        "timestamp": "2026-03-01 11:45:00",
        "source": "news",
        "headline": "Geopolitical tensions in Strait of Hormuz escalate; crude oil surges 8%",
        "text": "Naval blockades and drone activity in key shipping lanes have disrupted global oil exports. Energy analysts warn of supply chain bottlenecks and elevated freight insurance premiums.",
        "company": "XOM",
        "ground_truth_sentiment": "negative",
        "ground_truth_sentiment_score": -0.82,
        "ground_truth_event": "Geopolitical"
    },
    {
        "timestamp": "2026-03-01 13:00:00",
        "source": "news",
        "headline": "JPMorgan Chase reports record Q1 investment banking revenue beating estimates",
        "text": "JPMorgan Chase & Co. delivered blowout quarterly earnings, driven by strong advisory fees and robust net interest income despite broader market volatility.",
        "company": "JPM",
        "ground_truth_sentiment": "positive",
        "ground_truth_sentiment_score": 0.82,
        "ground_truth_event": "Earnings"
    },
    {
        "timestamp": "2026-03-01 14:20:00",
        "source": "news",
        "headline": "FDA issues unexpected warning letter to Pfizer regarding manufacturing facility",
        "text": "The US Food and Drug Administration issued a formal regulatory compliance notice to Pfizer concerning quality control standards at its key biologics plant.",
        "company": "PFE",
        "ground_truth_sentiment": "negative",
        "ground_truth_sentiment_score": -0.65,
        "ground_truth_event": "Regulatory"
    },
    {
        "timestamp": "2026-03-01 15:45:00",
        "source": "news",
        "headline": "Apple acquires promising generative AI startup for $2.4 Billion",
        "text": "Apple Inc. finalized a multi-billion dollar acquisition to accelerate its on-device neural processing engine capabilities ahead of the upcoming iPhone launch.",
        "company": "AAPL",
        "ground_truth_sentiment": "positive",
        "ground_truth_sentiment_score": 0.70,
        "ground_truth_event": "Merger/Acquisition"
    },
    {
        "timestamp": "2026-03-02 09:00:00",
        "source": "news",
        "headline": "Regional energy supplier files for Chapter 11 bankruptcy following derivative default",
        "text": "A major midstream energy contractor defaulted on $500 million in senior debt obligations, raising credit contagion risks for syndicate bank lenders.",
        "company": "CVX",
        "ground_truth_sentiment": "negative",
        "ground_truth_sentiment_score": -0.91,
        "ground_truth_event": "Credit Event"
    },
    {
        "timestamp": "2026-03-02 10:15:00",
        "source": "news",
        "headline": "Microsoft Cloud Azure revenue accelerates 31% year-over-year",
        "text": "Microsoft reported strong cloud adoption across enterprise clients, boosting commercial cloud margins and forward growth guidance.",
        "company": "MSFT",
        "ground_truth_sentiment": "positive",
        "ground_truth_sentiment_score": 0.85,
        "ground_truth_event": "Earnings"
    },
    {
        "timestamp": "2026-03-02 11:30:00",
        "source": "news",
        "headline": "EU Antitrust commission launches formal inquiry into Amazon marketplace pricing practices",
        "text": "European Union regulatory authorities opened an investigation into alleged anti-competitive merchant fee structures on Amazon's regional ecommerce platforms.",
        "company": "AMZN",
        "ground_truth_sentiment": "negative",
        "ground_truth_sentiment_score": -0.60,
        "ground_truth_event": "Regulatory"
    },
    {
        "timestamp": "2026-03-02 13:45:00",
        "source": "news",
        "headline": "Tesla recalls 150,000 vehicles over steering assist software glitch",
        "text": "Tesla Inc announced an over-the-air recall for Model Y vehicles following consumer reports of intermittent power steering resistance during cold weather.",
        "company": "TSLA",
        "ground_truth_sentiment": "negative",
        "ground_truth_sentiment_score": -0.58,
        "ground_truth_event": "Product Launch"
    },
    {
        "timestamp": "2026-03-02 15:00:00",
        "source": "news",
        "headline": "Bank of America raises quarterly dividend by 10% following stress test approval",
        "text": "Bank of America Corp declared an increased capital distribution strategy, highlighting strong liquidity buffers and Tier 1 capital ratios.",
        "company": "BAC",
        "ground_truth_sentiment": "positive",
        "ground_truth_sentiment_score": 0.76,
        "ground_truth_event": "Earnings"
    },
    {
        "timestamp": "2026-03-03 09:30:00",
        "source": "news",
        "headline": "Global semiconductor supply chain disruptions threaten auto production lines",
        "text": "Unforeseen factory outages in Southeast Asia have tightened microcontroller supplies, impacting global automotive assembly schedules.",
        "company": "TSLA",
        "ground_truth_sentiment": "negative",
        "ground_truth_sentiment_score": -0.68,
        "ground_truth_event": "Macroeconomic"
    }
]

df_news = pd.DataFrame(news_items)
df_news.to_csv("data/sample_news.csv", index=False)
print("Saved data/sample_news.csv with", len(df_news), "records.")

# --- 2. SAMPLE TWEETS DATASET ---
tweets_items = [
    {
        "timestamp": "2026-03-01 09:20:00",
        "source": "twitter",
        "text": "$NVDA breaking out to new all-time highs! Datacenter demand is insane #AI #Stocks",
        "company": "NVDA",
        "ground_truth_sentiment": "positive",
        "ground_truth_sentiment_score": 0.85,
        "ground_truth_event": "Product Launch"
    },
    {
        "timestamp": "2026-03-01 10:05:00",
        "source": "twitter",
        "text": "$JPM exposure to commercial real estate loans could trigger credit downgrades if rates stay high",
        "company": "JPM",
        "ground_truth_sentiment": "negative",
        "ground_truth_sentiment_score": -0.62,
        "ground_truth_event": "Credit Event"
    },
    {
        "timestamp": "2026-03-01 11:50:00",
        "source": "twitter",
        "text": "Oil spiking hard today! $XOM and $CVX printing cash flow right now 🛢️📈",
        "company": "XOM",
        "ground_truth_sentiment": "positive",
        "ground_truth_sentiment_score": 0.78,
        "ground_truth_event": "Macroeconomic"
    },
    {
        "timestamp": "2026-03-01 13:10:00",
        "source": "twitter",
        "text": "Rumors of massive layoffs and restructuring at $META incoming next week",
        "company": "META",
        "ground_truth_sentiment": "negative",
        "ground_truth_sentiment_score": -0.55,
        "ground_truth_event": "Macroeconomic"
    },
    {
        "timestamp": "2026-03-01 14:30:00",
        "source": "twitter",
        "text": "Huge earnings beat for $MSFT! Azure growth completely blew past analyst consensus.",
        "company": "MSFT",
        "ground_truth_sentiment": "positive",
        "ground_truth_sentiment_score": 0.90,
        "ground_truth_event": "Earnings"
    },
    {
        "timestamp": "2026-03-02 09:15:00",
        "source": "twitter",
        "text": "Regulatory scrutiny on Big Tech $GOOGL ad monopoly case wrapping up soon. High fine expected.",
        "company": "GOOGL",
        "ground_truth_sentiment": "negative",
        "ground_truth_sentiment_score": -0.71,
        "ground_truth_event": "Regulatory"
    },
    {
        "timestamp": "2026-03-02 10:45:00",
        "source": "twitter",
        "text": "$AAPL Vision Pro sales surging in European markets ahead of target!",
        "company": "AAPL",
        "ground_truth_sentiment": "positive",
        "ground_truth_sentiment_score": 0.74,
        "ground_truth_event": "Product Launch"
    },
    {
        "timestamp": "2026-03-02 12:00:00",
        "source": "twitter",
        "text": "Uncertainty in credit markets! Moody's warning on $BAC leverage metrics.",
        "company": "BAC",
        "ground_truth_sentiment": "negative",
        "ground_truth_sentiment_score": -0.68,
        "ground_truth_event": "Credit Event"
    }
]

df_tweets = pd.DataFrame(tweets_items)
df_tweets.to_csv("data/sample_tweets.csv", index=False)
print("Saved data/sample_tweets.csv with", len(df_tweets), "records.")

# --- 3. SYNTHETIC WHOLESALE BANKING PORTFOLIO ---
sectors = ["Technology", "Financials", "Energy", "Healthcare", "Consumer Discretionary", "Consumer Staples"]
asset_classes = ["Loan", "Bond", "Derivative", "Equity"]
tickers = ["NVDA", "AAPL", "MSFT", "GOOGL", "JPM", "BAC", "GS", "MS", "WFC", "C", "XOM", "CVX", "PFE", "JNJ", "TSLA", "AMZN", "META", "DIS", "PG", "UNH"]

portfolio_rows = []
asset_id_counter = 101

for i in range(40):
    ac = asset_classes[i % len(asset_classes)]
    ticker = tickers[i % len(tickers)]
    
    # Map ticker to sector
    if ticker in ["NVDA", "AAPL", "MSFT", "GOOGL", "META"]:
        sec = "Technology"
    elif ticker in ["JPM", "BAC", "GS", "MS", "WFC", "C"]:
        sec = "Financials"
    elif ticker in ["XOM", "CVX"]:
        sec = "Energy"
    elif ticker in ["PFE", "JNJ", "UNH"]:
        sec = "Healthcare"
    elif ticker in ["TSLA", "AMZN", "DIS"]:
        sec = "Consumer Discretionary"
    else:
        sec = "Consumer Staples"

    notional = round(float(np.random.uniform(5000000, 50000000)), 2) # $5M to $50M
    current_val = round(notional * float(np.random.uniform(0.95, 1.05)), 2)
    
    pd_val = round(float(np.random.uniform(0.005, 0.04)), 4)
    lgd_val = round(float(np.random.uniform(0.30, 0.55)), 2)
    ead_val = current_val
    
    duration = round(float(np.random.uniform(2.5, 7.5)), 2) if ac == "Bond" else 0.0
    convexity = round(float(np.random.uniform(15.0, 60.0)), 2) if ac == "Bond" else 0.0
    delta = round(float(np.random.uniform(0.4, 1.2)), 2) if ac == "Derivative" else 1.0
    
    ratings = ["AAA", "AA", "A", "BBB", "BB"]
    rating = ratings[i % len(ratings)]
    
    portfolio_rows.append({
        "asset_id": f"AST-{asset_id_counter}",
        "asset_name": f"{ticker} {ac} Facility #{i+1}",
        "asset_class": ac,
        "sector": sec,
        "ticker": ticker,
        "notional_usd": notional,
        "current_value_usd": current_val,
        "pd": pd_val,
        "lgd": lgd_val,
        "ead": ead_val,
        "duration": duration,
        "convexity": convexity,
        "delta": delta,
        "credit_rating": rating
    })
    asset_id_counter += 1

df_portfolio = pd.DataFrame(portfolio_rows)
df_portfolio.to_csv("data/portfolio.csv", index=False)
print("Saved data/portfolio.csv with", len(df_portfolio), "assets total value: ${:,.2f}".format(df_portfolio['current_value_usd'].sum()))

# --- 4. STOCK PRICES DATASET FOR MODULE A REBALANCER ---
top15_tickers = ["NVDA", "AAPL", "MSFT", "GOOGL", "JPM", "BAC", "GS", "XOM", "CVX", "PFE", "JNJ", "TSLA", "AMZN", "META", "PG"]
start_date = datetime.date(2025, 9, 1)
num_days = 120

price_records = []
initial_prices = {
    "NVDA": 125.0, "AAPL": 225.0, "MSFT": 420.0, "GOOGL": 175.0,
    "JPM": 210.0, "BAC": 40.0, "GS": 480.0, "XOM": 115.0,
    "CVX": 150.0, "PFE": 28.0, "JNJ": 160.0, "TSLA": 240.0,
    "AMZN": 185.0, "META": 510.0, "PG": 170.0
}

current_prices = initial_prices.copy()

for d in range(num_days):
    dt_str = (start_date + datetime.timedelta(days=d)).strftime("%Y-%m-%d")
    for t in top15_tickers:
        daily_ret = np.random.normal(0.0005, 0.015)
        current_prices[t] = round(max(5.0, current_prices[t] * (1.0 + daily_ret)), 2)
        price_records.append({
            "date": dt_str,
            "ticker": t,
            "close": current_prices[t]
        })

df_prices = pd.DataFrame(price_records)
df_prices.to_csv("data/stock_prices.csv", index=False)
print("Saved data/stock_prices.csv with", len(df_prices), "price records across 15 tickers.")
