# Image to Layered HTML Prototype

[简体中文](README.zh-CN.md) · [Agent instructions](SKILL.md)

Turn approved app screenshots into editable, interactive HTML, or refine an existing page.

## Use it

```text
Use $image-to-layered-html-prototype to rebuild these screens as editable HTML.
Preserve the design, connect the primary actions and show browser comparisons.
```

**Provide:** Original page images, available assets/fonts and required interactions. For repairs, include the existing HTML.

**Receive:** Editable HTML/CSS/SVG, separate assets, working interactions and per-page comparison evidence.

You can ask only for concepts, prompts or a review. Approved references remain fixed during faithful reconstruction; a full-screen image with hotspots is not an editable result.

<details>
<summary>Installation (skip if the collection is installed)</summary>

No extra installation is needed with the collection. To install only this skill, clone the repository outside discovery directories and set the path below to that checkout.

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
# Clone here first if you have no checkout:
# git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
CODEX_SKILL_LINK="${HOME}/.agents/skills/image-to-layered-html-prototype"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing entry: preserve edits and inspect before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/image-to-layered-html-prototype" "$CODEX_SKILL_LINK"
fi
```

Maintain the source; do not copy it into `~/.codex/skills`. Preserve edits and move duplicate copies outside discovery directories when migrating. Refresh Codex if needed and verify one entry. Other agents should retain the complete folder and load `SKILL.md`.

</details>

<details>
<summary>Manual tools and troubleshooting</summary>

## Environment check and setup

Run from this skill directory. Capture needs Python 3.9+, Node.js 22+, npm, Playwright and a browser; measurement/validation additionally uses Pillow and PyYAML. Concepts need no rendering setup.

```sh
sh scripts/doctor.sh
# For a standalone installation when dependencies are missing:
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
npm install
npx --no-install playwright install chromium
sh scripts/doctor.sh
```

In a collection checkout use `npm ci` at the repository root instead of standalone `npm install`. Use `--scope python` or `--scope browser` for narrower checks. Python is needed in both scopes. Installed Chrome can be selected with `PLAYWRIGHT_CHANNEL=chrome` for doctor and capture. Use macOS/Linux or WSL; follow doctor output for missing runtimes and browser libraries. Keep dependent acceptance pending until repaired.

</details>

[MIT](LICENSE) · [Asset and dependency notices](THIRD_PARTY_NOTICES.md)
