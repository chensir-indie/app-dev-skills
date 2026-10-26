# Decision workbook — fill with actual evidence

Use only selected records from [research methods](../references/research-methods.md). They can appear as report blocks, a compact table or a linked appendix. Keep conclusion-changing qualifications in the main report. This is an authoring tool, not an extra mandatory chapter set.

## Research brief and method receipt

Decision / alternatives / audience:
User and recent situation (observed episode or analyst hypothesis):
Falsifiable question / consequence of a wrong choice:
Direct / indirect / substitute selection and exclusions from each comparison:
Time/budget/technical constraints:
Conditions matrix (version/device/region/role/tier/permissions/network/data/familiarity):
Selected method → completed/partial/not_run → inspected artifacts → allowable conclusion → missing proof:

## Capability row

Product / capability / exact requested outcome:
Declared path + source / observed completion + source:
can_complete / limited / cannot_complete / unverified (runtime result):
Prerequisite, tier, permission, scale, version / comparison mismatch:
Related feature, task, screen and data-flow nodes:

## Task protocol and raw attempt

Task ID / neutral scenario / reason it matters to the decision:
Start / observable correct end / durable outcome proof:
Timeout / stop / error / help / invalidation rules:
Equivalent dataset and reset / device and permissions / product order assignment:
Target participants / prior familiarity / sample rationale / silent or think-aloud:
Attempt: participant ID / product / task / order / trial / independent_success, helped_success, failure or invalid / seconds / errors / help events / timestamp / exclusion reason:
Summary: recruited unique people / valid first attempts / repeated trials / excluded technical trials and reasons / independent n/N / helped / failed / successful-only median and n / all-attempt times / event counts vs affected people:

## Heuristic issue card

ID / inspected page-state and trigger / evaluator and scope:
Fact + exact locator / observed issue, source-based concern or hypothesis:
Expectation / heuristic / affected task and consequence:
Frequency (including unknown) / impact / persistence / recovery:
Named severity scale + anchors or provisional impact risk:
Alternative explanation / confirmation or refutation probe:
Separate acquisition priority / roadmap decision and constraints:

## Market, reviews and commercial record (conditional)

Metric definition / source status / geography-platform-period / numerator-denominator / coverage limit:
Review sampling frame and selection / theme code / raw locators / contrary case / coder reconciliation:
Meaningful first-value event / entry cohort / eligible denominator / window / exclusions:
TCO scenario and currency-tax-period / known price items / usage caps and credits / unknown cost / integration documented vs exercised:

## Scoring record (optional)

Decision / predeclared criterion-weight / 1,3,5 observable anchors / reviewer-evidence-disagreement:
Common measured criteria / original-weight coverage / omitted unknowns:
Hard gate pass-fail-untested / total if defensible / plausible weight sensitivity:
Interpretation and the condition that reverses the choice:

## Finding → decision → experiment

Finding ID / bounded fact + E IDs / mechanism / affected task:
Impact observed-estimated-unknown / assumptions / alternative cause:
Recommendation adopt-adapt-defer-inspect / fit / cost-risk / dependency / fallback:
Experiment hypothesis / control / one changed mechanism / participants and assignment unit:
Primary event, denominator and window / sample rationale / guardrails:
Proposed threshold / stop-rollback / continue-revise-stop interpretations:
Known owner and review date, otherwise unassigned / not scheduled:
Execution status and result artifact, otherwise not_run:

## Worked transfer example: fictional note recovery

**Question:** Should Example Notes restore an interrupted draft automatically or open a recovery chooser? This is a fictional method demonstration, unrelated to any competitor's measured behavior.

**Evidence inspected:** fixture screenshot `D1`, draft text present in editor; fixture saved-state JSON `D2`, draft text and a different saved revision. Both are synthetic. No actual close/reopen recording exists.

**Capability judgment:** a draft object exists in the fixture; runtime recovery is **unverified**. The difference between draft and saved revision establishes a state conflict to handle, not a lost-data incident. Feature map retains edit/autosave/manual save; task map shows the missing reopen edge; screen map distinguishes editor from proposed chooser; technical map preserves draft/revision/restore consumer. None of those maps proves restoration.

**Issue concern:** on reopening, silently picking a version could show unexpected content. Heuristic lens: status visibility and user control. Frequency unknown; impact could be high if edits are discarded; persistence depends on overwrite behavior. Provisional impact risk, not a confirmed severity. Alternative: the runtime already merges safely. Probe: make different edits offline and on a second device, reopen and inspect both text and stored revisions.

**Decision:** defer choosing the chooser until the probe distinguishes recoverable local drafts from irreconcilable conflicts. A chooser adds an interruption to every reopen if applied indiscriminately. If the draft is always newest and recoverable, restore it with a visible recovery affordance; if conflicting valid versions occur, expose a choice with previews.

**Proposed experiment, not executed:** compare current reopening with automatic newest-draft restore plus undo, changing only recovery entry. Use equivalent different notes and AB/BA order among recruited note users; choose exploratory sample size based on available roles, not an invented population claim. Primary outcome: correct intended text reopened without moderator help per valid participant/task in a declared two-minute window. Guardrails: no stored version overwritten, readable long previews and successful undo. Continue only if correct restoration improves without losing either version; revise if users cannot identify the restored version; stop on irreversible loss. Recruitment, recording and outcome data remain absent.

The executable [study fixture](study-record.example.json) demonstrates arithmetic separately. Its fictional successes are not evidence that this recovery design works.

## Worked scoring refusal and sensitivity (fictional)

Suppose a decision predeclares task success 50%, recovery 30%, visual clarity 20%. These are custom teaching weights. A recovery anchor could be 1 = the interrupted text cannot be recovered under the protocol; 3 = a user can recover it through an explicit chooser; 5 = the intended draft returns with verified undo and both revisions retained. Write similarly observable anchors for the other criteria before rating.

With fictional A scored 4 / unknown / 5 and B scored 3 / 5 / 4, A's measured-weight coverage is 70%, B's is 100%. A's normalized partial score is `(0.5×4 + 0.2×5)/0.7 = 4.29`; B's full score is `3.80`. Comparing those numbers as an overall rank is invalid. On the common task/clarity criteria B is `3.29`; that bounded comparison omits recovery and cannot settle the decision. If A's eventual recovery score is 1 its full score becomes 3.30; if 5 it becomes 4.50. The missing observation can reverse the recommendation. Keep A's durable-recovery hard gate **untested**, not passed by its visual score.

For fully measured fictional C = 5 / 2 / 3 and D = 3 / 5 / 4, the original weights yield C=3.70, D=3.80. A plausible task-heavy choice 60% / 20% / 20% yields C=4.00, D=3.60. Report that rank as dependent on the task/recovery tradeoff; choose the relevant scenario with the decision owner rather than hiding the sensitivity behind two decimal places. These examples never supply missing scores for real competitors.
