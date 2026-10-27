# App Dev Skills

[简体中文](README.zh-CN.md)

Use these skills to research competing apps, rebuild interfaces, adapt layouts, create store covers, or build and upload an app. Choose the task below, then give your agent the materials it needs.

## Choose a skill

| Task | Skill | Result |
| --- | --- | --- |
| Research competitors | [app-competitor-analysis](skills/app-competitor-analysis/SKILL.md) | Reports and recommendations for your product |
| Rebuild or refine UI | [image-to-layered-html-prototype](skills/image-to-layered-html-prototype/SKILL.md) | Editable HTML and browser comparisons |
| Adapt for iPhone Duo | [iphone-duo-adaptation](skills/iphone-duo-adaptation/SKILL.md) | Layout analysis, adaptation advice and an interactive prototype |
| Create localized store covers | [app-store-cover-generator](skills/app-store-cover-generator/SKILL.md) | Editable covers and PNGs |
| Build or upload an app | [app-publish-skill](skills/app-publish-skill/SKILL.md) | Local build files and receipts for the requested stage |

## Output previews

**Competitor analysis: HTML report**

![Example Notes report with research navigation and a four-step journey map](skills/app-competitor-analysis/docs/report-example.png)

Browser screenshot of a report built with fictional Example Notes data.

**Store covers: multiple languages and devices**

![English, Chinese and Arabic store covers for iPhone and iPad](skills/app-store-cover-generator/docs/demo-contact.png)

Exported covers made with synthetic app screens and draft translations.

## Use

After installation, attach your materials or provide a project path, then adapt one of the requests below. Say what you want and where the work should stop. The agent will read the skill instructions and check the tools it needs. Include your preferred output language in the request.

- `Use the app-competitor-analysis skill to compare these apps for [product question]. Deliver per-app HTML reports and a comparison index; mark evidence gaps.`
- `Use the image-to-layered-html-prototype skill to rebuild these screenshots as editable HTML. Preserve the design and primary interactions; include browser comparisons.`
- `Use the iphone-duo-adaptation skill to analyze [project path] for iPhone Duo. Recommend minimal layout changes and create a complete interactive HTML prototype.`
- `Use the app-store-cover-generator skill with these screenshots and copy to create editable covers and PNGs for [locales and device sizes].`
- `Use the app-publish-skill skill to build and upload [project path] to TestFlight. Stop at Apple's upload receipt.`

## Install

Install [Node.js 22.20+](https://nodejs.org/en/download), which includes npm/npx. From your project folder, run the command for your agent, select the skills you need and keep the **Project** installation scope.

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

Open the same project folder in WorkBuddy and start a new task. The command installs to [`.agents/skills/`, a project skill directory listed by Tencent Cloud](https://developer.cloud.tencent.com/techpedia/2610). If WorkBuddy does not find the skills, [import](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) the generated `.agents/skills/<skill-name>` folder.

</details>

Start a new chat and use one of the requests above. You can skip installation if the skills are already installed. To use them across projects in Claude Code, Codex or Cursor, add `-g` to the command.

[Troubleshooting](docs/runtime.md) · [Contributing](CONTRIBUTING.md) · [MIT](LICENSE)
