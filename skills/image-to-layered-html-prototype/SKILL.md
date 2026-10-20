---
name: image-to-layered-html-prototype
description: Rebuild approved app UI images as editable layered HTML/CSS/SVG, or repair an existing reconstruction with measured reference geometry and browser comparisons. Also supports UI direction and prompt-only requests, shared design systems, multi-page prototypes and optional Flutter handoff.
---

# Image to Layered HTML Prototype

按请求选择概念、完整重建或既有修复分支。完整重建交付可编辑、可交互、通过逐页视觉复核的 HTML 原型：文字用 DOM，控件用可见语义元素，背板用 CSS/SVG，照片和主体用独立资产。重建默认 `layered_rebuild`；“一比一”提高视觉要求，整屏贴图、UI 切片、Canvas 或透明热区不能替代分层实现。

## 选择起点

| 用户目标与输入 | 从这里开始 | 完成边界 |
| --- | --- | --- |
| 仅要 UI 方向、提示词或参考图 | 按 [imagegen-workflow](references/imagegen-workflow.md) 交付所请求的方向、提示词或已查看的图 | 所请求的概念产物；不自动进入 HTML 重建 |
| 要完整原型，只有产品方向 | 按 imagegen workflow 生成、查看并锁定正视 UI 图，再进入下述流程 | 分层 HTML 与逐页验收 |
| 要完整原型，已有认可图片 | 直接锁定参考并测量，沿用已批准方向 | 分层 HTML 与逐页验收 |
| 修复已有 HTML 和参考图 | 保留源码、素材与交互，先保存修改前截图并盘点，再补独立参考测量与必要合同 | 请求的修复、更新证据与实际验收状态 |
| 多页参考 | 冻结完整页面清单；默认逐页闭环，要求先铺齐时用下述两阶段流程 | 全部请求页面的逐页状态 |

若目标实际是商店封面，先阅读当前环境可用的 `app-store-cover-generator` 的 SKILL.md，再按目标指导。若需要竞品研究，先整理已有证据与待确认问题，再阅读当前环境可用的相关研究技能；未安装时说明适用范围即可，不把安装新工具作为继续工作的前提。

执行依赖脚本前，在本 skill 目录运行 `sh scripts/doctor.sh`。仅做 Python 校验可用 `--scope python`，浏览器操作用 `--scope browser`；检查只读、不自动安装。缺项时按输出和 [环境支持](README.zh-CN.md#环境检查与安装) 修复重跑；保留草稿并继续独立设计工作，脚本与视觉验收保持 `pending`。纯方向或提示词任务无需渲染环境。

已有 HTML 先保留原始源码与修改前截图，在现有目标画板根元素上补 `data-artboard` 属性（已有则沿用，不重建 wrapper），再做初始盘点，随后进入第 1 步补合同：

```sh
node scripts/inventory_page.cjs /absolute/path/to/page
```

它要求 `index.html`、`reference/source.png` 和目标根元素的 `[data-artboard]`，仅生成实现盘点与真实截图；不生成参考坐标、合同或验收结果。

## 1. 冻结参考与验收目标

保存原尺寸正视参考、SHA-256、页面/状态、语言和样例数据；细节裁图辅助测量，整图仍是基准。按 [render-contract](references/render-contract.md) 锁定图片像素、CSS 像素、DPR 与实际浏览器环境。

按 [design-system](references/design-system.md) 建立本次所需的 tokens 与组件。**实现前**按 [acceptance](references/acceptance.md#one-to-one-visual-standard) 冻结 `one_to_one` 阈值和具名角色 ROI；保留不可放宽上限，不用放宽阈值、改基准或排除整块 UI 消除失败。

完成条件：参考、状态和验收目标可追溯。多页从全部参考冻结 `expected-pages.json`，使遗漏页面也能被批量检查发现。

## 2. 独立测量并建立合同

按 [reference-geometry](references/reference-geometry.md) 独立测源图，再与 DOM 对照；已有页面的初始盘点不能代替源图测量。文字、按钮、重要背板/图标的 `referenceBounds` 是源图推导的目标 layout box，`bounds` 是实现边界；文字可见字形另记 `referenceInkBounds`、方法和绑定原图 SHA 的证据。OCR ink box 不等于 CSS 行盒，DOM 自动值不属于源图实测。

按 [geometry-contract](references/geometry-contract.md)、[typography-contract](references/typography-contract.md) 与 [layer-manifest](references/layer-manifest.md) 建立几何/字体表及唯一 selector，覆盖全部可见文字与控件。

完成条件：实现与参考测量来源明确，合同覆盖全部可见层。

## 3. 重建素材与分层 HTML

先按 [asset-audit](references/asset-audit.md) 与 [reconstruction](references/reconstruction.md) 校准关键主体、背景、字体和不规则轮廓，再按 [html-css-contract](references/html-css-contract.md) 实现独立图层及可见交互。优先原素材；缺失时提取或重建单个素材，记录来源与不确定性。`inferred` 不豁免视觉不合格，近似主体只能用于结构调试。

新素材放入真实 HTML，用同环境浏览器截图 A/B 核对全图和素材 ROI；无完整合同时用 `compare_candidate.py`，合同齐后用冻结 ROI 的 `compare_iteration.py`，细节见 [visual-convergence](references/visual-convergence.md)。A/B 改善不等于验收通过。

完成条件：文字能修改，主体/背板/投影可独立隐藏，主交互有可见结果及返回/关闭；基准视口、小/大屏和长文案有适配证据。

## 4. 采集并收敛

读取 [acceptance](references/acceptance.md) 采集规范与 [visual-convergence](references/visual-convergence.md) 修复循环。字体、图片解码后固定数据、时钟、滚动与动画，从当前源码采集截图、DOM 和哈希收据：

```sh
node scripts/capture_native.cjs /absolute/path/to/prototype playwright home
python3 scripts/diagnose_visual.py /absolute/path/to/prototype --state home
```

`state-id` 仅标记证据，**不会触发状态**。弹层、表单、选中项和路由须在同一浏览器会话真实操作并验证 landmark 后再采集。默认 `file://`、DPR=1；其他策略须按 render contract 明确实现，脚本不自动应用全部环境字段。

保留当前源码对应的原图/实际并排、叠加、零阈值原始差异及图层开关证明。按失败 ROI 和最差局部块先修主体、背景、字体，再修细节；每轮只改一类因素，保留前图并比较回退。同类区域连续两轮无改善时换素材或测量/重建方法。

ROI 并集至少覆盖原图 75%，对应角色 ROI 至少覆盖关键图层 80%；文字/按钮及占画面至少 1% 的层中心也须被覆盖。全图均值不能替代局部轮廓、文字和控件门槛，具体字段与固定上限以 acceptance 为准。

完成条件：每个请求状态都有真实触发与当前截图证据，冻结数值门槛通过。人工查看原图、截图、叠加、原始差异和图层证明，在 `manualReview.states[]` 对素材身份、背景、字体、轮廓、层级与控件逐项记录具体观察；明显差异保留 `pending`。

## 5. 逐页验收与交付

```sh
python3 scripts/validate_manifest.py /absolute/path/to/prototype/layer-manifest.json
python3 scripts/validate_prototype.py /absolute/path/to/prototype
```

严格校验与人工视觉复核都通过才记 `passed`。`--structure-only` 仅供诊断；文件存在、哈希收据和数值通过各自只证明其检查范围。报告结构可编辑、视觉还原、交互、适配四项证据，关键差异未清零时继续修复。确受素材/工具限制时列出具体缺失、尝试、误差和未过项。

多页每页执行同一门槛，任一页 `pending`，整批仍为 `pending`。批量检查和基础稿分诊见 [visual-convergence](references/visual-convergence.md#多页推进)。用户要求先铺齐时，先为全部参考交付独立 HTML、可编辑文字、语义控件、独立素材及原生截图，并核对资源/交互/尺寸；再逐页补合同、测量和严格验收。基础稿不能计为视觉通过，单页暂时受阻时继续其他可推进页面。

按 [design-system](references/design-system.md) 与 [acceptance](references/acceptance.md) 交付源码、独立 assets、参考、tokens、manifests、render config、state matrix、测量表、交互图和 `evidence/`。需要 Flutter 移交时再读 [flutter-mapping](references/flutter-mapping.md)。

后续交接引用现有文件，附目标/下一步、采用参考的路径与 SHA、页面/状态、源码入口和四项验收状态及未过项。原型截图保持原型身份；商店素材中的真实 App UI 需要另有实际 App 截图。
