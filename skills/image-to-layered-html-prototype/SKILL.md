---
name: image-to-layered-html-prototype
description: Rebuild approved app images as editable HTML/CSS/SVG or repair their fidelity; also supports UI concepts, prompts, scoped design reviews and refinement, multi-page design systems and optional Flutter handoff.
---

# Image to Layered HTML Prototype

Choose the requested branch. Full reconstruction defaults to `layered_rebuild`: editable DOM text, visible semantic controls, CSS/SVG backplates and separate photo/subject assets. A one-to-one request raises fidelity; full-screen images, UI slices, Canvas or transparent hotspots cannot replace editable layers.

## Choose the starting point

| Request | Action and endpoint |
| --- | --- |
| Directions, prompts or reference images only | Follow [imagegen workflow](references/imagegen-workflow.md); stop at the requested concept artifact |
| Full prototype from a product direction | Generate, inspect and lock a front-facing UI reference, then follow steps 1–5 |
| Full prototype from approved images | Preserve the approved direction and follow steps 1–5 |
| Fidelity repair of existing HTML | Preserve source/assets/interactions, save before captures and inventory the page; apply the relevant steps below |
| Design review or refinement | Follow [design quality review](references/design-quality-review.md); review-only does not edit, authorized refinement delivers changes and before/after checks without an automatic full pixel contract |
| Multiple references | Freeze every page; accept page by page unless the user requests all drafts first |

Distinguish faithful reconstruction from active refinement. “Improve” does not unlock frozen design constraints. For exploration/refinement, select one primary standard using [design sources](references/design-sources.md), preserving project conventions. If the goal is store artwork or competitor analysis, read the available corresponding skill's actual `SKILL.md` before routing; its absence need not block useful scoped work.

Before dependent scripts, run `sh scripts/doctor.sh` from this skill directory (`--scope python` or `--scope browser` as appropriate). Follow [setup](references/render-contract.md#environment-check-and-setup) for repairs. Concepts/prompts need no rendering environment; continue independent work while dependent checks remain `pending`.

For an existing reconstruction, preserve its source and before screenshot, add `data-artboard` to the existing root if absent, then run:

```sh
node scripts/inventory_page.cjs /absolute/path/to/page
```

It requires `index.html`, `reference/source.png` and `[data-artboard]`. Its DOM inventory/captures do not supply independent reference measurements or acceptance.

## 1. Freeze the reference and acceptance target

Record full-resolution reference/SHA, page/state, language and fixture data. Lock image/CSS pixels, DPR and browser environment using [render contract](references/render-contract.md); retain the full reference even when measuring crops.

Before implementation, establish [design tokens/components](references/design-system.md) and freeze `one_to_one` [limits and role ROIs](references/acceptance.md#one-to-one-visual-standard). Keep fixed ceilings and the baseline unchanged when checks fail. For multiple pages, freeze `expected-pages.json` from the complete reference set.

**Gate:** reference identity, states and acceptance targets are traceable.

## 2. Measure independently and establish contracts

Use [reference geometry](references/reference-geometry.md) to measure the source image before comparing with DOM geometry. Keep `referenceBounds` (source layout box), `bounds` (implementation box) and text `referenceInkBounds` (visible glyphs) distinct, with methods/evidence bound to the source SHA. OCR ink is not a CSS line box; copied DOM values are not source measurements.

Apply [geometry](references/geometry-contract.md), [typography](references/typography-contract.md) and [layer manifest](references/layer-manifest.md) contracts to all visible text and controls, using unique selectors.

**Gate:** complete layer contracts and independently attributable reference/implementation measurements.

## 3. Reconstruct assets and layered HTML

Apply [asset audit](references/asset-audit.md), [reconstruction](references/reconstruction.md) and [HTML/CSS contract](references/html-css-contract.md). Prefer original assets; extract or reconstruct missing individual assets with provenance and uncertainty. Approximate subjects can support structural debugging but not visual acceptance.

Place assets in the real HTML and compare actual browser A/B captures at full-image and asset-ROI scale. Use `compare_candidate.py` before contracts exist, then `compare_iteration.py` with frozen ROIs; follow [visual convergence](references/visual-convergence.md). Improvement alone is not acceptance.

**Gate:** independently editable/hideable layers, visible primary interactions with return/close behavior, and adaptation evidence for baseline, smaller/larger screens and long copy.

## 4. Capture and converge

Follow [acceptance](references/acceptance.md) and [visual convergence](references/visual-convergence.md). Wait for fonts/images; stabilize data, clock, scroll and animation. Capture current-source screenshots, DOM and hash receipts:

```sh
node scripts/capture_native.cjs /absolute/path/to/prototype playwright home
python3 scripts/diagnose_visual.py /absolute/path/to/prototype --state home
```

The state ID **labels evidence; it does not activate the state**. Trigger and verify routes/dialogs/forms/selections in the same browser session before capture. Defaults are `file://` and DPR=1; implement other render-contract policies explicitly.

Keep reference/actual pairs, overlays, threshold-0 raw diffs and layer-toggle proofs. Repair assets/background/fonts before details, one cause category per iteration, checking regressions. After two non-improving iterations in one category, change the asset or measurement/rendering method. Enforce acceptance's exact local limits: at least 75% ROI union, 80% matching-role coverage for key layers and required layer centers; full-image averages do not replace local checks.

Inspect [design quality](references/design-quality-review.md) without relaxing frozen limits or applying unrequested redesign. Record concrete observations for asset identity, background, typography, contours, layering and controls in `manualReview.states[]`.

**Gate:** every requested state has a real trigger/current capture, frozen numeric checks pass and visual inspection finds no unresolved mismatch.

## 5. Accept and deliver each page

```sh
python3 scripts/validate_manifest.py /absolute/path/to/prototype/layer-manifest.json
python3 scripts/validate_prototype.py /absolute/path/to/prototype
```

Mark `passed` only when strict validation **and** manual visual review pass. `--structure-only`, file/hash presence and numeric success establish only their own scope. Report editability, fidelity, interactions and adaptation separately. Repair critical differences; for actual blockers, record missing items, attempts, errors and failed checks.

Apply the gate to every page; any pending page leaves the batch pending. For all-drafts-first requests, follow [multi-page progress](references/visual-convergence.md#multi-page-progress): deliver editable drafts, separate assets and native captures for every reference, then finish measurements/contracts and strict acceptance per page. Continue feasible pages while another is blocked.

Deliver source, assets, references, tokens, manifests, render configuration, state matrix, measurement tables, interaction map and evidence under the [design-system](references/design-system.md) and [acceptance](references/acceptance.md) contracts. Read [Flutter mapping](references/flutter-mapping.md) only for that handoff. Link existing files with next goal, reference SHA, pages/states, entrypoints, four acceptance statuses and failed checks. Prototype captures remain distinct from actual app captures for store materials.
