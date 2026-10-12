# App Store Cover Generator

[简体中文](README.zh-CN.md) · [Skill instructions](SKILL.md)

**A product-agnostic, open-source skill for creating editable, multilingual App Store covers.**

Use this skill when an AI concept looks good but the web version loses its typography, spacing or detail—or when a finished design needs to work across languages and devices. Match one master, keep the words editable, then export and check the whole set.

![Original demo artwork with synthetic UI](docs/demo-contact.png)

This is the bundled demo with fictional branding and synthetic UI. Use your own app name, features, captures and visual direction. Slide count, device sizes, languages, palette and typography are project choices; the demo is not a required style.

## Install

Use the [Skills CLI](https://github.com/vercel-labs/skills) from your project directory:

```sh
npx skills@latest add chensir-indie/app-store-cover-generator --skill app-store-cover-generator
```

Choose your coding agent when prompted. Installation is project-local by default; add `-g` to make it available across projects. For global Codex installation:

```sh
npx skills@latest add chensir-indie/app-store-cover-generator --skill app-store-cover-generator -a codex -g
```

Use one installation method per agent and scope. If you already cloned this skill manually, update that copy instead of installing a duplicate. Installing the skill adds instructions and supporting files; it does not install Chromium or call an image-generation service.

<details>
<summary>Manual Codex installation</summary>

Clone into a new directory. Preserve any existing local edits first.

```sh
git clone https://github.com/chensir-indie/app-store-cover-generator.git ~/.codex/skills/app-store-cover-generator
```

For a clean clone, update with `git -C ~/.codex/skills/app-store-cover-generator pull --ff-only`. If you customized the files, review and merge updates intentionally.

</details>

For a Skills CLI installation, update with:

```sh
npx skills@latest update app-store-cover-generator
```

If the skill does not appear, check the installer's destination and open a new agent session. Do not install a second copy as a workaround.

## Try it

Attach a visual reference and real app screenshots, then ask your agent:

> Use $app-store-cover-generator. Create six App Store covers from these screenshots and this reference. First match one master at the same size. Then localize it for en-US, zh-Hans, ja and ar-SA in my iPhone and iPad slots. Keep headings editable, check text overflow and feature details, and export the complete set. Stop before uploading.

For an existing design:

> Use $app-store-cover-generator to audit my cover project. Check font consistency, clipped text and missing translations across every locale and device. Fix the affected covers while preserving the approved design.

Provide your app's actual features, intended slide order and target dimensions when available. The agent should reuse existing assets and ask only about missing decisions that matter.

## What you get

| Need                  | How the skill helps                                                                 |
| --------------------- | ----------------------------------------------------------------------------------- |
| Match an AI reference | Measure type, spacing, crop and materials; generate difficult art layers separately |
| Reuse the design      | Editable HTML/CSS, explicit copy and one canonical slide order                      |
| Localize covers       | 50 App Store locale presets, custom BCP 47 tags, script-aware font stacks and RTL   |
| Catch broken layouts  | Native-size export, overflow/collision checks and exact rendered-copy checks        |
| Review the whole set  | Individual PNGs, locale/device contact sheets and a hash manifest                   |

Generated art is optional. The toolkit does not call a paid API, translate your product automatically, upload to a store or publish social posts. Use whichever image tool your agent actually provides. Automated checks do not establish visual fidelity, translation quality or store approval.

## Languages and regions

The [catalog](assets/locales/app-store.json) covers the **50 language/region options** on [Apple's localization page](https://developer.apple.com/help/app-store-connect/reference/app-information/app-store-localizations/) checked on October 12, 2026. Regional variants remain separate: `en-US`/`en-GB`, `fr-FR`/`fr-CA`, `pt-BR`/`pt-PT`, and simplified/traditional Chinese.

Custom BCP 47 tags such as `fa-IR` and `sw-KE` are accepted for local cover projects. A custom tag is not proof of an App Store upload slot. Countries, storefronts and languages are different concepts; choose the locales enabled for your app.

The starter ships **three translated demo locales**, not 50 finished translations. Expanding a project creates empty copy fields while preserving existing text. Fill them explicitly; the exporter rejects missing translations instead of substituting English. Fonts are selected by script, but you must supply and inspect licensed fonts for your actual content. See [localization and font guidance](references/localization.md).

## Run the toolkit yourself

Requirements: Node.js 22+, npm, and Playwright Chromium. These steps use a separate working clone; choose a new directory name if it already exists.

```sh
git clone https://github.com/chensir-indie/app-store-cover-generator.git
cd app-store-cover-generator
npm ci
npx playwright install chromium
node scripts/init.mjs /tmp/my-covers
node scripts/serve.mjs /tmp/my-covers
```

Open the printed local URL. Edit the copied `project.json`, `style.css` and `media/` assets. Stop the preview with Ctrl+C when finished. Linux may need `npx playwright install --with-deps chromium`.

To add all store locales—or a selected list—to a **new** project copy:

```sh
node scripts/locales.mjs list
node scripts/locales.mjs add /tmp/my-covers /tmp/my-global-covers app-store
# Alternative: use ja,fr-FR,ar-SA,fa-IR instead of app-store.
# Fill the empty translations in /tmp/my-global-covers/project.json, then:
node scripts/locales.mjs check /tmp/my-global-covers
node scripts/export.mjs /tmp/my-global-covers /tmp/my-global-covers-output-01
node scripts/verify.mjs /tmp/my-global-covers-output-01
```

For the unchanged three-language demo, export `/tmp/my-covers` directly. Initialization and export refuse to overwrite existing directories. Each export needs a fresh output directory outside the source project.

An `automated-pass` still leaves `visualReview: pending`. Use `node scripts/review.mjs init OUTPUT REVIEW.json` to create the pending checklist, inspect and fill every cell, then run `node scripts/review.mjs check OUTPUT REVIEW.json`. This checks completeness and binds the record to that export; it does not judge the images for you. Inspect every contact sheet and native PNG. The starter uses system fonts, so different operating systems can produce different pixels; pin licensed local fonts for production. Device dimensions must match [Apple's current screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications).

## Reference and development

- [Art direction and prompts](references/art-direction.md)
- [Localization, typography and motion](references/localization.md)
- [Project schema and rendering contract](references/template-contract.md)
- [Quality checks and limitations](references/quality-gates.md)
- [Store handoff boundaries](references/delivery.md)

```sh
npm run check
```

See [CONTRIBUTING.md](CONTRIBUTING.md). CI tests the toolkit; it does not package or release an app. The description and installation structure take inspiration from [mattpocock/skills](https://github.com/mattpocock/skills).

## License

MIT for this repository's code, documentation and original demo SVG. External app screenshots, trademarks and third-party fonts retain their own rights. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
