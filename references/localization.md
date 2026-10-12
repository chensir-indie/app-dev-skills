# Localization and typography

## Locale selection

The versioned [App Store catalog](../assets/locales/app-store.json) records 50 locale IDs, its source and verification date. It is a preset, not a country-to-language lookup. Check Apple's current list again before store delivery. IDs use canonical BCP 47 base tags without extensions; aliases or casing mistakes are rejected rather than silently changing output paths. `ar-SA` is the store preset; `ar` is still a valid custom rendering locale.

Run from the skill directory:

```sh
node scripts/locales.mjs list
node scripts/locales.mjs add /path/to/project /path/to/new-project app-store
# Or select: ja,zh-Hant,fr-CA,ur-PK,fa-IR
node scripts/locales.mjs check /path/to/new-project
```

For **sample previews**, `npm run demo` exposes all 50 presets with native-language names and region codes. `node scripts/init.mjs NEW_PROJECT --locales app-store` saves that demo; pass a comma-separated preset list to select a subset. The explicit translations in [demo-copy.json](../assets/locales/demo-copy.json) are drafts. Regional English and French demo wording is intentionally shared in separate records. A custom tag without demo copy is rejected by this demo initializer; use the product expansion command above and provide its translation.

Expansion adds locales without deleting existing ones, never overwrites existing copy, and leaves new fields empty. It copies the entire trusted source project to a fresh directory; keep exports and secrets outside that source. The check reports every missing locale/slide/field and exits nonzero until the whole project validates. It checks completeness, not translation accuracy. Ask the agent to draft localized benefit copy from the approved source, then review it before export. Identical regional wording must be an explicit choice, never an automatic fallback.

The shared locale helper uses `Intl.Locale` to determine script and reading direction, including explicit script variants such as `pa-Arab` and `ar-Latn`. Unsupported scripts can use a locale's optional `fontFamilies` array plus local `@font-face` declarations. Tags can be syntactically valid without the installed fonts covering their glyphs; no claim is made that every writing system is verified.

## Text is data

Use semantic slide IDs and an explicit copy object for each locale. Never treat missing translations as English. Regional locales may share wording only by explicit decision; they still have separate output cells. Preserve brand names but translate in-app sample copy where appropriate. Do not mechanically translate line breaks.

Start with customer value and rewrite long text rather than squeezing it. Use a fixed title box, shared base size per device and consistent leading. A language may need a documented optical adjustment; do not make every slide a different size. The 0.60 minimum in the guidance is an example floor, not a target. The demo uses 0.80. Automatic per-box fitting is a guard against failure, not visual approval: review the scale distribution and rewrite cells that become visibly smaller.

## Fonts

Add a locally hosted font with permission to redistribute or supply it privately. Declare correct weights and scripts with @font-face. Set font-synthesis:none after providing the needed faces. Wait for document.fonts.ready and decode all images before export. CSS fontFamily and font readiness do **not** prove that every glyph used the intended font. Inspect actual rendered fonts with browser developer tools or a supported platform-font API, especially for CJK punctuation, Arabic shaping and emoji. Record the browser/OS and font-file hashes for reproducibility.

The starter selects system-font stacks by script (separate simplified/traditional Chinese, Japanese, Korean, Arabic, Hebrew, Indic and Thai profiles) and removes Latin negative tracking for joining scripts and CJK. Script-specific title leading avoids cutting off tall glyphs while retaining shared font-size tokens. Override `locales[].fontFamilies` with your licensed local face names when needed. RTL changes text flow, not device/art mirroring.

The open-source demo deliberately uses system fonts so no third-party font is silently redistributed. Its raster output is therefore not byte-identical across OSes; pin the browser, OS and font files for reproducible production exports. Do not advertise cross-machine pixel determinism from a lockfile alone.

## Long-copy and RTL review

Check German-like long words, Portuguese/Indonesian expansion, Japanese/Chinese line breaking and Arabic right-to-left reading. Set both lang and dir; use logical padding and alignment. Do not mirror app screenshots or logos just because text is RTL. Support locale-specific art paths when screenshot UI language changes. Ensure numeric/date examples and currency match the locale and product.

## Motion and raster UI

Generated lettering, tiny UI labels inside captures, embedded emoji and phased thumbnails bypass DOM audits. Inspect those pixels separately. Use the exact captured build when claiming candidate fidelity. Store screenshot requirements and product availability are distinct from a successful text-fit check.
