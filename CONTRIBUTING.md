# Contributing

Each folder under `skills/` is independently installable. Keep its SKILL.md, references, runtime assets, dependency manifests and LICENSE self-contained. Do not link from a skill to files outside its own directory. Repository-wide documentation and CI belong at the root.

Before changing a skill's responsibility, read [scope](SCOPE.md). Use the [glossary](GLOSSARY.md) and [workflow guide](docs/workflows.md) when changing evidence or completion wording. `python3 scripts/list_skills.py --json` discovers the current flat `skills/*/SKILL.md` entries; do not add a cached registry.

Use the [runtime setup](docs/runtime.md), run `sh scripts/doctor.sh`, then `npm run check`. It checks runtime readiness, collection metadata and local links, visual-tool regression tests, and browser behavior. Add a failing case before changing executable validation behavior. Keep root and standalone npm lockfiles in sync when dependencies change.

For focused checks:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
npm test -w app-store-cover-generator
npm test -w image-to-layered-html-prototype
npm run test:browser --workspaces
```

Use local, original or redistribution-cleared fixtures. Never include credentials, private absolute paths, customer data, app source code or private screenshots. Keep caches, exports and installed dependencies out of Git. Tests must not publish to store or social accounts.

Keep each skill entry focused; move detailed schemas into references. Keep English/Chinese README guidance aligned: task fit, inputs/outputs, installation, invocation, preflight and next references. Every standalone skill must include a read-only `scripts/doctor.sh` that diagnoses missing runtimes before invoking them, reports actionable repairs and exits nonzero for required failures. Test missing/old runtimes and relevant package/browser failures without removing host installations. Preserve the user's product, language and workflow choices. A validation tool must document its limitations and never fabricate reviewer judgments. The collection checker checks packaging and documentation paths; it is not a comprehensive secrets scanner.

When adding or renaming a skill, synchronize the folder/frontmatter name, `agents/openai.yaml`, both standalone READMEs, direct `SKILL.md` links in both root READMEs, doctor, tests and affected npm workspace configuration. When changing scope, update the description and default prompt as well as the workflow. Metadata must use the expected types and name the complete `$skill-name` token.

Keep action order, branch choice and completion gates in `SKILL.md`; put detailed algorithms, schemas and examples behind links that say when to read them. Installation and repair commands belong in the README. Aim to keep skill entries below 500 lines, review growth during edits, and document any necessary exception; do not remove evidence requirements to meet a length target.

Instruction changes need a scenario review for wrong-skill routing, existing-project repair, a narrow requested endpoint and missing capabilities. Record expected behavior, the source instruction and unresolved contradictions. See the [six-scenario evaluation](docs/skill-routing-evaluation-2026-10-20.md) for a worked example; a desk review is not a live model evaluation. Deterministic checks cover packaging, metadata and local Markdown paths/fragments, not language quality or semantic correctness. The Markdown checker supports this repository's documented forms, not every CommonMark extension or remote URL availability.

Swift/Vision OCR is optional and macOS-only. Keep core Python and browser validation portable. Browser scripts use Playwright Chromium by default; `PLAYWRIGHT_CHANNEL=chrome` explicitly selects an installed Chrome. Never treat changed browser rasterization as visual approval.

For a security issue, avoid public disclosure of secrets. Use GitHub private vulnerability reporting if enabled; otherwise contact the maintainer with a minimal non-sensitive description to arrange a private channel.
