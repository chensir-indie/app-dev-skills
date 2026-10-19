# Workflow and validation audit — 2026-10-12

Baseline: `7712a772c5dff6445274813ed8bfc952d9ef83dd`. Scope: complete skill instructions, design handoff, executable export/verification workflow and test coverage. No store or app release operations.

## Findings and changes

| Finding | Resolution |
| --- | --- |
| A blocked remote font or missing local font could fall back and still pass | Record blocked HTTP requests, HTTP errors, request failures and failed font loads as cell issues; block service workers |
| Removing a text audit marker bypassed a required check | Validate the exact declared text boxes in the DOM and require their text-audit records in the manifest |
| Transparent text could pass geometry checks | Detect ordinary transparent fill and zero opacity through the ancestor chain |
| Source edits between cells could leave stale source hashes | Compare initial and final source snapshots; source issues fail export and verification |
| A directory symlink could place output inside the source tree | Resolve source and destination-parent real paths before creating output |
| Motion frames could reuse identical content; filenames could collide | Check asset existence, distinct phase hashes, case-insensitive IDs and contact-sheet filename collisions |
| Visual review had no executable completeness or stale-export check | Add a pending per-cell review record, manifest digest binding, required evidence notes and separate exception status |
| Synthetic UI copy and repeated branding constrained real-capture layouts | Configurable textFields with headline required, plus project/slide showBrand; declared boxes still cannot evade auditing |
| Agent completion criteria were too implicit | Add measurable master/series criteria, reconstruction modes, source-input trust boundary and explicit review completion steps |
| Docs and runtime checks used separate contributor commands | Add npm run check for entry-field/local-link checks plus unit and browser suites; use the same command in CI |

## Evidence

Before fixes, all seven new pipeline regression scenarios failed against the baseline: missing audit marker, transparent ancestor, transparent fill, remote-font fallback, local-font fallback, source mutation, and source-nested symlink output. They pass after the fixes.

The final local `npm run check` passes **29 unit tests and 12 browser tests**. This includes the existing 50-locale × 2 native-canvas layout loop, review-record lifecycle (pending, stale, incomplete, duplicate, exception), optional UI copy/branding, manifest tampering, PNG integrity and source/path checks. Skill frontmatter validation and diff whitespace checks also pass. Documentation link checks cover local file targets and required entry fields; they do not validate external URLs, anchors or all YAML syntax.

Native export evidence (Git-ignored directories under `.test-output/`):

| Directory | PNG cells | Manifest SHA-256 |
| --- | --- | --- |
| `audit-native-20261012` | 12 | `41b49f06ea10ccd284f84f60bcec9325c194020e0d7725a664c063da82ad81d8` |
| `capture-only-output-20261012` | 1 | `e4c2768588d3f1cf9e26c68b969176533abd61241af44beca1a13e19915c8b80` |

The 12-cell export has a pending review scaffold. A Chinese contact sheet and the native no-brand/no-synthetic-UI variant were visually spot-checked for the changed rendering contract; no full design approval is claimed. The artwork remains the original synthetic demo, not a finished product campaign.

## Limits retained

The checker validates visual-review records, not visual judgment or approval authority. Different phase bytes do not prove different visible poses. Fonts, translation quality, raster UI language, complex compositing and reference fidelity require inspection. Source snapshots catch persistent differences, not transient edits restored between snapshots. Templates are trusted executable code; HTTP restrictions are not a security sandbox. Store eligibility and release authorization remain separate from local validation.
