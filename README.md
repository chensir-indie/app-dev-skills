# App Store Cover Generator

[简体中文](README.zh-CN.md) · [Agent instructions](SKILL.md)

A reusable Codex skill and small working toolkit for **AI artwork + editable web layouts + multilingual screenshot exports**.

AI can produce a convincing concept, but baked-in text, inconsistent font sizing and expensive per-language regeneration make it hard to ship. This skill assigns each part a clear owner: generated art for material and composition, HTML/CSS for copy and geometry, browser checks for repeatable quality evidence.

![Synthetic demo contact sheet](docs/demo-contact.png)

The preview is original demo art with synthetic UI. It is not a real product capture or the final visual style required for your app. [See the original NextNote example](https://x.com/NextNote_App/status/2100984993619366199).

## What is included

- Reference decomposition and editable-layer prompt recipes.
- Typography, localization, RTL and motion-feature guidance.
- A working HTML/CSS/JS starter with 3 locales, 2 devices and 2 slides.
- Safe local preview, fresh-directory initialization and batch PNG export.
- Geometry/overflow checks, exact matrix verification, SHA-256 manifests and contact sheets.
- Honest visual-review and store/publication boundaries.
- Unit and real-browser failure tests.

There is no paid API requirement. AskMATT and image-generation tools are optional integrations supplied by your agent environment. No undocumented provider API, store uploader or automatic social publisher is included.

## Install as a Codex skill

Clone into a **new** skill directory:

```sh
git clone https://github.com/chensir-indie/app-store-cover-generator.git ~/.codex/skills/app-store-cover-generator
```

If this path already exists, back it up or merge intentionally; do not delete an existing local skill blindly. Start a new Codex task if the skill is not discovered immediately, then ask:

> Use $app-store-cover-generator. Match this reference with my real app screenshots. Build six covers in English, Chinese and Japanese for the iPhone and iPad slots I specify. Keep text editable, show one master before expanding, audit every locale and export the matrix. Stop before uploading.

Agent-specific tools are not required to run the included standalone demo.

## Run the toolkit

Requirements: Node.js 22+, npm and a Playwright Chromium installation. Linux may need OS browser dependencies (`npx playwright install --with-deps chromium`).

```sh
npm ci
npx playwright install chromium
node scripts/init.mjs /tmp/my-covers
node scripts/serve.mjs /tmp/my-covers
# Open the printed loopback URL. Edit /tmp/my-covers/project.json and style.css.
node scripts/export.mjs /tmp/my-covers /tmp/my-covers-output-01
node scripts/verify.mjs /tmp/my-covers-output-01
```

Outputs contain individual PNGs, locale/device contact sheets and manifest.json. Every run needs a fresh output directory outside the source tree. `automated-pass` still leaves `visualReview: pending`.

Supply your own licensed fonts and real screenshots for production. The demo uses system fonts, so cross-OS pixel identity is not promised. Supported dimensions in the schema are safety bounds, not an App Store eligibility table. Confirm [Apple's current screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications) for your app.

## Customize

1. Freeze your customer benefit, real feature set, story order and locale/device slots.
2. Adapt the copied starter or reuse an existing web template using the [rendering contract](references/template-contract.md).
3. Put rights-cleared assets/fonts in media/ and provide every locale's copy explicitly.
4. Match one master at equal reference/render size, then expand the matrix.
5. Export, inspect every contact-sheet cell and review native PNGs. Record visual approval separately.

Read [prompt recipes](references/art-direction.md), [localization](references/localization.md) and [quality limits](references/quality-gates.md).

## Development

```sh
npm test
npm run test:browser
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for scoped changes and failure-oriented tests. GitHub CI runs tests only; it never packages apps, uploads store assets or publishes posts.

## License and attribution

MIT for the code, documentation and original demo SVG in this repository. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). External NextNote screenshots and trademarks are not included in that grant. Bring assets you have permission to use. No Apple, OpenAI, AskMATT or NextNote endorsement is implied.
