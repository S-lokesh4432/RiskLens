"""
Generator for Financial Sentiment (PhraseBank-style) & Financial Event Benchmark Datasets.
Outputs:
- data/phrasebank_eval.csv (100 sentiment benchmark sentences)
- data/event_eval.csv (100 event classification benchmark headlines)
"""

import os
import pandas as pd

os.makedirs("data", exist_ok=True)

# 1. 100 Financial PhraseBank-style Sentiment Samples (positive, negative, neutral)
phrasebank_data = [
    # Positive (35)
    {"text": "Operating profit increased by 15% to EUR 12.5 million compared to the previous year.", "label": "positive"},
    {"text": "Net sales rose 22% reaching record quarterly turnover.", "label": "positive"},
    {"text": "The company signed a major contract worth $45 million with an international government agency.", "label": "positive"},
    {"text": "EBITDA margin expanded 350 basis points driven by operational efficiency gains.", "label": "positive"},
    {"text": "Share price surged 12% following blowout quarterly earnings beat.", "label": "positive"},
    {"text": "The Board declared an increased annual dividend payout of $1.20 per share.", "label": "positive"},
    {"text": "Revenue accelerated 30% year-over-year beating Wall Street consensus estimates.", "label": "positive"},
    {"text": "Order backlog reached an all-time high of $2.4 billion.", "label": "positive"},
    {"text": "The merger will yield $150 million in annual synergy cost savings.", "label": "positive"},
    {"text": "FDA approved the new oncology drug candidate following successful Phase III clinical trials.", "label": "positive"},
    {"text": "Free cash flow doubled to $600 million supporting share repurchase expansion.", "label": "positive"},
    {"text": "Commercial cloud subscription revenue grew 34% driven by strong enterprise adoption.", "label": "positive"},
    {"text": "Rating agency upgraded senior debt credit rating to AAA with a stable outlook.", "label": "positive"},
    {"text": "The company successfully completed a $500 million oversubscribed bond placement.", "label": "positive"},
    {"text": "Gross profit margins improved to 48% due to falling raw material input costs.", "label": "positive"},
    {"text": "Management raised full-year organic revenue guidance to 10-12%.", "label": "positive"},
    {"text": "New AI chip architecture delivers 3x computational efficiency gains.", "label": "positive"},
    {"text": "Strategic partnership expands distribution network into high-growth Asian markets.", "label": "positive"},
    {"text": "Quarterly net income quadrupled to $85 million.", "label": "positive"},
    {"text": "The credit facility was renewed with reduced interest margins and improved covenants.", "label": "positive"},
    {"text": "Automotive delivery volume hit a record 450,000 vehicles in Q4.", "label": "positive"},
    {"text": "Cost cutting program delivered $80 million in operating expense reductions.", "label": "positive"},
    {"text": "Enterprise customer retention rate expanded to 96%.", "label": "positive"},
    {"text": "Biotech startup secured $120 million Series C funding round.", "label": "positive"},
    {"text": "Refinery throughput expanded 18% with zero safety incidents.", "label": "positive"},
    {"text": "Retail holiday sales surpassed forecasts by 8%.", "label": "positive"},
    {"text": "Joint venture won offshore wind concession tender.", "label": "positive"},
    {"text": "Software ARR surpassed $1 Billion benchmark milestone.", "label": "positive"},
    {"text": "Patent allowance secures market exclusivity through 2042.", "label": "positive"},
    {"text": "Operating cash flow funded full capital expenditure program.", "label": "positive"},
    {"text": "Debt-to-EBITDA leverage ratio declined to a conservative 1.2x.", "label": "positive"},
    {"text": "Subscribers grew by 5.2 million ahead of expectations.", "label": "positive"},
    {"text": "Yields on benchmark corporate bonds tightened 25 bps.", "label": "positive"},
    {"text": "Commercial real estate lease occupancy hit 98%.", "label": "positive"},
    {"text": "Strategic acquisition closed under budget and ahead of timeline.", "label": "positive"},

    # Negative (35)
    {"text": "Operating profit fell 40% due to declining demand in European markets.", "label": "negative"},
    {"text": "Company filed for Chapter 11 bankruptcy protection following debt default.", "label": "negative"},
    {"text": "Net loss widened to $120 million amid soaring raw material inflation.", "label": "negative"},
    {"text": "European Commission launched formal antitrust investigation into pricing practices.", "label": "negative"},
    {"text": "FDA issued a formal warning letter regarding manufacturing quality violations.", "label": "negative"},
    {"text": "Credit rating agency downgraded corporate bond rating to junk status.", "label": "negative"},
    {"text": "Automotive manufacturer issued safety recall covering 250,000 vehicles over brake failure.", "label": "negative"},
    {"text": "Revenue declined 18% missing consensus analyst expectations.", "label": "negative"},
    {"text": "Company defaulted on $300 million senior note interest payment.", "label": "negative"},
    {"text": "Geopolitical conflict disrupted crude oil shipping routes driving freight spikes.", "label": "negative"},
    {"text": "Federal Reserve rate hikes increased interest expense by $45 million.", "label": "negative"},
    {"text": "Commercial real estate debt portfolio suffered $1.5 billion loan loss provisions.", "label": "negative"},
    {"text": "Cybersecurity breach exposed 15 million customer records causing brand reputational damage.", "label": "negative"},
    {"text": "Factory explosion halted main production line for 6 weeks.", "label": "negative"},
    {"text": "CEO resigned unexpectedly following accounting audit irregularities.", "label": "negative"},
    {"text": "Labor union strike shut down manufacturing assembly plants.", "label": "negative"},
    {"text": "Regulatory authority imposed a $450 million antitrust compliance penalty.", "label": "negative"},
    {"text": "Inventory write-downs reduced gross profit by $60 million.", "label": "negative"},
    {"text": "Foreign exchange currency devaluation reduced translated net earnings by 14%.", "label": "negative"},
    {"text": "Drug candidate failed primary endpoint in Phase II clinical trials.", "label": "negative"},
    {"text": "Supply chain component shortages forced temporary assembly line shutdowns.", "label": "negative"},
    {"text": "Class action lawsuit filed alleging security fraud and misleading guidance.", "label": "negative"},
    {"text": "Retail foot traffic declined 12% during peak shopping season.", "label": "negative"},
    {"text": "Refinery outage reduced quarterly fuel production by 200,000 barrels.", "label": "negative"},
    {"text": "Dividend was suspended to preserve balance sheet liquidity.", "label": "negative"},
    {"text": "Restructuring plan involves laying off 15% of global workforce.", "label": "negative"},
    {"text": "Commercial paper credit facility access was restricted by syndicate lenders.", "label": "negative"},
    {"text": "Export restrictions blocked semiconductor shipments to key international markets.", "label": "negative"},
    {"text": "Consumer spending contraction squeezed retail operating margins.", "label": "negative"},
    {"text": "Mortgage delinquency rates climbed to 4.8%.", "label": "negative"},
    {"text": "Raw material chemical prices spiked 50% year-over-year.", "label": "negative"},
    {"text": "Aircraft fleet grounded over engine turbine blade cracking.", "label": "negative"},
    {"text": "Impairment charge of $800 million taken on goodwill asset values.", "label": "negative"},
    {"text": "Customer churn rate rose to 8.5% due to price increases.", "label": "negative"},
    {"text": "Debt coverage ratio violated senior lender financial covenants.", "label": "negative"},

    # Neutral (30)
    {"text": "The company will publish its second quarter financial results on August 15.", "label": "neutral"},
    {"text": "Annual general meeting of shareholders will be held in London next month.", "label": "neutral"},
    {"text": "Board of Directors appointed a new non-executive committee member.", "label": "neutral"},
    {"text": "The transaction is subject to customary closing conditions and regulatory approvals.", "label": "neutral"},
    {"text": "Headquarters relocated from Chicago to Dallas under administrative reorganization.", "label": "neutral"},
    {"text": "Trading in company shares resumed following temporary news pending halt.", "label": "neutral"},
    {"text": "Financial statements were prepared in accordance with IFRS accounting standards.", "label": "neutral"},
    {"text": "Company filed standard Form 10-K annual report with the Securities and Exchange Commission.", "label": "neutral"},
    {"text": "Quarterly conference call audio webcasting will begin at 10:00 AM Eastern Time.", "label": "neutral"},
    {"text": "The contract duration spans 36 months with standard extension options.", "label": "neutral"},
    {"text": "Total headcount remained flat at 45,000 employees worldwide.", "label": "neutral"},
    {"text": "Shareholder voting results were published on the investor relations portal.", "label": "neutral"},
    {"text": "The business operates across three primary reporting segments.", "label": "neutral"},
    {"text": "Tax rate guidance remains unchanged at 21%.", "label": "neutral"},
    {"text": "The credit facility matures in October 2028.", "label": "neutral"},
    {"text": "Auditors completed annual statutory balance sheet review.", "label": "neutral"},
    {"text": "Company held annual investor day presentation at New York Stock Exchange.", "label": "neutral"},
    {"text": "Corporate name change took effect on January 1.", "label": "neutral"},
    {"text": "Treasury stock repurchases were executed under pre-existing Rule 10b5-1 plan.", "label": "neutral"},
    {"text": "Subscribed share capital totals 100 million common shares.", "label": "neutral"},
    {"text": "Operating facilities include three domestic distribution centers.", "label": "neutral"},
    {"text": "Third party valuation firm conducted standard property asset appraisal.", "label": "neutral"},
    {"text": "Corporate sustainability report was released for public review.", "label": "neutral"},
    {"text": "Interim CFO appointed while executive search firm conducts candidate interviews.", "label": "neutral"},
    {"text": "The credit rating review process occurs annually in Q3.", "label": "neutral"},
    {"text": "The product is manufactured in compliance with ISO 9001 standards.", "label": "neutral"},
    {"text": "The lease agreement covers 50,000 square feet of office space.", "label": "neutral"},
    {"text": "Consolidated financial results reflect equity method accounting for affiliates.", "label": "neutral"},
    {"text": "Proxy statement was distributed to shareholders of record as of March 15.", "label": "neutral"},
    {"text": "Dividends will be paid on April 30 to shareholders registered by April 10.", "label": "neutral"}
]

df_pb = pd.DataFrame(phrasebank_data)
df_pb.to_csv("data/phrasebank_eval.csv", index=False)
print("Saved data/phrasebank_eval.csv with", len(df_pb), "labeled sentiment samples.")


# 2. 100 Financial Event Classification Headlines (12-15 items per 8 event labels)
event_data = [
    # Geopolitical (13)
    {"text": "Naval blockades in Strait of Hormuz disrupt crude oil exports surging Brent oil 8%", "event_type": "Geopolitical"},
    {"text": "Geopolitical conflict escalates in Eastern Europe threatening natural gas supplies", "event_type": "Geopolitical"},
    {"text": "Trade embargo imposed on foreign critical minerals exports", "event_type": "Geopolitical"},
    {"text": "Military conflict disrupts major red sea maritime shipping routes", "event_type": "Geopolitical"},
    {"text": "Government sanctions frozen foreign central bank assets", "event_type": "Geopolitical"},
    {"text": "Border dispute shuts down strategic freight pipeline", "event_type": "Geopolitical"},
    {"text": "Diplomatic crisis triggers immediate trade tariff hikes", "event_type": "Geopolitical"},
    {"text": "Maritime drone attacks force container ships around Cape of Good Hope", "event_type": "Geopolitical"},
    {"text": "State-backed cyber attack disables national energy grid infrastructure", "event_type": "Geopolitical"},
    {"text": "International treaty exit heightens cross-border trade friction", "event_type": "Geopolitical"},
    {"text": "Port blockade halts LNG terminal exports", "event_type": "Geopolitical"},
    {"text": "Geopolitical tensions trigger spike in sovereign war risk insurance premiums", "event_type": "Geopolitical"},
    {"text": "Sanctions compliance forces international bank asset freeze", "event_type": "Geopolitical"},

    # Macroeconomic (13)
    {"text": "Federal Reserve signals higher interest rates for longer as inflation stays elevated", "event_type": "Macroeconomic"},
    {"text": "US Consumer Price Index inflation surges 4.2% year-over-year", "event_type": "Macroeconomic"},
    {"text": "European Central Bank hikes benchmark interest rates 50 basis points", "event_type": "Macroeconomic"},
    {"text": "Gross Domestic Product growth slows to 0.4% signaling recession risks", "event_type": "Macroeconomic"},
    {"text": "Global central banks tighten monetary policy amid sticky core inflation", "event_type": "Macroeconomic"},
    {"text": "Unemployment rate climbs to 4.5% as labor market cools", "event_type": "Macroeconomic"},
    {"text": "Treasury yield curve inversion deepens to historic levels", "event_type": "Macroeconomic"},
    {"text": "Crude oil price surge accelerates global industrial manufacturing costs", "event_type": "Macroeconomic"},
    {"text": "Producer Price Index inflation beat triggers bond market sell-off", "event_type": "Macroeconomic"},
    {"text": "Central bank balance sheet quantitative tightening reduces banking system liquidity", "event_type": "Macroeconomic"},
    {"text": "Currency devaluations spark emerging market import cost surges", "event_type": "Macroeconomic"},
    {"text": "Housing starts plummet 15% under elevated mortgage interest rates", "event_type": "Macroeconomic"},
    {"text": "Wage growth pressure maintains elevated service sector inflation", "event_type": "Macroeconomic"},

    # Credit Event (13)
    {"text": "Energy contractor files for Chapter 11 bankruptcy following $500M bond default", "event_type": "Credit Event"},
    {"text": "Commercial real estate developer defaults on senior syndicated bank loan", "event_type": "Credit Event"},
    {"text": "Credit rating agency downgrades corporate debt to junk status CCC", "event_type": "Credit Event"},
    {"text": "Regional bank credit spread widens 300 bps over counterparty default fears", "event_type": "Credit Event"},
    {"text": "Distressed debt restructuring exchanges senior notes for equity", "event_type": "Credit Event"},
    {"text": "Corporate borrower breached debt-to-EBITDA leverage financial covenants", "event_type": "Credit Event"},
    {"text": "Subprime auto lender halts operations following liquidity freeze", "event_type": "Credit Event"},
    {"text": "Bond issuer missed coupon interest payment deadline", "event_type": "Credit Event"},
    {"text": "Syndicate lenders issue formal notice of default to wholesale borrower", "event_type": "Credit Event"},
    {"text": "Commercial mortgage backed security loan defaulted at maturity", "event_type": "Credit Event"},
    {"text": "Rating agency places senior debt obligations on credit watch negative", "event_type": "Credit Event"},
    {"text": "Credit default swap spreads surge to historic crisis highs", "event_type": "Credit Event"},
    {"text": "Corporate debtor files emergency financial restructuring petition", "event_type": "Credit Event"},

    # Regulatory (13)
    {"text": "FDA issues unexpected warning letter over quality control violations at plant", "event_type": "Regulatory"},
    {"text": "European Union Antitrust commission opens inquiry into tech pricing power", "event_type": "Regulatory"},
    {"text": "Securities Commission fines investment bank $200 million for compliance failures", "event_type": "Regulatory"},
    {"text": "Department of Justice files antitrust lawsuit to block corporate merger", "event_type": "Regulatory"},
    {"text": "Environmental agency levies record fine over industrial chemical spill", "event_type": "Regulatory"},
    {"text": "Banking regulator mandates higher Tier 1 capital buffer requirements", "event_type": "Regulatory"},
    {"text": "Data protection authority fines social network over privacy law breach", "event_type": "Regulatory"},
    {"text": "Regulatory inquiry launched into commercial bank anti-money laundering controls", "event_type": "Regulatory"},
    {"text": "Consumer protection bureau orders customer fee refunds", "event_type": "Regulatory"},
    {"text": "Energy regulator imposes strict carbon emissions cap regulations", "event_type": "Regulatory"},
    {"text": "Pharma company receives formal regulatory inspection non-compliance audit", "event_type": "Regulatory"},
    {"text": "Financial conduct authority restricts trading license following audit investigation", "event_type": "Regulatory"},
    {"text": "Trade commission blocks cross-border technology export license", "event_type": "Regulatory"},

    # Earnings (12)
    {"text": "JPMorgan Chase reports record Q1 earnings beating Wall Street consensus", "event_type": "Earnings"},
    {"text": "Microsoft Azure cloud revenue accelerates 31% driving profit beat", "event_type": "Earnings"},
    {"text": "Quarterly net income missed consensus forecast by 15%", "event_type": "Earnings"},
    {"text": "Company raises full-year earnings guidance following strong Q3 sales", "event_type": "Earnings"},
    {"text": "Board declared a 10% dividend payout increase after strong cash flows", "event_type": "Earnings"},
    {"text": "Operating profit margins contracted 200 bps in Q4 results", "event_type": "Earnings"},
    {"text": "Revenue declined 8% year-over-year in quarterly earnings release", "event_type": "Earnings"},
    {"text": "EBITDA expanded 25% beating analyst revenue expectations", "event_type": "Earnings"},
    {"text": "Company cut forward annual revenue guidance citing soft demand", "event_type": "Earnings"},
    {"text": "Earnings per share of $2.40 beat consensus by $0.35", "event_type": "Earnings"},
    {"text": "Free cash flow reached record $1.2 Billion in quarterly release", "event_type": "Earnings"},
    {"text": "Gross margin guidance reduced due to elevated manufacturing costs", "event_type": "Earnings"},

    # Product Launch (12)
    {"text": "NVIDIA unveils next-generation Blackwell Ultra AI chip architecture", "event_type": "Product Launch"},
    {"text": "Apple releases Vision Pro headset across European retail markets", "event_type": "Product Launch"},
    {"text": "Tesla announces over-the-air software update introducing autonomous driving features", "event_type": "Product Launch"},
    {"text": "Automobile manufacturer recalls 150,000 vehicles over steering software glitch", "event_type": "Product Launch"},
    {"text": "Pharmaceutical firm launches new FDA-approved diabetes drug", "event_type": "Product Launch"},
    {"text": "Tech company unveils enterprise cloud AI assistant platform", "event_type": "Product Launch"},
    {"text": "EV maker delays new vehicle model production launch to 2027", "event_type": "Product Launch"},
    {"text": "Consumer electronics firm announces new flagship smartphone model line", "event_type": "Product Launch"},
    {"text": "Biotech startup debuts revolutionary gene editing clinical platform", "event_type": "Product Launch"},
    {"text": "Software provider releases new cloud security product suite", "event_type": "Product Launch"},
    {"text": "Medical device manufacturer recalls heart monitor over battery defect", "event_type": "Product Launch"},
    {"text": "Fintech platform launches real-time cross-border payment API", "event_type": "Product Launch"},

    # Merger/Acquisition (12)
    {"text": "Apple acquires generative AI startup for $2.4 Billion in cash", "event_type": "Merger/Acquisition"},
    {"text": "Pharma giant finalizes $15 Billion takeover acquisition of biotech firm", "event_type": "Merger/Acquisition"},
    {"text": "Energy producer enters definitive agreement to merge with regional peer", "event_type": "Merger/Acquisition"},
    {"text": "Private equity firm submits $8 Billion buyout bid for retail chain", "event_type": "Merger/Acquisition"},
    {"text": "Defense contractor acquires satellite manufacturing firm", "event_type": "Merger/Acquisition"},
    {"text": "Proposed mega-merger terminated following antitrust regulatory pressure", "event_type": "Merger/Acquisition"},
    {"text": "Bank completes acquisition of regional wealth management firm", "event_type": "Merger/Acquisition"},
    {"text": "Industrial firm divests non-core chemical division for $900M", "event_type": "Merger/Acquisition"},
    {"text": "Tech firm acquires cybersecurity startup to bolster cloud defense", "event_type": "Merger/Acquisition"},
    {"text": "Shareholders approve all-cash merger agreement", "event_type": "Merger/Acquisition"},
    {"text": "Hostile takeover tender offer launched for semiconductor manufacturer", "event_type": "Merger/Acquisition"},
    {"text": "Joint venture partners finalize corporate asset merger", "event_type": "Merger/Acquisition"},

    # Other (12)
    {"text": "Company relocates corporate headquarters to new facility in Dallas", "event_type": "Other"},
    {"text": "Annual general meeting of shareholders scheduled for next Tuesday", "event_type": "Other"},
    {"text": "Board of Directors appoints new independent non-executive chairman", "event_type": "Other"},
    {"text": "Company releases annual corporate ESG sustainability report", "event_type": "Other"},
    {"text": "Shareholder proxy materials distributed for upcoming annual meeting", "event_type": "Other"},
    {"text": "Executive search firm retained to identify permanent Chief Financial Officer", "event_type": "Other"},
    {"text": "Company trading symbol updated on international stock exchange", "event_type": "Other"},
    {"text": "Statutory audit firm completed annual balance sheet review", "event_type": "Other"},
    {"text": "Company celebrates 50th anniversary milestone at corporate summit", "event_type": "Other"},
    {"text": "Investor day presentation broadcast scheduled for next week", "event_type": "Other"},
    {"text": "Corporate foundation donates $5M to educational STEM initiatives", "event_type": "Other"},
    {"text": "Company standard lease renewal finalized for regional office building", "event_type": "Other"}
]

df_ev = pd.DataFrame(event_data)
df_ev.to_csv("data/event_eval.csv", index=False)
print("Saved data/event_eval.csv with", len(df_ev), "labeled event classification headlines.")
