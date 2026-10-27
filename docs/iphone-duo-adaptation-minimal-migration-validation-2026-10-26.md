# Original-design Duo migration revision: 2026-10-26

This revision adds review of multiple iPhone Duo forms while requiring the smallest necessary changes to the original app. The workflow still starts with whole-app layout analysis, continues with adaptation recommendations, and ends with a complete HTML prototype. The [earlier BUILD WEB APPS evaluation](iphone-duo-adaptation-build-web-apps-validation-2026-10-26.md) has its own output, hashes and results. Those records remain evidence of the earlier revision.

## Maintained contract

Use the original app's screenshots, source, design tokens, components, copy and working navigation as the design reference. The [migration-review contract](../skills/iphone-duo-adaptation/references/migration-review.md) requires a record of what is retained, adapted or changed, with a reason for each change. Reviews must name the environments, preserve app state between them, and compare the original and adapted app at the same page, state and viewport. A wider display alone does not justify new columns, icons, features or a new visual style.

The catalog contains 68 rules and 42 sources. It retains the previous 66 IDs and adds `WORKFLOW-MINIMAL-001` and `WORKFLOW-POSES-001` as reusable workflow rules. Product tokens, optional columns, review dimensions, geometry assumptions and permitted changes remain project conventions with their own attribution. The collection ledger preserves previous decisions and historical conventions. Recording general rules in this skill-maintenance checkout does not establish that a product app implements them.

The [BUILD WEB APPS handoff](../skills/iphone-duo-adaptation/references/build-web-apps.md) selects `frontend-testing-debugging` to refine the existing design. The official upstream package is v0.1.2 at commit `0722921d5542fc593105c27bd52630babd8b8c2a`; its entrypoint SHA-256 is `03724620cf7e7de425b607a5492f572d867b1cf5d9c92c74bf50d057d7415e0b`. The run followed those upstream instructions without installing the plugin. Because the Browser plugin/skill was absent, it used the contract's regular Playwright route with installed Chrome. The in-app browser supported additional manual review. This refinement required no new concept, Image Gen run, dependency installation, account or deployment.

## Fixture and stage order

The reference is the supplied Pocket Notes synthetic HTML fixture. Its metadata declares a Capacitor/WKWebView shell, but it contains no compiled native host, real IMX capture or customer data. The revision reuses behavior from the previous generated prototype and takes its design from the original UI. This was a guided follow-up with a fresh independent evaluator; it did not test generation from scratch in isolation.

The author captured seven canonical states in ten contexts: Notes, Detail, New, Edit, Search, Settings and Delete confirmation. The analysis covers navigation, shared components, scrolling, fixed regions, original tokens and tasks. The recommendation handoff preserves the original single-page stack by default, gray canvas, white cards, 17px body, 28px headings, 12px cards, 8px controls, text labels, header Back, below-body Edit/Delete, inline Save/Cancel, case-sensitive search and Back/Cancel-to-Notes behavior.

The completed handoff snapshot was frozen at 04:05:12 UTC, before implementation. It contains decisions and targets for all 68 rules, seven project conventions, original and design references, and the pose matrix. The fresh evaluator observed it independently at 04:05:28 UTC, while the prototype directory was still absent, and verified all 16 snapshot hashes. First implementation was recorded at 04:06:33 UTC. The earlier planning-only snapshot remains an interim record and is excluded from evidence that the handoff requirement was met. Verification was still pending at that point.

A post-build amendment records the construction changes: restoration of the original action spacing and normal paragraph whitespace, and a repair to reading-anchor recapture after resizing. It also documents repairs to stable-ID saving, safe text insertion, keyboard card activation, skip-link routing, modal ownership and the intended density-setting behavior. Target-height and primary-color contrast corrections have measured before-and-after differences. Asynchronous hash-route assertion races and an overly strict one-word reading criterion were test-harness issues, recorded separately from product defects.

After the first candidate passed its tests, the supervising agent's final source review found a behavior that differed from the original: untouched Search showed all notes, while the original left results blank until the first input. A new independent regression reproduced 11 failures out of 15 assertions before repair; typing, clearing and returning already passed. The author restored the initial blank Search and the original blank empty-Notes view, recorded a second amendment, retained the first candidate's evidence and froze the corrected source.

## Named forms and output

The local review at `workspace/index.html` contains one persistent iframe for the adapted app, controls outside it for poses and stress tests, schematic form diagrams, live dimensions, state-continuity status, and 70 pairs of original and adapted captures. The comparison selector uses independent canonical captures without resetting the live draft. Pose changes resize the iframe viewport. Optional magnification to fit the review area is labeled separately and can be disabled.

The nine Duo contexts are outer upright/rotated, inner portrait/landscape, two-app current-app-left/right, and partial book/tabletop/standing. A tenth context retains the original phone baseline. They reuse the original component family; optional list/detail expansion is off by default. Keyboard obstruction and large text remain separate stress states.

The review checked form contexts and control placement against [Design for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111466/), [Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462/), [Duo HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) and [Prepare](https://developer.apple.com/iphone-duo/prepare/). Numeric canvas sizes and optional region rectangles are assumptions for this project's review, not official hardware specifications. Partial-fold contexts start without a region. The optional region model records ownership, units and provenance, and can be moved, deactivated or removed. The standing display and orientation are explicit review choices.

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
| Supervising agent's manual browser review | Original hierarchy and actions inspected; unsaved title/body survived inner → outer → left split → tabletop with the same instance ID. Final frozen revision was reloaded and inspected again |
| Original/adapted visual evidence | 70 pairs at matching viewport/state; independent original captures and final rendered captures retained. Copy, palette, type, geometry, actions, cards, navigation and stress states received visual review in addition to the automated checks |
| Focused Skill tests | 37 passed; collection documentation, Skill Creator validation, English scan and canonical discovery passed |
| Actual Codex discovery | Six current collection Skills enabled exactly once at canonical source paths, no errors; discovery link intact |
| Routing desk review | Unrelated website, whole-app minimal migration, explicit advice-only/no-write, and missing-capability branches reviewed against exact instruction links; no blocking text conflict. This is not another live model trial |
| Target-fixture ledger | Completion check passed: 38 general rules and seven conventions verified for their declared prototype scope, 15 native-only rules deferred, 15 framework-specific rules inapplicable |

The 347 independent browser assertions count individual checks, not independent scenarios or model success rates. To test reading continuity, the independent test selected one DOM caret character in a scrolled paragraph and measured that character's Range position through five named changes and five uncontrolled iframe resizes. Displacement stayed within 1 CSS px. Earlier attempts sampled a new first-visible word or caret after each rewrap, which compared different characters; those attempts remain recorded separately. VoiceOver and native IME behavior were not verified by these browser checks.

`PLAYWRIGHT_CHANNEL=chrome npm run check` passed doctor/docs and 329 unit checks, but the full command remains **failed**: the existing competitor-image browser test at `tests/competitor_html.browser.cjs:69` reports portrait bottom `-95.96875px` at a 1000px screen (root browser 8/9). No competitor renderer or test was changed. Downstream checks run separately passed 13/13 cover browser tests and the layered-prototype DOM checks. An initial downstream attempt without the Chrome channel found no bundled headless browser; rerunning with installed Chrome required no installation.

## Delivery and limits

The local evaluation bundle retains the runnable review and editable app, raw fixture inputs, completed handoff snapshot from before coding, amendments, rule ledger and frozen source versions. It also includes original and final captures, independent scripts and results, the negative control, and manual review evidence. The [revision evidence manifest](iphone-duo-adaptation/minimal-migration-evidence-2026-10-26.json) records the repository files and relative external artifact identities from that evaluation. Later wording edits to this report are outside those hashes. The local delivery location is supplied in the chat.

This verifies the declared synthetic HTML migration and instruction revision. Native hardware dimensions, automatic system bars, real reserved-region delivery, real keyboard/IME, VoiceOver, physical-device behavior and a real target-product migration remain unverified. No product repository, release, account, staging, commit or push was changed.
