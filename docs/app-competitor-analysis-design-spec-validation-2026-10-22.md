# Design specification and UX delivery validation — 2026-10-22

The canonical `app-competitor-analysis` Skill now authors one source-linked Design.md per detailed competitor analysis. Its [design contract](../skills/app-competitor-analysis/references/design-specification.md), renderer, HTML reading components, preview server and [authoring outline](../skills/app-competitor-analysis/assets/report-template.md) were changed before reapplying the workflow to the PoseGenius collection.

## Applied result

- 44 individual HTML reports and 44 `design/<id>/Design.md` documents; all 176 original maps and 338 source identities/locators retained.
- 101 inspected regions, 397 enumerated elements (including explicitly identified promotional elements), 96 component/state contracts, and 44 individual UX findings with alternative explanations, decisions and planned validation protocols.
- Nine products lack inspectable application UI pixels: p02, p03, p05, p10, p19, p27, p36, p40 and p41. Their documents export the evidence and acquisition routes without inventing visual specifications. Other images mainly depict selected official promotional states; no claim of app-wide runtime coverage is made.
- The HTML shows a design-document link, region inventory and user task/choice/feedback/recovery priorities. Duplicate UI flow summaries, decorative chapter numbers, repeated platform metadata, generic image instructions and raw always-visible citation strings were removed from the reading layer. Complete original research remains accessible.
- New UI/UX anchors account for the sticky header. Typography uses relative units. No additional client JavaScript was introduced for these panels.

## Actual checks

- 130 focused Skill tests pass, including missing evidence, measured values without method, missing visual category, absent reversal condition, HTML/Markdown inventory agreement, and preview hash/allowlist behavior.
- Collection `npm test` passes: 161 Python collection tests, 44 cover-tool unit tests and 83 layered-prototype tests. These totals include overlapping coverage; they are not additive research evidence.
- Documentation/discovery checks, Skill quick validation and `git diff --check` pass. The discovery link resolves to the canonical collection once.
- Static checks cover all 50 HTML pages, 176 maps, 630 feature nodes, 12,023 internal anchors and the original evidence/map comparison. Design document checks cover 2,049 local Markdown links/anchors and every authored element/component/protocol field.
- CUA Chromium checks cover all 44 products at actual 1280 and 390 CSS-pixel viewports (88 report checks, each with interface and interaction navigation). No horizontal page overflow or visible broken image was found; every report retains its four maps and Design.md link.
- Additional browser checks: document opens as Markdown text, source/back restoration, anchor clearance, keyboard protocol disclosure, 320-pixel layout, 200% text (36px UX body at 390px width), seven printable views, before-print protocol expansion and seven readable views/four maps with scripts disabled. Screenshot review includes image-rich, sparse and dense records.

The collection-wide `doctor` is not green: unrelated browser-dependent skills lack the installed Playwright headless executable. No browser package was installed. Browser review for this task used the permitted CUA browser route; terminal browser suites were not executed. This is not a claim that `npm run check` passed, Safari passed, performance was certified, competitor runtime was tested or participant studies were conducted.

## Reproduction and records

Project-local authored input and application scripts reside under `.test-output/app-competitor-analysis/20261022/design-contract-v3/`; they are not reusable Skill fixtures. Generated delivery resides in the PoseGenius `work/competitor-reports/20261022` collection. See its `verification.md`, `browser-review.json`, `static-verification.json` and `design-verification.json` for content identity and scope. The reusable server is `skills/app-competitor-analysis/scripts/preview_reports.py`; it serves only manifest-listed report HTML, Design.md and hashed assets on loopback.
