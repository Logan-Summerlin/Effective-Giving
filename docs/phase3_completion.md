# Phase 3 Completion: Evidence Map Prototype

Phase 3 of `docs/implementation_plan.md` is implemented as five draft, auditable evidence maps covering all initial cause areas. The maps remain internal research prototypes until named human review and the required second review of `Strong` and `Potentially Harmful` judgments are complete.

## Deliverables

- A canonical structured dataset at `data/evidence_maps/evidence_maps.json`.
- A dedicated evidence source registry at `data/evidence_maps/source_registry.csv`.
- Generated cause-area maps in `docs/evidence_maps/`.
- A deterministic renderer and stale-output check at `scripts/build_evidence_map_docs.py`.
- Automated Phase 3 completeness, vocabulary, provenance, guardrail, and generated-output tests.

## Exit-gate coverage

Each cause area includes:

1. a review question, target population, U.S. scope, search date, evidence cutoff, protocol limitations, and update date;
2. intervention categories with definitions, theories of change, comparators, outcomes, implementation requirements, equity considerations, adverse outcomes, and use boundaries;
3. a comparative table and intervention grades using the controlled methodology vocabulary;
4. explicit outcome metrics that preserve participant wellbeing and do not conflate it with government fiscal savings;
5. key-study IDs linked to a source registry with public URLs, retrieval dates, extraction notes, known limitations, and appraisal confidence;
6. positive, uncertain, weak/mixed, and potentially harmful findings rather than a one-sided “what works” list; and
7. research gaps and early-update triggers.

Across the five-map portfolio, the prototype identifies `Strong`, `Moderate`, `Promising`, `Mixed`, `Weak`, `Potentially Harmful`, and `Insufficient Evidence` interventions. Every individual map includes at least one favorable grade, one uncertainty grade, and one potentially harmful intervention. This preserves honest differences in evidence maturity rather than forcing every cause area into every grade.

## Research-status limitations

This implementation is a rapid evidence-map prototype, not a PRISMA systematic review. Searching and extraction were completed as a structured single-reviewer pass; there was no dual screening, formal certainty framework, pooled reanalysis, or outside review. Public use must therefore retain the draft label. In accordance with the evidence-grading policy, `Strong` and `Potentially Harmful` grades require a second reviewer before they are used in a public recommendation.

Phase 3 intentionally does not score charities, calculate marginal cost-effectiveness, analyze charity-specific room for more funding, or replace the website's placeholder cause-area content. Those are later phases in the implementation plan.
