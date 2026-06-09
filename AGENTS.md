# Agent Brief: U.S.-Focused Charity Effectiveness Website

This project designs a U.S.-focused charity effectiveness website that recommends charities based on expected social benefit per marginal donated dollar.

The source of truth is `docs/implementation_plan.md`. Read it before creating code, collecting data, drafting public pages, or changing project direction. Keep new work consistent with that plan unless the user explicitly asks to revise the plan.

Preserve the central evaluation standard: the project should estimate what additional donations would accomplish. Do not treat charity reputation, emotional appeal, or administrative-overhead ratios as substitutes for evidence of impact.

Maintain a clear distinction between financial transparency and impact transparency. A charity can have complete public filings while providing little evidence that its programs improve outcomes.

Use public data only unless a formal data-governance process is created. Appropriate early sources include IRS exempt-organization records, Form 990 filings, ProPublica Nonprofit Explorer, Candid/GuideStar subject to access rules, state charity registries, audited financial statements, annual reports, grant databases, government evaluations, and public research literature.

Every data pipeline or manual extraction process should record source URL, retrieval date, access method, license or usage notes, fields extracted, known limitations, and parsing confidence. If a claim cannot be traced to a source, do not publish it as fact.

Evidence should be graded on a spectrum: strong, moderate, promising, mixed, weak, potentially harmful, or insufficient. Consider causal identification, replication, U.S. relevance, effect size, implementation difficulty, risk of harm, and cost per outcome.

Cost-effectiveness work must expose assumptions, uncertainty ranges, moral weights, and sensitivity analysis. Separate human welfare benefits from government fiscal savings.

Before recommending a charity, analyze room for more funding. Identify whether additional donations would expand high-impact work, face bottlenecks, substitute for existing funding, or sit unused.

Initial cause areas are homelessness, criminal recidivism and reentry, criminal justice, legal immigrant integration, and drug addiction treatment and harm reduction.

Credibility protections are core requirements. Preserve conflict-of-interest disclosure, public correction logs, outside review, charity response periods, reproducible methods, negative findings, and update history.

Preferred development sequence: build the website template and information architecture first using clearly labeled placeholder content, create methodology and governance documents second, manually pilot a small set of charities third, build data automation fourth, then integrate verified content into the public website.
