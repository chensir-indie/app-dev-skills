# App Dev Skills

[简体中文](README.zh-CN.md)

Skills for app research, interface reconstruction, layout adaptation, store covers and publication. Pick a task, provide your material and ask your agent.

## Choose a skill

| Task | Skill | Guide and result |
| --- | --- | --- |
| Research competitors | [app-competitor-analysis](skills/app-competitor-analysis/SKILL.md) | [Reports and product decisions](skills/app-competitor-analysis/README.md) |
| Rebuild or refine UI | [image-to-layered-html-prototype](skills/image-to-layered-html-prototype/SKILL.md) | [Editable HTML and browser comparisons](skills/image-to-layered-html-prototype/README.md) |
| Adapt for iPhone Duo | [iphone-duo-adaptation](skills/iphone-duo-adaptation/SKILL.md) | [Layout analysis, advice and interactive prototype](skills/iphone-duo-adaptation/README.md) |
| Create localized store covers | [app-store-cover-generator](skills/app-store-cover-generator/SKILL.md) | [Editable covers and PNGs](skills/app-store-cover-generator/README.md) |
| Build or upload an app | [app-publish-skill](skills/app-publish-skill/SKILL.md) | [Local artifacts and stage receipts](skills/app-publish-skill/README.md) |

## Use

Once installed, attach screenshots, files or a project path in Codex and ask:

```text
Use $image-to-layered-html-prototype to rebuild these screenshots as editable
HTML. Preserve the design and primary interactions; include browser comparisons.
```

Each guide includes a copyable request. Specify your goal and stopping point; the agent reads the instructions and checks the tools needed for that task.

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

</details>

[Troubleshooting](docs/runtime.md) · [Contributing](CONTRIBUTING.md) · [MIT](LICENSE)
