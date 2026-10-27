# App Competitor Analysis

[简体中文](README.zh-CN.md) · [Agent instructions](SKILL.md)

Understand competitor apps and turn evidence into product decisions.

## Use it

```text
Use $app-competitor-analysis to compare these apps for my product decision.
Deliver an HTML report per app and a comparison index. Mark evidence gaps.
```

**Provide:** Competitor names/links, screenshots or recordings, and the product question you want answered.

**Receive:** Per-app HTML, a comparison index, four visual maps and evidence-linked recommendations. Detailed UI analysis also produces Design.md. Keep the delivered assets folder beside the HTML.

Name a narrow question if you do not need a full study. Missing evidence stays explicit.

<details>
<summary>See an example</summary>

![Renderer output using fictional Example Notes data.](docs/report-example.png)

Actual Chrome capture of `assets/report-bundle.example.json`, generated on 2026-10-27 using fictional Example Notes data. The original example and image use [MIT](LICENSE); host-system fonts are rendered, not redistributed as font files.

</details>

<details>
<summary>Installation (skip if the collection is installed)</summary>

No extra installation is needed with the collection. To install only this skill, clone the repository outside discovery directories and set the path below to that checkout.

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
# Clone here first if you have no checkout:
# git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
CODEX_SKILL_LINK="${HOME}/.agents/skills/app-competitor-analysis"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing entry: preserve edits and inspect before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/app-competitor-analysis" "$CODEX_SKILL_LINK"
fi
```

Maintain the source; do not copy it into `~/.codex/skills`. Preserve edits and move duplicate copies outside discovery directories when migrating. Refresh Codex if needed and verify one entry. Other agents should retain the complete folder and load `SKILL.md`.

</details>

<details>
<summary>Manual tools and troubleshooting</summary>

## Run the helpers

Python 3.9+ is needed only for bundled rendering/audit tools. Run from this skill directory; use the interpreter reported by doctor. No pip packages are required for core helpers.

```sh
sh scripts/doctor.sh
python3 scripts/render_reports.py assets/report-bundle.example.json --output /tmp/teardown-demo --format linked
```

The command renders a synthetic example to a **new** directory. Open its index.html. For real work, follow [HTML delivery](references/html-delivery.md); the agent authors the analysis before rendering. Browser review remains required.

</details>

[MIT](LICENSE)
