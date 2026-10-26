# General guidance and project conventions

Read when proposing adaptation decisions and materializing workspace rules. Preserve the main sequence: **whole-app layout analysis → adaptation recommendations → complete HTML prototype**. These layers identify provenance and applicability; they do not add a default product-implementation stage.

## General guidance

The [rule catalog](../assets/official-rules.json) maintains reusable Apple guidance, framework contracts, engineering boundaries, and collection workflow policy. `workflow_constraint` identifies collection policy such as analyzing the baseline, delivering HTML, using the preferred builder, and recording evidence. It is not an Apple-prescribed delivery workflow for every app. API documentation cannot substitute for target-product runtime evidence.

Keep a complete snapshot and stable IDs; workspace-ledger `bindings` describe application to the target app. Explain inapplicability, uncertainty, or later native verification rather than silently editing rule text or removing inconvenient rules. General routing identifies the actual framework. Mark another framework's dedicated rules not applicable; framework identity itself is not an app-specific product convention.

## Project conventions

Page scope, functional entrypoints, permissions, sending conditions, draft lifetime, read/unread behavior, and follow-bottom policy come from user instructions, project contracts, or explicit product decisions. Record them separately in `project_conventions`. They may inherit general guidance or express project-specific behavior; an Apple citation does not turn these choices into cross-app requirements.

The reusable [migration-review contract](migration-review.md) requires original-design preservation and named environment review. The target app's actual tokens, density, chosen columns/navigation, breakpoint values, pose-preset dimensions, region assumptions, and permitted visual deltas are project facts or decisions. Preserve their attribution and do not present them as universal Apple specifications. A generated concept becomes an adopted design target only with attributable authorization.

Use a stable `PROJECT-` ID and provide a title, `origin`, attributable local `basis`, applicability, phases, statement, and `parent_rule_ids`. Then record implementation under the same status/file/evidence gates as general bindings. Allowed origins are `user_instruction`, `project_contract`, and `product_decision`. Project conventions cannot redefine or impersonate canonical rule IDs. Parent IDs reference existing general rules; an independent convention may use an empty array with its project basis documented.

Project conventions have a separate Markdown section and participate in ordinary and completion checks. Do not hide them in an unchecked annotation. Old ledgers without the array remain compatible as an empty array. After adding entries, run `render` then `check` under the [workspace-rule contract](workspace-rules.md).

## Boundaries of the IMX example

The [IMX example](../assets/project-conventions.imx.example.json) separately registers the chat-specific parts of the six-point review: current layout/prototype scope, message geometry, region modeling, accessible tasks, and engineering evidence. It derives from the user-supplied IMX v1.0 text and is not a renewed review of real source or UI.

Merge relevant entries only when the target is IMX or the user explicitly adopts them, after reading existing project agreements. Do not import them into unrelated apps. Retain the confirmed redesign scope and existing business contracts; an example mentioning rich messages, sending, or overlays does not authorize adding those capabilities. A Skill/rules-maintenance task does not authorize IMX UI changes, real-account operations, or release.

For other apps, derive conventions from their own baseline and user constraints and reference applicable general IDs. A ledger's `verified` status applies only to its declared check scope. Keep HTML, Skill-maintenance checks, and actual app acceptance as separate evidence.
