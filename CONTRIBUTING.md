# Contributing

## Questions and bug reports

Use the selected skill's README for setup or [runtime support](docs/runtime.md) for environment failures. Report the skill, revision, command/request, expected/actual result and sanitized doctor output in [Issues](https://github.com/chensir-indie/app-dev-skills/issues). For visual failures include the reference, browser and viewport. Report vulnerabilities through GitHub private reporting when available; otherwise request a private channel without posting secrets or exploit details.

## Package and source rules

- Use the flat `skills/<name>/SKILL.md` layout. Each package owns its references, assets, scripts, dependencies, bilingual README and license; local runtime links stay inside it.
- Maintain one source checkout and the Codex collection symlink. Preserve local edits; compatibility paths may be symlinks to that source, with one discovered entry per skill.
- Add a skill only for a recurring task with distinct inputs, actions and an observable result. Explain overlap, runtime needs and independent installation. Product-specific credentials, account mappings and release history belong in product workspaces.
- Each skill has a read-only `scripts/doctor.sh` with actionable repairs and a nonzero exit for missing required tools. Keep root/standalone lockfiles aligned. Test absent/old runtimes with fixtures, not by removing host installations.

## Instructions and documentation

Keep selection and installation in the root README. Each skill README needs only a use case, copyable prompt, inputs/outputs and optional setup. Put execution order and completion gates in `SKILL.md`; disclose detailed branch contracts through local references. Avoid duplicate walkthroughs, documentation indexes and dated cleanup reports.

Use English for instructions/references/metadata and align bilingual guides. Preserve the user's output language, original-language evidence and legal notices. Retain required evidence and license files; remove obsolete explanations and repair their callers.

For additions, renames, removals or scope changes, synchronize folder/frontmatter, `agents/openai.yaml`, both skill READMEs, both root catalogs, references, doctor and affected tests/configuration. Keep metadata types valid and the exact `$skill-name` token in default prompts. Search for stale names and links.

## Verification

| Change | Checks |
| --- | --- |
| Documentation/instructions | `npm run check:docs`, language parity and affected route review |
| Validation code | Failure fixture for the original problem, focused tests, then `npm run check` |
| Other tool/package changes | Relevant focused tests, then `npm run check` |

See [runtime support](docs/runtime.md#focused-verification) for setup. For changed instructions, inspect wrong-skill requests, existing-project repair, narrow endpoints and missing capabilities; report expected behavior and limitations in the task/PR. Static scenarios are not live agent tests. Automated checks do not replace visual or provider evidence. Tests use local synthetic fixtures, without publishing.

## Submit the change

Explain the problem, resulting behavior, checks actually run and limitations. Preserve unrelated edits. Exclude credentials, private paths, customer data and unlicensed fixtures; retain applicable licenses. Ordinary documentation cleanup needs no new historical report.
