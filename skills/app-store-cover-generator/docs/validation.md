# Validation — 2026-10-10

- Official skill-creator `quick_validate.py`: passed, using an isolated Python environment with PyYAML 6.0.3.
- `npm test`: 11 passed.
- `npm run test:browser`: 3 passed; real Chromium execution including clipping, occlusion, collision, missing images, route language mismatch, path traversal, overwrite protection and damaged/stale exports.
- Native export: 12/12 cells passed; 6 locale/device contact sheets generated.
- `verify.mjs`: exact dimensions, opaque nonuniform PNG content, matrix and hashes passed.
- Local Markdown references checked: no broken targets.
- Public-source review: no credentials, private app code, private filesystem paths, real note contents or third-party font/device assets included.

The first native run exposed tight headline leading; an added phase strip exposed foreground occlusion. Both were fixed before the final run. Automated checks alone would not establish visual quality; all 12 cells were also inspected in the final demo contact sheet.

[Machine-readable evidence](validation.json) records source hashes, output hashes and environment. The preview is an illustrative starter. Arabic copy is demo text, not a native-speaker-approved store translation. System fonts can differ on another OS. Full app-store artwork still requires app-specific art direction, licensed fonts, real screenshots and visual review.
