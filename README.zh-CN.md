# App Dev Skills

**把设计参考变成可编辑页面，再制作多语言商店封面。**

[English](README.md) · [选择技能](#选择技能) · [快速开始](#快速开始) · [环境支持](docs/runtime.zh-CN.md) · [贡献指南](CONTRIBUTING.md)

[![Checks](https://github.com/chensir-indie/app-dev-skills/actions/workflows/check.yml/badge.svg)](https://github.com/chensir-indie/app-dev-skills/actions/workflows/check.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-193d34)](LICENSE)

这是一个可独立安装的 **Agent 技能与配套脚本合集**。按手头材料和目标选择入口；两个技能都能单独使用，无须走完整条流程。

## 选择技能

| 你现在有什么 | 技能与使用说明 | 交付什么 |
| --- | --- | --- |
| 待探索的设计问题、已认可截图或待评审/优化的页面 | [Image to Layered HTML Prototype](skills/image-to-layered-html-prototype/README.zh-CN.md) · [Agent 指令](skills/image-to-layered-html-prototype/SKILL.md) | 按所选分支交付概念/提示词、设计评审/优化，或可编辑 HTML/CSS/SVG、素材、设计标准与浏览器对比 |
| 真实 App 截图、视觉参考、目标语言和尺寸 | [App Store Cover Generator](skills/app-store-cover-generator/README.zh-CN.md) · [Agent 指令](skills/app-store-cover-generator/SKILL.md) | 可编辑封面、语言 × 设备 × 页面 PNG 矩阵、联系表与哈希/审查记录 |

```text
产品简报 → 设计方向或图片提示词
                       ↓ 用户要求重建时继续
认可设计图 → 分层原型与视觉证据
                       ↓ App 实现与设备测试
真实 App 截图 → 多语言封面与导出审查
```

原型不代表 App 已交付；素材导出不代表已经上传或发布。每个阶段分别保留证据与完成标准。

开始或推荐流程前，先读取对应的 `SKILL.md`。各分支何时完成、阶段之间传哪些产物，见[工作流与交接](docs/workflows.zh-CN.md)。本地 checkout 可运行 `python3 scripts/list_skills.py` 查看实际入口，不会安装内容；自动化使用时追加 `--json`。

## 快速开始

### 1. 安装需要的技能

使用 [Skills CLI](https://github.com/vercel-labs/skills)（需要 Node.js 22.20+）查看远程可用技能，再选择安装：

```sh
npx skills@latest add chensir-indie/app-dev-skills --list
npx skills@latest add chensir-indie/app-dev-skills --skill image-to-layered-html-prototype
```

制作商店素材时替换为 `app-store-cover-generator`；重复 `--skill` 可同时安装两项。按提示选择 Agent，全局安装到 Codex 时追加 `-a codex -g`。远程安装使用已发布版本；尚未推送的修改请从本地目录安装。

<details>
<summary>手动安装到 Codex，包括没有 Node.js 的环境</summary>

在技能发现目录之外克隆仓库，再复制单个技能：

```sh
git clone https://github.com/chensir-indie/app-dev-skills.git
mkdir -p ~/.codex/skills
# 仅在目标目录尚不存在时复制。
test ! -e ~/.codex/skills/image-to-layered-html-prototype && \
  cp -R app-dev-skills/skills/image-to-layered-html-prototype ~/.codex/skills/
```

其他技能使用同样方式。保留完整的 `SKILL.md`、脚本、参考和素材；更新前保留本地修改。同一 Agent、同一安装范围只用一种方式，合集根目录不能当作单个 skill 安装。如果 Agent 尚未发现技能，开启新会话再调用。

</details>

### 2. 提供材料并调用

选择对应示例，把范围替换为自己的实际需求：

**还原界面**

```text
用 $image-to-layered-html-prototype 还原这些已认可截图中的全部页面。
文字、背板、图标与素材独立可编辑，重点校准字体、轮廓和遮挡。
提供真实浏览器截图、局部差异与尚未通过的项目。
```

**制作商店封面**

```text
用 $app-store-cover-generator，根据这些真实 App 截图与视觉参考制作六张封面。
覆盖英文、简体中文、日文以及指定的手机/平板尺寸。
先匹配一个母版，再扩展矩阵、导出并审查。
```

### 3. 执行脚本前检查环境

安装技能只会添加指令和文件，Python 与浏览器依赖另行配置。在**已安装的技能目录**运行：

```sh
sh scripts/doctor.sh
```

检查会列出缺少的运行时、依赖包或浏览器支持，给出修复命令，并在必要条件未满足时以失败状态退出；不会自动安装。浏览器工具需要 Node.js 22+、npm 与 Playwright；分层原型的图像和结构检查还需要 Python 3.9+ 及文档列出的依赖包。只做概念设计时可以先推进设计部分。

具体安装、按任务检查和第一条工具命令见各技能 README。维护此仓库时，先按[仓库环境说明](docs/runtime.zh-CN.md)完成配置，再运行 `npm run check`。

## 输出示例

![英文、中文、阿拉伯文在手机与平板上的示例封面导出联系表](skills/app-store-cover-generator/docs/demo-contact.png)

这是内置原创示例的真实工具导出；App UI 为合成示例，翻译为草稿。封面工具提供 50 个语言区域预设与自定义渲染目标，产品文案及商店适用性仍须审查，详见[模板合同](skills/app-store-cover-generator/references/template-contract.md)。

## 下一步

- [环境配置与故障支持](docs/runtime.zh-CN.md)：缺 Python/Node/依赖包/浏览器时如何修复，独立安装和仓库安装的区别、平台支持与定向检查。
- [贡献指南](CONTRIBUTING.md)：独立打包规则、测试和安全样例。
- [工作流与交接](docs/workflows.zh-CN.md)：选择分支、判断完成、把证据带入下一阶段。
- [范围](SCOPE.md)与[共用术语](GLOSSARY.md)：维护边界；[mattpocock/skills 对照报告](docs/mattpocock-skills-comparison-2026-10-20.md)记录来源、取舍和落地结果。
- [原型设计质量评审](skills/image-to-layered-html-prototype/references/design-quality-review.md)：选择一套主规范，按层级、布局与排版改进，用真实截图评审，保留忠实复刻边界。
- [原型设计标准](skills/image-to-layered-html-prototype/references/design-system.md)：几何、图层和组件合同。素材、字体缺失可能阻止逐像素一致，需要保留实际差异。
- [封面本地化](skills/app-store-cover-generator/references/localization.md)：翻译、字体与 RTL。生成图片为可选能力，使用 Agent 环境已有工具及其访问条件。

本仓库沿用 `chensir-indie/app-store-cover-generator` 的 Git 历史。旧克隆应更新 remote，工具工作目录改为 `skills/app-store-cover-generator`；旧版整仓库 skill 安装需要迁移到单个子目录，迁移前保留本地修改。

代码、文档与原创示例素材使用 [MIT](LICENSE)；用户截图、生成素材和第三方字体另有权利边界，见[第三方声明](THIRD_PARTY_NOTICES.md)。
