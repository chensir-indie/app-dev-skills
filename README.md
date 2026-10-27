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

- `Use the app-competitor-analysis skill to compare these apps for [product question]. Deliver per-app HTML reports and a comparison index; mark evidence gaps.`
- `Use the image-to-layered-html-prototype skill to rebuild these screenshots as editable HTML. Preserve the design and primary interactions; include browser comparisons.`
- `Use the iphone-duo-adaptation skill to analyze [project path] for iPhone Duo. Recommend minimal layout changes and create a complete interactive HTML prototype.`
- `Use the app-store-cover-generator skill with these screenshots and copy to create editable covers and PNGs for [locales and device sizes].`
- `Use the app-publish-skill skill to build and upload [project path] to TestFlight. Stop at Apple's upload receipt.`

## Install

Choose your tool below. Install the complete skill folder, including its scripts, references and assets. Keep the source checkout for updates.

First clone once (or use your existing checkout). The terminal commands below are for macOS/Linux; use them in WSL only when the agent runs in that same WSL environment. Continue in the same terminal.

```sh
APP_DEV_SKILLS_DIR="$HOME/src/app-dev-skills"
# Already cloned? Set the existing path above and skip git clone.
mkdir -p "$(dirname "$APP_DEV_SKILLS_DIR")"
git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
```

<details>
<summary><b>Claude Code</b></summary>

Link one selected skill for all local projects:

```sh
APP_DEV_SKILL="iphone-duo-adaptation" # Choose a name from the table.
APP_DEV_SKILL_LINK="$HOME/.claude/skills/$APP_DEV_SKILL"
mkdir -p "$(dirname "$APP_DEV_SKILL_LINK")"
if [ -e "$APP_DEV_SKILL_LINK" ] || [ -L "$APP_DEV_SKILL_LINK" ]; then
  printf '%s\n' 'Already exists: inspect it; existing files are preserved.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/$APP_DEV_SKILL" "$APP_DEV_SKILL_LINK"
fi
```

Start a new session and type `/iphone-duo-adaptation`, or describe the task. Change the name above to install another skill. [Claude Code skill directories](https://code.claude.com/docs/en/skills#choose-where-skills-load).

</details>

<details>
<summary><b>Codex</b></summary>

Link the full collection once. If this checkout is already connected, skip this step.

```sh
APP_DEV_SKILL_LINK="$HOME/.agents/skills/app-dev-skills"
mkdir -p "$(dirname "$APP_DEV_SKILL_LINK")"
if [ -e "$APP_DEV_SKILL_LINK" ] || [ -L "$APP_DEV_SKILL_LINK" ]; then
  printf '%s\n' 'Already exists: inspect it; existing files are preserved.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills" "$APP_DEV_SKILL_LINK"
fi
```

Start a new session and select a skill with `$`, for example `$iphone-duo-adaptation`. Keep one collection link; do not also install individual copies in `~/.codex/skills`. [Codex skill discovery](https://developers.openai.com/codex/skills).

</details>

<details>
<summary><b>Cursor</b></summary>

Local Cursor also reads `~/.agents/skills/`. If you installed the collection for Codex, reuse that installation; otherwise run:

```sh
APP_DEV_SKILL_LINK="$HOME/.agents/skills/app-dev-skills"
mkdir -p "$(dirname "$APP_DEV_SKILL_LINK")"
if [ -e "$APP_DEV_SKILL_LINK" ] || [ -L "$APP_DEV_SKILL_LINK" ]; then
  printf '%s\n' 'Already exists: inspect it; existing files are preserved.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills" "$APP_DEV_SKILL_LINK"
fi
```

Start a new session, type `/` and select the skill. Avoid duplicate installations in `.cursor/skills` or `.claude/skills` when the same skill is already discovered. This setup is for local agents; cloud sessions need their own skills. [Cursor skill directories](https://cursor.com/docs/skills).

</details>

<details>
<summary><b>WorkBuddy</b></summary>

1. Open **Experts · Skills · Connectors → Skills → Add skill → Upload skill**.
2. Select one complete folder from the checkout, such as `skills/iphone-duo-adaptation`. Import the skill folder, not the whole repository or just `SKILL.md`.
3. Confirm it appears and is enabled under **Installed**, then ask WorkBuddy to use that skill by name.

You can also download and extract the repository ZIP from GitHub's **Code → Download ZIP** without a terminal. Reimport from the source after updates. [WorkBuddy import guide](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market).

</details>

Check that each selected skill appears once. Tool installation does not install rendering or mobile build dependencies; the agent checks those when the task needs them.

[Troubleshooting](docs/runtime.md) · [Contributing](CONTRIBUTING.md) · [MIT](LICENSE)
