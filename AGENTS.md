# Repository maintenance

Maintain independently installable skills in `skills/<name>/SKILL.md`. Preserve unrelated local changes. Read [CONTRIBUTING.md](CONTRIBUTING.md) and the target skill before editing; use [runtime support](docs/runtime.md) when running tools.

- Keep this checkout as the single source, exposed through `~/.agents/skills/app-dev-skills`. Preserve edits and compatibility symlinks; verify one discovered entry per skill. Do not maintain copied installations.
- Keep instructions, references and discovery metadata in English; keep the English/Chinese root README aligned and honor the user's deliverable language.
- Keep selection, request examples and installation in the bilingual root README; do not add per-skill READMEs. Put optional installation behind a disclosure. Detailed execution belongs in `SKILL.md` and its local references; root maintenance documents are not skill runtime dependencies.
- Remove stale reports, unused assets and superseded explanations with the change that makes them obsolete; check callers, tests and evidence bindings first. Keep product-specific history out of distributed skills.
- Discover entries with `python3 scripts/list_skills.py`. Follow the contribution verification table; a structural check does not prove agent behavior or visual acceptance.

For iPhone Duo changes, read its [workspace-rule contract](skills/iphone-duo-adaptation/references/workspace-rules.md) and the [materialized ledger](docs/iphone-duo-adaptation/workspace-rules.md). Account for every catalog rule; keep app-specific agreements in `project_conventions`. Edit JSON and regenerate Markdown, preserving decisions and evidence. Materialization alone does not prove app implementation or verification.
