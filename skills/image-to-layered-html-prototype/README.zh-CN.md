# Image to Layered HTML Prototype

[English](README.md) · [技能入口](SKILL.md)

将 imagegen 设计图或已有截图还原为可编辑的 HTML/CSS/SVG 原型。文字、图标、异形背板、主体、背景与导航独立分层，通过真实浏览器截图逐项校准。

## 安装与调用

```sh
npx skills@latest add chensir-indie/app-dev-skills --skill image-to-layered-html-prototype
```

> 用 $image-to-layered-html-prototype 根据这些认可图提取统一设计规范，制作分层 HTML，核对字体、图标、异形背板、遮挡与交互，并给出真实浏览器截图。

图像生成通过 Agent 环境提供；已有参考时不需要生成 API。生成式素材提取不能保证恢复被遮挡的原始像素，也不能用整张截图替代可编辑界面。

## 工具运行

需要 Node.js 22+、Python 3.9+、npm。在本技能目录运行：

```sh
npm ci
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
npx playwright install chromium
npm test
npm run test:browser
```

默认使用 Playwright Chromium；使用已安装 Chrome 可设置 `PLAYWRIGHT_CHANNEL=chrome`。可选 Swift/Vision OCR 仅支持 macOS。Linux 和 Windows 注意事项见 [英文运行说明](README.md#toolkit-setup)。

## 主要规范

- [imagegen 出图与素材拆分](references/imagegen-workflow.md)
- [六级设计标准](references/design-system.md)
- [真实图层合同](references/layer-manifest.md)
- [截图坐标、DPR 与环境](references/render-contract.md)
- [验收与证据](references/acceptance.md)
- [差异诊断与逐轮修复](references/visual-convergence.md)
- [Flutter 移交边界](references/flutter-mapping.md)

截图脚本的 state-id 只标记结果，不会替你打开弹窗或切换页面；状态必须实际触发并验证。源图实测坐标与实现 DOM 坐标需要独立记录。每页分别报告结构、视觉、交互和适配，自动测试通过不能当作审美或像素一致证明。

使用 [MIT](LICENSE)，依赖与素材权利见 [第三方声明](THIRD_PARTY_NOTICES.md)。
