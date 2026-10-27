# Six-level design standards

This file guides design decisions. Machine fields retain the existing layer-manifest, render-contract and acceptance formats; do not create a competing acceptance schema.

For exploration or authorized refinement, establish the task, primary design system and change scope using [design quality review](design-quality-review.md). For faithful reconstruction, extract standards from the approved image. Reuse existing project files for shared standards and record page exceptions explicitly rather than creating another token authority. Consult [sources](design-sources.md) when choosing standards/tools.

## 0. Visual direction

Describe the focal subject, main action, background light/dark structure, text contrast, materials, density, whitespace and distinctive reference features in implementable terms. For example: “a plant extends beyond a translucent irregular backplate, above a separate light selected pill and dark camera button.” Avoid only saying “premium, spacious, fresh.” This example does not require every product to use plants or glass styling.

## 1. Foundation variables

Sample the reference into design-tokens.json and generate/synchronize CSS variables. Record each value's source as measured / inferred / unresolved, its associated reference and measurement notes.

| Category | Parameters to specify |
| --- | --- |
| Color | Background, primary/secondary text, icons, borders, selected and disabled; color separate from opacity |
| Typography | Family, actual CJK fallback, font files/licensing source, weight, size, line-height and tracking |
| Layout | Baseline canvas, margins, module spacing, alignment anchors, content width and system-bar regions |
| Shape | Individual corner radii, stroke thickness, irregular paths/viewBox and optical button bounds |
| Material | Gradient direction/stops, opacity, blur and shadow offset/spread/color |
| Icons | Source, viewBox, visible bounds, stroke, caps, joins, fill/stroke and optical placement |
| States | default, selected, pressed, focus, disabled and applicable loading/error |
| Motion | Durations/easing needed by actual interactions and reduced-motion mode; values not inferable from a static image remain inferred |

Use primitive → semantic → component references, such as palette → navigation.selectedSurface → bottom-navigation selected pill. Do not tweak the same semantic value independently on every page. When references actually differ, record component variants rather than forcing an inaccurate uniform rendering.

Samples from transparent overlays are final composited colors, not original CSS colors. Calibrate against the actual composite; applying the original opacity again to a sampled composite would wash it out.

## 2. Layers and assets

Create separate layer-manifest entries for background, texture, decoration, backplates, subject, text, icons, controls and overlays. Record parent/stacking-context relationships in geometry-table; numeric z-index values alone do not prove correct occlusion.

For backplates, record top steps, sloped-edge endpoints, curvature changes, corner tangencies, the closed path, fill/stroke/shadow. Measure visible segments and label subject-occluded portions inferred. Do not replace an irregular contour with a rectangle merely because it is easier in CSS.

Position cutout subjects using visible alpha bounds. Large transparent PNG margins mean the same width can produce different apparent scale. Record intrinsic size, alpha bounds and the target visible rectangle, then calibrate object-fit/object-position.

Keep navigation hierarchy, visual occlusion layers and DOM implementation hierarchy distinct and explicit.

## 3. Component standards

Define only components actually in scope. Record in component-spec.md:

- anatomy: layers/selectors for background, icon, copy and state indicator.
- geometry: outer box, inner padding, gaps, text baseline, visible icon dimensions and radii/paths.
- states: colors, size changes, semantic attributes and visible feedback for every requested state.
- interaction: trigger, outcome, return/close, keyboard behavior and demo-data versus real-service boundaries.
- content: copy provenance, maximum/long-copy strategy, localization and empty values.
- evidence: consuming pages/states, reference regions, captures and unresolved differences.

For bottom navigation, measure shell and inset selected block dimensions/margins separately. Ordinary items may stack icon/text while the camera button uses a row; selected pills, unselected items and primary actions need not share equal widths. Define current-page selection separately from pressed feedback. Use consistent-source SVG icons or precise redraws; emoji are not final substitutes.

Record visible dimensions and target sizes separately; expanded hit areas must not obscure neighboring controls. Show fidelity work separately from accessibility/adaptation revisions. Explicitly record low contrast in a reference rather than silently changing it and claiming identity, or declaring the flawed draft production-accessible.

## 4. Pages and states

In page-map.md, list navigation hierarchy, entry/exit, primary actions and target routes. Bind each reference state through [state-matrix.json](state-matrix.md). Home, lists, details, settings, forms and dialogs belong only when requested; completeness is not permission to add product features.

Pixel-compare states with user references. Necessary loading/empty/error/permission states without references reuse component standards and are labeled designed/inferred. Assess their usability and style consistency without inventing source images or claiming reference comparison passed. The current strict validator requires referenced states; put unreferenced supplemental states in supplemental-states.md with interaction evidence, not in the reference-comparison state table as if references existed.

Check every consumer after shared-component changes, especially text, inputs and buttons reused in detail/edit pages and dialogs. Report per-page status rather than hiding a distorted page in an average.

## 5. Acceptance and handoff

Reproduce the baseline viewport first, then inspect narrow/wide viewports, long copy and keyboard/scrolling. A locked image does not establish responsive-product behavior; verify separately. Navigation between deliverables clearly distinguishes reference images from actual HTML, opening actual HTML by default and showing side-by-side/overlay comparisons separately.

For each page deliver runnable HTML/CSS/JS, separate assets, editable variables, layer/component/page standards, actual captures, diffs and interaction evidence. The following layout is an example; required filenames come from the existing references:

```text
prototype/
  index.html, styles.css, app.js
  assets/                       # separate subjects, photos, fonts and textures
  reference/                    # locked originals, never loaded by the running page
  design-tokens.json, layer-manifest.json, asset-manifest.json
  render-config.json, state-matrix.json
  geometry-table.md, typography-table.md, interaction-map.md
  component-spec.md, page-map.md
  evidence/                     # browser captures, DOM, receipts, comparisons and layer proofs
  acceptance.json
```

A Flutter handoff reuses these standards/assets, then calibrates the native implementation through flutter-mapping.md. HTML acceptance neither authorizes app changes/publication nor proves Flutter or physical-device acceptance.
