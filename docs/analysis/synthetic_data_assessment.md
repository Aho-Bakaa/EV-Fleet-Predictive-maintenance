# Synthetic Data Analysis and Relevance Filter

## Dataset Origin (Confirmed)

The core fleet datasets were generated from scratch via notebook code, not collected from production telemetry.
Primary generator notebook: `C:\Users\anmol\OneDrive\Desktop\Work\EV_FLEET\data_generation.ipynb`.

Evidence in code includes repeated usage of:
- `np.random.seed(...)`
- `rng = np.random.default_rng(...)`
- `rng.normal(...)`, `rng.uniform(...)`, `rng.random(...)`
- `df.to_csv('fleet_base_data_v2.csv', ...)`
- `df_final.to_csv('fleet_complete_v2.csv', ...)`

## Startup Critique of Synthetic Data

Pros:
- Fast way to prototype an end-to-end ML + API system.
- Lets us test feature engineering and alert logic before real data integrations.

Risks:
- Reported metrics can be overly optimistic because train/test come from the same synthetic generator assumptions.
- Correlation plots may encode generator design choices, not real-world causality.
- Startup buyers/investors may challenge production transferability without real fleet validation.

## What Is Relevant to Keep in GitHub

Keep:
- `docs/analysis/Report.pdf` for narrative context.
- `docs/analysis/model_training_results.csv` as baseline benchmark table.
- `docs/analysis/*features.txt` for model input transparency.
- `docs/assets/correlations/*.png` as exploratory evidence (explicitly labeled synthetic).

Exclude:
- Raw large CSVs (`fleet_complete_v2.csv`, `fleet_base_data_v2.csv`, etc.) from repo history.
- Notebook outputs not directly tied to model/API narrative.
- Environment-specific one-off scripts and caches.

## Recommendation for Electric AI Startup Pitch

Present this as:
- Phase 1: Synthetic-data validated MVP (current state).
- Phase 2: Real telemetry pilot with 1-3 fleets for calibration and external validation.

Positioning language:
- "The current models and plots are based on controlled synthetic fleet simulations and are intended for architecture validation, not final production claims."
