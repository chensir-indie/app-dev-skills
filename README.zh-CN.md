# App Dev Skills

**面向 App 研究、可编辑原型、布局适配与商店交付的可复用 Agent 技能。**

[English](README.md) · [选择技能](#选择技能) · [开始使用](#开始使用) · [文档导航](docs/README.zh-CN.md) · [贡献指南](CONTRIBUTING.md)

[![检查](https://github.com/chensir-indie/app-dev-skills/actions/workflows/check.yml/badge.svg)](https://github.com/chensir-indie/app-dev-skills/actions/workflows/check.yml)
[![MIT 许可](https://img.shields.io/badge/license-MIT-193d34)](LICENSE)

把截图、产品问题与现有 App 项目变成可以检查的成果：有证据的研究报告、可编辑界面、多语言商店素材，以及精确的发布记录。按当前目标选用一个技能即可，无须走完整条流程。

`skills/` 下的每个目录都可独立安装，包含自身指令、参考、检查工具和许可证。技能通过你的 Agent 与已有工具运行；安装本身不会提供模型服务、媒体生成器或移动开发工具链。

## 选择技能

| 你现在有什么 | 技能与使用说明 | 交付什么 |
| --- | --- | --- |
| 竞品截图、录屏、官方资料或已授权分析的文件 | [App Competitor Analysis](skills/app-competitor-analysis/README.zh-CN.md) · [Agent 指令](skills/app-competitor-analysis/SKILL.md) | 每个竞品独立 HTML 与详细 Design.md、带证据的 UI/UX 和功能树/任务流/页面关系/数据流，以及跨竞品索引 |
| 待探索的设计问题、已认可截图或待评审/优化的页面 | [Image to Layered HTML Prototype](skills/image-to-layered-html-prototype/README.zh-CN.md) · [Agent 指令](skills/image-to-layered-html-prototype/SKILL.md) | 按所选分支交付概念/提示词、设计评审/优化，或可编辑 HTML/CSS/SVG、素材、设计标准与浏览器对比 |
| 使用 SwiftUI、UIKit、Flutter、React Native 或 WKWebView 壳、需要适配 iPhone Duo 或动态窗口的 iOS 应用 | [iPhone Duo Adaptation](skills/iphone-duo-adaptation/README.zh-CN.md) · [Agent 指令](skills/iphone-duo-adaptation/SKILL.md) | 全 App 布局分析、全量规则账本、保留原设计的最小必要适配，以及展示具名 Duo 形态和浏览器对比的完整 HTML 原型 |
| 真实 App 截图、视觉参考、目标语言和尺寸 | [App Store Cover Generator](skills/app-store-cover-generator/README.zh-CN.md) · [Agent 指令](skills/app-store-cover-generator/SKILL.md) | 可编辑封面、语言 × 设备 × 页面 PNG 矩阵、联系表与哈希/审查记录 |
| 现有 App，以及打包、上传 TestFlight、商店资料更新或后续发布阶段的明确需求 | [App Publish Skill](skills/app-publish-skill/README.zh-CN.md) · [Agent 指令](skills/app-publish-skill/SKILL.md) | 项目自有 Fastlane 编排、精确源码与产物证据、回执即停的 TestFlight 上传，以及分别限定范围的元信息、截图、验收和提审流程 |

执行前读取对应的 `SKILL.md`。只完成某个阶段、修复现有项目或判断交付是否完整时，参阅[工作流与交接](docs/workflows.zh-CN.md)。

## 输出示例

![合成 App 封面示例的真实导出联系表：英文、中文、阿拉伯文，包含手机和平板尺寸](skills/app-store-cover-generator/docs/demo-contact.png)

这是内置封面工具的真实导出。App UI 为合成示例，翻译为草稿；工具提供 50 个语言区域预设与自定义渲染目标，生产文案和商店适用性仍须审查。[查看封面指南](skills/app-store-cover-generator/README.zh-CN.md)。

## 开始使用

### 1. 让 Codex 直接读取一个源码目录

把仓库保存在技能发现目录之外，通过一个软链接暴露 `skills/`。以下适用于 macOS、Linux 或 WSL 的**首次安装**：

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
mkdir -p "$(dirname "$APP_DEV_SKILLS_DIR")"
git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
```

已有 checkout 时，把 `APP_DEV_SKILLS_DIR` 设为它的绝对路径，跳过克隆。先检查 `~/.agents/skills` 和 `~/.codex/skills` 中的合集及单技能安装，保留本地修改，并把被替换的副本移到这两个发现目录之外。

```sh
CODEX_SKILLS_DIR="${HOME}/.agents/skills"
mkdir -p "$CODEX_SKILLS_DIR"
if [ -e "$CODEX_SKILLS_DIR/app-dev-skills" ] || [ -L "$CODEX_SKILLS_DIR/app-dev-skills" ]; then
  printf '%s\n' 'Existing app-dev-skills entry: inspect it before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills" "$CODEX_SKILLS_DIR/app-dev-skills"
fi
```

命令保留已有入口，包括断开的链接。必要时新开 Codex 会话，确认每个技能只出现一次，并解析到此 checkout。以后直接维护源码，新增技能会随合集一起发现。[完整安装、迁移与其他 Agent](docs/getting-started.zh-CN.md#安装与发现验证)。

### 2. 提供材料并调用

例如，附上已认可的截图，然后提出请求：

```text
用 $image-to-layered-html-prototype 将这些已认可页面还原成可编辑的 HTML/CSS/SVG。
保留原设计与交互，提供真实浏览器截图、测量差异和未完成项。交付说明使用中文。
```

说明材料、范围、交付语言与结束阶段。技能指令和发现元数据使用英文，中文指南及原文证据保留；交付语言由你的需求决定。[复制适合任务的示例](docs/getting-started.zh-CN.md#任务示例)。

### 3. 执行脚本前检查环境

在所选技能目录运行 `sh scripts/doctor.sh`。它会报告缺失依赖和修复命令，不自动安装。按该技能 README 配置所需环境。阅读和规划无需提前装齐渲染工具；开发合集或运行完整检查时，再配置全套仓库环境。

[环境要求与故障排查](docs/runtime.zh-CN.md) · [完成首次任务](docs/getting-started.zh-CN.md#完成首次任务)

## 怎样判断完成

- **研究：**结论可追溯到证据，技术推断与缺失观察明确标注。
- **原型：**提供可编辑源码和真实浏览器检查。原生应用实现与设备验收属于后续阶段。Duo 适配保留原应用设计，默认交付整体布局分析 → 建议 → 完整 HTML 原型；它不是 Apple 官方 App Resizability Skill。
- **素材：**导出、本地化检查与视觉审查覆盖所需矩阵；导出不代表已上传商店。
- **发布：**遵循应用当前发布合同与请求终点。TestFlight 上传在精确产物取得 Apple 成功回执后结束；处理、测试者访问、审核和公开可用分别核验。

详细边界见[范围](SCOPE.md)、[共用术语](GLOSSARY.md)和[工作流](docs/workflows.zh-CN.md)。

## 文档与贡献

- [文档导航](docs/README.zh-CN.md)：用户指南、技术合同与注明日期的验证记录。
- [贡献指南](CONTRIBUTING.md)：仓库结构、独立打包、语言约定与验证要求。
- [问题反馈](CONTRIBUTING.md#questions-and-bug-reports)：排查入口和可复现问题所需信息。
- [安全报告](SECURITY.md)：如何报告漏洞并保护私有数据。

## 许可与来源

合集原创代码、文档与示例素材使用 [MIT](LICENSE)。另行安装的依赖与用户提供的素材保留各自条款，详见[第三方声明](THIRD_PARTY_NOTICES.md)。

本仓库沿用 `chensir-indie/app-store-cover-generator` 的 Git 历史。旧克隆与复制安装可按[迁移指南](docs/getting-started.zh-CN.md#更新与迁移)处理。
