---
name: app-store-cover-generator
description: Create editable App Store screenshot covers from a visual reference and real app captures. Use when the user wants to match an AI cover design, reuse it as a web template, localize covers across languages and devices, or fix inconsistent typography and text overflow.
metadata:
  short-description: Generate and verify editable multilingual store covers
---

# App Store Cover Generator

Produce separate, editable screenshot covers with an evidence-backed locale/device matrix. AI art supplies material and composition; HTML/CSS owns localizable words and repeatable geometry. A contact sheet is review evidence, not an upload screenshot.

## Start from the requested stage

- **Direction or prompt only:** analyze the reference and deliver the requested concept. Do not build a full pipeline by default.
- **Build or refine covers:** follow the workflow below; reuse a working template rather than replacing it unnecessarily.
- **Audit existing covers:** inspect both the rendered images and editable source. Report the exact cells affected; do not redesign unrelated slides.
- **Store upload or social publishing:** follow [delivery.md](references/delivery.md) only when that stage is requested. Creating covers grants no upload or publication authority.

## Freeze the brief

Record app, customer, supported features, canonical slide IDs/order, enabled locales, device display slots/dimensions, visual reference, source screenshots, and requested terminal stage. Version/build identity matters for release work, not an early design prompt. Discover current store requirements instead of assuming every app needs nine slides or both phone and tablet.

Ask only for decisions that cannot be inferred from the app or reference. If assets are missing, make an explicitly labeled concept and list what is needed for store-ready output. Never invent product capabilities, reviews, prices, or usage metrics.

## Match the reference before scaling the matrix

Read [art-direction.md](references/art-direction.md) for decomposition and reusable prompts. Inspect the reference and identify title size relative to canvas width, line breaks, top inset, text-to-device gap, camera angle, device crop, materials, highlights, floating panels and motion cues. Keep icon/name where useful; do not repeat the lockup on every slide automatically.

Build one representative cover and compare it at the **same rendered dimensions** as the reference. CSS pixels, image pixels, font face, weight, tracking, line height and export scale all affect perceived size. Fix the shared tokens before creating every locale. Do not call a rough CSS substitute reference-faithful just because its structure matches.

Generate only the difficult art layers. Keep translated titles out of generated pixels. Place real app captures into frames without changing feature claims. Record which pixels are captures, illustrations or composites. Motion posters need visibly different phases or expressive poses; a static repeated thumbnail does not show motion. Read [localization.md](references/localization.md) before expanding the language set.

## Implement and run

The bundled [starter](assets/starter/index.html) is a small working baseline, not the mandatory final style. Copy it to a project before customization. See [template-contract.md](references/template-contract.md) for the data shape and extension points.

From this skill directory (Node 22+):

```sh
npm ci
npx playwright install chromium
node scripts/init.mjs /path/to/new-cover-project
node scripts/serve.mjs /path/to/new-cover-project
# Open the printed local URL, then edit project.json, CSS and art.
node scripts/export.mjs /path/to/new-cover-project /path/to/new-output
node scripts/verify.mjs /path/to/new-output
```

The initializer and exporter refuse to overwrite existing directories. The server binds to loopback and serves only the selected project. Exports reject network assets for reproducibility; store approved local artwork/fonts with provenance. The starter contains original demo SVG art and explicit synthetic UI, not NextNote source code or a shipped-app capture.

For global coverage, use `node scripts/locales.mjs list` and `node scripts/locales.mjs add PROJECT NEW_PROJECT app-store` (or a comma-separated BCP 47 list). This preserves existing text and leaves new translations empty. Fill them, then run `node scripts/locales.mjs check PROJECT`. The catalog has 50 store locale presets; custom tags are local rendering targets, not assumed upload slots. Read [localization.md](references/localization.md) for regional variants, fonts and RTL.

Keep one story order, explicit copy for every locale and no silent English fallback. Keep title/support text in fixed boxes. Use one base typographic token per device and a reviewed locale adjustment when necessary; rewrite long copy before shrinking. The example 0.60 scale floor is a design guardrail, not an Apple rule. Read [quality-gates.md](references/quality-gates.md) for exact automated coverage and its limits.

## Inspect the deliverable

1. Run the exporter and verifier. Failures must identify locale/device/slide; preserve the failed report and correct source before a fresh export.
2. Open every locale/device contact sheet and inspect all cells. Examine native PNGs for long copy, CJK, RTL, raster UI text, motion details, overlaps, weak contrast and mismatched device shapes.
3. Compare the representative final render against the approved reference at equal size. Use a side-by-side crop or overlay where useful. Record visible differences; never invent a visual similarity percentage.
4. Record visual approval separately from the automated report. Passing geometry/hash checks does not mean pixel-perfect fidelity, translation accuracy, licensed artwork, or App Store approval.
5. Deliver editable source, PNG matrix, contact sheets, manifest/hashes, audit results, source attribution and unresolved limits. Stop at the authorized stage.

## Supporting references

- [Art direction and prompt recipes](references/art-direction.md)
- [Localization, fonts and motion](references/localization.md)
- [Template schema and commands](references/template-contract.md)
- [Quality gates and troubleshooting](references/quality-gates.md)
- [Store handoff and public case studies](references/delivery.md)
- [NextNote: lessons from the original workflow](references/nextnote-case-study.md)
