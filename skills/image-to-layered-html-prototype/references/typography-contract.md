# Typography contract

Typography is geometry. A text layer is incomplete until its box, baseline, and rendering metrics are recorded.

## Required fields

Keep one row per text layer in `typography-table.md`:

| id | x | y | width | height | font family | fallback | weight | size | line height | letter spacing | alignment | locale | confidence |
| --- | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| hero-title | 47 | 276 | 560 | 92 | SF Pro Display | Arial, sans-serif | 700 | 48px | 1.05 | -0.4px | left | zh-TW | measured |

Also record the text baseline, maximum line count, wrapping rule, opacity, and whether the value is product data or reference-only visual copy.

## Measurement rules

- Measure the visible glyph ink box and baseline in the canonical reference pixels. Record the separate target CSS line/layout box inferred from them; OCR ink height must not be compared directly with DOM line-height.
- Record the font file and checksum when the original font is available.
- If the exact font is unknown, record the closest tested fallback and mark confidence as `inferred`; do not claim pixel identity for the glyph rasterization.
- Use explicit `font-size`, `font-weight`, `line-height`, `letter-spacing`, `max-width`, and alignment. Do not rely on browser defaults.
- Keep locale and writing direction explicit. CJK glyph metrics, punctuation spacing, and Latin fallback can change the measured width.
- Use the same browser and device-pixel-ratio for the reference screenshot and the prototype screenshot.

## HTML contract

```css
.hero-title {
  position: absolute;
  left: 47px;
  top: 276px;
  width: 560px;
  font-family: "SF Pro Display", Arial, sans-serif;
  font-size: 48px;
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.4px;
  text-align: left;
  white-space: normal;
}
```

Transcribe screenshot text into visible editable DOM text. Fit candidate fonts to the visible glyphs and report uncertainty about the original font. Reference values are fixtures, never real business data. Do not rasterize UI text or mark it flattened to avoid reconstruction.

## Acceptance

At native size, verify each text layer's box, baseline, line count, wrap point, and opacity. If a font cannot be reproduced, report the residual difference instead of compensating by changing the layout or font size.
