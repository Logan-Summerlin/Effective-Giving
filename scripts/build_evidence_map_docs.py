#!/usr/bin/env python3
"""Render Phase 3 evidence-map Markdown from the canonical JSON dataset."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/evidence_maps/evidence_maps.json"
OUTPUT = ROOT / "docs/evidence_maps"


def render_map(item: dict, studies: dict[str, dict]) -> str:
    lines = [
        f"# {item['cause_area'].replace('_', ' ').title()} Evidence Map",
        "",
        "> **Draft Phase 3 research prototype — not a charity recommendation.** "
        "This map grades intervention categories. It does not establish a charity's implementation fidelity, "
        "marginal cost-effectiveness, or room for more funding.",
        "",
        "## Document control",
        "",
        f"- **Map ID:** `{item['map_id']}`",
        f"- **Status:** `{item['status']}`",
        f"- **Review question:** {item['review_question']}",
        f"- **Population/geography:** {item['population_geography']}",
        f"- **Search date:** {', '.join(item['search']['search_dates'])}",
        f"- **Evidence cut-off:** {item['search']['evidence_cutoff']}",
        f"- **Lead reviewer:** {item['reviewers']['lead']}",
        f"- **Conflicts:** {item['reviewers']['conflicts']}",
        f"- **Outside review:** {item['reviewers']['outside_review_status']}",
        f"- **Next review due:** {item['reviewers']['next_review_due']}",
        "",
        "## Plain-language summary",
        "",
        item["plain_language_summary"],
        "",
        "The table deliberately preserves favorable, uncertain, weak, and harmful findings. A `Strong` grade "
        "means the intervention category has comparatively credible evidence for specified outcomes—not that every "
        "provider is effective or that an additional donation is cost-effective.",
        "",
        "## Search and selection method",
        "",
        f"- **Repositories:** {', '.join(item['search']['repositories'])}",
        f"- **Search concepts:** {'; '.join(item['search']['search_strings'])}",
        f"- **Included:** {item['search']['inclusion_criteria']}",
        f"- **Excluded:** {item['search']['exclusion_criteria']}",
        f"- **Screening:** {item['search']['screening_process']}",
        f"- **Risk of bias:** {item['search']['risk_of_bias_method']}",
        f"- **Protocol deviations:** {item['search']['protocol_deviations']}",
        f"- **Missing-literature risks:** {item['search']['missing_literature_risks']}",
        "",
        "## Comparative intervention map",
        "",
        "| Intervention | Grade | Main outcome/effect | Confidence |",
        "|---|---|---|---|",
    ]
    for intervention in item["interventions"]:
        effect = intervention["effect_size_range"].replace("|", "\\|")
        lines.append(
            f"| [{intervention['name']}](#{intervention['intervention_id'].lower()}) | "
            f"**{intervention['evidence_grade']}** | {effect} | {intervention['confidence'].title()} |"
        )

    lines += ["", "## Outcome metrics", ""]
    for metric in item["metrics"]:
        lines += [
            f"### {metric['metric_id']}: {metric['name']}", "",
            f"- **Unit:** {metric['unit']}",
            f"- **Decision importance:** {metric['importance']}",
            f"- **Interpretation:** {metric['notes']}", "",
        ]

    lines += ["## Intervention details", ""]
    for intervention in item["interventions"]:
        study_links = ", ".join(
            f"[{study_id}](#{study_id.lower()})" for study_id in intervention["key_study_ids"]
        )
        lines += [
            f"### {intervention['intervention_id']}: {intervention['name']}", "",
            f"**Evidence grade: {intervention['evidence_grade']} ({intervention['confidence']} confidence).** "
            f"{intervention['grade_rationale']}", "",
            f"- **Definition and theory of change:** {intervention['definition']}",
            f"- **Target population and setting:** {intervention['target_population_and_setting']}",
            f"- **Comparator:** {intervention['comparator']}",
            f"- **Outcomes and timeframe:** {intervention['outcomes_and_timeframe']}",
            f"- **Evidence summary/effect range:** {intervention['effect_size_range']}",
            f"- **Key studies:** {study_links}",
            f"- **Causal strength and bias:** {intervention['causal_strength_and_risk_of_bias']}",
            f"- **U.S. applicability:** {intervention['us_relevance_and_external_validity']}",
            f"- **Cost/resource evidence:** {intervention['cost_resource_range']}",
            f"- **Implementation and fidelity:** {intervention['implementation_requirements_and_fidelity_risks']}",
            f"- **Scale, equity, and distribution:** {intervention['scalability_equity_and_distribution']}",
            f"- **Harms:** {intervention['adverse_outcomes_and_harm_risk']}",
            f"- **Recommended use:** {intervention['recommended_use_cases']}",
            f"- **Do not use as:** {intervention['cases_where_not_to_use']}",
            f"- **Primary metrics:** {', '.join(intervention['primary_metric_ids'])}",
            f"- **Open questions:** {'; '.join(intervention['open_research_questions'])}", "",
        ]

    used = dict.fromkeys(sid for i in item["interventions"] for sid in i["key_study_ids"])
    lines += ["## Study inventory", ""]
    for study_id in used:
        study = studies[study_id]
        lines += [
            f"### {study_id}", "",
            f"- **Source:** [{study['title']}]({study['url']})",
            f"- **Design/source type:** `{study['source_type']}`",
            f"- **Appraisal confidence:** `{study['appraisal_confidence']}`",
            f"- **Known limitations:** {study['known_limitations']}",
            f"- **Retrieved:** {study['retrieval_date']}", "",
        ]

    lines += ["## Research gaps and update triggers", "", "### Priority research gaps", ""]
    lines += [f"- {gap}" for gap in item["research_gaps"]]
    lines += ["", "### Early-update triggers", ""]
    lines += [f"- {trigger}" for trigger in item["update_triggers"]]
    lines += ["", "## Publication and interpretation guardrails", ""]
    lines += [f"- {guardrail}" for guardrail in item["publication_guardrails"]]
    return "\n".join(lines) + "\n"


def build(check: bool = False) -> int:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    studies = {study["study_id"]: study for study in payload["study_catalog"]}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    stale = []
    for item in payload["maps"]:
        path = OUTPUT / f"{item['map_id'].removeprefix('evidence-map-')}.md"
        rendered = render_map(item, studies)
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != rendered:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(rendered, encoding="utf-8")
    if stale:
        print("Stale generated evidence maps: " + ", ".join(stale))
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if generated Markdown is stale")
    raise SystemExit(build(parser.parse_args().check))
