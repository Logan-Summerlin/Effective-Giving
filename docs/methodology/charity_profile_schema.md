# Charity Profile Schema

**Status:** Phase 1 draft, implemented by the Phase 2 prototype
**Machine-readable companion:** `data/schemas/charity_profile.schema.json`

## Purpose and boundaries

A charity profile standardizes identity, financial, program, transparency, evidence, and funding information without implying that every field is known or that a listed charity is effective. The stable internal identifier is based on the legal entity’s EIN when available. Separate legal entities, chapters, affiliates, and fiscally sponsored projects must not be merged merely because they share a brand.

The schema separates four kinds of content:

1. **Source-derived facts** copied or normalized from public records.
2. **Analyst calculations** reproducible from cited inputs.
3. **Analyst judgments** such as evidence grades and applicability assessments.
4. **Publication status** indicating whether a record is merely a candidate, under review, or eligible for a recommendation.

`null` is not interchangeable with zero. A missing amount means the source or extraction did not establish a value; zero means the source affirmatively reported zero.

## Required top-level objects

| Object | Required content | Rule |
|---|---|---|
| `schema_version` | Semantic version | Changes when meaning or validation changes. |
| `charity_id` | Stable internal ID | Phase 2 uses `us-ein-#########`; never recycle it. |
| `selection` | Cause area, rationale, status | Inclusion must say `prototype_candidate_not_evaluated` until a real review begins. |
| `identity` | EIN, legal name, headquarters | EIN is the strongest entity key. |
| `financials` | Zero or more fiscal-year records | Every year cites a source; no cross-year mixing. |
| `programs` | Program-level records | Keep outputs separate from outcomes. |
| `transparency` | Financial and impact transparency | Grade independently. |
| `evaluation` | Evidence, cost-effectiveness, funding gap | Remains `not_assessed`/`null` during Phase 2. |
| `field_quality` | Status by field/group | Uses only the controlled vocabulary below. |
| `provenance` | Source IDs, URLs, retrieval metadata | Every material fact must be traceable. |
| `review` | Manual review state and notes | Reviewer actions must be dated. |
| `record_updated_at` | ISO date | Date normalized record last changed. |

## Identity fields

Required: `ein`, `legal_name`, headquarters city and state. Supported fields include alternate names, website, full headquarters address, ZIP, service geography, operating scope, NTEE code, subsection, and exempt-status code.

Entity resolution order:

1. exact EIN;
2. legal name plus address and Form 990 metadata;
3. website domain, state registration, and alternate names;
4. manual review for every uncertain match.

Never infer that a national parent and local chapter share finances or program outcomes. A fiscally sponsored project should link to, but remain distinguishable from, its sponsor.

## Financial-year fields

The intended financial record includes fiscal year, total revenue and expenses, program/administrative/fundraising expenses, government grants, private donations, program-service revenue, investment income, assets, unrestricted assets, cash reserves, liabilities, net assets, and executive compensation. Each record must identify its filing period and source.

Validation rules:

- monetary values are integers in source-reported U.S. dollars unless metadata says otherwise;
- fiscal years must be plausible four-digit years;
- liabilities, expense totals, and assets cannot be silently made positive if a source uses another convention;
- component totals that differ from a reported total are retained and flagged, not “fixed”;
- calculations across different fiscal years are forbidden;
- no overhead ratio may be interpreted as an impact score.

The Phase 2 API does not expose all desired Form 990 lines. Unavailable fields are explicitly `null` and `missing` rather than guessed.

## Program and outcome fields

Each program record should contain `program_id`, name, cause area, intervention type, target population, service description, delivery model, annual participants, geography, eligibility, reported outputs, reported outcomes, source IDs, and quality status.

An **output** is an activity count (meals served, clients enrolled, legal cases opened). An **outcome** is a change in wellbeing or circumstances (housing stability, recidivism, overdose mortality). Charity-reported outcomes must be labeled as such until independently validated. Program claims do not inherit causal credibility merely because a charity publishes them.

## Transparency fields

Financial transparency records the availability and quality of filings, audited statements, annual reports, and financial explanations. Impact transparency records outcome definitions, denominators, follow-up, attrition, comparison groups, methodology, limitations, and public evaluation reports. A profile can be strong on one and weak on the other.

## Evaluation fields

Evaluation records may eventually contain intervention evidence grade, charity-specific implementation assessment, cost per outcome, marginal cost-effectiveness range, room-for-more-funding scenarios, major uncertainties, review dates, reviewer team, and recommendation category. Phase 2 sets these to `not_assessed`, `not_evaluated`, or `null`.

Permitted future recommendation categories are defined in `docs/product/recommendation_categories.md`. No recommendation is valid without evidence, implementation, cost-effectiveness, and room-for-more-funding review.

## Data-quality vocabulary

- `verified`: checked by a human against the cited source or by an approved deterministic validation rule.
- `machine_extracted`: parsed without human verification.
- `manual_review_needed`: plausible but unresolved or high-risk.
- `conflicting_sources`: credible sources disagree and neither has been selected without explanation.
- `missing`: the collection process looked for the field and did not find it.
- `not_applicable`: the concept genuinely does not apply.

Quality attaches to individual fields whenever practical. A record-level status must not conceal weaker component fields.

## Provenance contract

Every source entry must include source ID, URL, retrieval date, access method, usage/license notes (in the registry), extracted fields, limitations, raw snapshot or auditable reference, and parsing confidence. Derived values additionally record formula version, input source IDs, assumptions, and code/notebook path.

## Versioning and changes

Schema changes require:

1. an updated machine-readable schema;
2. migration or regeneration of existing records;
3. tests for the new rule;
4. an update-history note; and
5. explicit review if a change could alter a published verdict.
