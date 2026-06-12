# Phase 3 Evidence Map Data

`evidence_maps.json` is the canonical structured Phase 3 research prototype. It contains five cause-area maps, intervention definitions and grades, outcome metrics, research gaps, review controls, and a shared study catalog.

`source_registry.csv` is the auditable source ledger for every study or evidence synthesis cited by the maps. Each row records its public URL, access method, retrieval date, usage note, extracted fields, limitations, and appraisal confidence.

The Markdown files in `docs/evidence_maps/` are generated views. Rebuild them with:

```bash
python scripts/build_evidence_map_docs.py
```

Use `python scripts/build_evidence_map_docs.py --check` in validation. This phase is a rapid, single-reviewer prototype rather than an exhaustive systematic review. No intervention grade transfers automatically to a charity, and these files do not estimate cost-effectiveness or room for more funding.
