# Marginal Cost-Effectiveness Model

## Decision question

The model estimates the expected **incremental human welfare benefit produced by an additional donation**, not the charity’s historical average efficiency. Results are ranges and scenarios, not precise facts.

## Core structure

For charity `c` and funding scenario `s`:

```text
incremental outcome_j
  = additional dollars
  × spend-through rate
  × allocation to intervention
  ÷ marginal cost per participant
  × incremental causal effect_j
  × implementation adjustment
  × displacement adjustment
  × duration/decay adjustment

welfare value
  = Σ(incremental outcome_j × published moral weight_j)
    - expected harms

marginal cost-effectiveness
  = welfare value / additional dollars
```

All terms use low/base/high or probability distributions where justified. Correlated uncertainties must not be treated as independent merely for convenience.

## Required inputs

- funding scenario and time horizon;
- spend-through timing and restricted/unrestricted allocation;
- marginal—not average—program cost;
- participant eligibility, take-up, dosage, and attrition;
- causal effect range and evidence grade;
- charity/intervention applicability and implementation adjustment;
- counterfactual service access and funding displacement;
- outcome duration, decay, and deadweight;
- material adverse outcomes;
- moral weights with version and rationale; and
- inflation year, discount rate, and currency basis.

Every input records source, source date, analyst transform, quality status, and sensitivity range.

## Outcome categories

The common framework may include income, physical and mental health, housing stability, incarceration and recidivism, overdose mortality, legal status, employment, family stability, education, victimization, and quality of life. Avoid double counting intermediate and final outcomes—for example, counting both employment income and a wellbeing estimate that already includes that income without an adjustment.

## Moral weights

Moral weights are visible value judgments. Publish a default set, rationale, units, and version; provide alternative views emphasizing health, liberty, or poverty reduction. No recommendation should depend on an undisclosed weight. Phase 1 defines this requirement but intentionally does not set numerical weights before Phase 4 research.

## Human welfare and fiscal effects

Report separately:

- **Human welfare:** health, safety, liberty, income, stability, and other person-centered outcomes.
- **Government fiscal effects:** changes in public spending or revenue.

Fiscal savings are not automatically social benefits: transfers, administrative costs, and displaced services require interpretation. A headline welfare estimate must not add government savings unless the model states a defensible social value and prevents double counting.

## Uncertainty and sensitivity

At minimum publish:

1. pessimistic, central, and optimistic estimates;
2. parameter ranges and source quality;
3. one-way sensitivity for major inputs;
4. scenario sensitivity for moral weights, displacement, effect persistence, and marginal cost;
5. break-even values for decision-critical assumptions;
6. probability of harm or null impact where estimable; and
7. a qualitative confidence statement tied to evidence and data quality.

If plausible assumptions reverse the ranking, say so prominently. Do not report more significant digits than the inputs support.

## Model validation

- independently reproduce formulas;
- unit-test signs, units, bounds, and scenario ordering;
- reconcile modeled spending with source financials without forcing equality;
- compare outputs with external estimates while explaining differences;
- review for omitted harms and double counting;
- snapshot ranking outputs and require review of changes; and
- publish code, input tables, and a model changelog.

## Publication threshold

A public estimate requires cited inputs, a documented room-for-more-funding scenario, intervention evidence grade, charity applicability assessment, uncertainty analysis, welfare/fiscal separation, reviewer sign-off, and a date for reassessment. Otherwise display `not estimated` rather than a placeholder number.
