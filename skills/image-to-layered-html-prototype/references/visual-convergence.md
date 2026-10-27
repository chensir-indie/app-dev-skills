# Visual convergence: from failing captures to acceptance

Use this process when `validate_prototype.py` fails visual checks. It does not guarantee pixel identity for every flattened image. It requires fixing repairable differences and retesting against the same frozen standards. Structural success, clickability or reduced overall MAE does not establish visual acceptance.

If existing HTML lacks contracts, preserve original source and before screenshots first. Initial `inventory_page.cjs` use requires `index.html`, `reference/source.png` and `data-artboard` on the target root. Add the attribute to the existing root without rebuilding the wrapper/layout. Inventory describes implementation, not independent reference measurements.

## 1. Resolve decisive assets first

Before fine typography work, inspect dominant subjects, photos, texture and decoration. Compare reference and candidate side by side: object count, visible contours, holes, perspective, lighting, crop, shadows and alpha edges. **Semantic similarity is not asset identity.** Prefer separate assets from the same generation when available. Otherwise use imagegen extraction/editing under [reconstruction.md](reconstruction.md), preserving the untouched reference. If visible extracted contours remain wrong, reconstruct again or change methods rather than placing a merely similar subject over the page.

Place candidate photos/subjects in actual HTML layers and capture both page versions with the same browser/viewport. Do not compare a raw asset directly to a full-page reference. Without complete page contracts, use `scripts/compare_candidate.py` for local A/B:

```sh
python3 scripts/compare_candidate.py \
  --reference /abs/page/reference/source.png \
  --baseline /abs/page/evidence/previous-browser.png \
  --candidate /abs/page/evidence/candidate-browser.png \
  --roi LEFT TOP RIGHT BOTTOM \
  --out /abs/page/evidence/asset-candidate.json
```

The script requires matching dimensions for the reference and both **actual full-page browser captures**. It reports full-image/asset-ROI MAE, contour difference and RGB bias. The candidate must improve the asset ROI without regressing the full page. `keep for further visual review` recommends further inspection, not acceptance. Verify the asset contains no text, buttons, card borders or menus; record provenance, prompt, SHA and limitations. With complete contracts, frozen-ROI `compare_iteration.py` and final strict validation remain authoritative.

Keep the background in its own UI-free layer: sample unobstructed color/light fields, then match gradient stops, texture, blur and decorative paths. Reference crops containing text, buttons or backplates are not independent background assets. If the original font is unavailable, compare several actually rendered families and choose the closest glyphs/baseline, recording unresolved font-provenance uncertainty.

## 2. Freeze acceptance targets and locate errors

Freeze reference SHA, dimensions, state, named-role ROIs and `one_to_one` limits in `design-tokens.json` before tuning. Limits must also satisfy [acceptance.md](acceptance.md)'s non-relaxable ceilings. Each iteration begins with fresh current-HTML screenshots, DOM and hash receipts through `capture_native.cjs`, then diagnosis:

For batch drafts without contracts, use [multi-page progress](#multi-page-progress) triage first. Complete the selected page's contracts before frozen-ROI diagnosis. Triage scores are not acceptance results; low whole-image MAE does not permit skipping text, buttons or contours.

```sh
python3 scripts/diagnose_visual.py /path/to/prototype --state <state-id> \
  --out /path/to/prototype/evidence/visual-diagnosis.json \
  --overlay-out /path/to/prototype/evidence/visual-overlay.png \
  --heatmap-out /path/to/prototype/evidence/visual-heatmap.png
```

Nonzero exit means at least one frozen visual metric failed. The report ranks regions by excess MAE × ROI area and includes worst 128px blocks, changed-pixel ratio, edge disagreement and mean `actual - reference` RGB. Ranking prioritizes the largest affected areas; overlapping ROI errors cannot simply be added. Numbers locate differences, not their layer causes. Inspect reference, actual, overlay, heatmap and isolated-layer captures. Keep threshold-0 raw diffs rather than only tolerance-filtered results.

Contour difference independently affects each ROI's result. Inspect irregular backplates, subject edges, buttons and icons separately in contour overlays; similar mean colors must not conceal wrong shapes.

## 3. Repair one cause category at a time

Choose from worst regions and layer evidence:

| Observation | Inspect first |
| --- | --- |
| Large solid-color or brightness bias | Background/panel colors, opacity, blending, blur and shadows |
| High differences on both sides of an object | Subject asset, alpha boundary, scale, crop, rotation and layering |
| Double edges around text | Family, weight, size, baseline, line height, tracking and antialiasing environment |
| Local differences at thin lines or corners | SVG paths, stroke widths, radii and optical alignment |
| Apparent whole-page shift | Reference coordinates, viewport/DPR, status bar, safe area or capture scroll position |

Change one cause category per iteration, reload current source, await fonts/image decoding and capture at native size. Keep the prior capture, then run:

```sh
python3 scripts/compare_iteration.py /path/to/prototype --state <state-id> \
  --before evidence/iteration-before.png --after evidence/native.png \
  --out evidence/iteration-report.json
```

The report compares full-image and every ROI's before/after errors. If the full page improves but a key region regresses, inspect overlays before retaining the change. Resolve large/high-contrast areas before small icons. Do not conceal wrong assets with CSS color blocks or hide wrong fonts by scaling text. `compare_iteration.py` recommends convergence steps; final acceptance still requires strict `validate_prototype.py` plus manual contour/hierarchy checks.

After two consecutive iterations without improvement in one category, stop local tweaking and reconsider asset, measurement or rendering methods. If key assets cannot be reliably extracted, record exactly what is missing, failed attempts and affected ROIs. Structural delivery can continue, but visual status stays `pending`; do not call it accepted.

## 4. Pass the acceptance gate

For every requested page/state, rerun native-size capture, DOM/layer proofs, `diagnose_visual.py` and strict `validate_prototype.py`. ROI union covers at least 75% of the reference, with matching-role coverage of at least 80% for text, buttons, subjects and important panels/icons. Full image and key ROIs remain below frozen limits and fixed ceilings. Open the reference, current browser capture, overlay, raw diff and layer-toggle proofs. Check subject identity, background, glyphs, contours, occlusion and controls, recording concrete observations in `manualReview.states[]` under [acceptance.md](acceptance.md). Any of the six checks failing leaves `pending`. `--structure-only` establishes only the HTML layer contract.

End multi-page delivery with a per-page status table. One failing page does not establish batch success. If any requested pages remain incomplete in the current turn, name them and their main differences; an index or first pilot is not the finished page set.

## Multi-page progress

Freeze `expected-pages.json` as an array of page directory names from all reference directories. For drafts without contracts, run:

```sh
python3 scripts/triage_batch.py /absolute/path/to/pages \
  --expected-pages /absolute/path/to/pages/expected-pages.json \
  --out /absolute/path/to/pages/visual-triage.json
```

It reports missing artifacts, existing native captures' full-image MAE and worst local blocks. By default, close strict acceptance on the page closest to completion before the next page. `nextAcceptanceCandidate` is only a suggestion; choose using `visualRepairOrder` and user priorities. A missing asset on one page does not stop the whole batch.

When the user requests all drafts first, use two stages. First create separately openable HTML pages with editable DOM text, semantic buttons, independent assets and native captures. Check image loading, exclusion of references from runtime, basic interactions and dimensions, then report draft status. Second complete tokens, source measurements, contracts, named ROIs and strict acceptance per page. Openable-page count is not accepted-page count.

Finally run:

```sh
python3 scripts/validate_batch.py /absolute/path/to/pages \
  --expected-pages /absolute/path/to/pages/expected-pages.json \
  --out /absolute/path/to/pages/batch-acceptance.json
```

Batch results use each page's strict exit code and fail for omitted HTML or existing reference directories. Index images, average errors and a first pilot cannot replace per-page results. Record pending pages, major differences and attempted repairs. Keep critically blocked pages `pending`, continue other feasible pages, then revisit them.
