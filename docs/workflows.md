# Workflow boundaries

[简体中文](workflows.zh-CN.md)

Maintainer reference: use this when changing skill responsibilities or handoffs. Users can invoke a skill directly from the [catalog](../README.md#choose-a-skill).

| Skill | Default endpoint | Boundary |
| --- | --- | --- |
| Competitor analysis | Evidence-linked reports and product recommendations | Inferences remain labeled; analysis does not approve a design |
| Layered HTML | Editable pages and browser comparisons | Concepts/reviews may stop earlier; prototype captures are not real app captures |
| iPhone Duo | Whole-app analysis → recommendations → complete HTML prototype | Explicit advice-only scope ends earlier; native implementation/device acceptance is separate |
| Store covers | Editable source and reviewed locale/device/slide exports | Export does not authorize upload |
| App publication | The requested local or provider stage | Exact TestFlight upload receipt ends upload work; processing, distribution, review and public release remain separate |

The selected `SKILL.md` owns execution and acceptance. For cross-stage work, pass existing artifact paths/hashes, source/state context, observed versus inferred findings, completed checks and remaining gaps. Preserve prior decisions and authorization; handoffs do not add approval steps.

Duo's catalog, populated pre-implementation handoff, project conventions and browser evidence remain governed by its [workspace-rule contract](../skills/iphone-duo-adaptation/references/workspace-rules.md). This collection's ledger is maintenance evidence, not target-app acceptance.
