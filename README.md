# Medical-Debt Affordability Risk Monitor

Quantifies consumer repayment burden and financial exposure from medical debt using
CFPB complaint microdata, CFPB published research, and CMS healthcare-cost data.

## Data sources (all public, all cited in-app)

1. **CFPB Consumer Complaint Database** — full bulk download (18.2M complaints,
   retrieved Oct 2026). Medical-debt subset: Product = "Debt collection" and
   Sub-product = "Medical debt" (n = 77,968). Note: CFPB's medical-debt
   sub-product tag begins April 2017.
2. **CFPB published research** — the Bureau's January 2025 medical-debt rule
   estimated $49B in medical bills on the credit reports of ~15M Americans
   (rule vacated July 2025; figures are the CFPB's).
3. **CMS Procedure Price Lookup** — national average Medicare payment amounts by
   procedure, grouped into cost tiers.
4. **CMS National Health Expenditure Accounts** — per-capita personal health care
   spending by state, used in geographic risk segmentation.
5. **U.S. Census Bureau** — 2024 state resident-population estimates (per-100k denominators).

## What the project does

- **Repayment-burden quantification:** 77,968 medical-debt complaints characterized
  by year, state (per 100k), company, issue and company response.
- **Affordability-risk segments:** states segmented on two real inputs —
  medical-debt complaints per 100k (CFPB) and per-capita health spending (CMS) —
  via median-split quadrants. Rule-based, fully explainable.
- **Repayment scenarios:** for each CMS procedure-cost tier, months-to-repay under
  illustrative monthly payment capacities ($50/$100/$250, stated assumptions,
  0% interest typical of medical debt). Scenarios are labeled as modeled, not empirical.
- **Dashboard monitoring:** Streamlit app with trend, geography, driver, and
  scenario views.

## Key findings (v1)

- Complaints peaked in 2021 (10,490), fell 31% by 2024 (7,265), rebounded 22% in 2025 (8,843).
- 47% of medical-debt complaints dispute that the debt is owed at all.
- 89% close with only an explanation; 0.3% close with monetary relief.
- Geographic burden concentrates in the South (GA 54.7 per 100k leads; FL, SC, AL,
  LA, TX, MS, NC all in the top 10).

## Caveats

- Complaints are a self-selected sample of consumer distress, not a prevalence
  survey. Rates are a burden *signal*, not a population estimate.
- Repayment scenarios use stated illustrative assumptions, not observed balances.

## Run it

```
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

## Reproduce the analysis

```
python scripts/extract_medical.py   # streams the CFPB bulk CSV -> data/medical_debt_complaints.csv
python scripts/analyze_phase1.py    # findings + charts
```
