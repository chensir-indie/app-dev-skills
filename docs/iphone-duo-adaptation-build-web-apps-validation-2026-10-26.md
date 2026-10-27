# BUILD WEB APPS integration and English revision: 2026-10-26

The synthetic fixture passed its browser evaluation after repairs to the output and a correction to the implementation process. Native-device and assistive-technology acceptance remain unverified. The full collection check still failed on an unrelated browser test.

## Change and scope

The user requested BUILD WEB APPS as the preferred workflow for the HTML stage, English skill documentation, and an end-to-end evaluation of the running output. The default sequence is to analyze the whole app's layout, recommend adaptations, then build a complete HTML prototype. The existing SwiftUI, UIKit, Flutter, React Native/Expo, and WKWebView-shell contracts remain available. Requests for less work still stop at the specified stage.

The [Skill](../skills/iphone-duo-adaptation/SKILL.md), invocation metadata, references, catalog/example prose, and generated rule Markdown are now English. The legacy standalone README path remains as an English compatibility pointer. This language change does not impose a new language on an existing product's localized UI. Collection-level bilingual documents retain their other responsibilities.

The revision preserved all 65 previous rule IDs, kinds, phases, source-ID mappings, source URLs and individual source-check dates. It added `WORKFLOW-BUILDER-001` and the local `SKILL-BUILDER-CONTRACT` source, bringing the catalog to 66 rules and 40 sources. Of those rules, 21 apply only to native work. The collection ledger retained its bindings, statuses, targets and evidence while the prose and snapshot were updated. Each target app still needs its own applicability review and acceptance checks.

## Preferred builder and execution mode

The [official OpenAI use case](https://learn.chatgpt.com/use-cases/idea-to-proof-of-concept) points to [openai/plugins BUILD WEB APPS](https://github.com/openai/plugins/tree/main/plugins/build-web-apps). The selected public package was v0.1.2 at commit `0722921d5542fc593105c27bd52630babd8b8c2a`.

| Actual upstream entrypoint | SHA-256 |
| --- | --- |
| `skills/frontend-app-builder/SKILL.md` | `9273de02827b29534be28fb2b37154c1571ac38b4e20d3ef5482b7e22af67394` |
| `skills/frontend-testing-debugging/SKILL.md` | `03724620cf7e7de425b607a5492f572d867b1cf5d9c92c74bf50d057d7415e0b` |
| `.codex-plugin/plugin.json` | `7bc0085538adf72c31b5c2b42410fe699e6fe15e382fdc309cfd973c4c5db9a0` |

Local and session discovery found no installed or loaded BUILD WEB APPS package, and plugin search did not return it. The run used its instruction skills from a read-only checkout of the public source. It did not install a package, create a maintained copy, open an account or set up hosting. Sites was not used as a substitute.

The [handoff contract](../skills/iphone-duo-adaptation/references/build-web-apps.md) selects these instructions and records their identity and execution mode. It passes the completed baseline, recommendations, design and rules to the builder, and keeps the output local and editable. It also retains the builder's Image Gen design-first requirement and exceptions, token and component extraction, browser tasks, direct review of the design and final images, copy comparison, and a record of mismatches. Payment, storage, framework and hosting capabilities are used only when needed. If the builder is unavailable, the report must name the fallback actually used.

## Evaluation design and isolation

The synthetic Pocket Notes fixture contains Notes, Detail, Edit/New, Search, Settings and Delete confirmation, with blue branding and two original notes. Its manifests describe a Capacitor/WKWebView shell, but the runnable input is HTML; no native app was compiled or toolchain verified. The fixture contains no real IMX content, customer data or product-device captures.

Before the generating agent started, the supervising agent froze the input and candidate skill hashes and an independent acceptance checklist covering pages, tasks, process and fault detection. The request supplied neither an implementation nor an expected layout. Outputs were kept outside the collection and product repositories. The run performed no installations, account actions or publication. It inherited the model configuration without a model or reasoning override; the evaluator interface did not expose a verified exact model identifier.

The first attempt consulted workflow memory during baseline work. It was interrupted before prototype construction and archived, so it did not count as a complete isolated run. A new agent with no inherited chat received only the raw fixture, current skill, upstream contracts and available tools. Memory, prior outputs and the supervising agent's review directory were excluded.

A research child agent from the discarded attempt later wrote three advisory files to the reused workspace path. Those files were quarantined. The new generator reported seeing only their filenames, without opening or using their contents. It had independently fetched primary-source texts, which were retained. The discarded attempt and the isolation audit are both recorded.

The isolated run captured 24 screenshots of the original layout and documented the baseline, recommendations and coverage. It generated concepts for the main expanded view, narrow list and editor. One concept changed the required heading from “All Notes” to “Notes”; the generator rejected it and produced a replacement before coding. The design handoff and accepted concept hashes were frozen at 02:44:51 UTC. Prototype files were first created at 02:46:19 UTC. The supervising agent independently recorded the baseline and design artifacts before the prototype HTML existed.

The prototype was also opened in the in-app browser. Its rendered accessibility tree showed selection, editor entry, cancellation, preservation of saved content and return navigation. These observations establish browser/AX behavior; VoiceOver tasks were not tested.

Independent testing found defects before acceptance. Resizing from narrow to wide moved the visible reading location by 2,047 words in a long paragraph. At 390px width, 200% text clipped the Settings destination. The supervising agent also found that the skip link's `#workspace` fragment collided with hash routing and discarded an open edit draft. The generator repaired these defects and added direct regression checks.

A suspected native-dialog Tab-wrap failure also occurred in a minimal Chrome dialog. The test had incorrectly treated neutral document or browser-boundary focus as focus reaching background app controls, so that restriction was removed. The generator separately strengthened modal containment while retaining Escape and close behavior. This was an intentional enhancement; the probe did not establish a Chrome defect. The original failure and probe evidence is retained.

The process audit found that the initial rule bindings and project conventions were filled after preliminary implementation, contrary to the stage-2 handoff requirement. The generator recorded the late completion, attributed all 66 rules and 10 conventions, and froze the completed handoff at 03:01:47 UTC. It then reviewed the preliminary implementation against that handoff and began another construction, rendering and QA iteration. The record preserves the late handoff and the original design freeze; the correction does not erase the earlier process failure.

## Final runtime and output results

Final prototype source was frozen at 03:06:00 UTC. The supervising agent independently verified the initial 80 delivery and evidence file hashes, all 21 candidate skill text files, and all five original input files. A later evidence-only addendum confirmed the existing Playwright 1.64.0 / Node v24.14.0 metadata and expanded the manifest to 84 files. It preserves the original report and manifest without changing the three prototype files or their accepted browser results. No prototype or input drift was found.

| Check | Actual result |
| --- | --- |
| Generating agent's browser suite | 19 grouped checks and 32 main captures passed; supplemental single-paragraph, skip-link, modal, direct-file, rendered-metrics and unobstructed-feedback checks passed |
| Independent browser acceptance | **27/27 passed**, with identical source hashes before/after, matching the final freeze |
| Reading continuity | Independently measured visible word ordinal 2562 → 2557 → 2562 on narrow → wide → narrow; the small difference is line wrapping, replacing the earlier 2,047-word jump |
| Large text | At 390px and 200% root text, the Settings control fits within x=12…378; 320px, expanded and low-height combinations also passed |
| Skip-link regression | Editor route and both unsaved values remain intact; focus moves into main content. The supervising agent also verified keyboard activation in the in-app browser after reloading the final source |
| Rule ledger | Completion check passed: 66 general rules and 10 project conventions; 32 general rules verified for their declared browser scope, 15 native-only deferred, 19 inapplicable, and all 10 project conventions verified |
| Resource and input integrity | No relevant console errors or failed resources; original fixture unchanged; browser source hashes stable |
| Fault detection | Four actual-ledger faults rejected: missing binding, changed standard snapshot, pending adopted convention, missing evidence. Clean/restored controls passed. Dead Save and missing stylesheet faults were also detected without changing delivered source |
| Visual review | The generator, independent reviewer and supervising agent inspected accepted concepts and final captures. They compared copy, hierarchy, palette, typography, geometry, component states, navigation, editor, large text, low height and overlays |

The independently inspected screenshots use the final source. One supplemental modal image was captured before the page settled, using a full-page capture with stale dimensions. It was replaced with a verified 1000×430 viewport capture and records of the image dimensions and DOM geometry. The original image had already been overwritten before preservation was requested, so a labeled replay records the stale extent. The live DOM contained one dialog with correct viewport geometry; the issue was classified as a capture error.

| Delivered file | SHA-256 |
| --- | --- |
| `prototype/index.html` | `3f78f0b745297abedeec0358c60ed1248166acd534880b9cb53b28726047ecd0` |
| `prototype/styles.css` | `ffc598a2a4b080fc0c812bbdaf3b4e1022e5e820454dbf117afdd9799bdd01b5` |
| `prototype/app.js` | `9c0c924190d7e249bacd63668fefbeb9f4fdfb1fc96e5a3b7ecf6ad95d0549e1` |

The local evaluation bundle retains the raw fixture inputs, accepted and rejected concepts, baseline, recommendations, design documents and amendments. It also contains the original and completed handoff snapshots, final rule ledger, runnable HTML/CSS/JS, author checks, independent browser scripts, results and screenshots, fault cases, and provenance. The [evidence manifest](iphone-duo-adaptation/build-web-apps-validation-evidence-2026-10-26.json) records artifact paths and hashes from that evaluation. Later wording edits to this report are outside those hashes. Open `workspace/prototype/index.html` directly; the local preview tab is also retained. No build or installation is required.

## Completed collection and routing checks

- Skill Creator validation and collection metadata/local-documentation checks passed.
- English migration checks passed for all packaged text and generated workspace-rule files. No CJK text remains there; historical validation records are not rewritten as new results.
- **37 focused tests passed**. A renderer regression first failed with the old-language output, then passed after English rendering was implemented. Validation semantics remained unchanged.
- Actual Codex app-server `skills/list` with force reload found the current six collection Skills enabled exactly once from canonical source paths, without discovery errors. The Duo description includes BUILD WEB APPS; the existing collection discovery link remains intact.
- A separate fresh analysis/advice-only React Native scenario covered all four supplied screens, separated reported facts from unmeasured behavior, retained brand and navigation, checked current primary sources, and respected no-write/no-prototype/no-install boundaries. Missing Xcode/browser/builder did not block advice. This is a behavior check, not product runtime acceptance.
- `PLAYWRIGHT_CHANNEL=chrome npm run check` passed doctor/docs and **329 unit checks** (202 root Python, 44 cover Node, 83 prototype Python). Root browser results remain **8/9**: the existing competitor-image assertion at `tests/competitor_html.browser.cjs:69` reports portrait-card bottom `-95.96875px` at a 1000px screen. This failure was previously reproduced without Duo changes; no competitor renderer/test was modified here. The full collection check is still failed.
- The blocked downstream command was run separately: **13/13 cover browser tests and prototype DOM checks passed** in Chrome 155.0.8059.86.

## Evidence boundaries

This isolated run verifies the fixture in the tested environment. General model reliability, a real IMX adaptation, native Duo bars, regions, keyboard and bridges, and physical-device behavior remain unverified. VoiceOver and Full Keyboard Access also need their own task tests; keyboard and DOM checks do not establish those results.

No product-source change, release, staging, commit or push was performed. The evidence manifest binds the updated Skill, collection rule ledger, command results, and external local evaluation artifacts without embedding private product paths or input data in this repository.
