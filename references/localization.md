# Localization and typography

## Text is data

Use semantic slide IDs and an explicit copy object for each locale. Never treat missing translations as English. Regional locales may share wording only by explicit decision; they still have separate output cells. Preserve brand names but translate in-app sample copy where appropriate. Do not mechanically translate line breaks.

Start with customer value and rewrite long text rather than squeezing it. Use a fixed title box, shared base size per device and consistent leading. A language may need a documented optical adjustment; do not make every slide a different size. The 0.60 minimum in the guidance is an example floor, not a target. The demo uses 0.80. Automatic per-box fitting is a guard against failure, not visual approval: review the scale distribution and rewrite cells that become visibly smaller.

## Fonts

Add a locally hosted font with permission to redistribute or supply it privately. Declare correct weights and scripts with @font-face. Set font-synthesis:none after providing the needed faces. Wait for document.fonts.ready and decode all images before export. CSS fontFamily and font readiness do **not** prove that every glyph used the intended font. Inspect actual rendered fonts with browser developer tools or a supported platform-font API, especially for CJK punctuation, Arabic shaping and emoji. Record the browser/OS and font-file hashes for reproducibility.

The open-source demo deliberately uses system fonts so no third-party font is silently redistributed. Its raster output is therefore not byte-identical across OSes; pin the browser, OS and font files for reproducible production exports. Do not advertise cross-machine pixel determinism from a lockfile alone.

## Long-copy and RTL review

Check German-like long words, Portuguese/Indonesian expansion, Japanese/Chinese line breaking and Arabic right-to-left reading. Set both lang and dir; use logical padding and alignment. Do not mirror app screenshots or logos just because text is RTL. Support locale-specific art paths when screenshot UI language changes. Ensure numeric/date examples and currency match the locale and product.

## Motion and raster UI

Generated lettering, tiny UI labels inside captures, embedded emoji and phased thumbnails bypass DOM audits. Inspect those pixels separately. Use the exact captured build when claiming candidate fidelity. Store screenshot requirements and product availability are distinct from a successful text-fit check.
