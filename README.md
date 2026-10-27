# App Dev Skills

![App Dev Skills — From evidence to delivery](docs/assets/app-dev-skills-cover.png)

[简体中文](README.zh-CN.md)

**App Dev Skills is a coordinated suite of agent skills for the app development workflow**, covering key stages from competitor research and interface prototyping to device adaptation, store artwork, and local builds/uploads.

Competitor research → Editable interface prototypes → iPhone Duo adaptation → Store covers → Local builds and uploads

Use the skills together as your project progresses, or install an individual skill for the stage you need. Give your agent a task with the relevant inputs and desired result; the examples below show what each skill produces.

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

Start a new chat in the same project and use one of the requests below. You can skip installation if the skills are already installed. To use them across projects in Claude Code, Codex or Cursor, add `-g` to the command.

## How to use

1. Open your app project in your agent and start a new chat after installation.
2. Name the skill and supply the input: screenshots, competitor links, approved designs, or a project path.
3. State the result you need, your preferred output language, and where the work should stop. The agent reads the skill and checks the tools needed for that task.

Choose a task and copy its request, replacing the bracketed inputs:

| Task and skill | Copyable request |
| --- | --- |
| [Research competitors](skills/app-competitor-analysis/SKILL.md) | Use the app-competitor-analysis skill to compare [apps and evidence] for [product question]. Deliver per-app HTML reports and a comparison index in English; mark evidence gaps. |
| [Rebuild or refine UI](skills/image-to-layered-html-prototype/SKILL.md) | Use the image-to-layered-html-prototype skill to rebuild [attached screenshots] as editable HTML. Preserve the design and primary interactions; include browser comparisons. |
| [Adapt for iPhone Duo](skills/iphone-duo-adaptation/SKILL.md) | Use the iphone-duo-adaptation skill to analyze [project path] for iPhone Duo. Recommend minimal layout changes and create a complete interactive HTML prototype. |
| [Create store covers](skills/app-store-cover-generator/SKILL.md) | Use the app-store-cover-generator skill with [screenshots and copy] to create editable covers and PNGs for [locales and device sizes]. |
| [Build or upload an app](skills/app-publish-skill/SKILL.md) | Use the app-publish-skill skill to build and upload [project path] to TestFlight. Stop at Apple's upload receipt. |

Installation adds the skill instructions. Rendering, browser checks, and mobile builds may need additional tools; follow the agent's environment check or the [runtime guide](docs/runtime.md) for the selected task.

## Usage examples and results

These two examples use bundled synthetic materials and actual generated previews. They demonstrate the output format, not findings about a real competitor or store-approved artwork. The paths in the requests below assume a checkout of this repository; for an installed skill, provide its actual directory instead.

### Example 1: Turn competitor research into a readable HTML report

**Input:** the bundled [Example Notes research bundle](skills/app-competitor-analysis/assets/report-bundle.example.json), containing fictional app analysis and task flows.

**Request:**

```text
Use the app-competitor-analysis skill with
skills/app-competitor-analysis/assets/report-bundle.example.json
to generate a linked HTML report in ./output/competitor-demo.
Keep the synthetic-data labels and evidence gaps. Include the report index
and visual maps, and open the generated report to check its layout and navigation.
Do not add findings about real apps.
```

**Result:** a portable HTML report folder with an index, research chapters, evidence-linked maps, and shared local assets. For your own study, supply competitor links/screenshots and a product question; the agent must gather and author the analysis before rendering it.

![Example Notes report with research navigation and a four-step journey map](skills/app-competitor-analysis/docs/report-example.png)

Actual browser screenshot of the fictional Example Notes report. [View full-size image](skills/app-competitor-analysis/docs/report-example.png).

### Example 2: Create store covers for several languages and devices

**Input:** the bundled [cover starter](skills/app-store-cover-generator/assets/starter/) and its synthetic app screens. The preview below shows English, Chinese, and Arabic across iPhone and iPad layouts.

**Request:**

```text
Use the app-store-cover-generator skill to create a demo cover project
in ./output/store-cover-demo using the bundled starter and synthetic screens.
Create English, Simplified Chinese, and Arabic variants for iPhone and iPad.
Keep headings editable and label all translations as drafts.
Deliver HTML/CSS source, exported PNGs, and contact sheets;
check text overflow and Arabic right-to-left layout. Do not upload to a store.
```

**Result:** editable cover source, PNGs for the requested language/device combinations, and contact sheets for review. For your own app, replace the synthetic screens with real captures and supply approved copy and target dimensions.

![English, Chinese and Arabic store covers for iPhone and iPad](skills/app-store-cover-generator/docs/demo-contact.png)

Actual exported covers using synthetic app screens and draft translations. [View full-size image](skills/app-store-cover-generator/docs/demo-contact.png).

To explore the bundled cover demo locally, follow the [repository setup](docs/runtime.md#set-up-the-repository), run `npm run demo`, and open the URL printed in the terminal. Stop the preview with Ctrl+C.

[Troubleshooting](docs/runtime.md) · [Contributing](CONTRIBUTING.md) · [MIT](LICENSE)
