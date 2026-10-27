# App Dev Skills

[简体中文](README.zh-CN.md)

Skills for app research, interface reconstruction, layout adaptation, store covers and publication. Pick a task, provide your material and ask your agent.

## Choose a skill

| Task | Skill | Result |
| --- | --- | --- |
| Research competitors | [app-competitor-analysis](skills/app-competitor-analysis/SKILL.md) | Reports and product decisions |
| Rebuild or refine UI | [image-to-layered-html-prototype](skills/image-to-layered-html-prototype/SKILL.md) | Editable HTML and browser comparisons |
| Adapt for iPhone Duo | [iphone-duo-adaptation](skills/iphone-duo-adaptation/SKILL.md) | Layout analysis, advice and interactive prototype |
| Create localized store covers | [app-store-cover-generator](skills/app-store-cover-generator/SKILL.md) | Editable covers and PNGs |
| Build or upload an app | [app-publish-skill](skills/app-publish-skill/SKILL.md) | Local artifacts and stage receipts |

## Output previews

**Competitor analysis — HTML report**

![Example Notes report with research navigation and a four-step journey map](skills/app-competitor-analysis/docs/report-example.png)

Actual browser capture using fictional Example Notes data.

**Store covers — multiple languages and devices**

![English, Chinese and Arabic store covers for iPhone and iPad](skills/app-store-cover-generator/docs/demo-contact.png)

Actual export using synthetic app screens and draft translations.

## Use

Once installed, attach your material or project path and use a request below. Specify the goal and stopping point; the agent reads the instructions and checks the required tools.

- `Use $app-competitor-analysis to compare these apps for [product question]. Deliver per-app HTML reports and a comparison index; mark evidence gaps.`
- `Use $image-to-layered-html-prototype to rebuild these screenshots as editable HTML. Preserve the design and primary interactions; include browser comparisons.`
- `Use $iphone-duo-adaptation to analyze [project path] for iPhone Duo. Recommend minimal layout changes and create a complete interactive HTML prototype.`
- `Use $app-store-cover-generator with these screenshots and copy to create editable covers and PNGs for [locales and device sizes].`
- `Use $app-publish-skill to build and upload [project path] to TestFlight. Stop at Apple's upload receipt.`

## Install

If Codex already uses this checkout, no reinstall is needed.

<details>
<summary>First installation or migration</summary>

### 1. Connect Codex to one source checkout

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
# Skip cloning if you already have a checkout; set its path above.
mkdir -p "$(dirname "$APP_DEV_SKILLS_DIR")"
git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
mkdir -p "$HOME/.agents/skills"
if [ -e "$HOME/.agents/skills/app-dev-skills" ] || [ -L "$HOME/.agents/skills/app-dev-skills" ]; then
  printf '%s\n' 'Existing entry: preserve edits and inspect before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills" "$HOME/.agents/skills/app-dev-skills"
fi
```

For macOS/Linux/WSL. Use your existing checkout path and skip cloning when applicable. Maintain one source and one discovery link; do not copy into `~/.codex/skills`. Preserve edits and move duplicate copies outside discovery directories before migration. Refresh Codex if needed and verify one entry per skill. Other agents should retain each chosen skill folder and load `SKILL.md`.

To install just one skill, use `skills/<name>` as the symlink source and `~/.agents/skills/<name>` as its destination in the command above. Choose either collection or single-skill discovery so each skill appears once.

</details>

[Troubleshooting](docs/runtime.md) · [Contributing](CONTRIBUTING.md) · [MIT](LICENSE)
