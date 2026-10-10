# Quality gates and troubleshooting

## What the bundled tools actually check

- Project: explicit copy, canonical IDs/order, legal filename components, duplicate IDs, dimensions, art paths and provenance.
- Browser: loaded images, font-load completion, text-box scroll overflow, minimum scale, Range rectangle bounds against canvas and rectangular clipping ancestors, approximate text collisions and sampled occlusion.
- Export: exact PNG dimensions, decodable/CRC-valid data, opaque pixels and nonuniform image content.
- Matrix: exact expected cells, record identity, hashes, extra PNGs and per-locale/device contact sheets.

The checks do not read text inside images, prove glyph-font identity, detect all occlusion, measure contrast, assess translation, establish asset rights or judge design fidelity. Rotated bounding rectangles may produce conservative false positives. Clip paths, masks, transparent overlays and pointer-events:none can escape sampling. Nonuniform is only a blank-image sanity check, not proof of useful content. Record and inspect every flagged cell; do not suppress all warnings for a rotated template.

## Visual review record

After running export/verify, create a separate review file with the export manifest digest, reviewer/date, exact cells inspected, reference comparison, typography, raster UI language, motion-phase details, image crop/contrast and remaining differences. A changed export requires a new review. Inspect **all cells**, not only one language-family representative; representatives help prioritize deep checks but do not waive full-matrix review.

For each cell use pass / needs-fix / accepted-exception. An exception needs exact scope and reason; never invent user approval. Compare at native size and at 160–220 px thumbnail width. Keep text comfortably readable rather than treating the scale floor as permission to use tiny copy.

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
