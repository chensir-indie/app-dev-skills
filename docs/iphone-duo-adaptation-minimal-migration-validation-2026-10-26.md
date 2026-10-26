# Original-design Duo migration revision — 2026-10-26

This revision responds to the requirement to show multiple iPhone Duo forms and complete adaptation with the smallest necessary changes to the original application. The workflow remains **whole-app layout analysis → adaptation recommendations → complete HTML prototype**. The [earlier BUILD WEB APPS evaluation](iphone-duo-adaptation-build-web-apps-validation-2026-10-26.md) and its output remain historical evidence; their hashes and results are not substituted for this revision.

## Maintained contract

The original application's screenshots, source, design tokens, components, copy and working navigation are the design authority. The [migration-review contract](../skills/iphone-duo-adaptation/references/migration-review.md) requires a retain/adapt/change record, justified minimal deltas, named environments, one continuing app state, and original/adapted comparisons at the same page, state and viewport. A wider display does not automatically introduce columns, icons, features or a new aesthetic.

The catalog now contains **68 rules and 42 sources**. Its previous 66 IDs are retained; `WORKFLOW-MINIMAL-001` and `WORKFLOW-POSES-001` add reusable workflow policy. Actual product tokens, optional columns, review dimensions, geometry assumptions and permitted changes remain separately attributed project conventions. The collection ledger preserves its previous decisions and historical conventions; general-rule materialization in a Skill-maintenance checkout does not establish implementation in a product app.

The [BUILD WEB APPS handoff](../skills/iphone-duo-adaptation/references/build-web-apps.md) selects the actual existing-design `frontend-testing-debugging` route for this refinement. The selected official upstream package is v0.1.2 at commit `0722921d5542fc593105c27bd52630babd8b8c2a`; its entrypoint SHA-256 is `03724620cf7e7de425b607a5492f572d867b1cf5d9c92c74bf50d057d7415e0b`. This is upstream instruction execution, not an installed plugin. The Browser plugin/skill was absent, so the contract's regular Playwright path used installed Chrome. The available in-app browser provided additional manual review. No new concept, Image Gen run, dependency installation, account or deployment was required by this refinement route.

## Fixture and actual stage order

The supplied original **Pocket Notes synthetic HTML fixture** is the reference. Metadata declares a Capacitor/WKWebView shell; it is not a compiled native host, a real IMX capture or customer data. The previous generated prototype supplied reusable behavior, while the original UI controlled the design. This is a guided follow-up refinement, with a separate fresh independent evaluator, rather than a new isolated cold-start generation trial.

The author captured seven canonical states in ten contexts: Notes, Detail, New, Edit, Search, Settings and Delete confirmation. The analysis covers navigation, shared components, scrolling, fixed regions, original tokens and tasks. The recommendation handoff preserves the original single-page stack by default, gray canvas, white cards, 17px body, 28px headings, 12px cards, 8px controls, text labels, header Back, below-body Edit/Delete, inline Save/Cancel, case-sensitive search and Back/Cancel-to-Notes behavior.

The populated pre-implementation snapshot was frozen at **04:05:12 UTC**. It contains all 68 rule decisions/targets, seven project conventions, original/design references and the pose matrix. The fresh evaluator independently observed it at **04:05:28 UTC**, while the prototype directory was still absent, and verified all 16 snapshot hashes. First implementation was recorded at **04:06:33 UTC**. The earlier planning-only snapshot is explicitly retained as interim history, not counted as the actual gate. Verification correctly remained pending before implementation.

Changes during construction are recorded in an honest post-build amendment: original action spacing and normal paragraph whitespace were restored; a reading-anchor recapture after real resizing was repaired. Stable-ID saving, safe text insertion, keyboard card activation, skip-link routing, modal ownership and the stated density-setting intent are documented repairs. Measured target-height and primary-color contrast corrections are explicit deltas. Asynchronous hash-route assertion races and an overly strict one-word reading criterion were harness issues, retained separately from product defects.

The parent's final source review found another real preservation defect after the first candidate passed its existing tests: untouched Search showed all notes, while the original left results blank until the first input. A new independent regression reproduced 11 failures out of 15 assertions before repair; typed/cleared/return behavior already passed. The author restored initial blank Search and original blank empty-Notes presentation, recorded a second amendment, retained the first candidate's evidence and created a new source freeze. This illustrates why passing the initial task matrix alone does not establish complete source fidelity.

## Named forms and output

The complete local `workspace/index.html` review contains one persistent adapted App iframe, external pose/stress controls, schematic form diagrams, live dimensions and continuity status, plus 70 original/adapted capture pairs. Its comparison selector uses independent canonical captures and does not reset the live draft. The actual iframe viewport changes; optional fit magnification is separately labeled and can be disabled.

The nine Duo contexts are outer upright/rotated, inner portrait/landscape, two-app current-app-left/right, and partial book/tabletop/standing. A tenth context retains the original phone baseline. They reuse the original component family; optional list/detail expansion is off by default. Keyboard obstruction and large text remain separate stress states.

The qualitative context and control-placement basis was checked against [Design for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111466/), [Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462/), [Duo HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) and [Prepare](https://developer.apple.com/iphone-duo/prepare/). Every numeric canvas size and optional region rectangle is a project review assumption, not an official hardware specification. Partial-fold contexts start without a region; the optional model can be moved, deactivated or removed and records ownership, units and provenance. Standing display/orientation is an explicit review choice.

## Executed checks

The corrected final implementation was frozen at **04:18:59 UTC**, before regenerated final captures and acceptance; the superseded 04:13:06 candidate is retained separately. Browser environment: Playwright 1.64.0, Node v24.14.0, installed Chrome 155.0.8059.86. No browser security flags were weakened.

| Check | Result |
| --- | --- |
| Author acceptance | 20 grouped browser checks; original states, live geometry, CRUD/search, continuity, overlays, 200% text, keyboard/regions, optional hierarchy, intermediate widths/reduced motion and direct-file opening |
| Author source-state regression | 24 checks passed against fresh original/adapted Search and empty-Notes behavior; final gallery and delivery captures regenerated after the correction |
| Independent page/task matrix | 150 assertions passed across ten contexts, including all seven canonical states and original task semantics |
| Independent continuity | 38 assertions passed for one instance, draft/selection, owned dialogs and long-paragraph reading through named and uncontrolled intermediate resizing |
| Independent stress/portability | 71 assertions passed for text/keyboard constraints, off-center active/inactive/removed regions, optional layout, comparison isolation, mobile review and direct `file://` operation |
| Independent source-state regression | 18 assertions passed for original/adapted initial Search, input/clear/return and pose continuity, plus blank empty Notes |
| Independent live gallery | 70 UI checks passed for matching original/adapted image pairs, actual dimensions and isolation from the live draft |
| Negative control | A disposable browser with Save submission disabled failed the create/save visible-result oracle; a clean control passed. Delivered source was unchanged |
| Parent manual browser review | Original hierarchy and actions inspected; unsaved title/body survived inner → outer → left split → tabletop with the same instance ID. Final frozen revision was reloaded and inspected again |
| Original/adapted visual evidence | 70 pairs at matching viewport/state; independent original captures and final rendered captures retained. Copy, palette, type, geometry, actions, cards, navigation and stress states reviewed separately from green assertions |
| Focused Skill tests | 37 passed; collection documentation, Skill Creator validation, English scan and canonical discovery passed |
| Actual Codex discovery | Six current collection Skills enabled exactly once at canonical source paths, no errors; discovery link intact |
| Routing desk review | Unrelated website, whole-app minimal migration, explicit advice-only/no-write, and missing-capability branches reviewed against exact instruction links; no blocking text conflict. This is not another live model trial |
| Target-fixture ledger | Completion check passed: 38 general rules and seven conventions verified for their declared prototype scope, 15 native-only rules deferred, 15 framework-specific rules inapplicable |

The 347 independent browser assertions are not 347 independent scenarios or a model success rate. For long reading, the independent test selected one DOM caret character in a scrolled paragraph and measured that same character's Range position through five named changes and five uncontrolled iframe resizes: displacement stayed within 1 CSS px. Re-sampling a new first-visible word/caret after each rewrap compares different characters; those exploratory oracle attempts remain recorded separately. Browser checks do not certify VoiceOver or native IME behavior.

`PLAYWRIGHT_CHANNEL=chrome npm run check` passed doctor/docs and 329 unit checks, but the full command remains **failed**: the existing competitor-image browser test at `tests/competitor_html.browser.cjs:69` reports portrait bottom `-95.96875px` at a 1000px screen (root browser 8/9). No competitor renderer or test was changed. Downstream checks run separately passed 13/13 cover browser tests and the layered-prototype DOM checks. An initial downstream attempt without the Chrome channel found no bundled headless browser; rerunning with installed Chrome required no installation.

## Delivery and limits

The local evaluation bundle retains the runnable review and editable App, raw fixture inputs, populated pre-code snapshot, amendments, rule ledger, source freezes, original/final captures, independent scripts/results, negative control and manual evidence. The [revision evidence manifest](iphone-duo-adaptation/minimal-migration-evidence-2026-10-26.json) binds repository and relative external artifact identities; the local delivery location is supplied in the chat.

This verifies the declared synthetic HTML migration and instruction revision. Native hardware dimensions, automatic system bars, real reserved-region delivery, real keyboard/IME, VoiceOver, physical-device behavior and a real target-product migration remain unverified. No product repository, release, account, staging, commit or push was changed.
