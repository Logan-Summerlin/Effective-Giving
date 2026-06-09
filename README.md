# U.S.-Focused Charity Effectiveness Website

This project is a blueprint for a U.S.-focused charity evaluation website. Its purpose is to help donors identify charities that are likely to create the greatest social benefit per additional donated dollar.

The project is modeled on the core idea of effective giving: recommendations should be based on evidence, cost-effectiveness, transparency, room for more funding, and marginal impact. It should not rank charities mainly by reputation, emotional appeal, or administrative-overhead ratios.

The permanent source-of-truth document is `docs/implementation_plan.md`. Read that file before building code, collecting data, writing public analysis, or making architectural decisions.

The initial cause areas are homelessness, criminal recidivism and reentry, criminal justice, legal immigrant integration, and drug addiction treatment and harm reduction.

The project should begin with a public-facing website template and information architecture before heavy research, data ingestion, or charity evaluation begins. The first website skeleton should use clearly labeled placeholder content only. It must not present fake rankings, fake charity evaluations, or fabricated cost-effectiveness estimates as real findings.

After the website template exists and can be inspected, the project should define the charity profile schema, source registry, evidence grading method, cost-effectiveness model, room-for-more-funding method, review templates, and governance policies before attempting large-scale data ingestion.

Key principles are simple: distinguish financial transparency from impact transparency, treat evidence as a spectrum rather than a yes-or-no label, publish uncertainty and moral assumptions, analyze what the next donated dollar would accomplish, and protect credibility through corrections, conflicts disclosure, charity response periods, and reproducible methods.

The best next step is Phase 0 from the implementation plan: create the actual website template, including homepage, recommendation index, charity review layout, cause-area layout, methodology page, corrections page, filter mockup, and visible placeholder warnings.
