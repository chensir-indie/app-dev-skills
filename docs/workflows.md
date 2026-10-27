# Workflow boundaries

[简体中文](workflows.zh-CN.md)

Use this guide when changing what a skill does or how it hands work to another skill. To choose and use a skill, start with the [catalog](../README.md#how-to-use).

| Skill | Default result | Limits |
| --- | --- | --- |
| Competitor analysis | Reports with supporting evidence and product recommendations | Label inferences. Analysis does not approve a design. |
| Layered HTML | Editable pages and browser comparisons | Concept or review requests may stop earlier. Label prototype screenshots separately from real app screenshots. |
| iPhone Duo | Whole-app analysis, recommendations, then a complete HTML prototype | Stop earlier for an explicit advice-only request. Native implementation and device acceptance are separate stages. |
| Store covers | Editable source and reviewed exports for each language, device and slide | Permission to export does not include permission to upload. |
| App publication | The local or provider stage the user requested | For a TestFlight upload, stop at the receipt for the exact artifact, version and build. Verify processing, distribution, review and public release separately. |

Follow the selected `SKILL.md` for execution and acceptance. When handing work to the next stage, include existing artifact paths and hashes, their source and current state, findings with observations and inferences clearly distinguished, completed checks, and remaining gaps. Carry forward prior decisions and authorization without adding approval steps.

For Duo, follow the [workspace-rule contract](../skills/iphone-duo-adaptation/references/workspace-rules.md) for the full rule catalog, the completed handoff before implementation, project conventions and browser evidence. This collection's ledger records skill maintenance. Acceptance of a target app requires that app's own evidence.
