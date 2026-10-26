# iPhone Duo 适配

[English](README.md) · [Agent 工作流](SKILL.md)

面向已有 App，默认先分析全应用布局，再给出适配建议，最终交付完整可交互 HTML。保留原设计，以必要的最小改动适配。支持 SwiftUI、UIKit、Flutter、React Native/Expo 及 WKWebView 壳；其他框架先保留共享设计与 HTML 路径，不虚构引擎 API。

这是社区工作流。中文页面是面向使用者的指南；Skill 指令、元数据、技术引用、规则目录和生成的规则 Markdown 继续保持英文，产品 UI 按目标 App 与用户要求使用相应语言。

## 输入 → 流程 → 交付

![Duo 适配流程示意：原始窄屏界面与保留同一草稿的宽屏布局](docs/workflow.svg)

*合成 UI 的 HTML 布局示意。宽屏排列只是设计选择示例，不是强制分栏、设备规格或原生真机结果。*

### 准备哪些输入

| 输入 | 需要提供什么 |
| --- | --- |
| 当前 App | 仓库或可运行界面、当前截图/录屏及已知框架；标出无法访问的页面。 |
| 覆盖范围 | 全部已知页面、导航、共享组件与主要任务，包含草稿、弹层和返回路径。 |
| 设计约束 | 需要保留的 tokens、文案与组件，以及明确授权的设计改动。 |
| 评审条件 | 可用设备/模拟器参考、目标场景、产出语言和终点；假设持续标明。 |

### 一项任务如何完成

示例：适配笔记 App，保留列表、编辑器和草稿；切换适用评审场景时，选中的笔记和未保存文字不丢失。

| 步骤 | 处理什么 | 产生什么 |
| --- | --- | --- |
| 1. 清点全应用 | 识别框架，对照原 App 检查每个已知页面与任务。 | 布局基线、覆盖矩阵、保留/适配/改动决策。 |
| 2. 绑定并冻结 | 逐条判断目录规则，施工前填入适用决策、计划目标和项目约定。 | 填实的 JSON 台账、生成的 Markdown、设计建议和冻结交接包。 |
| 3. 构建原型 | 可用时使用已发现的 BUILD WEB APPS 路线；保留可编辑本地源码，准确记录回退路径。 | 设计连续、主要任务可用的完整交互 HTML。 |
| 4. 操作验证 | 切换适用的内外屏方向、左右分屏及部分折叠场景，检查键盘、文字与弹层。 | 浏览器截图、同状态原始/适配对照和状态连续性记录。 |
| 5. 回填验收 | 将实际证据关联规则编号，修复差异，记录后续原生阶段事项。 | 检查过的台账、评审后的原型和明确限制。 |

### 交付后如何使用

目标 App 默认包含 `docs/iphone-duo-adaptation/workspace-rules.json` 及生成的 `.md`，另附布局/设计分析、可编辑 `index.html` 与相对路径素材、实际浏览器证据。原型目录可沿用项目约定；不要求先转换生产框架。

打开交付的本地原型，操作主要任务，切换评审场景并检查选中项、草稿和相关滚动位置；与原 App 的同页面同状态对照。评审控制应在 App 界面之外。[工作区规则](README.md#materialize-every-rule-in-the-app-workspace)提供台账命令，[运行环境](README.md#runtime-and-evidence)说明依赖。

**完成标准：** 默认 HTML 范围覆盖全应用并有实际交互/视觉证据，全部目录规则都有记录。台账检查只验证记录完整性；HTML 不证明原生保留区域支持或真机验收。明确仅分析的任务在构建前结束。

## 安装与第一次调用

已有合集源码链接会自动发现本技能，无需重复安装。单独安装时参考[单一源码安装](README.md#install-from-one-source)，保留现有修改并确认只有一个发现入口。

```text
使用 $iphone-duo-adaptation 分析这个现有 iOS App。
先识别 UI 框架并清点全部页面和任务，再按 Apple iPhone HIG 给出有依据的适配意见。
保留原设计，交付完整可交互 HTML、逐条规则台账、同状态原始/适配对照
和实际浏览器验证。此次以 HTML 交付为终点。
```

在技能目录运行 `sh scripts/doctor.sh`；完整[安装和环境说明](README.md#runtime-and-evidence)在英文指南。Python 3.9+ 用于标准库规则工具；只读指令可使用 `--scope instructions`。本包不内置渲染运行时，浏览器检查需要 Agent 或项目现有工具；缺少 Xcode 不阻塞独立的 HTML 工作。

## 按任务深入

- [全应用布局分析](references/layout-analysis.md)与[最小迁移](references/migration-review.md)
- [工作区规则合同](references/workspace-rules.md)与[项目约定](references/project-conventions.md)
- [BUILD WEB APPS 交接](references/build-web-apps.md)、[设备展示](references/device-presentation.md)与[HTML 合同](references/html-prototype.md)
- [框架识别](references/frameworks.md)、[官方依据](references/official-basis.md)与[验证边界](references/validation.md)

原创工作流采用 [MIT](LICENSE)。外部 Apple、Flutter、React Native、Expo 和 MDN 资料保留各自条款。
