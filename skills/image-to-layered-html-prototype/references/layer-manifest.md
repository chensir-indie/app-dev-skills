# Schema 2: DOM-backed layer contract

Use schema=2 and mode=layered_rebuild. reference has path (local packaged image), sha256, width, height.
Every layer: id, type, selector (one actual DOM element), z, bounds {x,y,width,height}.
Bounds use artboard CSS pixels in the default DPR=1 reference coordinate system. For text, button, important panel and icon layers, also record independently measured `referenceBounds` with the same object shape. `bounds` describes the implementation; `referenceBounds` describes the locked image. See [reference-geometry.md](reference-geometry.md). Do not populate both from a DOM audit.

Every text layer also records `referenceInkBounds`, `referenceInkMethod` and `referenceInkEvidence`. The evidence JSON must identify the locked source SHA and contain that exact measured box. The strict validator recomputes high-contrast pixel-core boxes from the source ROI; OCR boxes are checked against source-hashed observations. Add the evidence JSON to the acceptance artifact hashes. These are glyph pixels, not CSS line boxes, so `referenceBounds` remains independently required.

Supported types: text, button, control, svg, svg-path, css-shape, raster, group.
Raster role is subject/photo/decoration/logo; never a screenshot of UI.
Use asset for real local files; inline SVG/CSS is linked by selector, not an invented filesystem path.
Include all visible text and controls, including dates, metrics, metadata, navigation labels, secondary actions and state labels.

Text layer (Traditional Chinese sample content; use the actual requested locale and copy):
```json
{
  "id":"title","type":"text","selector":"#title","z":70,
  "bounds":{"x":32,"y":190,"width":230,"height":58},
  "referenceBounds":{"x":32,"y":190,"width":230,"height":58},
  "text":"今日養護",
  "typography":{
    "fontFamily":"PingFang TC","fallback":["sans-serif"],
    "weight":400,"fontSize":43,"lineHeight":58,"letterSpacing":1,
    "baseline":234,"opacity":1,"color":"#ffffff","align":"left",
    "wrap":"nowrap","locale":"zh-Hant","confidence":"inferred"
  }
}
```
Numbers are illustrative, not measurements from the user's reference.
Button interaction: event, label, visibleOutcome. A label-only hotspot is not valid.
For an irregular panel record full valid SVG path (no ellipses), viewBox and sampled reference anchors.
Mark important panels and icons with `visualRole: "panel"` or `visualRole: "icon"`; strict visual acceptance then requires matching-role ROIs to cover their visible bounds. Do not mark a rectangular approximation of an irregular reference as the measured panel contour.
Geometry source/uncertainty is separate from implementation geometry; source inferred does not permit a failed visible comparison.

Native form fields use `type: "control"`, not a pretend button or a duplicate text overlay. Record `interaction` plus `control: {tag: "input", inputType: "text", value: "reference fixture", disabled: false, readOnly: false}`. Textarea/select omit inputType. Their referenceBounds describe the independently measured field, not glyph ink. The DOM audit reads actual value/type/state; strict validation requires visible native input/textarea/select, an uncovered center, matching value/state and controls ROI coverage. Record the visible value font/ink in typography evidence and exercise real fill/select with visible feedback. Unknown source field or value line boxes remain pending. Password audit values are masked, never copied into evidence.
