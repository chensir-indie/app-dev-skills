# Geometry contract

Use native reference pixels as the source of truth. The prototype may scale the complete artboard for preview, but it must not change the internal geometry.

## Geometry table

Keep a table beside the prototype with one row per reference-critical element:

| id | x | y | width | height | spacing anchors | radius/path | confidence |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| hero-backplate | 47 | 499 | 760 | 562 | page-left, section-top | `layers/hero-backplate.svg` | measured |
| bottom-nav | 30 | 1678 | 793 | 126 | safe-bottom | 63px | measured |

Coordinates are in the canonical image's native pixel space. Name the anchors used to measure each distance, for example `page-left → hero-backplate.x` or `hero-title.baseline → hero-copy.top`.

## Spacing

Measure the distance between visible landmarks, not the distance between arbitrary DOM boxes. Store vertical and horizontal gaps separately. Include safe-area and system-chrome offsets. In CSS, express the values as artboard pixels and scale the artboard once:

```css
.artboard { width: 853px; height: 1844px; }
.artboard__hero { left: 47px; top: 499px; width: 760px; height: 562px; }
```

Do not distribute items with `space-between`, auto margins, or responsive percentage widths when matching a fixed reference. Those tools can be used only outside the canonical artboard.

## Corner radii and irregular panels

Use `border-radius` only when the reference contour is a regular circle, capsule, or rounded rectangle. Record the radius in native pixels and verify it at two or more corners.

If the contour has changing curvature, a slanted edge, a notch, an asymmetric corner, or a plant-shaped cutout, trace it as an SVG path or alpha mask. Keep fill, border, blur, and shadow as separate layers. A rounded rectangle with a guessed radius is a failed reconstruction even if its color is correct.

## Asset slicing

For every cutout or crop, record:

- source file and checksum;
- intrinsic pixel width and height;
- visible alpha bounds, if the asset has transparency;
- source crop rectangle;
- destination rectangle in artboard pixels;
- scale mode and object position;
- whether the crop was measured or inferred.

Prefer an original transparent asset. When only a flattened reference exists, extract/reconstruct the isolated subject with the available image editing tool and trace measurable geometry; record inferred occluded regions. Never use the full screenshot as the UI. See reconstruction.md.

## Acceptance

Render at the canonical width and height. Compare the raw screenshot before scaling. A geometry change is accepted only when:

1. the geometry table and layer manifest agree;
2. the screenshot has no viewport or safe-area drift;
3. an overlay or image diff confirms the subject, panel contour, text baselines, and bottom navigation are in the measured bounds;
4. critical shape/spacing differences are resolved. Labels such as inferred or font rasterization explain remaining evidence, but do not waive failed visual limits.
