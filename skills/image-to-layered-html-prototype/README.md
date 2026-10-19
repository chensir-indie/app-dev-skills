# Image to Layered HTML Prototype

[简体中文](README.zh-CN.md) · [Skill instructions](SKILL.md)

Reconstruct approved imagegen UI concepts or screenshots into editable HTML/CSS/SVG. Keep text, icons, irregular panels, subjects and navigation in independent layers; compare real browser captures with the frozen reference.

## Install and invoke

```sh
npx skills@latest add chensir-indie/app-dev-skills --skill image-to-layered-html-prototype
```

> Use $image-to-layered-html-prototype to rebuild these references as editable HTML, extract a shared design system, and verify typography, contours, layer order and interactions with real browser screenshots.

Image generation is optional and supplied by your agent environment. This toolkit does not bundle or require a paid image API. It cannot recover hidden original layers or promise exact pixels from regenerated assets.

## Toolkit setup

Run from this skill directory. Requirements: Node 22+, Python 3.9+, npm.

```sh
npm ci
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
npx playwright install chromium
npm test
npm run test:browser
```

For Linux OS dependencies use `npx playwright install --with-deps chromium`. For Windows activate `.venv\Scripts\Activate.ps1` and ensure `python3` is on PATH. Browser helpers default to Playwright Chromium. To use installed Chrome, set `PLAYWRIGHT_CHANNEL=chrome`; record the actual version in your evidence. Optional `measure_text_ink.swift` uses Apple Vision and requires macOS; pixel-core measurement and core validators do not.

## Workflow and commands

1. [Generate or reuse a reference and separate assets](references/imagegen-workflow.md).
2. [Extract the six-level design system](references/design-system.md), then measure geometry and typography.
3. Implement editable layers and visible interactions. Keep full reference images outside the runtime page.
4. Populate the [layer manifest](references/layer-manifest.md), asset manifest, tokens, render config and state matrix.
5. Capture, compare and iterate. From this skill directory:

```sh
node scripts/inventory_page.cjs /absolute/path/to/prototype
node scripts/capture_native.cjs /absolute/path/to/prototype playwright home
python3 scripts/validate_manifest.py /absolute/path/to/prototype/layer-manifest.json
python3 scripts/validate_prototype.py /absolute/path/to/prototype
```

Inventory requires `index.html` and `reference/source.png`; it only drafts implementation observations. Capture requires the completed input manifests described in [acceptance](references/acceptance.md). Its state id labels evidence; it does not trigger navigation or a dialog. Use a real browser interaction flow before capturing non-entry states. The reference-sized helper uses DPR=1 and does not apply all render-config environment fields automatically.

Validators need independent reference measurements, runtime hashes, screenshots, ROI comparisons and honest review records. Merely having the files is insufficient. `--structure-only` is diagnostic, not visual acceptance. Read [visual convergence](references/visual-convergence.md) for A/B comparisons and batch workflows.

## Boundaries

The checker can catch stale evidence, missing layers, geometry and image differences; it cannot certify aesthetics, font identity, asset rights or honest visual judgment. Numerical tolerance is not literal pixel identity. Synthetic test fixtures exercise validators and are not reconstructed product screenshots. Flutter handoff is optional and does not establish native-device acceptance.

[MIT](LICENSE). Dependencies and asset rights are described in [third-party notices](THIRD_PARTY_NOTICES.md).
