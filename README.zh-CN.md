# App Dev Skills

[English](README.md)

面向 App 开发的开源 Agent 技能合集：从设计参考图到可编辑原型，再到多语言商店封面。两个 skill 可单独安装、独立使用。

## 包含的技能

| Skill | 解决什么问题 | 交付什么 |
| --- | --- | --- |
| [image-to-layered-html-prototype](skills/image-to-layered-html-prototype/SKILL.md) | 将 imagegen 设计图或截图还原成分层页面 | 设计规范、HTML/CSS/SVG、独立素材、浏览器截图、局部差异报告、可选 Flutter 移交 |
| [app-store-cover-generator](skills/app-store-cover-generator/SKILL.md) | 根据真实 App 截图制作商店宣传图 | 可编辑封面、多语言与设备尺寸导出、联系表、审查记录 |

完整流程是：**设计参考 → 分层 HTML → App 实现 → 真实 App 截图 → 商店封面**。合集覆盖原型与商店素材两个阶段，原生 App 实现需另行执行；也可以直接使用其中一个技能。

## 安装

使用 [Skills CLI](https://github.com/vercel-labs/skills) 查看并安装：

```sh
npx skills@latest add chensir-indie/app-dev-skills --list
npx skills@latest add chensir-indie/app-dev-skills --skill image-to-layered-html-prototype --skill app-store-cover-generator
```

按提示选择 Agent。全局安装到 Codex 时追加 `-a codex -g`；只装一个时保留对应的 `--skill`。技能安装不会自动安装运行工具所需的依赖。

手动安装时，先克隆仓库，再把需要的 `skills/<技能名>` 整个目录复制到 Agent 的技能目录。Codex 通常使用 `~/.codex/skills/`；不要把仓库根目录作为一个 skill 安装。目标已存在时先保留并检查本地修改，不直接覆盖。完整命令见 [英文说明](README.md#install)。

## 使用

```text
用 $image-to-layered-html-prototype 把这些已认可设计图还原为可编辑 HTML。
逐项匹配背景、异形背板、植物遮挡、字体、图标、按钮和选中态，
提供真实浏览器截图与差异记录。
```

```text
用 $app-store-cover-generator，根据这些真实 App 截图和设计参考，
制作指定语言、设备尺寸的商店封面，保留可编辑文字，验证后导出，不上传商店。
```

图像生成使用 Agent 环境已有工具；已有参考时不需要额外生成 API。整张截图加透明按钮不能算分层 HTML，测试通过也不等于视觉完全一致或人工审查通过。

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

## 从旧仓库迁移

本仓库沿用 `app-store-cover-generator` 的 Git 历史。原技能名称与调用方式保持不变，代码位于 `skills/app-store-cover-generator/`。旧克隆请更新 remote，运行原工具时切换到该目录。曾将整个仓库安装成 skill 的用户需要迁移到对应子目录，迁移前保留本地修改。

## 开源协议

代码、文档与自有示例素材使用 [MIT](LICENSE)。外部 App 截图、字体、生成素材的使用权需另行确认；见 [第三方声明](THIRD_PARTY_NOTICES.md) 与 [贡献说明](CONTRIBUTING.md)。
