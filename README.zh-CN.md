# App Dev Skills

[English](README.md)

这套技能可以帮你分析竞品、还原界面、适配布局、制作商店封面，以及打包和上传应用。先按任务选择技能，再把所需材料交给 Agent。

## 选择技能

| 你想做什么 | 技能 | 你会得到什么 |
| --- | --- | --- |
| 分析竞品 | [app-competitor-analysis](skills/app-competitor-analysis/SKILL.md) | 报告与产品建议 |
| 还原或优化界面 | [image-to-layered-html-prototype](skills/image-to-layered-html-prototype/SKILL.md) | 可编辑 HTML 与浏览器对比 |
| 适配 iPhone Duo | [iphone-duo-adaptation](skills/iphone-duo-adaptation/SKILL.md) | 布局分析、适配建议与交互原型 |
| 制作多语言商店封面 | [app-store-cover-generator](skills/app-store-cover-generator/SKILL.md) | 可编辑封面与 PNG |
| 打包或上传应用 | [app-publish-skill](skills/app-publish-skill/SKILL.md) | 本地构建文件与指定阶段的回执 |

## 产物预览

**竞品分析：HTML 报告**

![Example Notes 竞品报告，包含研究导航和四步用户旅程图](skills/app-competitor-analysis/docs/report-example.png)

这是用虚构的 Example Notes 数据制作的报告，图片来自浏览器截图。

**商店封面：多语言、多设备**

![英语、中文和阿拉伯语的 iPhone 与 iPad 商店封面](skills/app-store-cover-generator/docs/demo-contact.png)

这些封面由工具导出，使用的是模拟应用界面和翻译草稿。

## 使用

安装后，附上材料或项目路径，参考下面的示例说明需求。写清楚想完成什么、做到哪一步即可，Agent 会读取技能指令并检查所需工具。希望用中文交付时，也请在请求中说明。

- `用 app-competitor-analysis 技能 分析这些竞品，回答［产品问题］。输出各应用 HTML 报告与对比索引，标明证据缺口。`
- `用 image-to-layered-html-prototype 技能 把这些截图还原成可编辑 HTML，保留原设计与主要交互，提供浏览器对比。`
- `用 iphone-duo-adaptation 技能 分析［项目路径］的 iPhone Duo 适配，以最小布局改动给出建议并制作完整交互 HTML 原型。`
- `用 app-store-cover-generator 技能 根据这些截图和文案，制作［语言和设备尺寸］的可编辑商店封面与 PNG。`
- `用 app-publish-skill 技能 将［项目路径］打包上传 TestFlight，拿到 Apple 上传回执后结束。`

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

安装后新开一个会话，就可以使用上方示例。已经安装过的技能无需重复安装。若想在 Claude Code、Codex 或 Cursor 中跨项目使用，在命令末尾加 `-g`。

[环境排查](docs/runtime.zh-CN.md) · [贡献](CONTRIBUTING.md) · [MIT](LICENSE)
