# Effective Giving: U.S. Charity Effectiveness

This repository contains a public website template and the research foundation for evaluating which U.S. charities are most likely to create the greatest social benefit from an **additional donated dollar**. The project is in prototype development. It publishes **no charity recommendations or effectiveness findings yet**.

The permanent product and research scope is defined in [`docs/implementation_plan.md`](docs/implementation_plan.md). Contributors must read that plan and [`AGENTS.md`](AGENTS.md) before changing project direction, collecting data, or drafting public claims.

## Current implementation status

- **Phase 0 — Website template:** complete. The static pages in `website/src/pages/` demonstrate the intended information architecture with conspicuous placeholder labels.
- **Phase 1 — Research and governance foundation:** complete. Methodology, governance, data-source, and review templates are under `docs/`.
- **Phase 2 — Minimum viable data prototype:** complete. `data/processed/charity_profiles.json` contains 50 non-evaluated charity identity/financial prototypes—10 in each initial cause area—with raw source snapshots, field-level quality flags, and documented provenance.
- **Phase 3 — Evidence map prototype:** complete as a draft internal research product. Five structured maps cover 31 intervention categories, shared outcome metrics, 27 public evidence sources, explicit harms, research gaps, and review controls. These grades apply to intervention categories—not charities—and have not yet received outside review.
- **Phases 4 onward:** not started. The repository does not yet contain marginal cost-effectiveness estimates, charity reviews, or recommendations.

A record’s inclusion in the Phase 2 dataset means only that it was selected to test the schema and workflow. **Selection is not endorsement, evaluation, ranking, or a claim of impact.** Form 990 availability demonstrates a kind of financial transparency; it does not demonstrate impact transparency or effectiveness.

## Evaluation standard

The central question is: **what would additional funding accomplish?** Reviews must distinguish:

1. financial transparency from impact transparency;
2. activities and outputs from outcomes caused by a program;
3. evidence about an intervention from evidence about a particular charity’s implementation;
4. average historical cost from marginal cost and room for more funding;
5. human welfare benefits from government fiscal savings; and
6. empirical estimates from moral weights and other value judgments.

Evidence grades use: `Strong`, `Moderate`, `Promising`, `Mixed`, `Weak`, `Potentially Harmful`, and `Insufficient Evidence`. Uncertainty, contrary evidence, negative findings, and missing data are publication requirements rather than optional caveats.

## Initial cause areas

- homelessness;
- criminal recidivism and reentry;
- criminal justice;
- legal immigrant integration; and
- drug addiction treatment and harm reduction.

## Repository map

```text
docs/
  implementation_plan.md          Product source of truth
  methodology/                    Evaluation and governance rules
  product/                        Preregistered public-product templates
  templates/                      Evidence-map research template
  evidence_maps/                  Generated Phase 3 cause-area maps
  data_sources/                   Source-specific collection notes
data/
  charity_selection.csv           50 deliberately scoped prototype candidates
  source_registry.csv             Source-level provenance registry
  raw/propublica/                 Immutable API response snapshots
  processed/                      Normalized JSON/CSV and quality report
  schemas/                        Machine-readable profile schema
  evidence_maps/                  Canonical maps and evidence source registry
scripts/
  build_charity_prototype.py      Reproducible public-data ingestion job
  build_evidence_map_docs.py      Deterministic Phase 3 Markdown renderer
tests/
  test_phase2_data.py             Dataset, provenance, and schema checks
  test_phase3_evidence_maps.py    Evidence-map completeness and provenance checks
website/src/                      Static Phase 0 website template
```

## Rebuild and validate the research prototypes

Python 3.11+ is sufficient; the pipeline and tests use only the standard library.

```bash
# Deterministically rebuild normalized outputs from committed raw snapshots.
python scripts/build_charity_prototype.py --retrieval-date 2026-06-12

# Explicitly refresh public API snapshots and record a new retrieval date.
# Review resulting source changes before committing them.
python scripts/build_charity_prototype.py --refresh --retrieval-date YYYY-MM-DD

# Regenerate Phase 3 evidence-map documents from canonical JSON.
python scripts/build_evidence_map_docs.py

# Confirm generated documents are current.
python scripts/build_evidence_map_docs.py --check

# Validate Phase 2 records plus Phase 3 maps, grades, metrics, provenance, and guardrails.
python -m unittest discover -s tests -v
```

The refresh path queries the public ProPublica Nonprofit Explorer API. Its organization object reports IRS exempt-organization data, and its filing extracts expose selected Form 990 fields. See [`docs/data_sources/propublica_nonprofit_explorer.md`](docs/data_sources/propublica_nonprofit_explorer.md). A refresh must never silently turn records into public claims; interpretation requires the later evidence, cost-effectiveness, funding-gap, charity-response, and review workflows.

## Contributor workflow

1. Read the implementation plan and applicable methodology document.
2. Register a public source before using it.
3. Preserve raw source material or an auditable reference when terms permit.
4. Normalize values without inferring missing facts.
5. attach an allowed quality status to every extracted field.
6. Separate source-derived values, analyst calculations, and judgments.
7. Manually review high-stakes or ambiguous records.
8. Run tests and source-completeness checks.
9. Record conflicts, corrections, and update history publicly when content is published.

Allowed quality statuses are `verified`, `machine_extracted`, `manual_review_needed`, `conflicting_sources`, `missing`, and `not_applicable`.

## Key documents

- [Charity profile schema](docs/methodology/charity_profile_schema.md)
- [Evidence grading](docs/methodology/evidence_grading.md)
- [Cost-effectiveness model](docs/methodology/cost_effectiveness_model.md)
- [Room for more funding](docs/methodology/room_for_more_funding.md)
- [Research and publication governance](docs/methodology/research_governance.md)
- [Conflict-of-interest policy](docs/methodology/conflict_of_interest_policy.md)
- [Corrections policy](docs/methodology/corrections_policy.md)
- [Charity review template](docs/product/charity_review_template.md)
- [Cause-area evidence-map template](docs/templates/cause_area_evidence_map_template.md)
- [Phase 2 manual review report](docs/phase2_manual_review.md)
- [Phase 3 completion record](docs/phase3_completion.md)
- [Phase 3 evidence-map data notes](data/evidence_maps/README.md)

## Data and licensing

Only public sources may be used until a formal data-governance process authorizes otherwise. Source access does not imply unrestricted redistribution rights. Each registry row records usage notes and limitations; contributors must re-check current provider terms before refreshing or redistributing data. Do not commit confidential charity submissions, personal data unnecessary for evaluation, access credentials, or licensed content the project lacks permission to republish.
