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

Requires [Node.js 22.20+](https://nodejs.org/en/download) with npm/npx. Run your tool's command from the project folder, select the skills you need and keep the **Project** installation scope.

<details>
<summary><b>Claude Code</b></summary>

```sh
npx skills add chensir-indie/app-dev-skills -a claude-code
```

</details>

<details>
<summary><b>Codex</b></summary>

```sh
npx skills add chensir-indie/app-dev-skills -a codex
```

</details>

<details>
<summary><b>Cursor</b></summary>

```sh
npx skills add chensir-indie/app-dev-skills -a cursor
```

</details>

<details>
<summary><b>WorkBuddy</b></summary>

```sh
npx skills add chensir-indie/app-dev-skills -a universal
```

Open the same project folder in WorkBuddy and start a new task. [Tencent Cloud lists `.agents/skills/` as a project skill directory](https://developer.cloud.tencent.com/techpedia/2610), matching this command’s output. If your client does not discover the skills, [import](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) the generated `.agents/skills/<skill-name>` folder as a fallback.

</details>

Start a new chat and use a request above. Already installed? Skip reinstalling. For global Claude Code, Codex or Cursor installation, add `-g` to the command.

[Troubleshooting](docs/runtime.md) · [Contributing](CONTRIBUTING.md) · [MIT](LICENSE)
