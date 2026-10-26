# Documentation

[简体中文](README.zh-CN.md) · [Collection overview](../README.md)

Choose a guide by the task you are doing. The root README is the skill catalog; each skill's `SKILL.md` is its execution contract. This index connects those entrypoints without introducing another registry.

## Use the collection

| You want to… | Read |
| --- | --- |
| Choose a skill from your inputs and desired output | [Skill catalog](../README.md#choose-a-skill) |
| Install, verify discovery, try a first task or migrate an old installation | [Getting started](getting-started.md) |
| Repair a missing runtime, package or browser | [Runtime setup and support](runtime.md) |
| Decide where to stop or hand artifacts to another skill | [Workflows and handoffs](workflows.md) |
| Interpret an evidence or completion claim | [Shared terms](../GLOSSARY.md) |
| Ask a question or report a reproducible problem | [Support](../CONTRIBUTING.md#questions-and-bug-reports) |

For schemas, design rules and tool commands, open the selected [skill guide](../README.md#choose-a-skill), then follow its `SKILL.md` references. Each standalone package owns those contracts; this index does not repeat them.

## Contribute and maintain

- [Contributing](../CONTRIBUTING.md): development setup, package structure, change checklist and verification.
- [Collection scope](../SCOPE.md): responsibilities, overlap and criteria for adding a skill.
- [Security policy](../SECURITY.md) and [third-party notices](../THIRD_PARTY_NOTICES.md): reporting and provenance.

## Validation and design history

<details>
<summary>Historical records — not required for everyday use</summary>

These are dated observations of particular files, environments and tasks. They are not a support matrix, a live CI dashboard or proof that a new product has passed. Some records refer to private local artifacts or ignored test output that is not included in the checkout. Follow the recorded public commands where available; unavailable evidence remains unavailable. Historical records retain their original language.

| Area | Records |
| --- | --- |
| Collection documentation and routing | [Documentation review, 2026-10-26](documentation-review-2026-10-26.md); [English instructions, 2026-10-26](english-skills-validation-2026-10-26.md); [routing scenarios, 2026-10-20](skill-routing-evaluation-2026-10-20.md); [collection comparison, 2026-10-20](mattpocock-skills-comparison-2026-10-20.md) |
| Competitor analysis | [Initial delivery, 2026-10-20](app-competitor-analysis-validation-2026-10-20.md); [research methods, 2026-10-21](app-competitor-analysis-methods-validation-2026-10-21.md); [report design, 2026-10-22](app-competitor-analysis-design-validation-2026-10-22.md); [design specification, 2026-10-22](app-competitor-analysis-design-spec-validation-2026-10-22.md); [interaction, 2026-10-23](app-competitor-analysis-interaction-validation-2026-10-23.md) |
| Layered prototype | [Design quality, 2026-10-21](prototype-design-quality-evaluation-2026-10-21.md) |
| iOS adaptation | [Initial workflow and framework revisions](iphone-duo-adaptation-validation-2026-10-23.md); [builder, 2026-10-26](iphone-duo-adaptation-build-web-apps-validation-2026-10-26.md); [minimal migration, 2026-10-26](iphone-duo-adaptation-minimal-migration-validation-2026-10-26.md); [device presentation, 2026-10-26](iphone-duo-adaptation-device-fidelity-validation-2026-10-26.md) |
| Store artwork | [Toolkit validation](../skills/app-store-cover-generator/docs/validation.md); [locale validation](../skills/app-store-cover-generator/docs/global-locales-validation.md); [workflow audit, 2026-10-12](../skills/app-store-cover-generator/docs/workflow-audit-2026-10-12.md) |
| Publication | [Tool and scenario checks, 2026-10-26](app-publish-skill-validation-2026-10-26.md) |

Current local readiness comes from the relevant `doctor.sh`; current automated results come from the checks you actually run. Neither replaces artifact-specific review or provider evidence.

</details>
