# Repository maintenance

This repository packages independently installable app-development skills. User instructions determine task scope; preserve unrelated local changes.

Read only the maintenance material relevant to the change:

- Adding a skill or changing its responsibility: read [SCOPE.md](SCOPE.md).
- Editing instructions, metadata, scripts or packaging: read [CONTRIBUTING.md](CONTRIBUTING.md), then the target skill's actual `SKILL.md`.
- Changing stage boundaries or evidence wording: read [GLOSSARY.md](GLOSSARY.md) and [workflows](docs/workflows.md).
- Running tools or diagnosing missing dependencies: read [runtime support](docs/runtime.md).

Discover entrypoints with `python3 scripts/list_skills.py`. Keep the flat `skills/<name>/SKILL.md` layout and each installed skill self-contained; root maintenance documents are not runtime dependencies.

When adding, renaming, removing or changing a skill's scope, synchronize its frontmatter, `agents/openai.yaml`, both standalone READMEs, both root README entries, references, doctor and affected tests/workspace configuration. Inspect the working tree for old names; do not maintain a second hardcoded skill list.

For executable validator changes, add a failure fixture that demonstrates the problem. Run focused checks during iteration and `npm run check` before delivering collection/tool changes. For instruction-only changes, check documentation and review relevant routing scenarios; use the [recorded scenarios](docs/skill-routing-evaluation-2026-10-20.md) as examples, not proof of model execution.
