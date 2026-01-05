
# Fixed Income Risk Analysis

This project analyzes fixed income portfolio performance under varying **interest rate and credit spread environments**, with a focus on identifying key risk drivers and evaluating hedging effectiveness.  
The analysis applies quantitative modeling and scenario-based evaluation to support **risk-aware portfolio decision-making**.

*This project was completed as a group project for a graduate-level fixed income course and focuses on translating quantitative models into interpretable risk insights.*

---

## Key Objectives

- Identify the relative impact of **interest rate risk vs. credit spread risk** on fixed income portfolio returns  
- Evaluate how **hedging frequency** affects PnL stability and downside risk  
- Assess the effectiveness of **delta hedging strategies** under different market and volatility conditions  

---

## Key Findings & Insights

- Credit spread movements were a **primary driver of portfolio volatility**, particularly during stressed market periods.  
- More frequent hedging rebalancing improved hedge accuracy but introduced **higher transaction-driven PnL variability**, highlighting a trade-off between precision and cost.  
- Delta hedging reduced short-term volatility, but its effectiveness diminished under rapidly changing volatility regimes.  
- Scenario-based analysis demonstrated how **model assumptions materially impact risk estimates**, reinforcing the importance of model transparency in risk management and decision-making.

---

## Key Features

- Credit spread and interest rate risk decomposition  
- SABR model calibration for volatility modeling  
- Swaption pricing using the Black-76 framework  
- Delta hedging strategy evaluation and PnL comparison across rebalancing frequencies  

---

## Project Structure

**Fixed-Income/**
- processData.py — Data cleaning and preprocessing  
- class2.py — Model calibration and risk calculations  
- group.py — Portfolio construction  
- Hedged.py — Hedging strategy and PnL analysis  
- plot.py — Visualization  

---
## Tech Stack

- Python (NumPy, Pandas, Matplotlib)
- Time-series analysis
- Quantitative risk modeling
- Scenario analysis and analytical reporting
