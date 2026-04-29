# Malaysian House Price Index Prediction
**Linear Algebra Group Project**

Predicting the Malaysian House Price Index (MHPI) using two linear algebra techniques: Least Squares Regression and Discrete Dynamical Systems. Data spans 2010–2023.

---

## Problem Statement

Housing affordability is a growing concern in Malaysia. This project uses macroeconomic indicators to model and forecast the MHPI, answering: *which economic factors drive house prices, and where are prices headed?*

---

## Dataset

14 years of annual data (2010–2023), compiled from official Malaysian sources:

| Variable | Source | Range |
|---|---|---|
| `price_index` | MHPI (Bank Negara / NAPIC) | 100.0 – 218.3 |
| `Population_000s` | DOSM Malaysia | 28,589 – 33,402 (thousands) |
| `GDP_RM_Million` | DOSM (2010–2014 back-calculated) | RM 1.82M – RM 3.14M million |
| `OPR_Rate_Percentage` | Bank Negara Malaysia | 1.75% – 3.25% |

> GDP for 2010–2014 was back-calculated from the 2015 base using official BNM annual growth rates.

---

## Methods

### 1. Least Squares Regression (LSR)

Fits a multi-variable linear model using the normal equation:

$$\mathbf{x} = (\mathbf{A}^T \mathbf{A})^{-1} \mathbf{A}^T \mathbf{b}$$

**Model equation (standardized):**
```
Price Index = 170.06 + 33.28(Population) + 3.37(GDP) - 1.30(OPR Rate)
```

**Results:**
- R² = **0.9975** (explains 99.75% of variance)
- RMSE = ±1.86 index points
- Population is the strongest predictor (r = 0.998)

### 2. Discrete Dynamical System (DDS)

Models price as a sequential process — next year's price depends on this year's:

$$P_{t+1} = aP_t + b$$

**Fitted equation:**
```
P_{t+1} = 0.9098 × P_t + 24.11
```

**Results:**
- R² = **0.9936**
- RMSE = ±2.61 index points
- Growth factor |a| < 1 → **stable system**, converges to equilibrium P* ≈ 267.20
- Forecast: MHPI reaches ~233.7 by 2027

---

## Key Findings

- MHPI grew **118.3%** from 2010 to 2023 (~8.45%/year average)
- **Population** is the dominant driver (r = 0.998 with MHPI)
- **OPR Rate** has a negative relationship — higher interest rates suppress prices
- Both models agree the system is stable and converging toward ~267 index points
- LSR is better for causal explanation; DDS is better for standalone forecasting

---

## Files

```
.
├── analysis.ipynb          # Main notebook — all analysis, plots, and results
├── gdp_back-caclulate.py   # Data prep script — merges population, GDP, OPR data
├── project_final_data.csv  # Final cleaned dataset used in analysis
├── gdp_state_real_supply.csv
├── opr-decision.csv
├── population_malaysia.csv
└── Table MHPI 2024P.xlsx   # Raw MHPI data from NAPIC
```

---

## How to Run

```bash
# Install dependencies
pip install pandas numpy matplotlib seaborn scipy

# Run data prep (if regenerating project_final_data.csv)
python gdp_back-caclulate.py

# Open the main analysis
jupyter notebook analysis.ipynb
```

---

## Tech Stack

- Python 3
- NumPy (matrix operations, normal equations)
- Pandas (data wrangling)
- Matplotlib / Seaborn (visualizations)
- SciPy (Q-Q plots, distribution checks)
