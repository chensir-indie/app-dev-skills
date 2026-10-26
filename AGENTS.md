# Repository maintenance

This repository packages independently installable app-development skills. User instructions determine task scope; preserve unrelated local changes.

Read only the maintenance material relevant to the change:

- Adding a skill or changing its responsibility: read [SCOPE.md](SCOPE.md).
- Editing instructions, metadata, scripts or packaging: read [CONTRIBUTING.md](CONTRIBUTING.md), then the target skill's actual `SKILL.md`.
- Changing stage boundaries or evidence wording: read [GLOSSARY.md](GLOSSARY.md) and [workflows](docs/workflows.md).
- Running tools or diagnosing missing dependencies: read [runtime support](docs/runtime.md).

Discover entrypoints with `python3 scripts/list_skills.py`. Keep the flat `skills/<name>/SKILL.md` layout and each installed skill self-contained; root maintenance documents are not runtime dependencies.

Maintain skill instructions, references and discovery metadata in English for international distribution; follow CONTRIBUTING.md for localized guides, original-language evidence and legal-notice exceptions. Preserve the user's requested artifact language.

For Codex development, maintain this checkout as the single source and expose `skills/` through one `~/.agents/skills/app-dev-skills` symlink. Installation guidance must preserve existing edits and avoid maintained copies in `~/.codex/skills`; compatibility symlinks may point to the same source when existing tools require them, with discovery checked for duplicates.

For skill additions, renames, removals or scope changes, follow the [synchronization requirements](CONTRIBUTING.md#instructions-and-documentation). For every change, use the [verification table](CONTRIBUTING.md#verification); recorded routing scenarios are examples, not proof of model execution.

When maintaining or applying iPhone Duo adaptation, read the [workspace-rule contract](skills/iphone-duo-adaptation/references/workspace-rules.md) and this checkout's [materialized rule ledger](docs/iphone-duo-adaptation/workspace-rules.md). Keep every catalog rule accounted for; record app-specific agreements separately in `project_conventions`, maintain decisions and evidence in JSON, and regenerate its Markdown. Keep the Duo Skill and generated rule prose in English. Rule materialization alone does not prove an app has implemented or verified them.
