# Phase 2 Data Prototype

This directory contains 50 **non-evaluated** charity profile prototypes, balanced at 10 records across each of the five initial cause areas. Inclusion tests data collection and schema design only; it is not a recommendation or claim of effectiveness.

## Files

- `charity_selection.csv`: stable selection list and neutral rationale.
- `source_registry.csv`: documentation plus one source row per charity endpoint.
- `raw/propublica/*.json`: public API snapshots retained for reproducibility.
- `processed/charity_profiles.json`: canonical normalized records.
- `processed/charity_profiles.csv`: flat discovery/export view; JSON remains canonical.
- `processed/data_quality_report.json`: counts and known source gaps.
- `manual_review.csv`: stratified review ledger for two records per cause area.
- `schemas/charity_profile.schema.json`: machine-readable structural contract.

## Regeneration

Run `python scripts/build_charity_prototype.py --retrieval-date 2026-06-12` to regenerate from snapshots. Use `--refresh` only when deliberately updating source data; provide the actual retrieval date, inspect changes, rerun tests, and update manual review if material fields changed.

Raw API data may include public names and addresses of nonprofit entities. Do not add unnecessary personal information. Check provider terms before redistribution. Missing values remain missing, and no downstream consumer should treat a blank as zero.
