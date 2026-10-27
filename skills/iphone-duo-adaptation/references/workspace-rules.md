# Materialize every rule in the target workspace

Read after the current app's layout inventory and before adaptation recommendations. Record **every** rule, recommendation, and applicability boundary from the [rule catalog](../assets/official-rules.json) in the target workspace. External links, a claim of following HIG, or a handpicked subset do not satisfy materialization.

## One catalog, two workspace representations

`assets/official-rules.json` is this Skill's maintained catalog. It provides stable IDs, kinds, phases, applicability, statements, workspace actions, verification methods, and sources. It distinguishes Apple guidance, framework contracts, engineering boundaries, product choices, and workflow policy. Recommendations and product choices remain identifiable as such. The catalog also includes SwiftUI, UIKit, React Native, and WebView-specific rules. Apply only those relevant to the identified framework; mark the others not applicable with framework evidence.

Run the tool for the user's **target app workspace**. Default outputs:

```text
docs/iphone-duo-adaptation/workspace-rules.json
docs/iphone-duo-adaptation/workspace-rules.md
```

JSON is the project ledger containing a complete catalog snapshot and rule bindings. Markdown is generated from that JSON, with separate general-rule and project-convention sections. To use an established artifact directory, pass a workspace-relative `--output-dir`, such as `.scratch/iphone-duo-adaptation`. Ordinary product tasks write there, not back into the installed Skill.

The helper requires Python 3.9+ with no pip packages. Layout analysis and HTML work need no Xcode or device; browser acceptance requires an available browser. From the Skill source directory, replace the target path:

```sh
sh scripts/doctor.sh
python3 scripts/workspace_rules.py init --workspace /path/to/app
python3 scripts/workspace_rules.py check --workspace /path/to/app
```

Read and maintain existing records; `init` does not overwrite them. After changing project fields in JSON, run `render` then `check`. Existing nongenerated Markdown is preserved. When the catalog changes, review the differences and preserve existing decisions/evidence during reconciliation; an old ledger is not a passing copy of the new standard.

## Bind each rule

Each canonical ID has exactly one binding with the complete source and applicability retained:

| Field | Required content |
| --- | --- |
| `status` | `pending`, `implemented`, `verified`, `not_applicable`, `deferred`, or `blocked`; initial pending does not mean complete |
| `reason` | Project facts explaining inapplicability, deferral, or blockage; unfinished work is not inapplicable work |
| `decision` | How the current app applies the rule: layout/component/state behavior, product tradeoffs, and justified exceptions |
| `targets` | Workspace-relative baseline/design paths and implementation destinations; before implementation, pending items may identify planned paths, clearly distinguished from files already present |
| `evidence` | Executed captures, task records, measurements, or check-result files; planned checks are not evidence |

Connect each `workspace_action` to actual pages and shared components: **rule ID → baseline evidence/applicability → adaptation decision → Design/HTML/source location → checks and actual evidence**. Apply relevant layout, navigation, typography, color, spacing, hit-area, text-scaling, input, and overlay rules in the existing `Design.md` or equivalent, then in HTML. Native-only rules may be deferred with reasons for an HTML task while remaining recorded. Missing Xcode neither removes rules nor blocks independent HTML work.

## Pre-implementation handoff gate

Complete this stage-2 gate **before the first creation or edit of prototype implementation in the current iteration**. Inventory/source reads, current-app captures, and analysis/design/ledger work can precede it. A catalog initialized with empty pending bindings is materialized, but it is not ready for implementation.

For every catalog rule, assess applicability against the identified framework, app, and requested endpoint. Fill applicable `decision` and `targets` with page/component behavior and planned implementation destinations; include baseline/design paths that already exist. Keep unexecuted work `pending`, with no invented evidence. Mark exclusions `not_applicable` with reasons; native-only work may be `deferred` with its exact boundary and later check. Record actual blockers separately. Register attributable adopted agreements in `project_conventions`, including original-design preservation, any authorized scope changes, selected responsive arrangements, and review assumptions that are specific to this app.

Render and check the ledger, then inspect its content against the whole-app analysis. Ordinary `check` allows empty pending records and therefore cannot enforce this readiness gate by itself. Pending planned implementation targets need not exist yet; `implemented`/`verified` targets and claimed evidence must satisfy the tool's actual path and evidence checks. Do not mark an item implemented merely to make its planned path appear complete.

Freeze the **populated** JSON and generated Markdown, original-design references, page/task/environment matrix, [retain/adapt/change record](migration-review.md), design/recommendation handoff, and builder route/acceptance plan. Record file identities/hashes and timestamp before implementation starts; pass those exact inputs to the selected builder. If a decision changes during construction, record a new handoff revision and its reason before applying that change. Final verification will update statuses/evidence without retroactively changing what the pre-implementation snapshot contained.

For an existing prototype or a late-discovered gap, preserve the actual earlier chronology and label the missing/late gate. Begin a new revision with the populated frozen handoff before its first implementation edit. A later completed ledger cannot prove that the earlier run followed the required order; never backdate evidence or describe planned verification as executed.

## Separate general guidance from project conventions

The catalog and `bindings` remain reusable. Apple guidance, framework contracts, engineering boundaries, and Skill workflow policy keep their own `kind` and source. Put app-specific behavior, scope constraints, and selected designs in the optional top-level `project_conventions` array. Old ledgers without it are treated as having an empty array. See [project conventions](project-conventions.md).

Each project convention contains:

| Field | Contract |
| --- | --- |
| `id`, `title` | A unique stable `PROJECT-` ID and clear title |
| `basis`, `origin` | Attributable requirement, project contract, or decision; origin is `user_instruction`, `project_contract`, or `product_decision` |
| `applies_when`, `phases`, `statement` | Applicable facts, phases using the catalog's four phase values, and project behavior |
| `parent_rule_ids` | Existing general-rule IDs; may be empty for independent business agreements, without inventing Apple provenance |
| `status`, `reason`, `decision`, `targets`, `evidence` | The same state, reasons, decisions, planned/actual workspace targets, and executed-evidence boundaries as a general binding |

General layout and continuity rules can inform a messaging app; sending, read status, draft lifetime and redesign boundaries remain project conventions. Register known attributable agreements only; do not prepopulate business obligations for an unidentified app or rewrite project choices into the general catalog.

Read project Agent instructions and add a **conditional short pointer** in the existing `AGENTS.md` or equivalent: during Duo adaptation, read the generated rules and design contract. Preserve existing instructions and avoid copying the entire catalog into that entrypoint or imposing Duo policy on unrelated work. When the user prohibits file writes, provide structured unmaterialized records and gaps without claiming workspace materialization.

## Acceptance and ongoing consistency

```sh
python3 scripts/workspace_rules.py render --workspace /path/to/app
python3 scripts/workspace_rules.py check --workspace /path/to/app --complete
```

Ordinary checks validate the exact catalog snapshot, full coverage, project-convention fields and parent IDs, paths, and JSON/Markdown synchronization. They allow pending work and do not establish completion. Completion checks include registered project conventions and reject unfinished or unsupported applicable items. They permit reasoned inapplicability and reasoned deferral only for rules belonging exclusively to the later native phase. This validates **record integrity**, not semantic Apple compliance, visual judgment, or native support.

Before implementation, apply the populated handoff gate above. Before final HTML delivery, compare each rule with actual pages/states, fix inconsistencies, and update evidence. Analysis, recommendations, design, HTML, and browser checks share rule IDs. Report pending materialized records honestly. A Skill-maintenance checkout without a target app can establish catalog materialization, not that app pages already implement it.
