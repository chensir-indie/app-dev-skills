# Contributing

[Documentation](docs/README.md) · [Security](SECURITY.md)

## Questions and bug reports

For setup failures, use [runtime troubleshooting](docs/runtime.md); for missing or duplicate skills, use [discovery troubleshooting](docs/getting-started.md#verify-the-installation). Search [existing issues](https://github.com/chensir-indie/app-dev-skills/issues) before opening a report. English and Chinese are welcome.

Include the affected skill and endpoint, source revision/local changes, installation method, OS/agent/runtime versions, exact command or sanitized prompt, minimal reproducer, expected/actual result and relevant doctor output. For visual failures, include the browser, viewport, zoom, fonts and a shareable reference. Use relative paths and synthetic inputs. Send vulnerabilities and credential exposures through [Security](SECURITY.md), not a public issue. No response time is promised.

For feature proposals, explain the starting material, desired output and gap in an existing skill. New responsibilities must meet [scope criteria](SCOPE.md#adding-a-responsibility).

## Package and source rules

- Keep the flat `skills/<name>/SKILL.md` layout. Each skill includes its references, assets, scripts, dependency manifests and license; runtime links stay inside its own directory. Root `scripts/`, `tests/` and `docs/` maintain the collection.
- Maintain one source checkout, exposed through `~/.agents/skills/app-dev-skills`. Preserve existing edits when migrating copies; compatibility symlinks may point to the same source after verifying one discovered entry per skill. Use the [installation guide](README.md#1-connect-codex-to-one-source-checkout).
- Discover entries with `python3 scripts/list_skills.py --json`, rather than maintaining another registry. Product accounts, credentials, private assets and release decisions belong in the product workspace.
- Every skill includes a read-only `scripts/doctor.sh`: diagnose required runtimes before invoking them, report repairs, and exit nonzero on required failures. Test absent/old runtimes and applicable package/browser failures without removing host installations.
- Keep root and standalone lockfiles aligned when dependencies change. Core Python/browser checks remain portable; Swift/Vision OCR is optional and macOS-only.

## Instructions and documentation

Keep branch selection, action order and completion gates in `SKILL.md`; link to detailed schemas and examples only where needed. Aim for fewer than 500 lines per entry; explain necessary exceptions without weakening evidence requirements. Installation and repair commands belong in user guides.

Use English for instructions, references, default guides and `agents/openai.yaml`. Localized guides, multilingual fixtures, original-language evidence and legal notices may retain their language. Preserve identifiers, paths, schema keys and compatibility contracts. The user's requested deliverable language and workflow take precedence.

Maintain one authoritative explanation for each collection concern: homepage for installation/selection, getting-started for first use/migration, runtime guide for dependencies, workflows for stage handoffs, and this guide for contribution rules. Standalone skill guides must remain usable without those root documents. Keep English/Chinese guidance aligned; preserve linked anchors or update their callers.

When adding, renaming, removing or changing a skill's scope, update its folder/frontmatter, `agents/openai.yaml`, both standalone READMEs, direct `SKILL.md` links in both root catalogs, references, doctor and affected tests/workspace configuration. Descriptions and default prompts must match the new scope; metadata must use the expected types and complete `$skill-name` token. Search for stale names.

## Verification

Set up dependencies with [runtime support](docs/runtime.md), then choose checks by the change:

| Change | Required verification |
| --- | --- |
| Documentation or instructions only | `npm run check:docs`; inspect affected routing scenarios and language parity |
| Executable validation | Add a failure fixture demonstrating the original problem; run focused tests, then `npm run check` |
| Other collection/tool changes | Run relevant focused tests, then `npm run check` |

`npm run check` already runs doctor, documentation, unit and browser checks; a separate full doctor immediately before it is redundant. Focused commands and browser-channel setup are in [runtime support](docs/runtime.md#focused-verification). Tests must not publish to store or social accounts.

For instruction changes, review wrong-skill routing, existing-project repair, a narrow endpoint and missing capabilities where affected. Record expected behavior, the governing instruction and contradictions in the PR or existing task record. Use the [recorded scenarios](docs/skill-routing-evaluation-2026-10-20.md) as examples, not proof of live model execution. A new dated report is useful only when it preserves reusable evidence or a substantive decision; routine documentation cleanup needs no separate report.

Documentation checks cover packaging, metadata and supported local Markdown paths/fragments, not remote availability, semantic correctness or secrets. Visual acceptance still requires inspection of the actual result; browser rasterization or a passing doctor is not approval.

## Submit the change

Describe the concrete problem, resulting behavior, checks actually run and any limitations. Distinguish existing failures and environment blockers from new regressions. Link a permitted reproducer or before/after evidence when useful; dated results should name the tested source and environment.

Keep unrelated edits, caches, exports and dependencies out of the change. Fixtures must be original or redistribution-cleared. Review the diff for credentials, private paths, customer data, app source and screenshots. Ignored local logs may support the work, but the public description must explain enough to reproduce the result. Preserve applicable licenses and provenance.
