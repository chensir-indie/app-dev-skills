# App Dev Skills

**把设计参考变成可编辑页面，再把真实 App 截图变成多语言商店封面。**

[English](README.md) · [快速开始](#快速开始) · [技能选择](#选择合适的技能) · [调用示例](#调用示例) · [贡献指南](CONTRIBUTING.md)

[![Checks](https://github.com/chensir-indie/app-dev-skills/actions/workflows/check.yml/badge.svg)](https://github.com/chensir-indie/app-dev-skills/actions/workflows/check.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-193d34)](LICENSE)

![设计参考到分层 HTML；独立完成 App 实现后，以真实截图制作商店封面](docs/assets/workflow.svg)

这是一个 **Agent 指令 + 可运行工具**的开源合集，面向独立开发者、App 团队和与编码 Agent 协作的设计师。两个技能分别处理“设计图落地”和“商店素材交付”，可以单独安装，不绑定某个产品或视觉风格。

## 为什么做这个项目

AI 生成的设计图很好看，落成页面时却常常变了样：字体比例不对、图标不一致、异形背板变成圆角矩形、主体被错误遮挡。到了商店封面阶段，换一种语言又可能出现换行、字号与设备裁切不统一。

App Dev Skills 把这两段流程拆成可执行、可检查的步骤：

- **保持可编辑：** 文字用 DOM，背板与图标用 CSS/SVG，照片和主体是独立素材。
- **用实际证据检查：** 浏览器原尺寸截图、几何测量、局部差异与可见交互结果。
- **跨产品复用：** 品牌、内容、语言、设备尺寸来自项目输入，共享变量与组件负责一致性。
- **如实报告完成度：** 自动校验、视觉审查、原生实现和发布分别记录。

## 选择合适的技能

| | 分层 HTML 原型 | App Store 封面生成 |
| --- | --- | --- |
| **名称** | [`image-to-layered-html-prototype`](skills/image-to-layered-html-prototype/SKILL.md) | [`app-store-cover-generator`](skills/app-store-cover-generator/SKILL.md) |
| **输入** | 已认可的 imagegen 图、截图，可附已有 HTML | 真实 App 截图、视觉参考、语言与设备尺寸 |
| **过程** | 测量 → 拆素材 → 分层实现 → 对照 → 校准 | 匹配母版 → 本地化 → 批量导出 → 审查 |
| **输出** | HTML/CSS/SVG、设计规范、独立素材、截图与差异记录 | 可编辑封面工程、PNG 矩阵、联系表、哈希与审查记录 |
| **适合解决** | 字体、异形背板、图标、层级与遮挡不一致 | 多语言、多尺寸、多个封面之间的视觉不一致 |
| **后续阶段** | 可移交 Flutter；原生实现与设备验证另行执行 | 产品审查后交付素材；不自动上传商店 |

## 具体功能

### 1. 从平面设计图到分层页面

- 提取**六级设计标准**：视觉方向、基础变量、图层/素材、组件、页面/状态、验收。
- 分开记录文字行盒与可见字形，校准字族、回退字体、字重、字号、行高、基线和颜色。
- 使用 SVG 路径还原**不规则背景板**，明确主体、阴影、文字、按钮和导航的遮挡顺序。
- 检查真实 DOM 文本、原生表单、图片加载、被隐藏或遮挡的元素。
- 对整页和关键区域分别做截图比较，保留原图、实际截图、叠加图、差异图与源码哈希。
- 支持逐页推进和批量状态报告，明确缺失证据及尚未解决的差异。

整张截图加透明按钮不能算分层原型。重新生成的素材也不能冒充从原图无损恢复的素材。

[工具与操作说明 →](skills/image-to-layered-html-prototype/README.zh-CN.md) · [完整设计标准 →](skills/image-to-layered-html-prototype/references/design-system.md)

### 2. 从真实 App 截图到多语言封面

- 根据视觉参考搭建 HTML/CSS 母版，让标题和辅助文字保持可编辑。
- 提供 **50 个语言区域预设**，支持自定义 BCP 47、按文字系统选择字体、RTL 从右向左布局。
- 显式管理每个语言版本文案，固定封面顺序，组织“语言 × 设备 × 页面”矩阵。
- 导出原尺寸 PNG、审查联系表和绑定源文件的哈希清单。
- 检查缺失翻译、文字溢出、元素碰撞、素材加载失败、矩阵缺项和过期导出。
- 把视觉与翻译审查保留为独立步骤，避免“脚本通过”代替真正看图。

50 个预设代表可配置的目标，不是自动完成的正式翻译，也不代表所有商店上传槽位均适用。示例文案明确属于演示草稿。

[工具与操作说明 →](skills/app-store-cover-generator/README.zh-CN.md) · [本地化规范 →](skills/app-store-cover-generator/references/localization.md)

## 看看真实工具输出

![工具实际导出的示例联系表，包含英中阿语言与手机平板布局](skills/app-store-cover-generator/docs/demo-contact.png)

**这是工具实际导出的自有 starter 示例。** 界面与插画为合成演示，不是已发布 App 的截图；它展示语言与设备矩阵，也不限定最终产品的设计风格。可查看 [可编辑源文件](skills/app-store-cover-generator/assets/starter/index.html) 与 [导出合同](skills/app-store-cover-generator/references/template-contract.md)。

## 快速开始

安装需要的技能，提供对应素材，再按名称调用。技能安装与运行工具依赖是两个步骤；只有执行浏览器/Python 工具时才需要后者。

## 安装

使用 [Skills CLI](https://github.com/vercel-labs/skills) 查看并安装：

```sh
npx skills@latest add chensir-indie/app-dev-skills --list
npx skills@latest add chensir-indie/app-dev-skills --skill image-to-layered-html-prototype --skill app-store-cover-generator
```

按提示选择 Agent。全局安装到 Codex 时追加 `-a codex -g`；只装一个时保留对应的 `--skill`。技能安装不会自动安装运行工具所需的依赖。

手动安装时，先克隆仓库，再把需要的 `skills/<技能名>` 整个目录复制到 Agent 的技能目录。Codex 通常使用 `~/.codex/skills/`；不要把仓库根目录作为一个 skill 安装。目标已存在时先保留并检查本地修改，不直接覆盖。完整命令见 [英文说明](README.md#install)。

## 调用示例

**还原已认可界面**

```text
用 $image-to-layered-html-prototype 处理这三张已认可设计图。
先提取共享变量与组件，再把所有页面实现为可编辑 HTML。
重点匹配异形背板、植物遮挡、文字比例和底栏选中胶囊。
给出真实浏览器截图及仍未解决的差异。
```

**修复现有页面偏差**

```text
用 $image-to-layered-html-prototype 对照参考图检查这个 HTML。
先修背景板轮廓、文字和图标位置，保留认可素材，不修改基准原图。
每轮给出关键区域修复前后的差异。
```

**制作多语言商店素材**

```text
用 $app-store-cover-generator，根据真实 App 截图和视觉参考，
制作六张封面，覆盖英语、简体中文、日语及我指定的手机/平板尺寸。
保持文字可编辑，先匹配一张母版，再扩展并导出矩阵；不上传商店。
```

## 运行与验证

需要 Node.js 22+、Python 3.9+、npm 与 Playwright Chromium。在仓库根目录运行：

```sh
npm ci
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r skills/image-to-layered-html-prototype/requirements.txt
npx playwright install chromium
npm run check
```

Linux 浏览器系统依赖使用 `npx playwright install --with-deps chromium` 安装。Windows 激活脚本是 `.venv\Scripts\Activate.ps1`，npm 中的测试命令要求 PATH 上有 `python3`。可选的 Swift/Vision OCR 脚本仅支持 macOS，核心校验不依赖它。

- [分层 HTML 工具说明](skills/image-to-layered-html-prototype/README.zh-CN.md)
- [商店封面工具说明](skills/app-store-cover-generator/README.zh-CN.md)
- `npm run demo` 运行原有封面示例，示例 UI 为合成数据。
- `npm run check` 检查安装结构、文档链接、两个技能的回归与浏览器行为；CI 不打包或发布 App。

## 两个技能如何衔接

```text
认可设计图 → 分层 HTML + 视觉证据
                  ↓
          独立完成 App 实现与设备测试
                  ↓
真实 App 截图 → 可编辑封面 → 多语言导出与审查
```

先用原型技能建立实现依据；App 开发与真机验证完成后，再把真实截图交给封面技能。宣传图不能暗示应用尚未实现的功能。

## 常见问题

**这是“一句话自动开发 App”吗？** 不是。它提供 Agent 工作流与测量、重建、检查工具，仍需要检查输出并修正差异。

**必须有 imagegen 或 API key 吗？** 已有参考图和独立工具不需要。生成或编辑新素材使用 Agent 环境已有能力，访问条件与费用由对应工具决定。

**能保证绝对一比一吗？** 不能无条件保证。原始素材缺失、字体差异、浏览器渲染和生成素材漂移都可能造成误差。工作流会保留参考、测量差异并报告未通过项。

**支持哪些 Agent？** 技能使用 `SKILL.md` 结构，已验证 Codex 安装与 Skills CLI 识别。其他 Agent 可通过 Skills CLI 支持的方式安装，但图像和浏览器能力取决于各自环境。

**50 种语言都能直接上线？** 预设提供语言方向和字体配置，正式产品文案仍需补齐与审查，示例翻译不能直接视为正式版本。

**会自动发布吗？** 不会。导出、审查、上传商店和社交发布各自独立，需要对应授权与验证。

## 从旧仓库迁移

本仓库沿用 `app-store-cover-generator` 的 Git 历史。原技能名称与调用方式保持不变，代码位于 `skills/app-store-cover-generator/`。旧克隆请更新 remote，运行原工具时切换到该目录。曾将整个仓库安装成 skill 的用户需要迁移到对应子目录，迁移前保留本地修改。

## 开源协议

代码、文档与自有示例素材使用 [MIT](LICENSE)。外部 App 截图、字体、生成素材的使用权需另行确认；见 [第三方声明](THIRD_PARTY_NOTICES.md) 与 [贡献说明](CONTRIBUTING.md)。
