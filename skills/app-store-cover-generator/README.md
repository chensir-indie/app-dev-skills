# App Store Cover Generator

[简体中文](README.zh-CN.md) · [Agent instructions](SKILL.md)

Create editable, localized App Store covers from real app captures and a visual reference.

## Use it

```text
Use $app-store-cover-generator with these captures and reference.
Create 3 slides in en-US and zh-Hans at the supplied dimensions.
Export and visually review all images; stop at local delivery.
```

**Provide:** Real captures, feature claims/copy, visual reference, languages, image dimensions and slide count. Include the current project for revisions.

**Receive:** Editable HTML/CSS, exported PNGs, contact sheets and review records for the requested languages/devices/slides.

Concept-only and focused-fix requests are supported. Existing projects are preserved. Store upload is a separate requested stage.

<details>
<summary>See an example</summary>

![Actual export using synthetic UI and draft translations.](docs/demo-contact.png)

Actual export using synthetic UI and draft translations.

</details>

<details>
<summary>Installation (skip if the collection is installed)</summary>

No extra installation is needed with the collection. To install only this skill, clone the repository outside discovery directories and set the path below to that checkout.

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
# Clone here first if you have no checkout:
# git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
CODEX_SKILL_LINK="${HOME}/.agents/skills/app-store-cover-generator"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing entry: preserve edits and inspect before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/app-store-cover-generator" "$CODEX_SKILL_LINK"
fi
```

Maintain the source; do not copy it into `~/.codex/skills`. Preserve edits and move duplicate copies outside discovery directories when migrating. Refresh Codex if needed and verify one entry. Other agents should retain the complete folder and load `SKILL.md`.

</details>

<details>
<summary>Manual tools and troubleshooting</summary>

## Before running the toolkit

Rendering needs Node.js 22+, npm, Playwright and a usable browser. Run from this skill directory:

```sh
sh scripts/doctor.sh
```

Doctor reports repairs without installing. A standalone skill uses `npm install`; a collection checkout uses `npm ci` at its root. Follow [setup](references/template-contract.md#environment-check-and-setup) and [initialize/preview/export commands](references/template-contract.md#commands). Start from the template only for new work; inspect the exported images before recording review.

</details>

[MIT](LICENSE) · [Asset and dependency notices](THIRD_PARTY_NOTICES.md)
