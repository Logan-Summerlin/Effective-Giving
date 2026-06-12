#!/usr/bin/env python3
"""Build the Phase 2 charity-profile prototype from public ProPublica API data.

The API organization object is derived from IRS exempt-organization records, while
``filings_with_data`` contains selected fields extracted from Form 990 filings.
Raw responses are retained so every normalized value can be audited.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SELECTION_PATH = ROOT / "data" / "charity_selection.csv"
RAW_DIR = ROOT / "data" / "raw" / "propublica"
PROCESSED_JSON = ROOT / "data" / "processed" / "charity_profiles.json"
PROCESSED_CSV = ROOT / "data" / "processed" / "charity_profiles.csv"
SOURCE_REGISTRY = ROOT / "data" / "source_registry.csv"
QUALITY_REPORT = ROOT / "data" / "processed" / "data_quality_report.json"
API_TEMPLATE = "https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json"
VALID_QUALITY = {
    "verified",
    "machine_extracted",
    "manual_review_needed",
    "conflicting_sources",
    "missing",
    "not_applicable",
}


def digits(ein: str) -> str:
    return re.sub(r"\D", "", ein).zfill(9)


def read_selection() -> list[dict[str, str]]:
    with SELECTION_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 50:
        raise ValueError(f"Expected exactly 50 selected charities, found {len(rows)}")
    eins = [digits(row["ein"]) for row in rows]
    if len(set(eins)) != len(eins) or any(len(ein) != 9 for ein in eins):
        raise ValueError("Selection EINs must be unique nine-digit identifiers")
    counts = Counter(row["cause_area"] for row in rows)
    if set(counts.values()) != {10} or len(counts) != 5:
        raise ValueError(f"Expected 10 charities in each of five cause areas: {counts}")
    return rows


def fetch(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "EffectiveGivingPrototype/0.1 (public research prototype)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def load_payload(row: dict[str, str], refresh: bool) -> tuple[dict[str, Any], Path]:
    ein = digits(row["ein"])
    raw_path = RAW_DIR / f"{ein}.json"
    if refresh or not raw_path.exists():
        payload = fetch(API_TEMPLATE.format(ein=ein))
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.12)
    else:
        payload = json.loads(raw_path.read_text(encoding="utf-8"))
    if digits(str(payload["organization"]["ein"])) != ein:
        raise ValueError(f"Payload EIN mismatch for {ein}")
    return payload, raw_path


def quality(value: Any, *, present_status: str = "machine_extracted") -> str:
    return present_status if value not in (None, "") else "missing"


def normalize(row: dict[str, str], payload: dict[str, Any], raw_path: Path, retrieved: str) -> dict[str, Any]:
    org = payload["organization"]
    filings = payload.get("filings_with_data") or []
    latest = max(filings, key=lambda item: (item.get("tax_prd") or 0, item.get("updated") or ""), default={})
    ein_digits = digits(row["ein"])
    source_id = f"propublica-org-{ein_digits}"
    identity = {
        "ein": f"{ein_digits[:2]}-{ein_digits[2:]}",
        "legal_name": org.get("name"),
        "alternate_names": [],
        "website_url": None,
        "headquarters": {
            "address": org.get("address"),
            "city": org.get("city"),
            "state": org.get("state"),
            "zip": org.get("zipcode"),
        },
        "service_geography": None,
        "operating_scope": None,
        "ntee_code": org.get("ntee_code"),
        "subsection_code": org.get("subsection_code"),
        "tax_exempt_status_code": org.get("exempt_organization_status_code"),
    }
    financials = {
        "fiscal_year": latest.get("tax_prd_yr"),
        "tax_period": latest.get("tax_prd"),
        "form_type_code": latest.get("formtype"),
        "total_revenue": latest.get("totrevenue"),
        "total_expenses": latest.get("totfuncexpns"),
        "program_expenses": None,
        "administrative_expenses": None,
        "fundraising_expenses": None,
        "government_grants": None,
        "contributions_and_grants": latest.get("totcntrbgfts"),
        "private_donations": None,
        "program_service_revenue": latest.get("totprgmrevnue"),
        "investment_income": latest.get("invstmntinc"),
        "net_assets": latest.get("totnetassetend"),
        "unrestricted_assets": None,
        "cash_reserves": None,
        "total_assets": latest.get("totassetsend"),
        "liabilities": latest.get("totliabend"),
        "executive_compensation_total": latest.get("compnsatncurrofcr"),
        "filing_pdf_url": latest.get("pdf_url"),
    }
    identity_quality = {
        "ein": "machine_extracted",
        "legal_name": quality(identity["legal_name"]),
        "alternate_names": "missing",
        "website_url": "missing",
        "headquarters.address": quality(identity["headquarters"]["address"]),
        "headquarters.city": quality(identity["headquarters"]["city"]),
        "headquarters.state": quality(identity["headquarters"]["state"]),
        "headquarters.zip": quality(identity["headquarters"]["zip"]),
        "service_geography": "missing",
        "operating_scope": "missing",
        "ntee_code": quality(identity["ntee_code"]),
    }
    financial_quality = {key: quality(value) for key, value in financials.items()}
    return {
        "schema_version": "0.1.0",
        "charity_id": row["charity_id"],
        "selection": {
            "cause_area_primary": row["cause_area"],
            "selection_rationale": row["selection_rationale"],
            "selection_status": row["selection_status"],
            "recommendation_status": "not_evaluated",
        },
        "identity": identity,
        "financials": [financials] if latest else [],
        "programs": [],
        "transparency": {
            "financial_transparency_grade": "not_assessed",
            "impact_transparency_grade": "not_assessed",
        },
        "evaluation": {
            "evidence_grade": "not_assessed",
            "estimated_cost_per_outcome": None,
            "estimated_marginal_cost_effectiveness": None,
            "funding_gap": None,
            "uncertainty_range": None,
            "recommendation_category": "not_evaluated",
        },
        "field_quality": {
            "identity": identity_quality,
            "financials": financial_quality if latest else {"filing": "missing"},
            "programs": "manual_review_needed",
            "transparency": "manual_review_needed",
            "evaluation": "not_applicable",
        },
        "provenance": [
            {
                "source_id": source_id,
                "source_url": API_TEMPLATE.format(ein=ein_digits),
                "retrieved_at": retrieved,
                "access_method": "public JSON API over HTTPS",
                "raw_snapshot": str(raw_path.relative_to(ROOT)),
                "fields_extracted": ["IRS exempt-organization identity fields", "selected Form 990 financial fields"],
                "limitations": "API fields may lag filings; not all Form 990 lines are exposed; values have not been interpreted as evidence of impact.",
                "parsing_confidence": "high",
            }
        ],
        "review": {
            "manual_review_status": "not_reviewed",
            "last_reviewed": None,
            "review_notes": None,
        },
        "record_updated_at": retrieved,
    }


def write_profiles(profiles: list[dict[str, Any]]) -> None:
    PROCESSED_JSON.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED_JSON.write_text(json.dumps(profiles, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    columns = [
        "charity_id", "ein", "legal_name", "cause_area_primary", "city", "state", "ntee_code",
        "fiscal_year", "total_revenue", "total_expenses", "total_assets", "liabilities",
        "financial_record_status", "manual_review_status", "source_id",
    ]
    with PROCESSED_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for profile in profiles:
            financial = profile["financials"][0] if profile["financials"] else {}
            writer.writerow({
                "charity_id": profile["charity_id"],
                "ein": profile["identity"]["ein"],
                "legal_name": profile["identity"]["legal_name"],
                "cause_area_primary": profile["selection"]["cause_area_primary"],
                "city": profile["identity"]["headquarters"]["city"],
                "state": profile["identity"]["headquarters"]["state"],
                "ntee_code": profile["identity"]["ntee_code"],
                "fiscal_year": financial.get("fiscal_year"),
                "total_revenue": financial.get("total_revenue"),
                "total_expenses": financial.get("total_expenses"),
                "total_assets": financial.get("total_assets"),
                "liabilities": financial.get("liabilities"),
                "financial_record_status": "machine_extracted" if financial else "missing",
                "manual_review_status": profile["review"]["manual_review_status"],
                "source_id": profile["provenance"][0]["source_id"],
            })


def write_registry(profiles: list[dict[str, Any]], retrieved: str) -> None:
    columns = [
        "source_id", "source_name", "source_type", "source_url", "access_method", "retrieval_date",
        "license_or_usage_notes", "update_frequency", "fields_extracted", "known_limitations", "parsing_confidence",
    ]
    with SOURCE_REGISTRY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerow({
            "source_id": "propublica-nonprofit-explorer-api-v2",
            "source_name": "ProPublica Nonprofit Explorer API v2 documentation",
            "source_type": "documentation",
            "source_url": "https://projects.propublica.org/nonprofits/api/",
            "access_method": "public web page over HTTPS",
            "retrieval_date": retrieved,
            "license_or_usage_notes": "Publicly accessible; users must review current ProPublica terms before reuse or redistribution.",
            "update_frequency": "Documentation and upstream data update on provider schedule",
            "fields_extracted": "API semantics and endpoint structure",
            "known_limitations": "Third-party interface to IRS-derived data; documentation may change.",
            "parsing_confidence": "not_applicable",
        })
        for profile in profiles:
            provenance = profile["provenance"][0]
            writer.writerow({
                "source_id": provenance["source_id"],
                "source_name": f"ProPublica organization and filing record for {profile['identity']['legal_name']}",
                "source_type": "IRS-derived exempt-organization and Form 990 API record",
                "source_url": provenance["source_url"],
                "access_method": provenance["access_method"],
                "retrieval_date": retrieved,
                "license_or_usage_notes": "Publicly accessible API; review ProPublica terms and IRS source notices before redistribution.",
                "update_frequency": "Provider-updated as IRS records and filing extracts become available",
                "fields_extracted": "; ".join(provenance["fields_extracted"]),
                "known_limitations": provenance["limitations"],
                "parsing_confidence": provenance["parsing_confidence"],
            })


def write_quality_report(profiles: list[dict[str, Any]], retrieved: str) -> None:
    cause_counts = Counter(p["selection"]["cause_area_primary"] for p in profiles)
    missing_filings = [p["charity_id"] for p in profiles if not p["financials"]]
    missing_ntee = [p["charity_id"] for p in profiles if not p["identity"]["ntee_code"]]
    statuses = Counter()
    for profile in profiles:
        for group in (profile["field_quality"]["identity"], profile["field_quality"]["financials"]):
            statuses.update(group.values())
    invalid = set(statuses) - VALID_QUALITY
    if invalid:
        raise ValueError(f"Invalid quality statuses: {sorted(invalid)}")
    report = {
        "generated_at": retrieved,
        "record_count": len(profiles),
        "cause_area_counts": dict(sorted(cause_counts.items())),
        "records_without_extracted_form_990_financials": missing_filings,
        "records_without_ntee_code": missing_ntee,
        "field_quality_status_counts": dict(sorted(statuses.items())),
        "interpretation_warning": "Record presence and financial transparency do not establish program effectiveness. No profile in this dataset has been evaluated or recommended.",
    }
    QUALITY_REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Re-download all public API snapshots")
    parser.add_argument("--retrieval-date", default=date.today().isoformat(), help="ISO date recorded in provenance")
    args = parser.parse_args()
    date.fromisoformat(args.retrieval_date)
    profiles = []
    for row in read_selection():
        payload, raw_path = load_payload(row, args.refresh)
        profiles.append(normalize(row, payload, raw_path, args.retrieval_date))
    profiles.sort(key=lambda p: (p["selection"]["cause_area_primary"], p["identity"]["legal_name"] or ""))
    write_profiles(profiles)
    write_registry(profiles, args.retrieval_date)
    write_quality_report(profiles, args.retrieval_date)
    print(f"Built {len(profiles)} profiles across {len(set(p['selection']['cause_area_primary'] for p in profiles))} cause areas")


if __name__ == "__main__":
    main()
