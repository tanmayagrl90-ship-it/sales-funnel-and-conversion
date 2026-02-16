# sales-funnel-and-conversion

Sales Funnel & Conversion — Drop-off Analysis

This repository contains a reproducible project to analyze user drop-off across a purchase funnel, calculate key conversion KPIs, visualize problem stages, and provide prioritized recommendations (pricing, UX, A/B tests).

Quick start (prototype):

1) Create and activate a Python environment

   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```

2) Generate synthetic data and open the analysis notebook

   ```bash
   python src/data_generator.py --n-users 5000 --out data/synthetic_funnel.csv
   jupyter lab notebooks/sales_funnel_analysis.ipynb
   ```

What this delivers

- `notebooks/sales_funnel_analysis.ipynb` — exploratory analysis, visualizations, KPI exports, actionable recommendations
- `src/data_generator.py` — realistic synthetic funnel event generator (used by the notebook)
- `data/` — place for input CSVs and generated samples
- `reports/` — KPI CSVs and exported figures

Next steps / recommended scope

1. Prototype (current): runnable notebook + synthetic data for stakeholder demos.
2. Productionize: add a lightweight dashboard (Streamlit), scheduled ETL to refresh KPIs, and A/B experiment reporting.
3. Validation: plug real event stream / analytics export (CSV, BigQuery) and add tests for data quality (missing stages, timestamp anomalies).

If you want, I can:
- add a Streamlit dashboard scaffold
- add CI / Docker for scheduled KPI generation
- connect real data sources (CSV / DB)

Enjoy — open the notebook to run the analysis and see the KPI summaries.
