# App Dev Skills

[简体中文](README.zh-CN.md)

Open-source agent skills for turning visual ideas into editable app prototypes and localized App Store artwork. Each skill can be installed and used independently.

## Skills

| Skill | Use it for | Output |
| --- | --- | --- |
| [image-to-layered-html-prototype](skills/image-to-layered-html-prototype/SKILL.md) | Reconstruct approved imagegen designs or screenshots | Design tokens, editable HTML/CSS/SVG layers, real browser captures, region diffs and optional Flutter handoff |
| [app-store-cover-generator](skills/app-store-cover-generator/SKILL.md) | Create store covers from real app captures and a visual reference | Editable cover project, localized/device PNG matrix, contact sheets and review evidence |

A typical workflow is **design reference → layered HTML → app implementation → real app captures → store covers**. The prototype skill supports implementation handoff; these skills do not automatically implement or ship an app. You can enter at either stage.

## Install

With the [Skills CLI](https://github.com/vercel-labs/skills), list available skills, then select either or both:

```sh
npx skills@latest add chensir-indie/app-dev-skills --list
npx skills@latest add chensir-indie/app-dev-skills --skill image-to-layered-html-prototype --skill app-store-cover-generator
```

Choose your agent when prompted. For a global Codex installation, append `-a codex -g`. Skill installation and toolkit dependency installation are separate steps.

For manual installation, clone the repository outside your agent's skills directory and copy the desired **individual** `skills/<name>` directory into its discovery directory. For Codex:

```sh
git clone https://github.com/chensir-indie/app-dev-skills.git
mkdir -p ~/.codex/skills
# First verify this destination does not already exist.
test ! -e ~/.codex/skills/image-to-layered-html-prototype && \
  cp -R app-dev-skills/skills/image-to-layered-html-prototype ~/.codex/skills/
```

Use the same approach for `app-store-cover-generator`. Preserve local changes when updating. Do not install the collection root as a single skill; it intentionally has no `SKILL.md`.

## Use

```text
Use $image-to-layered-html-prototype to reconstruct these approved designs
as editable HTML. Match the typography, irregular panels, icons and layer
order, and show real browser screenshots with remaining differences.
```

```text
Use $app-store-cover-generator with these real app captures and this visual
reference. Create editable covers for my chosen languages and devices,
verify the export matrix, and stop before uploading.
```

Image generation uses the tools available to your agent. Existing references do not require a generation API. Screenshots are never silently substituted for editable UI, and automated checks do not certify visual approval, translation quality or literal pixel identity.

## Run the toolkits

Requirements: Node.js 22+, Python 3.9+, npm and Playwright Chromium. From the repository root:

```sh
npm ci
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r skills/image-to-layered-html-prototype/requirements.txt
npx playwright install chromium
npm run check
```

On Linux, install browser OS dependencies with `npx playwright install --with-deps chromium`. On Windows, activate `.venv\Scripts\Activate.ps1` and provide `python3` on PATH for the npm test commands. The optional Swift/Vision OCR helper requires macOS; it is not required for core validation.

- [Layered HTML setup and commands](skills/image-to-layered-html-prototype/README.md)
- [Store cover setup and commands](skills/app-store-cover-generator/README.md)
- `npm run demo` runs the original cover demo; its UI is synthetic, not a shipped app capture.
- `npm run check` runs packaging checks, both skill test suites and real browser checks. CI only checks the toolkit; it does not package or publish mobile apps.

## Repository layout

```text
skills/
  image-to-layered-html-prototype/  # Self-contained skill, Python + browser tools
  app-store-cover-generator/       # Self-contained skill, starter + export toolkit
scripts/                          # Collection packaging checks
tests/                            # Collection regression tests
```

This collection continues the history of `chensir-indie/app-store-cover-generator`. The cover skill name and `$app-store-cover-generator` invocation remain unchanged. Existing clones should update their remote to this repository, preserve local edits, and use `skills/app-store-cover-generator` as the toolkit working directory. Old whole-repository skill installations should be migrated to the individual skill directory; do not delete an edited installation blindly.

## Contributing and license

See [Contributing](CONTRIBUTING.md). Code, documentation and original bundled demo artwork use the [MIT license](LICENSE). User screenshots, generated artwork and third-party fonts are not implicitly licensed by this repository. See [third-party notices](THIRD_PARTY_NOTICES.md).
