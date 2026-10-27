# App Dev Skills

[English](README.md)

这套技能可以帮你分析竞品、还原界面、适配 iPhone Duo、制作商店封面，以及在本地打包和上传应用。先安装，再把任务交给 Agent，最后通过下方案例了解实际产物。

## 安装

先安装 [Node.js 22.20+](https://nodejs.org/en/download)，其中包含 npm/npx。然后在项目目录中运行所用 Agent 对应的命令，按提示选择技能，安装范围保留 **Project**。

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

在 WorkBuddy 中打开同一项目目录并新建任务。命令会把技能装到[腾讯云列出的项目技能目录 `.agents/skills/`](https://developer.cloud.tencent.com/techpedia/2610)。如果 WorkBuddy 没有识别到技能，可以[导入](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)生成的 `.agents/skills/<skill-name>` 文件夹。

</details>

安装后在同一项目中新开一个会话，就可以使用下方示例。已经安装过的技能无需重复安装。若想在 Claude Code、Codex 或 Cursor 中跨项目使用，在命令末尾加 `-g`。

## 如何使用

1. 在 Agent 中打开你的应用项目，安装技能后新开一个会话。
2. 指明要使用的技能，并提供输入材料：截图、竞品链接、已确认的设计稿或项目路径。
3. 写清楚需要什么结果、使用什么语言、做到哪一步。Agent 会读取技能指令，并检查当前任务需要的工具。

按任务选择技能，复制对应请求并替换方括号中的内容：

| 任务与技能 | 可复制的请求 |
| --- | --- |
| [分析竞品](skills/app-competitor-analysis/SKILL.md) | 用 app-competitor-analysis 技能，根据［应用与证据材料］分析［产品问题］。用中文输出各应用 HTML 报告与对比索引，标明证据缺口。 |
| [还原或优化界面](skills/image-to-layered-html-prototype/SKILL.md) | 用 image-to-layered-html-prototype 技能，把［附上的截图］还原成可编辑 HTML，保留原设计与主要交互，提供浏览器对比。 |
| [适配 iPhone Duo](skills/iphone-duo-adaptation/SKILL.md) | 用 iphone-duo-adaptation 技能，分析［项目路径］的 iPhone Duo 适配，以最小布局改动给出建议并制作完整交互 HTML 原型。 |
| [制作商店封面](skills/app-store-cover-generator/SKILL.md) | 用 app-store-cover-generator 技能，根据［截图和文案］制作［语言和设备尺寸］的可编辑商店封面与 PNG。 |
| [打包或上传应用](skills/app-publish-skill/SKILL.md) | 用 app-publish-skill 技能，将［项目路径］打包上传 TestFlight，拿到 Apple 上传回执后结束。 |

安装技能会添加任务指令。渲染、浏览器检查和移动应用构建可能还需要其他工具；按 Agent 的环境检查提示或所选任务的[运行环境指南](docs/runtime.zh-CN.md)配置即可。

## 使用案例与效果展示

下面两组案例使用仓库内的模拟材料，配图是实际生成的产物，用于展示交付形式，不代表真实竞品结论或已通过商店审核的素材。请求中的路径以本仓库检出目录为基准；如果使用已安装的技能，请替换为实际安装目录。

### 案例一：把竞品研究整理成可阅读的 HTML 报告

**输入材料：**仓库内的 [Example Notes 研究样例](skills/app-competitor-analysis/assets/report-bundle.example.json)，包含虚构应用的分析和任务流程。

**直接这样提需求：**

```text
用 app-competitor-analysis 技能，根据
skills/app-competitor-analysis/assets/report-bundle.example.json
在 ./output/competitor-demo 生成带本地资源链接的 HTML 报告。
保留模拟数据标注与证据缺口，包含报告索引和可视化图谱。
打开生成的报告，检查布局与导航。不要补写真实应用的结论。
```

**会得到：**可整体移动的 HTML 报告文件夹，包含索引、研究章节、关联证据的图谱和本地共享资源。换成你自己的研究时，提供竞品链接或截图，以及要解决的产品问题，由 Agent 先收集证据、撰写分析，再生成报告。

![Example Notes 竞品报告，包含研究导航和四步用户旅程图](skills/app-competitor-analysis/docs/report-example.png)

虚构 Example Notes 报告的实际浏览器截图。[查看原图](skills/app-competitor-analysis/docs/report-example.png)。

### 案例二：制作多语言、多设备的商店封面

**输入材料：**仓库内的[封面起始模板](skills/app-store-cover-generator/assets/starter/)及模拟应用界面。下图展示英语、中文和阿拉伯语在 iPhone 与 iPad 上的封面布局。

**直接这样提需求：**

```text
用 app-store-cover-generator 技能，基于内置起始模板和模拟界面，
在 ./output/store-cover-demo 创建演示封面项目。
制作英语、简体中文和阿拉伯语版本，覆盖 iPhone 与 iPad。
标题保持可编辑，所有翻译标注为草稿。
交付 HTML/CSS 源文件、导出的 PNG 和总览图，
检查文字溢出与阿拉伯语从右向左的布局。不要上传商店。
```

**会得到：**可编辑封面源文件、指定语言与设备组合的 PNG，以及供检查用的总览图。用于自己的应用时，替换成真实截图，提供已确认文案和目标尺寸。

![英语、中文和阿拉伯语的 iPhone 与 iPad 商店封面](skills/app-store-cover-generator/docs/demo-contact.png)

实际导出的封面，使用模拟应用界面和翻译草稿。[查看原图](skills/app-store-cover-generator/docs/demo-contact.png)。

想在本地浏览内置封面演示，可先完成[仓库环境配置](docs/runtime.zh-CN.md)，运行 `npm run demo`，再打开终端打印的网址。按 Ctrl+C 停止预览。

[环境排查](docs/runtime.zh-CN.md) · [贡献](CONTRIBUTING.md) · [MIT](LICENSE)
