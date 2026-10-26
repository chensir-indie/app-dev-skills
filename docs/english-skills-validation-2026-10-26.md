# English skill instructions — 2026-10-26

Historical snapshot before the later same-day video-skill relocation. The two video packages now belong to the video-production workspace's `.agents/skills/`; the current app-development catalog contains five skills. The seven-skill counts and checks below describe the pre-move English translation, not the current catalog.

## Scope

Standardized all seven canonical collection skills on English instructions and discovery metadata. Reviewed 94 files: seven `SKILL.md` entries, 73 Markdown references, seven English guides and seven `agents/openai.yaml` files. Existing English instructions were retained; Chinese instruction prose was translated in App Publish Skill, AI Storyboard Director and Image to Layered HTML Prototype. Remaining Chinese discovery prompts in App Competitor Analysis and Storyboard Shot Breakdown were translated too.

Skill names, paths, CLI arguments, schema keys, technical identifiers, numeric limits, authorization boundaries and completion states remain compatible. The source collection and existing discovery symlink were reused without copied installations. This pass changed documentation and metadata, not runtime code, app projects, store state or media.

The root maintenance instructions now require English skill instructions/references/metadata for future work. Root and standalone English guides use English language-navigation labels. Chinese guides remain localized user documentation. English instructions do not override the user's requested deliverable language.

## Preserved language-specific material

- Chinese `README.zh-CN.md` guides remain available and aligned with the English entrypoints.
- Multilingual UI resources, locale fixtures, source-language evidence and legal notices retain their original language.
- The prototype references retain two explicitly labeled Traditional Chinese examples: OCR sample text and a `zh-Hant` layer-text value. These are sample data, not untranslated instruction prose.
- The original-language FCML reference corpus, source identities/hashes and legacy `template_zh`/variable-binding protocol remain unchanged. Its SHA-256 still equals `f6eac20883f96b22bdfa3cf1f633a473269b4bc06624a01a778e95cfe9c7e3e8`; it contains 117 source records and 115 canonical mechanisms. English instructions explain this boundary and how to describe retrieved mechanisms faithfully without renaming machine keys or claiming an English dataset.
- AI Storyboard Director's upstream record now identifies the local English adaptation and distinguishes historical source hashes from current translated bytes. Licenses and attribution remain preserved.

## Verification

| Check | Observed result |
| --- | --- |
| Instruction/metadata language audit | No CJK instruction prose; only the two labeled prototype examples in the 94 reviewed files |
| Skill Creator validation | Seven skills PASS |
| Collection metadata, standalone packaging, Markdown links/anchors | PASS after repairing translated heading links |
| Actual Codex app-server `skills/list`, `forceReload:true` | Seven enabled canonical entries, all descriptions English, no duplicates/errors |
| Discovery link | Target/inode/mtime unchanged |
| Root Python unit suite | 230 PASS |
| Publication helper/doctor suite | 28 PASS |
| Prototype Python suite | 83 PASS |
| Director and shot-breakdown doctor failure fixtures | PASS |
| FCML structure/mapping validation | PASS; source corpus and helper bytes retained |
| `git diff --check` | PASS |

A CJK scan supports the language inventory; it does not prove translation quality by itself. Author review preserved stage routing, numerical limits and evidence qualifiers. A separate agent reviewed the English publication skill with native-Swift TF and listing-only scenarios. Its offline helper proposed `1.3.0 (211)`; the scenario used the native adapter and stopped at the exact Apple receipt without refreshing the build list. Listing-only reasoning preserved protected metadata, separate allowlists and the complete screenshot matrix without rebuilding or submitting review. The review found one ambiguous phrase, corrected from “Fix app/version identity” to “Pin the app/version identity.” This was an independent reasoning/fixture check, not a live store test. The translator also performed a separate author consistency check, which is not counted as independent.

Machine-local audit hashes, discovery results, unit logs and synthetic scenario evidence are retained under ignored `.test-output/english-skills-20261026/`.

This instruction-only pass did not rerun visual browser suites or certify new native/media execution. The existing whole-collection image-framing failure remains documented in the [publication validation record](app-publish-skill-validation-2026-10-26.md); it was not changed to make translation checks pass. Nothing was committed, pushed, published or uploaded.
