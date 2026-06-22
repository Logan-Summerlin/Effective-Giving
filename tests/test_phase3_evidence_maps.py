import csv
import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/evidence_maps/evidence_maps.json"
PAYLOAD = json.loads(DATA_PATH.read_text(encoding="utf-8"))
MAPS = PAYLOAD["maps"]
STUDIES = {study["study_id"]: study for study in PAYLOAD["study_catalog"]}
CAUSES = {
    "homelessness",
    "criminal_recidivism_reentry",
    "criminal_justice",
    "legal_immigrant_integration",
    "drug_addiction_treatment_harm_reduction",
}
GRADES = {
    "Strong", "Moderate", "Promising", "Mixed", "Weak",
    "Potentially Harmful", "Insufficient Evidence",
}
UNCERTAIN = {"Promising", "Mixed", "Weak", "Insufficient Evidence"}


class Phase3EvidenceMapTests(unittest.TestCase):
    def test_five_initial_cause_areas_are_covered_once(self):
        self.assertEqual(5, len(MAPS))
        self.assertEqual(CAUSES, {item["cause_area"] for item in MAPS})
        self.assertEqual(5, len({item["map_id"] for item in MAPS}))

    def test_each_map_is_substantive_and_meets_exit_gate(self):
        for item in MAPS:
            with self.subTest(map_id=item["map_id"]):
                self.assertGreaterEqual(len(item["interventions"]), 6)
                self.assertGreaterEqual(len(item["metrics"]), 3)
                self.assertGreaterEqual(len(item["research_gaps"]), 3)
                grades = {intervention["evidence_grade"] for intervention in item["interventions"]}
                self.assertTrue(grades & {"Strong", "Moderate"}, "missing supported intervention")
                self.assertTrue(grades & UNCERTAIN, "missing uncertain/weak intervention")
                self.assertIn("Potentially Harmful", grades)

    def test_portfolio_uses_every_methodology_grade(self):
        used = {i["evidence_grade"] for item in MAPS for i in item["interventions"]}
        self.assertEqual(GRADES, used)

    def test_interventions_complete_the_template(self):
        required = {
            "intervention_id", "name", "definition", "theory_of_change",
            "target_population_and_setting", "comparator", "outcomes_and_timeframe",
            "key_study_ids", "causal_strength_and_risk_of_bias", "effect_size_range",
            "us_relevance_and_external_validity", "cost_resource_range",
            "implementation_requirements_and_fidelity_risks",
            "scalability_equity_and_distribution", "adverse_outcomes_and_harm_risk",
            "evidence_grade", "grade_rationale", "recommended_use_cases",
            "cases_where_not_to_use", "confidence", "open_research_questions",
            "primary_metric_ids",
        }
        ids = []
        for item in MAPS:
            metric_ids = {metric["metric_id"] for metric in item["metrics"]}
            for intervention in item["interventions"]:
                self.assertEqual(required, set(intervention))
                self.assertTrue(all(intervention[key] for key in required))
                self.assertIn(intervention["evidence_grade"], GRADES)
                self.assertTrue(set(intervention["primary_metric_ids"]) <= metric_ids)
                self.assertTrue(set(intervention["key_study_ids"]) <= set(STUDIES))
                ids.append(intervention["intervention_id"])
        self.assertEqual(len(ids), len(set(ids)))

    def test_review_controls_and_limitations_are_explicit(self):
        for item in MAPS:
            self.assertEqual("draft_internal_not_for_charity_ranking", item["status"])
            self.assertEqual("2026-06-12", item["search"]["evidence_cutoff"])
            self.assertIn("single-reviewer", item["search"]["protocol_deviations"])
            self.assertEqual("Not yet externally reviewed", item["reviewers"]["outside_review_status"])
            self.assertEqual("2027-06-12", item["reviewers"]["next_review_due"])
            guardrails = " ".join(item["publication_guardrails"]).lower()
            self.assertIn("charity-specific", guardrails)
            self.assertIn("cost-effectiveness", guardrails)
            self.assertIn("fiscal", guardrails)
            self.assertIn("second review", guardrails)

    def test_metrics_do_not_conflate_welfare_and_fiscal_savings(self):
        for item in MAPS:
            metric_text = " ".join(
                f"{m['name']} {m['unit']} {m['notes']}" for m in item["metrics"]
            ).lower()
            self.assertNotIn("taxpayer savings", metric_text)
        homelessness = next(item for item in MAPS if item["cause_area"] == "homelessness")
        notes = " ".join(metric["notes"] for metric in homelessness["metrics"])
        self.assertIn("Do not equate lower public spending with wellbeing", notes)

    def test_study_catalog_and_registry_are_complete(self):
        self.assertGreaterEqual(len(STUDIES), 25)
        referenced = Counter(
            sid for item in MAPS for intervention in item["interventions"]
            for sid in intervention["key_study_ids"]
        )
        self.assertEqual(set(STUDIES), set(referenced))
        with (ROOT / "data/evidence_maps/source_registry.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(set(STUDIES), {row["study_id"] for row in rows})
        for row in rows:
            self.assertTrue(row["source_url"].startswith("https://"))
            self.assertEqual("2026-06-12", row["retrieval_date"])
            self.assertTrue(row["known_limitations"])
            self.assertIn(row["appraisal_confidence"], {"high", "moderate", "low"})

    def test_no_charity_is_graded_or_recommended(self):
        serialized = DATA_PATH.read_text(encoding="utf-8").lower()
        self.assertNotIn('"charity_id"', serialized)
        for item in MAPS:
            self.assertIn("not a charity recommendation", item["plain_language_summary"].lower())

    def test_generated_markdown_is_current(self):
        result = subprocess.run(
            [sys.executable, "scripts/build_evidence_map_docs.py", "--check"],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(5, len(list((ROOT / "docs/evidence_maps").glob("*.md"))))


if __name__ == "__main__":
    unittest.main()
