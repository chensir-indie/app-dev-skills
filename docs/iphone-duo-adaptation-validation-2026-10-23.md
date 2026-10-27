# iPhone Duo adaptation validation: 2026-10-23

The packaging and scenarios below describe the first revision. Later sections record the change to a layout-first workflow and HTML delivery. Earlier audit and implementation checks retain their original scope; they provide no evidence for that later HTML output.

## Scope and provenance

This revision added [iphone-duo-adaptation](../skills/iphone-duo-adaptation/SKILL.md) to the canonical `skills/` collection. The draft named in the request was unavailable at the external home-directory path on this machine, so the package was built from the supplied scope and newly checked official sources. No product app, release workflow or discovery symlink changed. Unrelated working-tree changes were preserved, and nothing was committed or pushed.

In this first revision, the skill started from a Flutter app's layout and state implementation and delivered an audit, a plan, or an authorized adaptation with runtime evidence. Visual reconstruction remained a separate workflow starting from an approved reference. The addition required no new Node/Python dependency or npm workspace. Its standalone shell preflight did not certify an iOS toolchain.

Apple source checks:

- [Prepare](https://developer.apple.com/iphone-duo/prepare/), [Duo HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) and [Raise the bar](https://developer.apple.com/videos/play/tech-talks/111462/) were read on the date above. The HIG Markdown representation was retrieved when the web reader rejected its content type.
- Local `xcodebuild -version`: Xcode **27.1**, build **27A9275**. Export help and an export to a new temporary directory succeeded; ten Skill folders included `app-resizability`.
- The exported `app-resizability/SKILL.md` was read with SHA-256 `c4ec32340d4a20c7af97784dc0128f517ea3e7922da087b2c32cf0758e4f6472`. Its native Swift/Objective-C scope is separate from this original Flutter workflow. No Apple Skill text was vendored or relicensed.
- Flutter's [displayFeatures contract](https://api.flutter.dev/flutter/widgets/MediaQueryData/displayFeatures.html) was checked: the documented list is populated only on Android. The package requires target-version evidence before claiming iOS reserved-region handling. No Flutter/iOS bridge or product adaptation was exercised.

## Packaging and discovery

| Check | Result and limits |
| --- | --- |
| Skill Creator `quick_validate.py skills/iphone-duo-adaptation` | Passed: structure, frontmatter and scaffold check |
| `python3 scripts/check_collection.py` | Passed: metadata, standalone packaging, root entries and local links |
| Targeted doctor | Passed with no toolchain; reports its instruction-only scope |
| New preflight regression fixtures | 2 passed: standalone execution with an empty PATH and rejection of an unsupported argument |
| Catalog | Four entries discovered dynamically; no cached list added |
| Actual Codex app-server `skills/list` | `forceReload: true`; all four collection skills enabled, one entry each, canonical source paths, no discovery errors |
| `git diff --check` | Passed |

Discovery used a temporary stdio app-server with `initialize`, then `skills/list` for this checkout. The existing collection symlink remained intact. Standalone installation links to the same source and preserves earlier edits; no second maintained installation was created.

## Independent agent checks

Three agents started without inherited chat history. Each received the candidate skill path, a realistic task and read-only repository access. They worked from supplied snippets or briefs without changing a product. The requests did not reveal the intended answer. These runs tested agent behavior; they did not run an app.

| Scenario | Actual behavior | Judgment and limits |
| --- | --- | --- |
| Existing Flutter audit only: cached startup width, split Scaffold branches, controller creation in build, fixed overlay coordinates, empty displayFeatures, assumed automatic AppBar conversion; no Duo targets | Read references, checked official APIs, identified sizing/controller/region/navigation risks, preserved the no-edit endpoint, supplied prioritized checks and identified missing target source/line numbers | Appropriate scoped audit. Also investigated View.of dependency in initState; no product tests or patches claimed |
| One-page camera plan only, Linux/no Xcode or Apple export/devices, professional-mode orientation constraint and no universal two-column layout | Produced a reviewable plan without installing tools or editing files. Retained product constraints, kept gallery structure optional, separated generic, simulator and hardware checks, marked runtime results pending | Missing capabilities did not block planning; hypothetical environment was not presented as measured product evidence |
| Pure Objective-C single-view defect; one file, no scene/plist migration | Rejected the Flutter Skill as the active route, proposed current view bounds in layoutSubviews, kept scope narrow and described unexecuted checks | Correct wrong-skill routing and scope preservation; no native file supplied or modified |

The review checked whether each agent chose the right workflow, avoided unintended edits, respected product decisions, and supported its platform and completion claims. All three stayed within the supplied request. These results do not establish general model reliability or completion of an app's Duo adaptation.

## Collection checks and unrelated failure

Ran `PLAYWRIGHT_CHANNEL=chrome npm run check` using installed Chrome **155.0.8059.86**. Default Chromium headless-shell was unavailable; the documented installed-Chrome option required no download or browser configuration change.

- Doctor and documentation checks passed.
- **294 unit checks passed**: 167 root Python, 44 cover-tool Node, 83 prototype Python tests.
- Root competitor browser suite: **8/9 passed**. `index image windows preserve full portrait, landscape and square framing at each layout` failed at a 1000px screen viewport: the portrait fixture bottom was `-95.96875px` outside the card content bounds.
- The same failure reproduced in an isolated temporary directory containing only the existing competitor skill and browser test, with existing npm dependencies linked. It contained no Duo skill or changed collection documents. The competitor renderer/test were not modified.
- The root browser failure stopped the npm chain. Separately ran `PLAYWRIGHT_CHANNEL=chrome npm run test:browser --workspaces`: **13/13 cover browser tests and prototype DOM checks passed**.

The full collection `npm run check` failed on a reproducible competitor-image layout issue outside this addition's scope. The new skill's packaging, discovery and behavior checks passed. Physical-device acceptance, store upload and release were not verified.

## Layout-first revision after user clarification

The user clarified the intended workflow: analyze the current app's overall layout, recommend adaptations based on official iPhone guidance, then deliver a complete HTML prototype that meets the quality requirements. That became the default sequence. An explicit request for analysis or advice can still stop earlier. Flutter implementation and native or device acceptance require later requests; they neither replace nor block HTML delivery.

This revision updated the entrypoint, description, default prompt, standalone READMEs, scope, collection READMEs, workflows, runtime guidance and doctor wording. It added self-contained requirements for [layout analysis](../skills/iphone-duo-adaptation/references/layout-analysis.md) and the [HTML prototype](../skills/iphone-duo-adaptation/references/html-prototype.md). Validation separates browser and visual acceptance from optional native implementation checks. Apple guidance on layout, tabs, toolbars, typography, accessibility and Duo was rechecked on the date above, with official rules distinguished from product choices.

Checks for this revision:

- Skill Creator validation, collection documentation/local links, the two standalone preflight tests and `git diff --check` passed.
- Actual Codex `skills/list` with force reload returned four enabled collection skills once each from canonical sources. The discovered Duo description included both whole-app analysis and final HTML delivery.
- Re-ran `PLAYWRIGHT_CHANNEL=chrome npm run check`: doctor/docs and the same 294 unit checks passed; root browser suite remained 8/9 with the same unrelated portrait-card `-95.96875px` failure. No unrelated renderer or test was modified.
- An independent reader reviewed the updated entrypoint, references and bilingual documentation for early-stop branches or conflicting completion criteria; no substantive contradiction was found.
- An independent forward run received an explicit analysis/advice-only request describing five camera-app screens, with Linux and no Xcode/browser. It covered all five, retained the professional-camera orientation exception, avoided universal two-column design, cited current Apple sources and reported unexecuted checks. It did not write HTML, change code, install tools or claim runtime acceptance. This validates the narrow-endpoint and missing-capability branches, not the default HTML result.

An independent run also exercised the default workflow using an original synthetic five-page notes-app snapshot with a deletion-confirmation layer. The evaluator captured every current layout, analyzed the whole app, and recorded decisions with their sources. It then produced editable HTML/CSS/JS for Notes, Detail, Edit/New, Search, Settings and confirmation. Twelve browser task groups passed in Chrome 155.0.8059.86, with zero console exceptions or failed resources and 47 screenshots (8 current, 39 prototype). The supervising agent inspected the final wide, narrow and enlarged-text evidence. The input hash stayed unchanged. This run verified the synthetic prototype before the workspace-rule addition below; it did not verify a product or native device.

## Recording the full rule catalog in the workspace

The user then asked for every rule, specification and recommendation in official-basis.md to be recorded in a consistent format and applied in the workspace. All of its original content was moved into [one canonical catalog](../skills/iphone-duo-adaptation/assets/official-rules.json). The original document points to that catalog and the workspace contract, removing the need to maintain a second prose rule set.

- The catalog contained 53 rules and 18 source records. It retained all original 47 IDs and split six rules to separate design and evidence requirements from native checks. Eighteen rules apply only to explicitly requested native implementation or acceptance. HTML tasks retain those records with reasons for deferral, without requiring Xcode or inventing native verification.
- This checkout's [Markdown rules](iphone-duo-adaptation/workspace-rules.md) and [JSON ledger](iphone-duo-adaptation/workspace-rules.json) were generated, with a conditional pointer added to AGENTS.md. The structural check passed with 35 pending and 18 native-deferred bindings. The checkout maintains skills and contains no target app, so this result does not establish implementation on app pages.
- The standalone helper uses the Python 3.9+ standard library and supports init, render, check and a stricter completion mode. It checks full catalog coverage, unchanged snapshot identity, project statuses, actual relative targets and evidence, Markdown synchronization, and workspace boundaries. Init preserves existing outputs; render preserves JSON annotations. Missing, older or unsupported runtimes produce explicit diagnostics.
- All 24 focused tests passed. They cover bundled-catalog compatibility, omitted, duplicate or unknown rule IDs, edited or stale standards, stale Markdown, missing evidence, path and symlink escapes, overwrite prevention, interrupted pair creation, and standalone installation.
- Re-ran the full collection check: doctor/docs and **316 unit checks passed** (189 root Python, 44 Node, 83 prototype Python). The same existing competitor browser image-card failure remains, with 8/9 root browser tests passing. No unrelated renderer or browser fixture was changed.

The helper checks whether records are complete and consistent. HIG compliance, visual quality and native support need separate review. Before a target app passes completion checks, every applicable rule must point to that app's design, HTML and actual evidence.

## Six-point supplement and project-convention separation

The user accepted six additions from the IMX rule review and asked to include them in both the skill and workspace rules. The workflow still moves from whole-app layout analysis to adaptation recommendations and a complete HTML prototype. This revision changed the skill and rule tools without adapting or running the IMX app.

| Accepted point | Reusable rule and contract | Project boundary |
| --- | --- | --- |
| Complete layout baseline | WORKFLOW-BASELINE-001; page relationships, navigation hierarchy, fixed/scroll regions, shared components, narrow/wide/low-height evidence | IMX chat scope is explicit; inventorying global relationships does not authorize redesigning Calendar or Apps |
| Complete interactive HTML gate | WORKFLOW-HTML-001; default three-stage endpoint, actual browser tasks and visual review | An explicit rules-only, analysis-only or advice-only request retains its endpoint; native investigation can proceed independently |
| Rich content geometry | CONTENT-LAYOUT-001; real pane width, wrapping/local scrolling, media ratios, async loading/pagination and semantic reading anchors | Confirm the app's actual content types; retain IMX Markdown, unread and follow-bottom semantics rather than inventing features |
| Region data contract | REGION-MODEL-001 and native-only NATIVE-REGION-001; kind/id/frame/isActive, owner coordinates, units and update/clear timing | Bridge fields are an engineering contract; Apple frame already includes margins and Flutter's Android-only displayFeatures population does not establish iOS behavior. HTML assumptions and actual bridge results remain separate |
| Accessible tasks | HIG-ACCESSIBILITY-001/004/005; main tasks, hidden-target fallback, modal return and Reduce Motion | Separate text/IME, keyboard-navigation and assistive-reading focus. IMX select/read/edit/send/close tasks retain its permissions, send conditions and draft ownership |
| Traceable evidence and build identity | WORKFLOW-TRACEABILITY-001 and native-only NATIVE-VALIDATION-001; per-rule evidence, source/artifact identity, production-navigation integration and affected Profile/Release paths | HTML, fixtures, Skill-maintenance checks and actual native/account acceptance are separate evidence scopes |

The catalog grew to 60 rules and 27 source records, retaining all previous 53 IDs and adding seven. Twenty rules apply only to native work. Apple and Flutter primary sources were checked for region behavior and build and test requirements. The `SKILL-*` source records identify local collection requirements separately from Apple's. Source-relative paths resolve from the catalog's `assets/` directory.

At that revision, the [project-convention contract](../skills/iphone-duo-adaptation/references/project-conventions.md) and six-point IMX example were self-contained. The project-specific fixture was later removed from the distributed skill; generic tests now cover explicit adoption. IMX examples start pending and are adopted only for the relevant project or when the user explicitly chooses them. Init does not import them.

This checkout's generated ledger retained 40 pending and 20 native-deferred general bindings, plus one separately verified collection-maintenance scope convention. That convention verifies the rule update and its scope only. It does not establish app, HTML or native acceptance. Catalog reconciliation preserved every existing binding and top-level workspace annotation. With no target app in this checkout, overall completion remains unverified.

The helper validates and renders optional `project_conventions` separately. It checks provenance, unique PROJECT- IDs and valid general-parent IDs, then applies the same status, path, evidence and completion requirements as for general rules. Old ledgers without the array remain compatible. Failure fixtures first exposed the unsupported project records with 84 failing subcases and one error. After implementation, 36 focused tests passed, including explicit adoption of the bundled IMX example and init's refusal to import it automatically.

Final checks on this revision:

- Targeted doctor, Skill Creator validator, collection metadata/documentation/local-link checks and `git diff --check` passed.
- Ledger render/check passed with 60 general rules and one collection convention; generated Markdown matches JSON. The helper checks structural traceability, not evidence semantics or HIG/visual/native quality.
- Actual Codex app-server `skills/list` with force reload returned all four collection skills enabled once each from their canonical sources, with no discovery errors. The existing collection link was retained.
- Independent read-only review confirmed the three-stage endpoint, general/project separation, non-blocking native boundary and project-validator gates. It identified the missing distinction between the three focus types; the catalog and implementation/validation contracts were corrected before final checks.
- `PLAYWRIGHT_CHANNEL=chrome npm run check` passed doctor/docs and **328 unit checks** (201 root Python, 44 cover Node, 83 prototype Python). Root browser tests remain **8/9**, failing the same existing `tests/competitor_html.browser.cjs:69` portrait-card assertion at a 1000px screen (`-95.96875px`). The existing unrelated failure still prevents the full npm chain from passing; no competitor renderer or browser fixture was modified in this supplement.

This rules-maintenance task did not request new product HTML. The earlier synthetic HTML results still describe that run; they were not rerun and do not establish current IMX acceptance. No product source, account, release, staging, commit or push action was performed. The [revision evidence manifest](iphone-duo-adaptation/six-point-validation-evidence-2026-10-23.json) identifies the files checked for the six-point revision on 2026-10-23. It excludes itself and this narrative to avoid a circular hash. Later edits are outside that manifest.

## Framework routing revision: 2026-10-26

The skill identifies the UI framework before choosing its implementation requirements. SwiftUI, UIKit, Flutter, React Native/Expo, and WKWebView shells (Capacitor, Cordova, Ionic, uni-app, Taro) have separate references and catalog rules. It also recognizes Compose Multiplatform, .NET MAUI, and Unity to avoid applying another framework's APIs to them. The default workflow still delivers whole-app layout analysis, recommendations linked to HIG, and a complete HTML prototype. The scenarios below were reviewed against the written instructions; no live model or product adaptation was run for this section.

| Scenario | Expected behavior | Instruction |
| --- | --- | --- |
| Existing SwiftUI or UIKit app, including an Objective-C UIKit screen | Use this skill and the Apple framework contract. HTML remains the default endpoint. A later source migration also uses the exported App Resizability skill when that export is available. | `SKILL.md` framework table; `references/apple-frameworks.md`; `FRAMEWORK-APPLE-001` |
| Existing Flutter app | Use the Flutter contract. Other framework rules are not applicable because the UI framework is Flutter. | `references/flutter-adaptation.md`; Flutter rules whose `applies_when` names Flutter |
| Existing React Native or Expo app | Use the React Native contract. Do not require Flutter `integration_test` or claim an iOS reserved-region API. | `references/react-native.md`; `FRAMEWORK-RN-001`; `FRAMEWORK-IMPL-001` |
| uni-app, Taro, Capacitor, Cordova, Ionic, or another WKWebView page | Use the WebView contract. Keep page CSS insets and native shell insets separate. | `references/webview-shells.md`; `FRAMEWORK-WEB-001` |
| Unity, .NET MAUI, or Compose Multiplatform UI | Identify the engine, continue HIG analysis and HTML, and do not transplant SwiftUI, Flutter, or React Native APIs. Product code waits until that engine's layout API is identified. | `references/frameworks.md`; `FRAMEWORK-ROUTE-001` |
| Explicit analysis or advice only | Stop at the requested stage and do not write the HTML prototype. | `SKILL.md` completion exception |
| No Xcode, simulator, or framework toolchain | Continue layout analysis and HTML. Keep native and framework-runtime checks pending. | `references/validation.md`; `WORKFLOW-EXPORT-004` |

The earlier Objective-C routing check rejected this skill because its scope was Flutter only. That result belongs to the 2026-10-23 run. The current instructions include UIKit. No contradiction was found between the HTML default and the framework-specific product gates: Flutter integration coverage applies only after the UI framework is Flutter and the user asks for product implementation.
