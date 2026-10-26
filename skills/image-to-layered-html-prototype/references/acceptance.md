# Browser evidence and final checks

Python scripts require Pillow; skill format validator separately requires PyYAML. Reuse an available runtime; do not silently change project dependencies.

## Capturing DOM

Use the available browser tool/Playwright runtime; do not install a second browser without need. For a standalone local prototype, run `node scripts/capture_native.cjs /absolute/path/to/prototype /absolute/path/to/playwright <state-id>` from the skill directory. It writes `evidence/native-<state-id>.png`, `evidence/dom-<state-id>.json` and `evidence/capture-<state-id>.json` in one browser session. Set `state.screenshot`, `state.dom` and `state.capture` to those paths. Run it again after any source or asset change. The receipt records browser version, URL, viewport/DPR and source hashes; strict validation compares those against the current files.
Mark the root data-artboard and images data-asset-role. Read scripts/audit_dom.js as a string and pass it to:
```js
await page.evaluate(async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.decode()));
});
// auditSource is the trusted local scripts/audit_dom.js source, never page data.
const audit = new Function('return (' + auditSource + ')')();
const observed = await page.evaluate(audit, manifest);
```
Save observed as evidence/dom.json through the browser runtime. Never hand-write observed text or bounds.
The audit is a heuristic, not proof against deliberately disguised screenshot tiles. Inspect DOM/assets and removal screenshots as well.
It also lists visible DOM text nodes and semantic controls that no layer selector covers. Make these lists empty by adding genuine layers to the manifest, never by hiding visible elements during capture.

## Proof screenshots

Capture before/after pairs for:
- withoutImages: hide subject/photo only; UI text, panels, buttons must remain.
- textEdited: temporarily change a visible heading, screenshot, restore.
- layerToggle: hide panel while retaining plant, then restore; inspect intersection pixels.
- interaction: trigger primary action; show its visible result and test return/close.
- responsive: baseline versus another width or long text; inspect overflow/overlap.

Mutations are temporary validation steps; restore before baseline capture. No source screenshot overlays during capture. Record observations in plain language and actual browser version/viewport/DPR.

## acceptance.json

The final validator checks schema, assets/hashes, observed DOM, geometry, recomputed whole-image/ROI errors, proof pairs, and unresolved findings. It does not replace human/model visual review. When it fails visually, run `scripts/diagnose_visual.py` as described in [visual-convergence.md](visual-convergence.md), repair the highest-impact cause, recapture, and rerun the same frozen limits. A pending report is not the endpoint of a request to finish the visual reconstruction.

For a multi-page request, freeze `expected-pages.json` from every supplied reference page before implementation. Pass it to both `scripts/triage_batch.py` and `scripts/validate_batch.py` with `--expected-pages`; strict batch validation fails if an expected HTML page is missing or an existing reference page is omitted from the list. Triage is diagnostic only, including for a page whose whole-image MAE is below 12; every page still needs the per-state role ROIs, layer contract, browser evidence, and manual review below.

## One-to-one visual standard

Set `design-tokens.json.fidelityProfile` to `one_to_one` before implementation. The validator rejects a missing or different profile and enforces these **ceilings** even if `acceptance.json` and `design-tokens.json` contain identical looser values. Freeze equal or tighter limits from the reference and expected browser rasterization; these ceilings are not targets to relax toward.

| Measure | Full page ceiling | Each ROI ceiling |
| --- | ---: | ---: |
| Mean absolute RGB error (0–255) | 8 | 8 |
| Changed-pixel ratio | 0.30 | 0.30 |
| Channel tolerance for changed pixels | 12 | inherited from page |
| DOM geometry difference | 2 CSS px | inherited from page |
| Normalized edge-disagreement ratio (1 px tolerance) | — | 0.15 |

Edge disagreement is the fraction of reference and actual edge pixels that have no counterpart within 1 px, divided by their combined edge count. Dividing by the full ROI area would hide a badly misplaced thin contour. These bounds reject obviously wrong renderings; they do **not** certify literal pixel identity. A literal one-to-one claim needs zero-difference evidence, or a precise account of unavoidable browser/rasterization differences. A different plant, a rectangular substitute for an irregular panel, wrong glyphs/icons, wrong z-order, or a composited UI screenshot remains a failure even if the numeric bounds pass. Keep the threshold-0 raw diff for review.

Give each ROI a `role`: `background`, `subject`, `panel`, `typography`, `controls`, `icon`, or `decoration`. Text layers require a `typography` ROI; buttons require `controls`; subject/photo rasters require `subject`; layers marked `visualRole: panel` or `visualRole: icon` require the corresponding ROI. The union of ROIs with the matching role must cover at least 80% of that layer's visible bounding box. Annotate irregular panels and important icons with `visualRole` in the layer manifest. Use tight local boxes for these roles rather than letting a full-page ROI stand in for contour and typography review.

Every state must cover at least 75% of its native reference with its ROI union. Every visible text/button and every raster, shape or SVG occupying at least 1% of the page needs its center in a ROI. These are minimum coverage checks, not permission to omit the remaining background: the full-image limit still applies. Use tight, named ROIs around title, backplate, subject, buttons, navigation and any dominant ornament. Every ROI freezes `maxMAE`, `maxChangedPixelRatio`, and `maxEdgeDisagreementRatio`; a visually wrong irregular silhouette can fail even when color averages look close. Browser-observed text font family, size, line height, spacing, weight, color and opacity must agree with the layer manifest. The script cannot establish that those declared values were measured correctly from the reference; the visual reviewer must still inspect the source, overlay, glyphs, contours and z-order.

For text, button and important panel/icon layers, `referenceBounds` must be measured from the locked reference before implementation geometry is copied into `bounds`. The validator compares the browser box to **both** sets of coordinates within `geometryPx`; a manifest that merely repeats its own DOM audit cannot pass when the independently measured reference differs. This checks placement and size, not exact ink contours. Record the measurement basis and uncertainty in `geometry-table.md` and review overlay/ROI edge evidence for shape, glyph and occlusion fidelity. Each text layer also needs `referenceInkMethod` and `referenceInkEvidence`; the source-hashed evidence must contain the recorded `referenceInkBounds`. The validator recomputes pixel-core boxes from the locked source ROI and requires the evidence file in the artifact hashes. This authenticates measurement provenance, but OCR ink does not establish the CSS line box or exact font contour. See [reference-geometry.md](reference-geometry.md).

```json
{
  "status":"passed",
  "manualReview":{
    "status":"passed",
    "states":[{
      "id":"home",
      "reference":"reference/source.png",
      "actual":"evidence/native-home.png",
      "checks":{
        "assetIdentity":{"status":"passed","observation":"Subject leaf shapes, pot and crop correspond to the reference"},
        "background":{"status":"passed","observation":"Color field, texture and decoration positions checked against the overlay"},
        "typography":{"status":"passed","observation":"Glyphs, color, baselines, weight and wrapping checked line by line"},
        "contours":{"status":"passed","observation":"Backplate curves, leaf edges, corners and icon contours checked"},
        "layerOrder":{"status":"passed","observation":"Plant, backplate, text and shadow occlusion order checked"},
        "controls":{"status":"passed","observation":"Button dimensions, selected state, icons and interaction feedback checked"}
      }
    }]
  },
  "unresolved":[],
  "states":[{
    "id":"home",
    "screenshot":"evidence/native-home.png",
    "dom":"evidence/dom-home.json",
    "capture":"evidence/capture-home.json",
    "limits":{"maxMAE":4,"maxChangedPixelRatio":0.15,"channelThreshold":8,"geometryPx":2},
    "regions":[
      {"id":"header-and-title","role":"typography","box":[0,0,591,400],"maxMAE":4,"maxChangedPixelRatio":0.15,"maxEdgeDisagreementRatio":0.03},
      {"id":"subject","role":"subject","box":[0,400,591,1030],"maxMAE":4,"maxChangedPixelRatio":0.15,"maxEdgeDisagreementRatio":0.03},
      {"id":"backplate","role":"panel","box":[0,400,591,1030],"maxMAE":4,"maxChangedPixelRatio":0.15,"maxEdgeDisagreementRatio":0.03},
      {"id":"actions-and-navigation","role":"controls","box":[0,1030,591,1280],"maxMAE":4,"maxChangedPixelRatio":0.15,"maxEdgeDisagreementRatio":0.03}
    ],
    "proofs":{
      "withoutImages":{"before":"evidence/native-home.png","after":"evidence/ui-only.png","passed":true,"observation":"All labels/panels remain"},
      "textEdited":{"before":"evidence/native-home.png","after":"evidence/title-edited.png","passed":true,"observation":"Actual heading changes"},
      "layerToggle":{"before":"evidence/native-home.png","after":"evidence/no-panel.png","passed":true,"observation":"Subject remains above panel"},
      "interaction":{"before":"evidence/native-home.png","after":"evidence/action.png","passed":true,"observation":"Visible result and close verified"},
      "responsive":{"before":"evidence/native-home.png","after":"evidence/compact.png","passed":true,"observation":"No overlap or horizontal overflow"}
    }
  }],
  "artifacts":[{"path":"index.html","sha256":"actual hash"}]
}
```
`manualReview` requires more than “looks close enough.” For every `state-matrix.json` state, `reference` must match its locked source image and `actual` must point to the captured browser baseline for that same state. All six categories require concrete observations. Use `pending` and explain uncertainty in `unresolved` when a check cannot be confirmed; a `passed` string cannot bypass the gate. Scripts check record completeness and screenshot binding. The reviewer must still open the source, capture, overlay and layer proofs; scripts cannot verify that observations are truthful.
Example tolerances are starting points, not a universal fidelity definition. Before implementation freeze per-state limits in design-tokens.json.validationLimits and per-state region arrays in validationRegions (both keyed by state id), copy them into acceptance, and explain their basis. Strict pixel identity uses zero channel threshold, MAE and changed-pixel ratio. Keep zero-threshold raw report even when allowing documented rasterization tolerance.
For a user-requested one-to-one reconstruction, do not choose limits after seeing the current error or call generous limits "pixel exact". Set a demanding full-image target and tighter critical ROIs from the reference and expected rasterization variation, then let the validator fail until the implementation meets them. Any later change to the target is a new, explicitly documented acceptance decision, not an implementation shortcut.
Cover title, backplate, subject, buttons and navigation ROIs, not only an easy blank background. Do not exclude major UI.
Each state in state-matrix.json needs evidence. Geometry/text may differ across states: store a per-state manifest via state.layerManifest when needed.

artifacts includes index.html, manifests, tokens, render config, all runtime CSS/JS/SVG/fonts, DOM reports, capture receipts, baseline and proof screenshots. Also hash runtime images via asset-manifest.json. If source or evidence changes, recapture and regenerate hashes. Hashes detect staleness only; they do not prove authenticity.

Four outcomes: structure passed/pending; visual passed/pending; interaction passed/pending; adaptation passed/pending. Filename presence never means visual passed. An unresolved wrong plant, wrong icon or panel contour is a failure even with low global error.
For multi-screen sets, run `python3 scripts/validate_batch.py /path/to/pages --out /path/to/pages/batch-acceptance.json`. It executes the strict validator on every directory with `index.html`, fails closed on missing evidence, and exits nonzero until every page passes. Keep the JSON result beside the review index. An index, contact sheet or average MAE is navigation/progress evidence, never a substitute for a page's source image, DOM audit, ROI report and rendered screenshot.
