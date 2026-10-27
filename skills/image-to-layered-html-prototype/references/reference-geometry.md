# Separate source-image measurement from implementation geometry

`referenceBounds` is an element's target layout box independently derived from the source image; `bounds` is its browser layout box in current HTML. Text also requires `referenceInkBounds` for visible source glyphs. Glyph ink excludes CSS line-height whitespace, so OCR boxes cannot be compared directly with DOM line boxes. Strict acceptance compares layout boxes, then uses source/actual glyph measurements, local diffs and manual review to assess ink.

## Measurement sequence

1. Lock the unscaled original, dimensions and SHA-256. Using the source, enlarged crops, a grid/ruler or image viewer, mark text/button/important panel/icon top-left coordinates and width/height in source coordinates. Do not derive reference coordinates backward from implementation screenshots.
2. In `geometry-table.md`, record element ID, `x/y/width/height`, measurement anchors, contour/radii, `measured` or `inferred`, and reasons for uncertainty. Transparent shadows/glows are not content boundaries; specify whether strokes are included. For text, record visible glyph ink first, then independently derive the target CSS line box using glyphs, baseline and intended line height. A parent card is not a text box, and an ink box is not a line box.
3. Put the target text line box or control/panel layout box in that layer's `referenceBounds`, and source glyph ink in `referenceInkBounds`. Each text layer also records `referenceInkMethod` (`apple-vision-ocr` or `high-contrast-pixel-core`) and `referenceInkEvidence` pointing to source-measurement JSON. Record DOM `bounds` separately; a real browser audit may provide it. Text layers need their own DOM wrappers matching target line boxes. With only OCR ink and no reliable line-box derivation, remain `pending`.
4. Confirm anchors using reference/actual overlays. If boxes match but contours differ, continue repairing shape/material. Bounding-box success is not visual acceptance.

On macOS, the following Traditional Chinese OCR example can measure both the reference and browser capture: `swift scripts/measure_text_ink.swift /absolute/path/to/reference.png zh-Hant 返回 繁體中文 > evidence/reference-ink-ocr.json`. The Chinese words are locale-specific sample input, not a required output language. Optional word arguments add ink boxes for specified words in merged OCR lines, separating text from a neighboring arrow. This read-only tool records image SHA, native dimensions, OCR text and glyph-ink boxes. Manually check missed characters, merged icons/text and punctuation. OCR only aids ink measurement; it neither generates `referenceBounds` automatically nor decides acceptance.

When OCR merges arrows, punctuation and text, select a tight text-only ROI on the source first. Then run `python3 scripts/measure_ink_core.py /absolute/path/to/reference.png --box 590 640 735 725 --mode dark` to measure its high-contrast pixel core; use `--mode light` for light text. Results include image SHA, ROI, color threshold and outer pixel box. Antialiased edges are excluded from the core, so this is a second positioning measurement that still requires enlarged-source inspection and cannot directly stand in for a CSS line box.

```json
{
  "id":"page-title", "type":"text", "selector":"#page-title",
  "bounds":{"x":32,"y":190,"width":230,"height":58},
  "referenceBounds":{"x":32,"y":190,"width":230,"height":58},
  "referenceInkBounds":{"x":34,"y":201,"width":224,"height":43}
}
```

These numbers illustrate the format, not an actual page measurement. `referenceBounds` is required for all text/buttons and layers with `visualRole` set to `panel` or `icon`. Strict geometry limits default to at most 2 CSS px. When the source cannot support a reliable boundary measurement, leave that page `pending`, explain the asset/measurement blocker and continue areas that can be measured. Do not copy implementation values and label them measured.

For irregular backplates, the bounding box constrains placement only. Also record SVG path, reference turning points/tangents, occlusion and a named `panel` ROI. For subjects with transparent edges, the outer box is coarse positioning; use `subject` ROIs, alpha edges and local contour comparisons. Typography also requires glyph, baseline, weight, tracking, line-spacing and color checks. Buttons also require internal icons, selected states, corners and hierarchy checks.
