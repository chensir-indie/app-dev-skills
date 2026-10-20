# App Store 封面生成 Skill

[English](README.md) · [Agent 指令](SKILL.md)

将真实 App 截图和视觉参考制作成可编辑、多语言的 App Store 封面。工具按语言、设备和页面矩阵导出原尺寸 PNG、总览图、文件哈希及复核记录。

## 从你的起点开始

| 已有材料 | 可以提出的任务 | 产出 |
| --- | --- | --- |
| 参考图或初步想法 | 视觉方向与提示词 | 封面概念，无需配置渲染环境 |
| App 截图与目标尺寸 | 制作可编辑封面 | HTML/CSS 项目及导出矩阵 |
| 已有封面项目 | 检查或局部修复 | 精确到矩阵单元的问题与复核结果 |

布局、品牌、页数和语言由项目决定。自动检查覆盖文案、几何、素材和完整性问题，视觉还原度与翻译质量仍需逐项检查。商店上传和社交发布需要单独授权。

本技能产出营销封面。若目标是把 App 页面重建为可点击界面，当前环境可用时先读 `image-to-layered-html-prototype`，按该目标继续。仅要方向或提示词时，停在所请求的概念产物，无需渲染环境。

## 安装与调用

在 App 项目目录使用 [Skills CLI](https://github.com/vercel-labs/skills)。该安装工具要求 Node.js **22.20+** 和 npm/npx；本 Skill 附带的工具本身要求 Node 22+：

```sh
npx skills@latest add chensir-indie/app-dev-skills --skill app-store-cover-generator
# 如需全局安装到 Codex，改用：
npx skills@latest add chensir-indie/app-dev-skills --skill app-store-cover-generator -a codex -g
```

选择目标 Agent 和安装范围。未发现 Skill 时新开一个 Agent 会话。通过 CLI 安装的副本可用 `npx skills@latest update app-store-cover-generator` 更新；更新前保留本地修改。

<details>
<summary>手动安装（没有 npx 时也可使用）</summary>

已有 Git 时，克隆到新目录，并仅将本 Skill 复制到尚不存在的目标目录：

```sh
git clone https://github.com/chensir-indie/app-dev-skills.git
mkdir -p ~/.codex/skills
test ! -e ~/.codex/skills/app-store-cover-generator && \
  cp -R app-dev-skills/skills/app-store-cover-generator ~/.codex/skills/
```

同一 Agent、同一范围使用一种安装方式。更新源仓库后，先审阅本地修改，再主动同步对应 Skill 子目录。

</details>

最小输入：应用与有依据的功能说明、真实截图（或明确要求制作概念）、参考图或设计方向、目标语言与设备尺寸、期望完成的阶段。例如：

> 使用 $app-store-cover-generator，根据这些截图和参考图，为 zh-Hans、en-US 制作指定 iPhone 尺寸的可编辑封面，导出矩阵并完成视觉复核，停在本地交付。

## 执行脚本前检查环境

安装 Skill 会添加指令和文件；渲染还需要 **Node.js 22+、npm、Playwright 和可启动的浏览器**。检查入口使用 POSIX `sh`，支持 macOS/Linux；Windows 请使用 WSL。进入已安装的 `app-store-cover-generator` 目录：

```sh
sh scripts/doctor.sh
# 仅检查运行时与依赖包；此结果不代表浏览器已可用：
sh scripts/doctor.sh --scope core
```

这个 shell 入口在缺少 Node/npm 时也能给出引导。它列出实际检查与精确修复命令，缺项时返回非零状态，不会自动安装软件。独立安装的 Skill 按提示在本目录执行 `npm install`；集合源码检出则在仓库根目录执行 `npm ci`。浏览器安装、Linux 系统库修复与 `PLAYWRIGHT_CHANNEL=chrome` 用法见[工具环境指南](references/template-contract.md#environment-check-and-setup)。

检查通过后，按[命令指南初始化、预览与导出](references/template-contract.md#commands)。交付包含可编辑源码、PNG、总览图、manifest/哈希和绑定该次导出的复核记录。自动导出通过后仍需视觉复核。

仅新项目从 starter 初始化；已有项目保留配置、素材、矩阵与审批历史，只修改请求的矩阵单元或共享源码，再更新受影响证据。后续交接引用项目/导出目录，附应用、下一阶段、矩阵、截图来源、最终哈希、绑定复核和待处理单元。概念图和原型截图导出后仍保留其身份。

## 按任务继续

- [参考还原与视觉方向](references/art-direction.md)
- [语言扩展、字体与 RTL](references/localization.md)
- [环境、项目结构与命令](references/template-contract.md)
- [质量校验、视觉复核与故障排查](references/quality-gates.md)
- [商店交接与发布边界](references/delivery.md)
- [开发与贡献](CONTRIBUTING.md)

采用 [MIT](LICENSE) 许可。外部截图、商标与字体保留各自权利，详见[第三方说明](THIRD_PARTY_NOTICES.md)。
