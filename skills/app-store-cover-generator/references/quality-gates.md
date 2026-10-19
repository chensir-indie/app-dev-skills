# Quality gates and troubleshooting

## What the bundled tools actually check

- Project: explicit copy, canonical IDs/order, legal filename components, duplicate IDs, dimensions, art paths and provenance.
- Browser: every declared audit box (including brand when enabled), hidden/transparent text, loaded images, font-load errors and completion, text-box scroll overflow, minimum scale, Range rectangle bounds against canvas and rectangular clipping ancestors, approximate text collisions and sampled occlusion.
- Export: failed/local or blocked/external asset requests, source hash changes detected between the initial and final snapshots, exact PNG dimensions, decodable/CRC-valid data, opaque pixels and nonuniform image content.
- Matrix: exact expected cells, record identity, required text-audit records, source hashes, extra PNGs and decodable per-locale/device contact sheets. Case-colliding IDs and ambiguous contact-sheet filenames fail project validation.
- Assets: referenced local art must exist; motion phases must have distinct paths and file hashes. Different bytes still require visual inspection for genuinely different poses.

The checks do not read text inside images, prove glyph-font identity, detect all occlusion, measure contrast, assess translation, establish asset rights or judge design fidelity. Rotated bounding rectangles may produce conservative false positives. Clip paths, masks, transparent overlays and pointer-events:none can escape sampling. Nonuniform is only a blank-image sanity check, not proof of useful content. Record and inspect every flagged cell; do not suppress all warnings for a rotated template.

## Visual review record

After export/verify, create the pending record outside the source project:

```sh
node scripts/review.mjs init /path/to/output /path/to/review.json
# Inspect the reference and every exported image, then fill the record.
node scripts/review.mjs check /path/to/output /path/to/review.json
```

The initializer refuses to overwrite a file. It records the exact manifest digest and every expected PNG, leaving reviewer, date, evidence notes and judgments empty/pending. Fill `reviewer` truthfully (an inspecting agent is valid), `reviewedAt` with an ISO timestamp, `referenceComparison`, and each cell. Use `pass`, `needs-fix` or `accepted-exception`; unresolved entries fail. Evidence notes should cover typography/scale, crop/spacing, raster UI language, contrast and feature/motion detail, with exact observed differences. For an original design, compare against the recorded brief and state that no external reference was supplied.

The checker first verifies the export, then rejects stale hashes, missing/extra/duplicate cells, pending/needs-fix judgments and missing evidence notes. Exceptions return `complete-with-exceptions`, separately from `complete`. An exception needs exact scope and reason; it cannot waive a failed automated check or invent user approval. The export manifest stays `visualReview: pending`; the separate bound record carries review evidence.

Inspect **all cells**, not only one language-family representative. Compare native size and 160–220 px thumbnails. The checker validates the record and its binding, not whether the reviewer actually looked or reached the correct judgment. Neither status grants upload or release authority.

## Reproducibility boundaries

Keep source files unchanged during export. Initial/final hashing catches persistent changes; it cannot detect a file changed and restored between snapshots or prove that JavaScript is deterministic. Record deterministic seeds/frozen animation phases where used. Exported pages are trusted project code, not a JavaScript sandbox. Service workers are blocked and HTTP requests restricted to the local origin, but this is not a security sandbox for hostile templates.

Network/local asset failures are errors even when a fallback font renders. CSS font readiness and a passing geometry audit still do not prove glyph identity. Transparent text checks cover ordinary CSS fill and opacity; filters, masks, painted glyph outlines and complex compositing remain visual-review work.

## Common failures

| Symptom                                         | Action                                                                                                                               |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Web title smaller than reference                | Compare at equal canvas width; inspect font, weight, glyph metrics, tracking, line height and device scale before changing px values |
| One locale fits but looks weak                  | Rewrite copy or adjust a documented locale token, then review all slides in that locale                                              |
| Generated title looks good but cannot translate | Regenerate text-free plate; move title to HTML                                                                                       |
| Repeated static phases                          | Extract genuinely different animation frames or regenerate isolated phases                                                           |
| Long folder/tile name hidden                    | Check every clipping ancestor and foreground layer, not only scrollWidth                                                             |
| Images missing at export                        | Inspect decode error, path case and local file existence; do not replace with a blank placeholder                                    |
| Font differs across machines                    | Vendor a licensed local face, verify actual glyph use and record environment                                                         |
| Export interrupted                              | Inspect incomplete report and preserve evidence; retry into a new directory                                                          |
| Blank or wrong-sized export                     | Check #cover dimensions, export=1 route and screenshot deviceScaleFactor                                                             |

## Store facts

Read current primary sources when preparing an actual upload. Do not encode a guessed universal device-size table in a skill.

- [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications)
- [Apple upload procedure](https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots/)
- [Apple asset guidance](https://developer.apple.com/app-store/asset-best-practices/)
- [Playwright screenshots](https://playwright.dev/docs/screenshots)

Sources checked while preparing this release: 2026-10-10. Recheck for the destination app; this toolkit does not certify store acceptance.
