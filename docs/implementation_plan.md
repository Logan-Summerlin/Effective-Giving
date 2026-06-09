# U.S.-Focused Charity Effectiveness Website Implementation Plan

> **For Hermes:** Use the `subagent-driven-development` skill if this plan is later implemented task-by-task by autonomous agents. Use this document as the permanent source of truth for product scope, data design, research process, governance, and phased execution.

**Goal:** Build a public U.S.-focused charity evaluation website that helps donors identify charities likely to create the greatest social benefit per additional donated dollar.

**Architecture:** The project should begin with a public-facing website template and information architecture, then build the research-and-data platform needed to fill that template with verified content. The core system will collect public charity data, standardize it into a structured database, map charities to evidence-backed interventions, estimate marginal cost-effectiveness, and publish transparent charity reviews with uncertainty, assumptions, source documents, and update history. The first website template must use clearly labeled placeholder content only; it must not present fake rankings, fake charity evaluations, or fabricated cost-effectiveness estimates.

**Tech Stack:** Recommended initial stack is Python for data pipelines and modeling, PostgreSQL for structured data, object storage for source documents, a static or server-rendered web frontend such as Next.js or Astro, and reproducible notebooks or scripts for research analysis. The stack can be revised later, but early work should prioritize auditability, reproducibility, and simple public documentation over complex engineering.

---

## 1. Plain-English Project Summary

This project is a website and research organization for evaluating charities that operate in the United States. Its purpose is to answer a practical donor question: if someone gives one more dollar today, which charity is most likely to turn that dollar into real social benefit?

The website should not rank charities by popularity, emotional storytelling, brand reputation, or the simple percentage of money spent on programs. Those factors can matter, but they are not enough. A charity can spend a high percentage on programs and still run programs that do not work. Another charity can have higher administrative costs but use them to deliver excellent services, measure outcomes carefully, and scale a highly effective intervention.

The website should evaluate charities by combining five kinds of evidence. First, it should examine whether the charity is financially transparent. Second, it should examine whether the charity reports meaningful outcomes, not just activities. Third, it should study whether the charity’s program type is supported by credible academic, policy, or government evidence. Fourth, it should estimate whether the charity delivers outcomes at a reasonable cost. Fifth, it should determine whether additional donations would expand effective work or simply replace money the charity would have received anyway.

The desired result is a trusted public resource for donors who want to improve lives in the United States using the best available evidence.

---

## 2. Core Principles

### 2.1 Marginal Impact Comes First

The central question is not “Is this charity good?” The central question is “What will the next donated dollar accomplish?” This distinction matters because some excellent organizations may already be fully funded, while some less famous organizations may have urgent room to expand high-impact work.

Every recommendation should include a room-for-more-funding analysis. The analysis should explain what the charity would likely do with the first $100,000, the next $250,000, the next $1 million, and the next $5 million. If those funding levels are unrealistic for a small charity, the report should say so and use smaller thresholds.

### 2.2 Evidence Is a Spectrum

The website must not treat “evidence-based” as a simple yes-or-no label. Some interventions are strongly supported by randomized trials and replicated studies. Some are promising but not yet proven. Some have mixed evidence. Some sound appealing but have weak evidence or even evidence of harm.

Every intervention should receive an evidence grade that explains the strength, relevance, and uncertainty of the research behind it.

### 2.3 Financial Transparency and Impact Transparency Are Different

A charity can file complete tax forms and still provide little useful information about whether its programs improve lives. Another charity may have imperfect public financial presentation but excellent program evaluation. The project should score financial transparency and impact transparency separately.

Financial transparency means the charity provides reliable information about revenue, expenses, assets, liabilities, executive compensation, fundraising, administrative spending, and program spending. Impact transparency means the charity clearly explains what it does, who it serves, what outcomes it measures, what evidence supports its work, and what results it has achieved.

### 2.4 Moral Assumptions Must Be Visible

Comparing different social outcomes requires value judgments. For example, donors may disagree about how to compare increased income, reduced incarceration, avoided overdose deaths, reduced homelessness, or improved legal stability. The website should publish default moral weights and allow users to view alternative rankings under different assumptions.

The goal is not to pretend that values do not matter. The goal is to make those values explicit enough that users can understand and modify them.

### 2.5 Negative Findings Are Part of the Product

The site should publish negative and uncertain findings. If a popular charity is not cost-effective, the site should explain why. If a program is emotionally compelling but has weak evidence, the site should say so plainly. If a charity refuses to provide important information, that should be visible.

Credibility comes from disciplined honesty, not from only publishing praise.

---

## 3. Target Users

The first target user is an individual donor in the United States who wants to give effectively but does not have time to read academic studies, Form 990 filings, and technical evaluation reports.

The second target user is a foundation program officer who wants a structured evidence review before making grants in a domestic cause area.

The third target user is a journalist, researcher, or policy analyst who wants transparent data on charity effectiveness.

The fourth target user is a charity leader who wants to understand how their organization could improve transparency, evidence quality, and donor confidence.

The website should serve nontechnical users through clear summaries, while also serving expert users through downloadable spreadsheets, technical reports, source documents, and reproducible methods.

---

## 4. Major Product Outputs

The project should eventually produce several public outputs.

The first output is a searchable database of U.S. charities with standardized financial, program, transparency, and evidence fields.

The second output is a set of cause-area evidence maps. These maps explain which types of interventions are strongly supported, promising, uncertain, weakly supported, or potentially harmful.

The third output is a set of charity reviews. Each review should include a summary verdict, a detailed technical report, cost-effectiveness estimates, major uncertainties, funding-gap analysis, source documents, charity response, and update history.

The fourth output is a recommendation system that identifies top charities overall and within specific cause areas.

The fifth output is a public methodology section explaining scoring, evidence grading, moral weights, uncertainty analysis, conflict-of-interest policy, correction policy, and update schedule.

---

## 5. Recommended Folder Structure

The project should begin with a website-template-first structure supported by documentation. The first public-facing skeleton should use placeholder data only, while the research documents define how real data will later be collected, evaluated, and published.

```text
us-charity-effectiveness-website/
  AGENTS.md
  README.md
  docs/
    implementation_plan.md
    methodology/
      evidence_grading.md
      cost_effectiveness_model.md
      moral_weights.md
      room_for_more_funding.md
      transparency_scoring.md
      conflict_of_interest_policy.md
      corrections_policy.md
    cause_areas/
      homelessness.md
      criminal_recidivism.md
      criminal_justice.md
      legal_immigrants.md
      drug_addiction_treatment.md
    data_sources/
      irs_exempt_organizations.md
      form_990.md
      propublica_nonprofit_explorer.md
      candid_guidestar.md
      state_charity_registries.md
      annual_reports_and_audits.md
    product/
      charity_review_template.md
      cause_area_page_template.md
      recommendation_categories.md
      user_filters.md
  data/
    raw/
    interim/
    processed/
    source_registry.csv
  notebooks/
  scripts/
  src/
    charity_effectiveness/
  tests/
  website/
    README.md
    package.json
    src/
      pages/
        index.*
        methodology.*
        recommendations.*
        charities/
          [slug].*
        cause-areas/
          [slug].*
        corrections.*
      components/
        CharityCard.*
        CharityReviewLayout.*
        CauseAreaLayout.*
        FilterPanel.*
        MethodologySummary.*
        PlaceholderNotice.*
      data/
        placeholder_charities.*
        placeholder_cause_areas.*
```

The `website/` directory should hold the first public-facing template and information architecture. The `docs/` directory should hold the research methodology and product design. The `data/` directory should hold source files and processed outputs. The `src/` directory should hold reusable data and modeling code. The `scripts/` directory should hold command-line jobs.

---

## 6. Data Infrastructure Plan

### 6.1 Purpose of the Charity Database

The charity database is the foundation of the project. It should combine public records from multiple sources into a single structured profile for each charity.

The database should not merely copy public records. It should standardize names, locations, cause areas, revenue, expenses, program descriptions, government grants, private donations, assets, and reported outcomes so that charities can be compared fairly.

### 6.2 Core Charity Profile Fields

Each charity profile should include a stable internal charity ID. It should also include the EIN, legal name, alternate names, website, headquarters address, city, state, ZIP code, service geography, and whether the charity operates nationally, statewide, regionally, locally, or in multiple locations.

Each profile should include financial fields. These should include annual revenue, annual expenses, program spending, administrative spending, fundraising spending, government grants, private donations, investment income, net assets, unrestricted assets, cash reserves, liabilities, and executive compensation.

Each profile should include program fields. These should include major programs, target population, cause area, intervention type, estimated number of people served, service delivery model, eligibility criteria, and available outcome reporting.

Each profile should include transparency fields. These should include whether the charity publishes audited financial statements, annual reports, Form 990 filings, program outcome reports, evaluation reports, theory of change, methodology notes, and data limitations.

Each profile should include evaluation fields. These should include evidence grade, impact transparency grade, financial transparency grade, estimated cost per outcome, estimated marginal cost-effectiveness, funding gap, uncertainty range, last review date, reviewer name or team, and recommendation category.

### 6.3 Primary Public Data Sources

The first source should be IRS exempt-organization data. This identifies tax-exempt organizations and provides basic registration information. It is useful for discovering the universe of organizations but is not enough for evaluation.

The second source should be IRS Form 990 filings. These filings provide revenue, expenses, assets, liabilities, executive compensation, program service descriptions, grants, and other financial information. Form 990 is central to financial transparency analysis.

The third source should be ProPublica Nonprofit Explorer. It provides searchable nonprofit records and access to many Form 990 filings. It is useful for prototyping because it is easier to query than raw IRS bulk files.

The fourth source should be Candid/GuideStar. This can provide profiles, categorization, and additional self-reported information, subject to licensing and access limits.

The fifth source should be state charity registries. These can provide registration status, state filings, enforcement actions, and solicitation information.

The sixth source should be audited financial statements and annual reports from charity websites. These may provide better program detail than Form 990 filings.

The seventh source should be grant databases. These can show whether a charity is supported by major foundations or government grants, but grants should not be treated as proof of effectiveness.

The eighth source should be program-level documents, such as evaluation reports, dashboards, outcome reports, strategic plans, and service manuals.

### 6.4 Source Registry Requirement

Every data source must be recorded in a source registry before it is used. The registry should include source name, source type, source URL, access method, retrieval date, license or terms-of-use notes, update frequency, fields extracted, known limitations, and parsing confidence.

This requirement protects the project from undocumented data provenance. If a number appears on the website, the team should be able to trace where it came from.

### 6.5 Data Quality Flags

Every extracted field should have a quality status. Recommended statuses are `verified`, `machine_extracted`, `manual_review_needed`, `conflicting_sources`, `missing`, and `not_applicable`.

A field marked `verified` has been checked by a human or by a reliable validation rule. A field marked `machine_extracted` was parsed automatically but not manually reviewed. A field marked `manual_review_needed` appears plausible but requires checking. A field marked `conflicting_sources` means two sources disagree. A field marked `missing` means the project looked for the field and did not find it. A field marked `not_applicable` means the field does not apply to that charity or program.

### 6.6 Entity Resolution

Many charities have similar names, multiple chapters, fiscal sponsors, affiliates, or old legal names. The project must avoid merging unrelated organizations and must avoid splitting one organization into several duplicates.

Entity resolution should use EIN as the strongest identifier. When EIN is missing or ambiguous, use legal name, address, website domain, state registration, and Form 990 metadata. All uncertain matches should be flagged for manual review.

### 6.7 Minimum Viable Data Prototype

The first data prototype should not attempt to ingest tens of thousands of charities. It should select 50 to 100 charities across the five initial cause areas. The purpose is to test the schema, source registry, extraction workflow, and review process before scaling.

The first prototype should include at least 10 charities in homelessness, 10 in criminal recidivism or reentry, 10 in criminal justice, 10 in legal immigrant integration, and 10 in drug addiction treatment or harm reduction.

---

## 7. Evidence Mapping Plan

### 7.1 Purpose of Evidence Maps

An evidence map is a structured summary of what research says about a category of intervention. It does not evaluate one charity by itself. Instead, it evaluates the kind of program the charity runs.

For example, if a charity runs permanent supportive housing, the evidence map should summarize research on permanent supportive housing. If a charity provides medication-assisted treatment for opioid use disorder, the evidence map should summarize the evidence for medication-assisted treatment.

### 7.2 Evidence Sources to Review

Researchers should review randomized controlled trials, quasi-experimental studies, systematic reviews, meta-analyses, government evaluations, benefit-cost studies, and high-quality implementation studies.

The project should use academic databases, government evaluation repositories, policy research organizations, and credible nonprofit evaluators. Examples include PubMed, Google Scholar, Campbell Collaboration, Cochrane Library, MDRC, RAND, Urban Institute, Mathematica, Arnold Ventures evidence resources, Washington State Institute for Public Policy, National Academies reports, federal agency evaluations, and state-level evaluations.

### 7.3 Evidence Grading Criteria

Every intervention should be graded on causal strength, replication, U.S. relevance, effect size, cost per outcome, implementation difficulty, scalability, equity considerations, risk of harm, and evidence freshness.

Causal strength asks whether the study design can credibly show that the program caused the outcome. Replication asks whether similar effects appear across multiple studies and locations. U.S. relevance asks whether the evidence applies to U.S. populations and institutions. Effect size asks how large the benefits are. Cost per outcome asks whether benefits are large relative to cost. Implementation difficulty asks whether the intervention requires rare expertise, unusual conditions, or intensive oversight. Risk of harm asks whether the intervention could backfire or produce unintended consequences.

### 7.4 Suggested Evidence Grades

Use `Strong`, `Moderate`, `Promising`, `Mixed`, `Weak`, `Potentially Harmful`, and `Insufficient Evidence` as plain-language grades.

`Strong` means multiple credible studies show meaningful positive effects in relevant settings. `Moderate` means credible evidence supports the intervention, but there are limits in replication, context, or effect size. `Promising` means early evidence is positive but still uncertain. `Mixed` means studies show inconsistent results. `Weak` means the available evidence does not provide much support. `Potentially Harmful` means credible evidence suggests possible negative effects. `Insufficient Evidence` means there is too little evidence to judge.

### 7.5 Evidence Map Template

Each evidence map should include the intervention name, cause area, target population, theory of change, main outcomes, summary of evidence, key studies, effect size range, cost range, implementation requirements, risks, uncertainty, recommended use cases, and open research questions.

---

## 8. Comparable Impact Metrics

### 8.1 Purpose of Common Metrics

Different charities pursue different outcomes. A homelessness charity may reduce shelter use. A legal aid charity may prevent eviction. A reentry charity may reduce reincarceration. A drug treatment charity may prevent overdose deaths.

To compare across cause areas, the project needs a common modeling framework. It does not need a perfect answer. It needs a transparent, adjustable, and honest estimate of expected social benefit per marginal dollar.

### 8.2 Outcome Categories

The model should include increased income, improved physical health, improved mental health, reduced homelessness, reduced criminal recidivism, reduced incarceration, reduced overdose deaths, improved legal status, increased employment, increased family stability, improved educational attainment, reduced victimization, fiscal savings to government, and quality-of-life improvements.

### 8.3 Moral Weights

A moral weight converts an outcome into a comparable value. For example, the project may assign a value to one year of stable housing, one overdose death averted, one year of incarceration avoided, one additional year of employment, or one quality-adjusted life-year gained.

The default moral weights should be published. The website should also allow alternative views. For example, one user may place higher weight on lifesaving health outcomes. Another may place higher weight on liberty and incarceration reduction. Another may place higher weight on poverty reduction.

### 8.4 Avoiding False Precision

The website should avoid presenting fragile estimates as if they are exact. Cost-effectiveness estimates should use ranges, confidence levels, and qualitative uncertainty notes.

For example, a report should say “we estimate this charity produces one year of stable housing for roughly $4,000 to $8,000, with moderate confidence,” rather than pretending the true number is exactly $5,217.

### 8.5 Government Fiscal Savings

Some interventions save government money by reducing jail time, emergency room visits, shelter stays, foster care placements, or court costs. These savings should be reported separately from human welfare benefits.

The project should not count fiscal savings as the whole value of an intervention. Avoiding homelessness matters even if the government does not save money. Avoiding incarceration matters because liberty and stability matter, not only because jail costs are expensive.

---

## 9. Marginal Cost-Effectiveness Plan

### 9.1 Central Question

For each recommended charity, analysts must estimate what additional donations would accomplish. This requires understanding budgets, current funding, waitlists, staffing, program capacity, expansion plans, bottlenecks, and alternative funding sources.

### 9.2 Information Needed from Charities

The project should request current budget, recent audited financials, program budgets, number of people served, unit costs, outcomes tracked, waitlists, planned expansion, staffing bottlenecks, restricted funding, unrestricted funding, reserves policy, government contracts, and what the charity would do with additional donations at different funding levels.

### 9.3 Funding-Gap Levels

Each full charity review should analyze at least four funding levels: first $100,000, next $250,000, next $1 million, and next $5 million. If a charity is too small for these levels, use smaller levels such as first $25,000, next $50,000, next $100,000, and next $250,000.

### 9.4 Displacement and Funging

The analysis must ask whether new donations truly expand services. A donation may be less impactful if it allows another funder to reduce support, replaces government funding, or funds activities that would have happened anyway.

This does not mean funging makes a charity bad. It means the analysis should identify how likely it is that additional dollars produce additional outcomes.

### 9.5 Bottlenecks

Additional donations may fail to create impact if the charity is constrained by hiring, housing supply, licensing, government approvals, referral pipelines, facility space, volunteer availability, legal restrictions, or participant recruitment.

Every room-for-more-funding estimate should name the likely bottlenecks.

---

## 10. Cause Area Pages

### 10.1 Criminal Recidivism and Reentry

This page should evaluate programs that help people leaving jail or prison avoid rearrest, reconviction, or reincarceration. It should cover transitional employment, reentry case management, housing support, cognitive behavioral therapy, prison education, mentoring, substance use treatment, and diversion programs.

Important metrics include cost per rearrest avoided, cost per reconviction avoided, cost per reincarceration avoided, cost per job placement, cost per sustained employment outcome, cost per stable housing outcome, and cost per participant completing the program.

The page should explain that recidivism is not one outcome. Rearrest, reconviction, and reincarceration measure different things and can be affected by policing, prosecution, supervision rules, and local policy.

### 10.2 Homelessness

This page should compare prevention, emergency shelter, rapid rehousing, permanent supportive housing, rental assistance, eviction legal defense, cash assistance, street outreach, and supportive services.

Important metrics include cost per person housed, cost per household stabilized, cost per year of housing stability, cost per eviction prevented, shelter-night reduction, emergency-service savings, health effects, and participant quality of life.

The page should distinguish between temporary shelter and stable housing. Emergency shelter may prevent immediate harm, but it is not the same as ending homelessness.

### 10.3 Legal Immigrants and Integration

This page should focus on people who are legally present in the United States or eligible for legal status. It should evaluate naturalization assistance, legal aid, English-language education, job placement, credential recognition, refugee resettlement, family stability services, and integration support.

Important metrics include cost per successful legal filing, cost per citizenship application completed, cost per naturalization achieved, cost per work authorization secured, earnings gains, employment gains, language gains, and long-term stability.

The page should be careful about legal categories. Refugees, asylum seekers, lawful permanent residents, temporary protected status holders, visa holders, and naturalization applicants face different processes and constraints.

### 10.4 Criminal Justice

This page should evaluate public defense support, bail assistance, expungement, fines-and-fees relief, restorative justice, prison education, sentencing reform organizations, and court navigation services.

Important metrics include cost per jail day avoided, cost per conviction avoided, cost per record cleared, cost per court appearance supported, cost per avoided warrant, cost per avoided driver’s license suspension, and long-term employment or housing gains.

The page should separate direct service charities from policy advocacy organizations. Both can be valuable, but they require different evidence and cost-effectiveness methods.

### 10.5 Drug Addiction Treatment and Harm Reduction

This page should review medication-assisted treatment, contingency management, recovery housing, harm reduction, syringe service programs, naloxone distribution, peer navigation, overdose prevention, and long-term treatment support.

Important metrics include cost per overdose death averted, cost per nonfatal overdose avoided, cost per person retained in treatment, cost per sustained recovery outcome, cost per infection avoided, cost per quality-adjusted life-year gained, and cost per participant connected to continuing care.

The page should distinguish moral discomfort from evidence. Some harm reduction programs may be politically controversial while still having strong evidence of reducing death and disease.

---

## 11. Charity Review Product Design

### 11.1 One-Page Summary Verdict

Every charity review should begin with a clear summary. It should say what the charity does, who it serves, whether the project recommends it, the main reason for the recommendation, the best estimate of cost-effectiveness, the major uncertainties, and whether the charity has room for more funding.

The summary should be understandable to a nontechnical donor in under five minutes.

### 11.2 Detailed Technical Report

The technical report should include all assumptions, source documents, data transformations, evidence mapping, cost calculations, uncertainty ranges, moral weights, funding-gap analysis, charity response, and reviewer notes.

The technical report should be detailed enough that an outside researcher can critique or reproduce the conclusion.

### 11.3 Downloadable Spreadsheets

Each reviewed charity should have downloadable spreadsheets showing financial extraction, outcome estimates, cost-effectiveness calculations, evidence references, and uncertainty ranges.

The spreadsheet should include notes explaining each field. It should not require the user to guess what a column means.

### 11.4 Source Documents

The website should link to source documents whenever legally and technically possible. If the source cannot be redistributed, the website should provide a citation, source URL, retrieval date, and access notes.

### 11.5 Charity Response Section

Before publishing a full review, the charity should receive a response period. The public report should include whether the charity responded, what corrections were made, and any unresolved disagreements.

The charity response section should not give charities veto power over criticism. It should give them a fair chance to correct factual errors.

### 11.6 Update History

Every charity review should show when it was first published, when it was last updated, what changed, and whether the recommendation category changed.

---

## 12. Recommendation Categories

The site should use several recommendation categories instead of a single ranked list.

`Top Charities` should include organizations with strong evidence, strong marginal cost-effectiveness, meaningful room for more funding, and adequate transparency.

`Strong but Funding-Constrained Charities` should include organizations that appear effective but cannot productively absorb much more funding right now.

`Promising but Uncertain Charities` should include organizations with plausible high impact but incomplete evidence, limited outcome data, or early-stage models.

`Policy-Leverage Opportunities` should include organizations whose work may change policy or systems. These require special methods because impact is uncertain, nonlinear, and often delayed.

`Charities Not Recommended Yet` should include charities that may be doing useful work but do not currently meet the evidence, transparency, or marginal-impact threshold for recommendation.

`Not Recommended` should be used carefully for charities where the project has enough evidence to conclude that donations are unlikely to be cost-effective compared with alternatives.

---

## 13. Website Features

The public website should allow users to browse top recommendations, search charity profiles, filter by cause area, filter by state, filter by evidence strength, filter by funding need, filter by confidence level, filter by political sensitivity, filter by religious affiliation, and filter by whether the charity accepts restricted donations.

Each cause-area page should include a plain-English overview, evidence map, recommended charities, promising charities, uncertain interventions, major research gaps, and a glossary.

Each charity page should include summary verdict, recommendation category, cause area, location, service geography, financial summary, intervention type, evidence grade, impact transparency grade, cost-effectiveness estimate, funding gap, source documents, technical report, and update history.

The website should include a methodology section. This section should explain how the project evaluates evidence, calculates cost-effectiveness, handles uncertainty, assigns moral weights, manages conflicts of interest, corrects mistakes, and schedules updates.

---

## 14. Governance and Credibility Protections

### 14.1 Conflict-of-Interest Policy

The project must publish a conflict-of-interest policy before publishing recommendations. The policy should explain whether staff, funders, advisors, or board members have relationships with reviewed charities. It should require disclosure of donations, consulting relationships, employment relationships, family relationships, and board service.

### 14.2 Correction Log

The website should maintain a public correction log. Corrections should include the date, page affected, error description, correction made, and whether the correction changed the recommendation.

### 14.3 Outside Review Board

The project should recruit outside academic or practitioner reviewers for methodology and cause-area evidence maps. Reviewers should be named unless there is a good reason not to name them.

### 14.4 Preregistered Review Templates

Before reviewing charities at scale, the project should publish review templates. This prevents the team from changing criteria after seeing which charities score well.

### 14.5 Reproducible Code

Ranking code and cost-effectiveness calculations should be reproducible. Sensitive information should be excluded, but public calculations should be auditable.

### 14.6 Annual Review Schedule

Each recommendation should have a scheduled update cycle. Top charities should be reviewed at least annually. Lower-priority profiles may be reviewed less often, but stale pages should be clearly marked.

---

## 15. Phased Execution Roadmap

### Phase 0: Website Template and Information Architecture

**Objective:** Create the public-facing website skeleton before heavy research, data ingestion, or charity evaluation begins.

**Tasks:** Choose the initial website framework, create the `website/` directory, build the homepage template, build the recommendation index template, build the charity review page template, build the cause-area page template, build the methodology page template, build the correction log page template, build the source/downloads section template, build the update-history display, and create a search/filter interface mockup using clearly labeled placeholder content.

**Required Guardrail:** All sample rankings, charity names, costs, ratings, and estimates used in this phase must be marked as placeholder or example content. The website template must not present fake recommendations, fake cost-effectiveness numbers, or plausible-looking charity evaluations as real findings.

**Exit Gate:** A user can navigate the website skeleton and understand what the finished product will contain, but all recommendations and evaluation values are visibly marked as placeholder or not yet evaluated.

### Phase 1: Research and Governance Foundation

**Objective:** Establish the project structure, scope, rules, methodology, and first research templates.

**Tasks:** Create or update project README, create methodology directory, write source registry template, write charity profile schema draft, write cause-area evidence map template, write charity review template, write cost-effectiveness model draft, write room-for-more-funding methodology, and write governance policy drafts.

**Exit Gate:** A new contributor can read the README, methodology documents, and templates and understand what the project is building, what data may be used, how charity reviews should be structured, and what credibility rules must be followed.

### Phase 2: Minimum Viable Data Prototype

**Objective:** Build a small database prototype with 50 to 100 charities across the initial cause areas.

**Tasks:** Select initial charities, record sources in `data/source_registry.csv`, extract basic IRS and Form 990 fields, create charity profile JSON or database records, flag missing and uncertain fields, and manually review a sample of records.

**Exit Gate:** The project has a working charity profile schema and at least 50 charity records with documented sources and data quality flags.

### Phase 3: Evidence Map Prototype

**Objective:** Create evidence maps for the five initial cause areas.

**Tasks:** Define intervention categories, collect key studies, summarize evidence, grade interventions, identify metrics, and list research gaps.

**Exit Gate:** Each cause area has a draft evidence map that identifies strongly supported, promising, uncertain, weak, and potentially harmful interventions.

### Phase 4: Cost-Effectiveness Model Prototype

**Objective:** Build a transparent model for comparing expected social benefit per marginal dollar.

**Tasks:** Define outcome units, define default moral weights, create uncertainty ranges, build example calculations, separate fiscal savings from human welfare benefits, and test sensitivity to moral weights.

**Exit Gate:** The project can produce a clear, reproducible cost-effectiveness estimate for at least three example interventions.

### Phase 5: First Charity Reviews

**Objective:** Produce complete pilot reviews for a small number of charities.

**Tasks:** Select one to two charities per cause area, collect financial and program data, map each charity to interventions, estimate cost per outcome, analyze room for more funding, request charity response, and publish draft reports internally.

**Exit Gate:** At least five complete pilot charity reviews exist, each with source documents, uncertainty notes, cost-effectiveness estimates, and funding-gap analysis.

### Phase 6: Website Content Integration

**Objective:** Replace placeholder website content with verified pilot reviews, methodology pages, evidence maps, source downloads, and update histories.

**Tasks:** Connect website pages to real pilot-review data, replace placeholder cause-area content with evidence-map summaries, publish methodology pages, attach downloadable spreadsheets or source summaries, display correction-log and update-history data, and verify that all public claims trace back to documented sources.

**Exit Gate:** A user can visit the prototype, understand the project, read pilot reviews, download supporting materials, and see how recommendations were produced.

### Phase 7: Scaling and Quality Control

**Objective:** Expand from pilot reviews to a larger charity database while protecting quality.

**Tasks:** Improve automated ingestion, add parser tests, expand entity resolution, add review workflow, recruit outside reviewers, document reproducibility process, and increase the number of reviewed charities.

**Exit Gate:** The project can reliably add new charities and update existing records without losing data provenance or methodological discipline.

### Phase 8: Public Launch

**Objective:** Release the website as a credible donor resource.

**Tasks:** Finalize top recommendations, publish methodology, publish conflict policy, publish correction policy, publish source registry, publish charity responses, prepare launch communications, and create a feedback process.

**Exit Gate:** The public site is live with documented methodology, reviewed recommendations, transparent uncertainty, and a process for corrections.

---

## 16. Bite-Sized Implementation Tasks for the First Build

These tasks implement Phase 0: the website template and information architecture. They should create a visible product skeleton without pretending that real evaluations already exist.

### Task 1: Choose the Website Template Stack

**Objective:** Decide the simplest initial website framework for a static, transparent, research-heavy site.

**Files:** Create `website/README.md`.

**Steps:** State the chosen stack, explain why it was chosen, describe how pages will be organized, describe how placeholder data will be labeled, and list the command that should eventually run the local development server.

**Verification:** A future implementer should know whether the project is using Astro, Next.js, plain static HTML, or another framework before writing template code.

### Task 2: Create the Website Directory Skeleton

**Objective:** Create the folder structure for public pages, reusable components, and placeholder data.

**Files:** Create `website/src/pages/`, `website/src/components/`, and `website/src/data/`.

**Steps:** Add placeholder files for the homepage, recommendations page, methodology page, corrections page, charity detail page template, cause-area page template, reusable layout components, filter panel component, placeholder charity data, and placeholder cause-area data.

**Verification:** The `website/` directory should clearly show where every major public page type will live.

### Task 3: Create the Placeholder Notice Component

**Objective:** Prevent users or future agents from mistaking mock content for real charity evaluations.

**Files:** Create `website/src/components/PlaceholderNotice.*`.

**Steps:** Write a reusable notice that says the current page uses placeholder content, no charities have been evaluated yet, and no rankings or cost-effectiveness numbers should be treated as real.

**Verification:** Every template page that contains example charity names, scores, or rankings must include this notice visibly near the top.

### Task 4: Build the Homepage Template

**Objective:** Create the first public landing-page structure.

**Files:** Create `website/src/pages/index.*`.

**Steps:** Include hero text, project purpose, explanation of marginal impact, cause-area overview, how recommendations will work, credibility protections, and links to methodology and recommendations pages.

**Verification:** A nontechnical visitor should understand the project’s purpose without reading the implementation plan.

### Task 5: Build the Recommendations Index Template

**Objective:** Show how top recommendations will eventually be browsed.

**Files:** Create `website/src/pages/recommendations.*` and `website/src/components/CharityCard.*`.

**Steps:** Create sections for top charities, strong but funding-constrained charities, promising but uncertain charities, policy-leverage opportunities, charities not recommended yet, and not recommended charities. Use placeholder records only.

**Verification:** All recommendation sections should render with placeholder notices and should avoid real-looking claims.

### Task 6: Build the Filter Panel Template

**Objective:** Create the user interface for filtering future recommendations.

**Files:** Create `website/src/components/FilterPanel.*`.

**Steps:** Include filters for state, cause area, evidence strength, funding need, confidence level, political sensitivity, religious affiliation, and whether the charity accepts restricted donations.

**Verification:** The filter panel should make the intended future search experience obvious, even if it is not connected to a real database yet.

### Task 7: Build the Charity Review Page Template

**Objective:** Create the standard page structure for individual charity reviews.

**Files:** Create `website/src/pages/charities/[slug].*` and `website/src/components/CharityReviewLayout.*`.

**Steps:** Include summary verdict, organization overview, program description, evidence assessment, financial transparency, impact transparency, cost-effectiveness estimate, room-for-more-funding estimate, major uncertainties, source documents, charity response, and update history.

**Verification:** The template should match the charity review product design in Section 11 and make all missing real values clearly marked as placeholder.

### Task 8: Build the Cause-Area Page Template

**Objective:** Create the standard page structure for cause-area research pages.

**Files:** Create `website/src/pages/cause-areas/[slug].*` and `website/src/components/CauseAreaLayout.*`.

**Steps:** Include plain-English overview, target population, intervention categories, evidence map summary, key metrics, recommended charities placeholder section, promising charities placeholder section, uncertain interventions, major research gaps, and glossary.

**Verification:** The template should support all five initial cause areas without requiring a custom layout for each one.

### Task 9: Build the Methodology Page Template

**Objective:** Create a public explanation of how recommendations will be produced.

**Files:** Create `website/src/pages/methodology.*` and `website/src/components/MethodologySummary.*`.

**Steps:** Include sections for evidence grading, cost-effectiveness, moral weights, room for more funding, transparency scoring, uncertainty, conflicts of interest, corrections, reproducibility, and update schedule.

**Verification:** A donor should be able to understand the basic evaluation method before reading technical reports.

### Task 10: Build the Corrections and Update-History Template

**Objective:** Make credibility protections visible from the first website version.

**Files:** Create `website/src/pages/corrections.*` and an update-history section inside the charity review layout.

**Steps:** Add fields for correction date, affected page, error description, correction made, whether the recommendation changed, review date, last update date, and next scheduled review.

**Verification:** The template should make public correction and update practices part of the product rather than an afterthought.

### Task 11: Build Placeholder Data Files

**Objective:** Provide safe sample content for template development.

**Files:** Create `website/src/data/placeholder_charities.*` and `website/src/data/placeholder_cause_areas.*`.

**Steps:** Use clearly fictional or generic entries such as `Example Housing Charity` and `Example Reentry Program`. Add fields needed by the homepage, recommendations page, charity page, and cause-area page.

**Verification:** No placeholder charity should be a real organization unless it is explicitly labeled as not evaluated and used only as a design example.

### Task 12: Run and Inspect the Website Template

**Objective:** Verify that the first website skeleton actually renders.

**Files:** Modify only files required to run the chosen website framework.

**Steps:** Install dependencies inside the project if required, start the local development server, open or fetch the homepage, and check that the homepage, recommendations page, methodology page, corrections page, one charity template, and one cause-area template render without errors.

**Verification:** Save the exact command output or browser/fetch result showing that the template runs. Do not call Phase 0 complete until the website skeleton has been exercised.

---

After Phase 0 is complete, continue with Phase 1 tasks: create `data/source_registry.csv`, `docs/methodology/charity_profile_schema.md`, `docs/methodology/evidence_grading.md`, `docs/methodology/cost_effectiveness_model.md`, `docs/methodology/room_for_more_funding.md`, `docs/product/charity_review_template.md`, `docs/methodology/conflict_of_interest_policy.md`, and `docs/methodology/corrections_policy.md`.

---

## 17. Data Model Draft

### 17.1 Charity Table

The `charity` table should store stable organization identity. Fields should include `charity_id`, `ein`, `legal_name`, `alternate_names`, `website_url`, `headquarters_city`, `headquarters_state`, `headquarters_zip`, `service_geography`, `ntee_code`, `cause_area_primary`, `cause_area_secondary`, `religious_affiliation`, `political_sensitivity`, `created_at`, and `updated_at`.

### 17.2 Financial Year Table

The `financial_year` table should store annual financial information. Fields should include `charity_id`, `fiscal_year`, `total_revenue`, `total_expenses`, `program_expenses`, `administrative_expenses`, `fundraising_expenses`, `government_grants`, `private_donations`, `net_assets`, `unrestricted_assets`, `cash_reserves`, `liabilities`, `executive_compensation_total`, `source_id`, and `data_quality_status`.

### 17.3 Program Table

The `program` table should store major programs. Fields should include `program_id`, `charity_id`, `program_name`, `cause_area`, `intervention_type`, `target_population`, `service_description`, `annual_participants`, `geography`, `eligibility`, `reported_outputs`, `reported_outcomes`, `source_id`, and `data_quality_status`.

### 17.4 Evidence Table

The `evidence` table should connect intervention types to research. Fields should include `evidence_id`, `intervention_type`, `cause_area`, `evidence_grade`, `key_studies`, `effect_size_summary`, `cost_summary`, `implementation_notes`, `harm_risks`, `u_s_relevance`, `last_reviewed`, and `reviewer_notes`.

### 17.5 Recommendation Table

The `recommendation` table should store evaluation results. Fields should include `charity_id`, `review_date`, `recommendation_category`, `summary_verdict`, `estimated_cost_effectiveness_low`, `estimated_cost_effectiveness_mid`, `estimated_cost_effectiveness_high`, `confidence_level`, `funding_gap_100k`, `funding_gap_250k`, `funding_gap_1m`, `funding_gap_5m`, `major_uncertainties`, `charity_response_status`, and `next_review_due`.

---

## 18. Quality Assurance and Testing

Data parsers should have unit tests using known sample filings. Scoring formulas should have tests that verify expected calculations. Charity profile schema validation should reject missing required identifiers, impossible financial values, and invalid recommendation categories.

Ranking outputs should have snapshot tests. A snapshot test records expected output for a fixed input dataset. If the ranking changes, reviewers must determine whether the change is intended.

Every public report should have a source completeness check. The check should confirm that all major factual claims have citations or source IDs.

Every cost-effectiveness model should have a sensitivity check. The check should show how rankings change under alternative moral weights or pessimistic assumptions.

---

## 19. Risk Register

The first risk is false precision. The project may create numbers that look more certain than they are. Mitigation: publish ranges, confidence levels, and uncertainty notes.

The second risk is data quality. Public filings may be incomplete, late, inconsistent, or hard to parse. Mitigation: use data quality flags and manual review for important fields.

The third risk is unfair charity comparisons. Charities may serve different populations or operate in different local contexts. Mitigation: compare within intervention types and explain context.

The fourth risk is ideological capture. Cause areas such as criminal justice, immigration, and harm reduction can be politically sensitive. Mitigation: publish methods, separate values from empirical claims, and use outside review.

The fifth risk is overreliance on charities’ self-reported outcomes. Mitigation: distinguish outputs from outcomes and charity-reported claims from independently evaluated evidence.

The sixth risk is underestimating implementation quality. A proven intervention can fail if implemented poorly. Mitigation: evaluate charity-specific implementation, not just intervention evidence.

The seventh risk is stale recommendations. Charity funding gaps and performance can change quickly. Mitigation: publish last-reviewed dates and update schedules.

---

## 20. Measures of Success

The project should measure whether it moves donations toward more effective U.S. charities. This can be tracked through donor surveys, referral links, charity-reported donation changes, and self-reported donor decisions.

The project should measure whether it identifies underfunded high-impact programs. This can be tracked by the number of funding gaps discovered, the amount of money moved to those gaps, and whether charities used funds as expected.

The project should measure whether it improves transparency. This can be tracked by whether charities publish better outcome reports after review, respond to data requests, or improve public documentation.

The project should measure whether it helps donors understand marginal impact. This can be tracked through user testing, comprehension surveys, and engagement with methodology pages.

The project should measure whether it builds a bridge between research and practical giving. This can be tracked by citations, partnerships, academic review participation, and use by foundations or donor advisors.

---

## 21. Best Immediate Next Step

The best next step is to complete Phase 0: create the actual website template and information architecture before beginning large-scale research or data ingestion. Start by choosing the initial website stack, creating the `website/` directory skeleton, building the homepage template, and adding a reusable placeholder notice that prevents mock content from being mistaken for real evaluations.

Do not publish real-looking recommendations during Phase 0. Use clearly fictional or generic placeholder entries only, and visibly label every example ranking, charity card, score, cost-effectiveness number, and cause-area recommendation as placeholder content.

After the website skeleton can be run and inspected, proceed to Phase 1 by creating the methodology and governance files: `data/source_registry.csv`, `docs/methodology/charity_profile_schema.md`, `docs/methodology/evidence_grading.md`, `docs/methodology/cost_effectiveness_model.md`, `docs/methodology/room_for_more_funding.md`, and `docs/product/charity_review_template.md`. Only after those files exist should the project manually evaluate 10 to 20 pilot charities.
