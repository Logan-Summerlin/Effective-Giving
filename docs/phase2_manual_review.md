# Phase 2 Manual Review Report

**Review date:** 2026-06-12
**Scope:** 10 of 50 records, stratified as two per cause area
**Purpose:** test identity matching, normalization, quality flags, source traceability, and the non-evaluation guardrail—not assess impact.

## Procedure

For each sampled record, the reviewer opened the committed ProPublica API snapshot, confirmed that the normalized EIN and legal name matched, confirmed cause-area selection was facially consistent with the public name/NTEE or documented rationale, compared latest extracted filing year and core totals to the snapshot, checked that unavailable desired fields remained `null`/`missing`, and confirmed all evaluation fields stayed `not_assessed` or `not_evaluated`.

Detailed outcomes are recorded in `data/manual_review.csv`. Nine sampled records had extractable Form 990 financials. The Fines and Fees Justice Center record did not expose a filing extract in the API response; the pipeline correctly retained identity data, emitted no financial record, and flagged the gap rather than imputing values.

## Findings

- No sampled EIN/name mismatch was found.
- No negative financial values or impossible liability-over-asset conditions were found in the sampled extracted totals; these checks are plausibility screens, not financial audits.
- Missing websites, program detail, service geography, and unsupported Form 990 line items remain explicit rather than inferred.
- The prototype does not contain evidence grades, cost-effectiveness estimates, funding gaps, ratings, or recommendations.
- NTEE codes and names are useful selection signals but are too coarse to establish exact program fit; every record still requires program-level review before Phase 3–5 work.

## Disposition

The sample passes the Phase 2 workflow check. `manual_review_status` remains separate from the normalized generated profiles so a rebuild cannot silently convert machine-extracted fields to verified facts; the review ledger is the authoritative record of human checks. Future production tooling should merge approved review decisions through a controlled workflow.
