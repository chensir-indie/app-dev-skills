# Research methods that change a decision

Use this before detailed competitor work or repairing an existing report. Adapted from the user-supplied **App Competitor Analysis Report Template v1.0 (2026-10-21)**; the portable examples are fictional. The template's example weights, sample sizes and targets are project choices, not professional standards. Keep the existing [product/state depth](analysis-depth.md), four visual maps and [technical contracts](technical-analysis.md); this layer determines what their evidence can support.

## 1. Freeze the question and comparison contract

Write a compact brief: decision owner/audience if known; one decision; alternatives including keeping the current approach; target user/job/context; consequence of choosing wrongly; available budget/time/technical constraints. Use a falsifiable question, such as “Does keeping an interrupted draft reduce restart work?” rather than “Which app has more AI?” Record unknown ownership rather than assigning a person.

Select direct, indirect and substitute approaches by the same job. A manual workaround or doing nothing can be a relevant substitute. Explain each selection. A broad landscape may contain many products while a task comparison uses only an equivalent subgroup. Preserve the user's entire requested inventory and explain exclusions from a specific comparison.

Before comparing results, make a conditions table: product/version/date, OS/device, locale/region, account age/role/tier, flags, permissions, network/cache, data scale and participant familiarity. Mark each mismatch and the conclusion it prevents. Cross-platform observations can explain mechanisms without establishing a speed winner. Analyst shortest paths and first-time participant paths are separate observations.

Choose the method from the claim, not the report's chapter list:

| Decision question | Do now | What completes this method | Evidence limit |
| --- | --- | --- | --- |
| How is the task organized? | Inspect official material, captures and authorized artifacts; reconcile features, states and objects | Source-linked capability matrix and all supported maps, with contrary evidence checked | Declared capability is not observed completion |
| What may confuse a user? | Heuristic inspection of actual available pages/states | Reproducible issue cards, inspection scope, impact/recovery and alternatives | Expert concern is not measured incidence |
| Can people complete the same task more easily? | Competitive task study below, if participants and access exist | Raw attempts, protocol, reviewed recordings and correctly denominated summaries | A plan or analyst walkthrough is not a participant study |
| Why do people need/change tools? | Ask about a recent real episode, trigger, workaround and outcome; code episodes with locators | Supported task statements and contradictory cases | Preference votes do not establish real behavior or prevalence |
| Does it activate/retain/convert? | Inspect first-value mechanism; use authorized event/cohort data for measured claims | Event definitions, window, denominator, segment and missingness | Onboarding presence or marketing attribution does not prove causal retention |
| Is it affordable/integrable? | Scenario TCO, entitlement and integration checks below | Dated comparable scenario, tested vs documented boundary | List price, SDK presence and company revenue are different evidence |
| Which direction should we choose? | Trace findings to decision cards; score only if useful | Reversible recommendation, tradeoff, discriminating experiment | Unequal evidence coverage cannot produce an overall winner |

For each selected method record **completed / partial / not_run**, artifacts inspected and remaining proof. `not_applicable` requires a decision-based reason. Missing participants/device access leaves the study `not_run`; continue source analysis and authorized acquisition. Do not convert plans into results to make a report look complete.

## 2. Develop needs and capability depth

For interviews, ask “Tell me about the last time…” and reconstruct trigger → attempted approach → failure/workaround → outcome. Preserve episode/source IDs, role and context. State a job as “When [context], [person] wants [progress] so that [outcome], but [constraint].” Mark an analyst-generated job hypothesis as such until episodes support it.

For capability comparisons use **can_complete / limited / cannot_complete / unverified**. Record the exact result, prerequisite, scope/tier/permission/scale, evidence status and source ID. Use `cannot_complete` for an evidenced failure under stated conditions; an untested or unmentioned feature is `unverified`. Official documentation can establish a declared path while its runtime completion remains unverified. Split those two fields instead of counting a declaration as a passed task.

Preserve atomic features in the feature map. Link each consequential matrix row to task/screen/data-flow nodes; the matrix must not flatten a feature-rich product into one adjective. Expose the last established terminal boundary: a generated idea, a committed edit, an in-memory image and a durable exported file are different results.

## 3. Run an equivalent-task study when feasible

Before recruitment/execution, fill the task and study records in [research-workbook.md](../assets/research-workbook.md):

1. Define task goal, neutral scenario, start state, observable correct end, timeout, stop/help/error rules and required proof. Avoid menu names or steps that coach the route. Separate observer interpretation from the participant's actions.
2. Recruit the relevant roles/experience and record prior product familiarity. Explain exploratory sample rationale; a small convenience sample does not estimate the whole market. Obtain the required consent before recording personal data.
3. Match the comparison contract. Use equivalent targets/data of equal difficulty, changing the actual target between products to reduce memory effects. Define/reset state consistently. Record mismatches instead of silently pooling them.
4. Counterbalance product order. For two products, distribute AB/BA; for more, use a documented balanced scheme when feasible. Record actual assignment and deviations. Repeated trials are correlated observations, not additional recruited users.
5. Use the same moderator instructions and help rule. Keep think-aloud and silent timing separate. Record every attempt, errors, help, stop/timeout and recovery; link recording timestamps. Technical invalidation keeps its original row and reason; unavailable duration/error/help measurements remain null rather than invented zeroes.
6. Review the actual outcome and recordings, including failures. Reconcile coding disagreements. Summarize by task/context and show participants, attempts, invalidations and repeated trials. Do not declare a statistically significant winner without a preplanned appropriate analysis and adequate sample.

### Metrics with denominators

- Independent success: `independent successful participants / valid selected participants`. Helped success and failure are mutually exclusive separate counts; their sum equals selected attempts.
- Default unit: first valid attempt per participant/product/task. A different repeated-measures analysis needs its own explicit method; do not feed repetitions to a participant-level percentage.
- Record time for **all** selected attempts to success, stop or timeout. Label successful-only median with its success `n`; two products' successful subsets may differ. Include the all-attempt distribution so fast survivors do not hide failures.
- Show error/help **event counts** and **affected participant counts** separately. A person who makes five errors is one affected participant.
- Use the same subjective instrument and anchors across products. A custom single question is not SUS; calculate named instruments only from their actual items and scoring method.
- A missing/not-run measure is null with its reason. For an observed zero success, show `0/N` with actual positive N. An all-invalid sample is unmeasured, not 0% success.

For this default unit, run `scripts/study_metrics.py` on a study JSON after the scoped doctor. Its output includes independent/helped/failure, success-only and all-attempt medians, invalid/repeated counts and the matched participant intersection. Read [study-record.example.json](../assets/study-record.example.json) for the executable schema. It is a **synthetic calculation fixture**, not recruited user data. The helper validates arithmetic/record consistency; analysts still inspect task equivalence, recordings, ordering, recruitment and missingness. Do not rank from its output alone.

## 4. Inspect usability, performance and accessibility separately

Use the [ten usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) as inspection lenses: system status; real-world language; control/undo; consistency; error prevention; recognition; efficient use; relevant presentation; error recovery; help. Inspect a page/state against its actual task, not every rule against every screenshot. Multiple reviewers, if available and authorized, inspect independently before merging; record a single reviewer honestly.

An issue card includes trigger, page/state, observed fact and locator, violated expectation, affected task/user, consequence, recovery and alternative explanation. Separate **observed issue**, **source-based concern**, and **untested hypothesis**. For a concern, state the evidence needed to confirm it rather than labeling the competitor broken.

Assess severity from frequency, impact and persistence. Frequency stays unknown without observations. Use either a named scale with its anchors or a declared project scale. The supplied template's high/medium/low scale is custom: high blocks/produces wrong core results; medium requires workaround/repeated repair; low adds limited friction. Assign a provisional impact risk to hypotheses, not a confirmed incident severity. NN/g's published scale is 0–4; do not relabel the template scale as that standard. Severity, evidence-acquisition priority and roadmap priority are separate fields.

For performance, name the boundary measured: click→feedback, request wait, usable content, completed task, durable result. Pin device/OS/build/thermal state/network/cache/output/mode, measuring tool and repeat count. Preserve raw trials and distributions, not an unsupported average or single universal FPS claim. Cold load, denied permission, empty/error/timeout, network loss/reconnect and background/resume are task-specific probes, not mandatory tests for every narrow study. Verify no lost or duplicate durable output where relevant.

For accessibility/control, inspect labels and reading/focus order, text scaling, noncolor state cues, target reachability, keyboard where applicable, permission denial/revocation, undo/export/delete. Pixel review supports visible concerns; screen-reader behavior requires actual use. A sampled audit is not WCAG or platform certification.

## 5. Evaluate growth, business and ecosystem only when relevant

For reviews, define platform/time/language/star strata and sampling/selection rule, retain raw locators, code themes and contrary cases. If a second coder is available, compare a subset and resolve disagreements. Theme share describes the collected sample, not all users. Do not silently sample only angry reviews.

Market metrics need name/definition, source, region/platform/window, numerator/denominator where applicable and reported vs estimated status. Downloads, MAU, paid subscribers, IAP receipts, net revenue and company revenue are not interchangeable. Compare like definitions/periods; show missing data instead of interpolating it.

Identify a meaningful first value event, prerequisite/setup burden, repeated-use trigger and who receives the result. Treat these as mechanism analysis until internal event data exists. Funnel/cohort claims require event definitions, entry cohort, time window, eligible denominator and exclusions. Public feature presence and company-attributed growth are not a causal conversion or retention experiment.

For commercial comparison, specify one workload: user/seat count, result quantity/quality, subscription period, currency/region/tax basis, minimum purchase, usage overage, required integrations, setup/training/migration effort and verification date. Separate payer/user/admin. Itemize known prices and unknown costs; a scenario with missing entitlement/credit rules has no defensible complete TCO. For API/SSO/export/migration, separate documented availability from authorized exercised behavior and failure/recovery. A bundled OS feature may have no separate app subscription; use device/platform dependence as its relevant cost boundary.

## 6. Score only when the decision benefits

Define criteria, weights and observable 1/3/5 anchors **before inspecting the final rank**. Record evidence/reviewer and disagreements; 2/4 require intermediate evidence. Template weights such as 40/25/20/15 are illustrative choices. Never treat the number of features or paragraphs as quality.

For the same fully measured criteria, total = Σ(weight × score), with weights summing to one. Missing/N/A is not zero. Show original-weight coverage; a normalized partial score `Σ(measured weight × score) / Σ(measured weight)` is descriptive only. Rank only on common measured criteria and show what was excluded. Preserve version/context differences. A hard gate (privacy, durable output, required permission policy) is pass/fail/untested and cannot be compensated by visual polish.

Run a sensitivity check by varying plausible weights and examining whether the recommendation changes; report unstable ordering as conditional. If the evidence lacks a common task/result, choose a mechanism comparison and decline a global numeric winner. Do not manufacture RICE inputs or revenue predictions to fill a matrix.

## 7. Convert findings into decisions and discriminating experiments

Use the workbook's finding/action/experiment records. A finding ties a bounded fact to source IDs, mechanism, consequence, plausible alternative causes and what would distinguish them. State impact as observed, estimated with assumptions, or unknown. Prefer a small ordered decision set over copying every feature.

An action identifies adopt/adapt/defer/inspect, fit, tradeoff/cost/dependencies, proposed owner/milestone only if known, and the result that reverses it. Distinguish confirmed repair, exploratory experiment and watch item. Recommendations do not authorize product implementation or assign people.

An experiment specifies falsifiable hypothesis; users/context; current baseline/control; one changed mechanism; assignment/unit; sample rationale; primary outcome with event/denominator/window; guardrails; proposed decision threshold; stop/rollback; owner/review time if known; continue/revise/stop interpretation. Exploratory prototype targets are proposed decision aids, not observed results or significance guarantees. For an online A/B study, plan randomization, sample and analysis separately; a proxy click is not verified task success.

Finish when the selected method has produced an inspectable artifact **and changed or bounded an actual decision**. A new heading, blank questionnaire, scoring sheet without anchors or task plan without any source analysis does not complete a requested teardown.

## Method provenance

Primary guidance: [competitive evaluations: expert review vs user testing](https://www.nngroup.com/articles/competitive-usability-evaluations/), [competitive redesign testing](https://www.nngroup.com/articles/redesign-competitive-testing/), [usability testing](https://www.nngroup.com/articles/usability-testing-101/), [heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), [severity: frequency, impact, persistence and 0–4 anchors](https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/). Consult current originals for attributed methods. These sources inform research conduct; Apple/Material/Carbon/Ant and the report's web quality checks govern presentation, not research validity.
