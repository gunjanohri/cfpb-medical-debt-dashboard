"""Medical-Debt Affordability Risk Monitor — CFPB complaints + CMS cost data."""
import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Medical-Debt Affordability Risk Monitor", layout="wide")
st.title("Medical-Debt Affordability Risk Monitor")
st.caption("Sources: CFPB Consumer Complaint Database (bulk download, retrieved Oct 2026) and "
           "CMS healthcare-cost data. See Methodology tab for vintage, coverage and caveats.")

F = json.load(open("findings_phase1.json"))
n = F["n_medical_debt_complaints"]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Medical-debt complaints analyzed", f"{n:,}")
k2.metric("Share of all debt-collection complaints", f'{F["medical_share_of_debt_collection_pct"]}%')
k3.metric("Top issue: debt not owed", "47.0%")
k4.metric("CFPB research context", "15M Americans / $49B")

t1, t2, t3, t4, t5 = st.tabs(["Trends", "Geography", "Complaint drivers", "Cost tiers & scenarios", "Methodology"])

with t1:
    st.subheader("Medical-debt complaints by year received")
    st.image("trend.png")
    st.markdown(
        "- Complaints peaked in **2021 (10,490)**, fell **31% by 2024 (7,265)**, then rebounded **22% in 2025 (8,843)**.\n"
        "- 2026 is a partial year (through Oct 5, 2026).\n"
        "- The CFPB's medical-debt sub-product tag begins in April 2017, so pre-2017 volumes are not comparable."
    )

with t2:
    st.subheader("Complaint burden by state (per 100k residents, 2024 Census population)")
    st.image("states.png")
    sr = pd.read_csv("state_rates.csv")
    st.dataframe(sr.head(15)[["State", "complaints", "per_100k"]].rename(
        columns={"State": "State", "complaints": "Complaints", "per_100k": "Per 100k residents"}),
        hide_index=True, use_container_width=True)
    st.markdown(
        "The South carries the heaviest burden: Georgia (54.7), Florida (43.7), South Carolina (33.8), "
        "Alabama (31.6), Louisiana (30.6), Texas (30.1) and Mississippi (29.9) are all in the top 10 — "
        "consistent with CFPB research finding medical debt concentrated in low-income Southern communities."
    )

with t3:
    st.subheader("What consumers complain about")
    st.image("issues.png")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top companies complained about**")
        st.image("companies.png")
    with c2:
        st.markdown("**How companies responded**")
        resp = pd.Series(F["company_response_mix"])
        st.dataframe((resp / resp.sum() * 100).round(1).rename("Share (%)"), use_container_width=True)
    st.markdown(
        "**Key texture:** 47% of medical-debt complaints dispute that the debt is owed at all, and "
        "89% of complaints close with only an explanation — just 0.3% close with monetary relief. "
        "The most-complained-about firms are medical-debt specialists (TeamHealth/HCFS, Transworld Systems, "
        "Commonwealth Financial, Capio Partners), not generalist collectors."
    )

with t4:
    st.subheader("Procedure-cost tiers and repayment scenarios")
    st.markdown(
        "National-average Medicare payments for 16 common procedures (CMS Procedure Price Lookup, "
        "2026 rates, hospital outpatient setting), grouped into quartiles. Repayment scenarios use the "
        "tier median as a conservative cost proxy at illustrative $50/$100/$250 monthly capacities, "
        "0% interest (typical for medical debt). **Scenarios are modeled with stated assumptions, not observed balances.**"
    )
    tiers = pd.read_csv("procedure_tiers.csv")
    st.dataframe(tiers[["procedure", "code", "avg_medicare_payment", "tier"]].rename(
        columns={"procedure": "Procedure", "code": "Code",
                 "avg_medicare_payment": "Avg Medicare payment ($)", "tier": "Cost tier"}),
        hide_index=True, use_container_width=True)
    st.image("scenarios.png")
    sc = pd.read_csv("repayment_scenarios.csv")
    st.dataframe(sc.rename(columns={"tier": "Tier", "tier_median_cost": "Tier median ($)",
        "monthly_payment_capacity": "$/month", "months_to_repay": "Months to repay",
        "extended_burden": ">24 mo burden", "n_procedures_in_tier": "Procedures"}),
        hide_index=True, use_container_width=True)
    st.markdown(
        "**Takeaway:** at $100/month, Tier 1-2 procedures clear in under a year, but Tier 3 "
        "(median $2,575) takes 26 months and Tier 4 (median $4,389) takes 44 months — extended "
        "burden territory. And these are conservative: uninsured patients often face chargemaster "
        "prices several multiples of Medicare rates."
    )
    st.subheader("State affordability-risk segments")
    st.markdown(
        "Rule-based quadrants (median splits) on two real inputs: medical-debt complaints per 100k "
        "(CFPB) and per-capita personal health care spending (CMS NHE, 2020). Counter-intuitive finding: "
        "the correlation is **negative (-0.36)** — the highest-burden states (GA, FL, SC, TX, NC) sit "
        "**below** median spending. Distress tracks affordability gaps, not absolute cost levels."
    )
    st.image("segments.png")
    sg = pd.read_csv("state_segments.csv")
    st.dataframe(sg[["state", "per_100k", "per_capita_spending", "segment"]].rename(
        columns={"state": "State", "per_100k": "Per 100k", "per_capita_spending": "Spending/capita ($)",
                 "segment": "Segment"}), hide_index=True, use_container_width=True)

with t5:
    st.subheader("Methodology and caveats")
    st.markdown(
        "- **Complaint data:** full CFPB Consumer Complaint Database bulk download (18.2M complaints, "
        "retrieved Oct 2026). Medical-debt subset = Product 'Debt collection' + Sub-product 'Medical debt' "
        f"(n={n:,}). Medical-debt tagging begins April 2017.\n"
        "- **Context figures:** the CFPB's January 2025 medical-debt rule estimated $49B in medical bills "
        "on the credit reports of ~15M Americans (rule vacated July 2025; figures are CFPB's).\n"
        "- **State rates** use 2024 Census resident-population estimates.\n"
        "- Complaints are a self-selected sample of consumer distress, not a prevalence survey — "
        "treat rates as a burden signal, not a population estimate."
    )
