# Production-Style Data Cleaning Pipeline (Intern-Friendly)

This mini-project demonstrates a production-minded approach to data cleaning for ML training data.

## What it demonstrates

- **Data contract validation** (required columns and field-level checks)
- **Deterministic cleaning** (normalization + type coercion)
- **Quarantine flow** (invalid rows are isolated with reason codes)
- **Deduplication policy** (latest record per user)
- **Data quality report** (row counts, quarantine rate, issue counts)
- **Test coverage** (end-to-end pipeline test)

## Project layout

```text
production_data_pipeline/
  src/data_pipeline/
    contracts.py
    cleaners.py
    quality.py
    io_utils.py
    pipeline.py
  tests/test_pipeline.py
  sample_data/raw_users.csv
```

## Run locally

From repository root:

```bash
PYTHONPATH=production_data_pipeline/src \
python -m data_pipeline.pipeline \
  --raw production_data_pipeline/sample_data/raw_users.csv \
  --clean production_data_pipeline/output/clean.csv \
  --quarantine production_data_pipeline/output/quarantine.csv \
  --report production_data_pipeline/output/report.json
```

## Run tests

```bash
PYTHONPATH=production_data_pipeline/src python -m unittest discover -s production_data_pipeline/tests -v
```

## Notes for real startup use

- Add a scheduler/orchestrator (Airflow, Dagster, Prefect)
- Persist metrics to monitoring dashboards and alert on thresholds
- Add CI checks and enforce data contracts in pull requests
- Version raw/clean datasets and pipeline code together
