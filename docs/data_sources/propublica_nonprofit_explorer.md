# ProPublica Nonprofit Explorer API

- **Role in Phase 2:** convenient public prototype interface to IRS-derived exempt-organization identity data and selected Form 990 filing extracts.
- **Documentation:** https://projects.propublica.org/nonprofits/api/
- **Access:** HTTPS JSON organization endpoints, one EIN at a time.
- **Collected fields:** EIN, legal name, address, city/state/ZIP, NTEE and exemption metadata; latest available filing year, revenue, expenses, assets, liabilities, contributions, program-service revenue, investment income, net assets, officer compensation, and filing PDF URL when exposed.
- **Raw retention:** `data/raw/propublica/{ein}.json`.
- **Normalized outputs:** `data/processed/charity_profiles.json` and `.csv`.
- **Retrieval date:** recorded in `data/source_registry.csv` and each profile.

## Limitations

The API is a third-party representation of IRS records, can lag filings, does not expose every Form 990 line, and may contain amended or differently processed filings. Absence is not proof that a filing or fact does not exist. Phase 2 does not infer websites, programs, outcomes, or effectiveness from this source.

## Usage notes

Public access does not settle all reuse rights. Re-check ProPublica’s current terms and IRS source notices before refresh, redistribution, or public product integration. Do not hammer the service; the refresh script makes sequential requests with a delay and retains snapshots for deterministic rebuilds.

## Verification path

Recommendation-stage research should verify identity and decisive financial values against the underlying Form 990/PDF, IRS Tax Exempt Organization Search, audited statements, and relevant state records. Disagreements receive `conflicting_sources` and manual review.
