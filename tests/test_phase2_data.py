import csv
import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = json.loads((ROOT / "data/processed/charity_profiles.json").read_text())
ALLOWED_QUALITY = {
    "verified", "machine_extracted", "manual_review_needed",
    "conflicting_sources", "missing", "not_applicable",
}
CAUSES = {
    "homelessness",
    "criminal_recidivism_and_reentry",
    "criminal_justice",
    "legal_immigrant_integration",
    "drug_addiction_treatment_and_harm_reduction",
}


class Phase2DataTests(unittest.TestCase):
    def test_has_50_unique_records_balanced_across_causes(self):
        self.assertEqual(50, len(PROFILES))
        self.assertEqual(50, len({p["charity_id"] for p in PROFILES}))
        self.assertEqual({cause: 10 for cause in CAUSES}, Counter(p["selection"]["cause_area_primary"] for p in PROFILES))

    def test_identifiers_and_entity_fields(self):
        for profile in PROFILES:
            self.assertRegex(profile["charity_id"], r"^us-ein-\d{9}$")
            self.assertRegex(profile["identity"]["ein"], r"^\d{2}-\d{7}$")
            self.assertEqual(profile["charity_id"][-9:], profile["identity"]["ein"].replace("-", ""))
            self.assertTrue(profile["identity"]["legal_name"])
            self.assertRegex(profile["identity"]["headquarters"]["state"], r"^[A-Z]{2}$")

    def test_no_profile_claims_an_evaluation_or_recommendation(self):
        for profile in PROFILES:
            self.assertEqual("prototype_candidate_not_evaluated", profile["selection"]["selection_status"])
            self.assertEqual("not_evaluated", profile["selection"]["recommendation_status"])
            self.assertEqual("not_assessed", profile["evaluation"]["evidence_grade"])
            self.assertEqual("not_evaluated", profile["evaluation"]["recommendation_category"])
            self.assertIsNone(profile["evaluation"]["estimated_cost_per_outcome"])
            self.assertIsNone(profile["evaluation"]["estimated_marginal_cost_effectiveness"])
            self.assertIsNone(profile["evaluation"]["funding_gap"])

    def test_quality_flags_use_controlled_vocabulary(self):
        for profile in PROFILES:
            for section in (profile["field_quality"]["identity"], profile["field_quality"]["financials"]):
                self.assertFalse(set(section.values()) - ALLOWED_QUALITY)
            self.assertIn(profile["field_quality"]["programs"], ALLOWED_QUALITY)
            self.assertIn(profile["field_quality"]["transparency"], ALLOWED_QUALITY)
            self.assertIn(profile["field_quality"]["evaluation"], ALLOWED_QUALITY)

    def test_financial_values_are_plausible_or_explicitly_missing(self):
        missing_financials = 0
        for profile in PROFILES:
            if not profile["financials"]:
                missing_financials += 1
                self.assertEqual("missing", profile["field_quality"]["financials"]["filing"])
                continue
            financial = profile["financials"][0]
            self.assertGreaterEqual(financial["fiscal_year"], 2000)
            for key in ("total_expenses", "total_assets", "liabilities"):
                if financial[key] is not None:
                    self.assertGreaterEqual(financial[key], 0)
        self.assertGreaterEqual(missing_financials, 1, "The prototype should preserve known source gaps")

    def test_combined_contributions_are_not_mislabeled_as_private_donations(self):
        for profile in PROFILES:
            if not profile["financials"]:
                continue
            financial = profile["financials"][0]
            self.assertIn("contributions_and_grants", financial)
            self.assertIsNone(financial["private_donations"])
            self.assertEqual("missing", profile["field_quality"]["financials"]["private_donations"])

    def test_every_record_has_a_raw_snapshot_and_registry_entry(self):
        with (ROOT / "data/source_registry.csv").open(newline="", encoding="utf-8") as handle:
            registry = {row["source_id"]: row for row in csv.DictReader(handle)}
        self.assertIn("propublica-nonprofit-explorer-api-v2", registry)
        for profile in PROFILES:
            source = profile["provenance"][0]
            self.assertIn(source["source_id"], registry)
            raw_path = ROOT / source["raw_snapshot"]
            self.assertTrue(raw_path.is_file())
            raw = json.loads(raw_path.read_text())
            raw_ein = str(raw["organization"]["ein"]).zfill(9)
            self.assertEqual(profile["identity"]["ein"].replace("-", ""), raw_ein)
            self.assertEqual("2026-06-12", registry[source["source_id"]]["retrieval_date"])

    def test_source_registry_has_required_metadata(self):
        required = {
            "source_id", "source_name", "source_type", "source_url", "access_method",
            "retrieval_date", "license_or_usage_notes", "update_frequency", "fields_extracted",
            "known_limitations", "parsing_confidence",
        }
        with (ROOT / "data/source_registry.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(51, len(rows))
        for row in rows:
            self.assertEqual(required, set(row))
            self.assertTrue(all(row[key].strip() for key in required))
            self.assertTrue(row["source_url"].startswith("https://"))

    def test_manual_review_is_stratified_and_passes(self):
        with (ROOT / "data/manual_review.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(10, len(rows))
        self.assertEqual({cause: 2 for cause in CAUSES}, Counter(row["cause_area"] for row in rows))
        self.assertTrue(all(row["result"].startswith("pass") for row in rows))
        self.assertEqual({p["charity_id"] for p in PROFILES} & {r["charity_id"] for r in rows}, {r["charity_id"] for r in rows})

    def test_json_schema_declares_required_phase2_guardrails(self):
        schema = json.loads((ROOT / "data/schemas/charity_profile.schema.json").read_text())
        self.assertEqual("0.1.0", schema["properties"]["schema_version"]["const"])
        self.assertEqual("not_evaluated", schema["properties"]["evaluation"]["properties"]["recommendation_category"]["const"])
        self.assertEqual(CAUSES, set(schema["properties"]["selection"]["properties"]["cause_area_primary"]["enum"]))

    def test_processed_csv_matches_json(self):
        with (ROOT / "data/processed/charity_profiles.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(50, len(rows))
        self.assertEqual({p["charity_id"] for p in PROFILES}, {r["charity_id"] for r in rows})


if __name__ == "__main__":
    unittest.main()
