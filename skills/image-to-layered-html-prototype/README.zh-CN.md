# Image to Layered HTML Prototype

[English](README.md) · [Agent 技能入口](SKILL.md)

把认可的 UI 图片还原为可编辑 HTML/CSS/SVG：适合截图重建、imagegen 设计稿落地、已有页面视觉修复和多页统一设计。文字、控件、背板、主体与导航分别实现，通过真实浏览器截图校准。

## 从你的输入开始

| 你已有 | 建议提供 | 得到什么 |
| --- | --- | --- |
| 仅要方向、提示词或参考图 | 产品用途、页面/任务、视觉约束 | 所请求的概念产物，不自动进入 HTML 重建 |
| 已认可截图 | 原文件、页面/状态名称，已知视口与语言 | 实测图层、可运行原型、差异证据 |
| 产品方向，并要求完整原型 | 产品用途、页面范围、视觉约束 | 用当前环境出参考图，再转分层原型 |
| 现有 HTML | 页面目录及各页认可参考 | 保留源码/素材/交互，先浏览器盘点，再定向修复与更新证据 |
| 多页参考 | 全部图片和实现优先级 | 共享 tokens、逐页状态及批量验收 |

完整重建分支交付 HTML/CSS/JS、独立 assets、tokens、几何/字体测量表、图层/素材合同、交互/状态合同，以及真实浏览器截图、差异图和具体复核记录。参考整图用于对照，运行时页面保持可编辑。

## 评审与提升设计质量

区分忠实复刻、主动优化和仅评审。复刻保持认可参考不变，仅评审不修改文件；已授权优化时，查看现有页面，选择一套主设计规范，按层级、布局、字体、图标/材质、边界状态逐轮改善。复用共享 tokens，用真实浏览器前后截图复核。

[设计质量流程](references/design-quality-review.md) 提供评审顺序与证据格式；[来源与可选工具](references/design-sources.md) 说明如何结合 Impeccable、UI/UX Pro Max、Vercel 指南及平台标准，无需安装这些工具或混搭视觉体系。这些流程补充像素检查，不保证审美结果，也不等于完整可访问性合规认证。

> 用 $image-to-layered-html-prototype 在现有设计方向内优化这个 HTML。先定位最影响层级、布局和排版的问题，再修共享组件，给我真实前后截图；保留明确锁定的参考几何。

## 安装与调用

Skills CLI 安装器需要 Node.js 22.20+ 和 npm；本技能工具本身的最低版本是 Node.js 22：

```sh
npx skills@latest add chensir-indie/app-dev-skills --skill image-to-layered-html-prototype
```

然后告诉 Agent：

> 用 $image-to-layered-html-prototype 根据这些已认可图片提取共享设计规范，制作可编辑分层 HTML，用真实浏览器截图验证图层和交互，并逐页报告视觉状态。

已有页面时可说：

> 用 $image-to-layered-html-prototype 对照参考修复这个 HTML 的背板轮廓与字体，保留修改前后的浏览器证据。

Agent 也可只使用设计流程。图像生成由当前 Agent 环境提供；已有认可图时无需生成 API。生成式重建无法保证恢复被遮挡的原始像素。

仅要方向或提示词时，交付这些产物即可结束，无需渲染环境。商店封面属于 `app-store-cover-generator`；竞品研究可以为设计需求提供证据。当前环境有相关技能时，先读对应技能再指导后续工作；讨论下一步无需先安装另一个技能。

## 环境检查与安装

进入已安装的技能目录，即本 README 所在目录。执行辅助脚本前运行：

```sh
sh scripts/doctor.sh
```

缺少环境时按输出修复，保留草稿并继续可独立完成的设计工作。依赖脚本的检查与视觉验收保持 pending，待环境就绪并实际运行后更新。

检查器从 `python3` 或 `python` 检测 Python 3.9+，实际导入 Pillow/PyYAML，检查 Node.js 22+、npm、Playwright，并真实启动浏览器。输出当前目录和对应修复命令，只读、不自动安装。所有 scope 的检查器本身都需要 Python；browser scope 无需 Pillow/PyYAML。

- `--scope python`：测量和校验所需环境。
- `--scope browser`：浏览器盘点和截图所需环境。
- 默认 `--scope all`：检查全部。退出码 `0` 就绪，`1` 缺失或损坏，`2` 参数错误。
- Swift/Vision OCR 仅供 macOS 可选使用；缺失不阻塞像素核心测量和核心校验。

没有 Python 时，从 [Python 官方下载页](https://www.python.org/downloads/) 安装，启用 PATH 后重开终端。Node.js/npm 从 [Node.js 官方下载页](https://nodejs.org/en/download) 安装。Python 依赖在技能目录配置：

```sh
python3 -m venv .venv  # 仅有 python 时使用 python
. .venv/bin/activate
python -m pip install -r requirements.txt
```

JavaScript 依赖按安装方式选择：

| 当前副本 | 在哪里运行什么 |
| --- | --- |
| 完整仓库 checkout | 仓库根目录运行 `npm ci`，由 workspaces 共用依赖 |
| 单独安装的 skill | 本技能目录运行 `npm install` |

然后回到本技能目录：

```sh
npx --no-install playwright install chromium
sh scripts/doctor.sh
```

Linux 若缺浏览器系统库，按本机管理员策略运行 `npx --no-install playwright install --with-deps chromium`。使用已安装 Chrome 时运行 `PLAYWRIGHT_CHANNEL=chrome sh scripts/doctor.sh --scope browser`，后续浏览器命令保持同一变量，并在证据中记录真实版本。

Windows 推荐通过 WSL 使用 POSIX shell；Git Bash 也可运行启动器。原生 PowerShell 激活虚拟环境用 `.venv\Scripts\Activate.ps1`，安装 Python 后可运行 `python scripts/doctor.py --scope all`。这些是配置路线说明，原生 Windows 全流程尚未经本次验证。下文命令统一用 `python3`；doctor 若报告的是 `python`，使用该解释器，并保持同一环境。下载失败时保留诊断并处理网络或包管理问题，再重跑检查；脚本不修改代理和 registry。

## 最短工作流

已有 HTML 先保留原始源码与修改前截图，在现有目标画板根元素上补 `data-artboard` 属性（已有则沿用，不重建 wrapper）。再运行下述盘点命令，随后补缺少的测量与合同；盘点只观察实现，不提供独立源图坐标。

```sh
node scripts/inventory_page.cjs /absolute/path/to/prototype
```

1. 锁定参考、状态与共享 tokens；按 [源图测量](references/reference-geometry.md) 独立记录参考坐标，冻结 [验收合同](references/acceptance.md)。
2. 按 [图层合同](references/layer-manifest.md) 实现可编辑图层与可见交互。
3. 合同齐全后采集入口状态并严格校验：

   ```sh
   node scripts/capture_native.cjs /absolute/path/to/prototype playwright home
   python3 scripts/validate_manifest.py /absolute/path/to/prototype/layer-manifest.json
   python3 scripts/validate_prototype.py /absolute/path/to/prototype
   ```

4. 查看原图、截图、叠加、原始差异与图层证明，按 [视觉收敛](references/visual-convergence.md) 修复失败区域，逐页重新采集和验收。

盘点要求 `index.html`、`reference/source.png` 和目标根元素的 `[data-artboard]`，只记录实现观察。截图脚本的 state-id 只命名证据；弹层、路由和选中态需真实操作并验证 landmark 后再采集。默认 DPR=1；脚本不自动应用全部 render-config 字段，见 [截图坐标与环境](references/render-contract.md)。

## 按阶段深入

| 当前工作 | 参考 |
| --- | --- |
| 出图或拆素材 | [imagegen 工作流](references/imagegen-workflow.md)、[素材重建](references/reconstruction.md) |
| 建共享规范 | [六级设计标准](references/design-system.md) |
| 测字体与轮廓 | [字体合同](references/typography-contract.md)、[几何合同](references/geometry-contract.md) |
| 采证与验收 | [验收](references/acceptance.md)、[视觉修复与多页推进](references/visual-convergence.md) |
| 移交 Flutter | [Flutter 边界](references/flutter-mapping.md) |

脚本能发现缺层、过期证据、几何与图片差异；严格校验需要独立源图测量和真实截图。`--structure-only` 仅供诊断，素材身份、字形、轮廓、遮挡仍需人工复核。关键差异未过的页面保持 pending，全部请求页面通过才算批量通过。Flutter 移交不等于真机验收。

后续交接引用已有产物，附下一任务、采用参考的路径/哈希、页面/状态 ID、源码入口，以及可编辑/视觉/交互/适配状态和未过项。原型截图保持原型身份；商店封面中的真实 App UI 需要另有实际 App 截图。

修改工具后，在本技能目录激活 Python 环境，运行 `npm test` 和 `npm run test:browser`。合成测试夹具只验证校验器行为，不能充当产品还原截图。

[MIT](LICENSE) · [依赖与素材权利](THIRD_PARTY_NOTICES.md)
