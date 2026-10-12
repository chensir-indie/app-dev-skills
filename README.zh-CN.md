# App Store 封面生成 Skill

[English](README.md) · [Skill 指令](SKILL.md)

一个开源 Agent Skill，基于视觉参考和 App 截图，制作可编辑、可本地化的 App Store 截图封面。

提供参考分析、HTML/CSS 实现、本地化、导出和复核流程。使用目标应用的素材与视觉方向，布局、品牌展示、页数、语言和设备尺寸均可配置。

## 核心能力

- **参考驱动设计**：分析字体、构图、间距与视觉图层，构建可编辑的封面项目。
- **模板复用**：将文案、素材与 HTML/CSS 布局分离，各输出版本保持统一的页面顺序。
- **多语言排版**：支持 App Store 语言区域预设、自定义 BCP 47 标签、按文字系统选择字体及从右到左排版。
- **批量导出**：按配置的语言、设备和页面导出原尺寸 PNG，生成总览图与文件哈希清单。
- **质量校验**：检查文案缺失、文字溢出、元素重叠、素材加载和导出完整性，并单独保留视觉复核记录。

交付内容包括可编辑项目、导出图片和复核资料。自动检查辅助人工判断视觉还原度与翻译质量。图片生成是可选步骤，使用 Agent 可用的工具；商店上传不属于本 Skill 的范围。

## 安装

在项目目录运行 [Skills CLI](https://github.com/vercel-labs/skills)：

```sh
npx skills@latest add chensir-indie/app-store-cover-generator --skill app-store-cover-generator
```

按提示选择 Agent，默认安装到当前项目。如需全局安装到 Codex：

```sh
npx skills@latest add chensir-indie/app-store-cover-generator --skill app-store-cover-generator -a codex -g
```

更新通过 Skills CLI 安装的副本：

```sh
npx skills@latest update app-store-cover-generator
```

<details>
<summary>手动安装到 Codex</summary>

克隆到尚不存在的目录：

```sh
git clone https://github.com/chensir-indie/app-store-cover-generator.git ~/.codex/skills/app-store-cover-generator
```

无本地修改时，用 `git -C ~/.codex/skills/app-store-cover-generator pull --ff-only` 更新。有本地修改时，先保留并审阅，再合并更新。同一个 Agent、同一个作用域选择一种安装方式。

</details>

安装会添加 Skill 指令与配套文件。运行附带的渲染工具还需要 Node.js 22+、npm 和 Playwright Chromium，安装命令见[工具指南](references/template-contract.md#commands)。如果尚未发现已安装的 Skill，可新开一个 Agent 会话。

## 使用

提供 App 截图、视觉参考、目标语言和设备尺寸，然后告诉 Agent：

> 使用 $app-store-cover-generator，根据这些素材制作 App Store 封面。保持设计可编辑，并导出配置的语言和设备版本。

对于已有项目：

> 使用 $app-store-cover-generator 检查这个封面项目，在保留已确认设计的基础上，修复排版或本地化问题。

Agent 根据 [SKILL.md](SKILL.md) 执行流程，并按需读取配套参考文档。

## 文档

- [视觉方向与参考分析](references/art-direction.md)
- [本地化与字体排版](references/localization.md)
- [项目格式、预览与导出命令](references/template-contract.md)
- [质量检查与复核](references/quality-gates.md)
- [交付范围](references/delivery.md)
- [贡献与开发](CONTRIBUTING.md)

## 许可

采用 [MIT](LICENSE) 许可。外部 App 截图、商标与第三方字体保留各自权利，详见[第三方说明](THIRD_PARTY_NOTICES.md)。
