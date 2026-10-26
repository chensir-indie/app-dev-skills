---
name: image-to-layered-html-prototype
description: Rebuild approved app UI images as editable layered HTML/CSS/SVG, or repair an existing reconstruction with measured reference geometry and browser comparisons. Also supports UI direction, scoped design critique and refinement, prompt-only requests, shared design systems, multi-page prototypes and optional Flutter handoff.
---

# Image to Layered HTML Prototype

Choose the concept, full reconstruction or existing-page repair branch that matches the request. Full reconstruction delivers an editable, interactive HTML prototype with visual review for every page: DOM text, visible semantic controls, CSS/SVG backplates, and separate photo/subject assets. Reconstruction defaults to `layered_rebuild`. A one-to-one request raises the fidelity requirement; full-screen images, UI slices, Canvas or transparent hotspots cannot replace a layered implementation.

## Choose the starting point

| User goal and input | Start here | Completion boundary |
| --- | --- | --- |
| UI directions, prompts or reference images only | Follow [imagegen-workflow](references/imagegen-workflow.md) to deliver the requested directions, prompts or inspected images | The requested concept artifact; no automatic HTML reconstruction |
| Complete prototype with only a product direction | Generate, inspect and lock a front-facing UI image using the imagegen workflow, then continue below | Layered HTML with per-page acceptance |
| Complete prototype with approved images | Lock and measure the references directly, preserving the approved direction | Layered HTML with per-page acceptance |
| Repair existing HTML against reference images | Preserve source, assets and interactions; save before screenshots and inventory the implementation, then add independent reference measurements and necessary contracts | The requested repair, refreshed evidence and actual acceptance status |
| Review or improve an existing page | Inspect it using [design quality review](references/design-quality-review.md), select the primary standard and identify issues; review-only does not edit, while authorized refinement proceeds directly | The requested review, or improved pages, before/after captures and interaction checks; no automatic full reconstruction |
| Multiple page references | Freeze the complete page inventory; close the loop page by page by default, or use the two-stage process below when all drafts are requested first | Per-page status for every requested page |

Distinguish **faithful reconstruction, active refinement and review only**. Approved images and one-to-one requests default to reconstruction. Interpret “improve” in context: it may mean correcting reconstruction errors or changing the design, and does not itself unlock frozen constraints. For exploration or active refinement, read [design quality review](references/design-quality-review.md); when selecting the primary design system or optional tools, read [sources and applicability](references/design-sources.md). Preserve the project's existing standards; use other guidance to fill gaps rather than mixing several component styles. Steps 1–5 apply to full reconstruction and corresponding repairs. End review-only or local refinement at its requested endpoint without requiring a full pixel contract.

If the real goal is store covers or competitor analysis, first read the actual `SKILL.md` for the available `app-store-cover-generator` or `app-competitor-analysis` skill and route by the goal. If unavailable, explain the relevant scope without making installation a prerequisite to useful work.

Before dependency-backed scripts, run `sh scripts/doctor.sh` in this skill directory. Use `--scope python` for Python checks or `--scope browser` for browser operations; checks are read-only and do not install. Follow their output and [environment setup](README.md#environment-check-and-setup) to repair and rerun. Preserve drafts and continue independent design work while script and visual acceptance remain `pending`. Direction-only and prompt-only tasks do not require a rendering environment.

For existing HTML entering reconstruction or fidelity repair, first preserve the original source and before screenshot. Add `data-artboard` to the existing target artboard root if absent, retaining its layout rather than creating another wrapper. Inventory it, then continue to step 1 to complete the contracts:

```sh
node scripts/inventory_page.cjs /absolute/path/to/page
```

This requires `index.html`, `reference/source.png` and the target root's `[data-artboard]`. It produces implementation inventory and actual screenshots, not reference coordinates, contracts or acceptance results.

## 1. Freeze the reference and acceptance target

Save the full-resolution, front-facing reference, SHA-256, page/state, language and fixture data. Detail crops aid measurement; the full image remains the baseline. Lock image pixels, CSS pixels, DPR and the actual browser environment using [render-contract](references/render-contract.md).

Establish the required tokens and components using [design-system](references/design-system.md). **Before implementation**, freeze `one_to_one` limits and named role ROIs using [acceptance](references/acceptance.md#one-to-one-visual-standard). Preserve the non-relaxable ceilings; do not erase failures by loosening limits, changing the baseline or excluding major UI.

Completion: the reference, state and acceptance target are traceable. For multiple pages, freeze `expected-pages.json` from all references so batch checks can detect omitted pages.

## 2. Measure independently and establish contracts

Measure the source image independently using [reference-geometry](references/reference-geometry.md), then compare with the DOM. The initial inventory of an existing page cannot replace source-image measurement. For text, buttons and important panels/icons, `referenceBounds` is the target layout box derived from the source image; `bounds` is the implementation box. Record text's visible glyphs separately as `referenceInkBounds`, with a method and evidence bound to the original SHA. OCR ink boxes are not CSS line boxes, and automatically copied DOM values are not source measurements.

Use [geometry-contract](references/geometry-contract.md), [typography-contract](references/typography-contract.md) and [layer-manifest](references/layer-manifest.md) to establish geometry/typography tables and unique selectors covering all visible text and controls.

Completion: implementation and reference measurements have distinct, clear provenance, and contracts cover every visible layer.

## 3. Reconstruct assets and layered HTML

Calibrate important subjects, backgrounds, fonts and irregular contours using [asset-audit](references/asset-audit.md) and [reconstruction](references/reconstruction.md), then implement independent layers and visible interactions using [html-css-contract](references/html-css-contract.md). Prefer original assets. If missing, extract or reconstruct a single asset and record provenance and uncertainty. `inferred` does not excuse a visible failure; approximate subjects are for structural debugging only.

Place new assets in the actual HTML and capture browser A/B comparisons in the same environment, checking the full image and asset ROIs. Without a complete contract, use `compare_candidate.py`; once contracts exist, use `compare_iteration.py` with frozen ROIs. See [visual-convergence](references/visual-convergence.md). An A/B improvement is not acceptance.

Completion: text can be edited, subject/backplate/shadow can be hidden independently, and primary interactions produce visible outcomes with return/close behavior. Keep adaptation evidence for the baseline, smaller/larger screens and long copy.

## 4. Capture and converge

Read the capture requirements in [acceptance](references/acceptance.md) and the repair loop in [visual-convergence](references/visual-convergence.md). After fonts load and images decode, fix data, clock, scrolling and animation, then capture screenshots, DOM and hash receipts from the current source:

```sh
node scripts/capture_native.cjs /absolute/path/to/prototype playwright home
python3 scripts/diagnose_visual.py /absolute/path/to/prototype --state home
```

`state-id` labels evidence; it **does not trigger the state**. Activate dialogs, forms, selections and routes in the same browser session, verify their landmarks, then capture. Defaults are `file://` and DPR=1. Implement other policies explicitly through the render contract; the script does not apply every environment field automatically.

Retain current-source reference/actual pairs, overlays, threshold-0 raw diffs and layer-toggle proofs. Repair subject, background and fonts before detail, guided by failing ROIs and worst local blocks. Change one cause category per iteration; keep the before capture and compare regressions. If the same category fails to improve for two consecutive iterations, change the asset or measurement/reconstruction method.

The ROI union must cover at least 75% of the reference, with matching-role ROIs covering at least 80% of key layers. Centers of text/buttons and layers occupying at least 1% of the page must also be covered. Full-image means cannot replace local contour, typography or control limits; use acceptance's exact fields and fixed ceilings.

After capture, inspect hierarchy, typography, icons/materials and edge states using the applicable [design quality review](references/design-quality-review.md) checks. Fix fidelity errors directly and list out-of-scope design suggestions separately. Design review cannot replace frozen pixel limits, and accessibility checks do not establish visual acceptance.

Completion: every requested state has an actual trigger and current capture, and frozen numeric limits pass. Inspect reference, actual, overlay, raw diff and layer proofs; record concrete observations for asset identity, background, typography, contours, layering and controls in `manualReview.states[]`. Obvious mismatches remain `pending`.

## 5. Accept and deliver each page

```sh
python3 scripts/validate_manifest.py /absolute/path/to/prototype/layer-manifest.json
python3 scripts/validate_prototype.py /absolute/path/to/prototype
```

Mark `passed` only when strict validation and manual visual review both pass. `--structure-only` is diagnostic; file presence, hash receipts and numeric success each establish only their own scope. Report separate evidence for editability, visual fidelity, interactions and adaptation. Continue repairing unresolved critical differences. If assets/tools are a real limitation, list the exact missing items, attempts, errors and failed checks.

Apply the same gate to every page. Any page `pending` leaves the batch `pending`. For batch checks and draft triage, see [multi-page progress](references/visual-convergence.md#multi-page-progress). When the user requests all drafts first, deliver separate HTML, editable text, semantic controls, independent assets and native-size captures for all references; check resources, interactions and dimensions. Then complete contracts, measurements and strict acceptance per page. A draft is not visual acceptance; continue other feasible pages while one page is temporarily blocked.

Deliver source, separate assets, references, tokens, manifests, render configuration, state matrix, measurement tables, interaction map and `evidence/` following [design-system](references/design-system.md) and [acceptance](references/acceptance.md). Read [flutter-mapping](references/flutter-mapping.md) only for a requested Flutter handoff.

For later handoff, link the existing files and include the goal/next action, chosen reference path/SHA, pages/states, source entrypoints, all four acceptance statuses and failed checks. Prototype captures remain prototype evidence; store materials depicting real app UI require separate actual-app captures.
