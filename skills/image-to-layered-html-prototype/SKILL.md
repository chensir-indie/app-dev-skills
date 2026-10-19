---
name: image-to-layered-html-prototype
description: Turn imagegen UI concepts or screenshots into a measured design system and editable layered HTML/CSS/SVG prototypes, with native-size screenshot comparison and optional Flutter handoff. Use for image-to-HTML reconstruction, irregular panels, precise typography and icons, and consistent multi-page prototypes.
---

# Image to Layered HTML Prototype

安装后首次运行工具，按 [README.md](README.md#toolkit-setup) 配置 Node/Python 依赖和 Playwright Chromium。可选 Swift OCR 仅限 macOS；核心重建与校验不依赖它。

## 交付目标

把认可的设计图实现为可编辑、可交互、视觉接近参考的 HTML/CSS/SVG 页面。文字是 DOM 文本，按钮是可见的语义控件，背板是 CSS/SVG，照片与植物使用独立图像资产。交付可运行页面、真实浏览器截图、分层证据和差异清单。

默认且正常验收模式为 **layered_rebuild**。“一比一”提高视觉要求，不改变可编辑要求。禁止用整屏图片、截图条带、含文字/控件的大块 UI 切片、Canvas 整屏绘制或透明热区替代分层实现。参考图只在独立对照页面显示。用户明确要求贴图演示时可另交 reference preview，但不能计入分层原型完成。

缺素材时先查原资产，再提取、重建或针对单个素材使用 imagegen；标注不确定性并继续可完成部分。**inferred 不豁免视觉不合格。** 不用随机近似素材替换原素材，不把玫瑰标成菊花，不改认可布局去适应手头素材。目标是视觉验收通过，而非仅产出一个结构正确的样板；请求多页时逐页推进并记录各页状态，不以单页试点代替整批交付。

## 1. 锁定参考和范围

先区分入口：已有认可图时直接测量重建；只有产品方向时按 [imagegen-workflow.md](references/imagegen-workflow.md) 生成设计图、检查并锁定版本；已有 HTML 时先核对其真实截图与参考。不要为了使用 imagegen 而重新生成已经认可的页面。

选择原尺寸正视图，保存文件和 SHA-256；细节裁图辅助测量，不能替换基准。已批准的图直接实现，不重复要求确认。新方向需要 imagegen 时读取可用 imagegen skill，生成正视 UI，避免透视手机样机；查看生成结果后再采用。

记录页面、状态、样例数据与语言。多页共享 tokens、图标和组件。读取 [render-contract.md](references/render-contract.md)，区分图片像素、CSS 像素与 DPR，避免 591px 图片被误截成 1773px。

完整设计标准按 [design-system.md](references/design-system.md) 分为视觉方向、基础变量、图层/素材、组件、页面/状态、验收六级。这里只建立本次页面需要的标准，不强加植物主题、绿色配色或任何固定模板。

## 2. 测量并拆解

读取 [geometry-contract.md](references/geometry-contract.md)、[typography-contract.md](references/typography-contract.md)、[asset-audit.md](references/asset-audit.md)。列出全部文字、控件、图像、背板、图标和装饰。

测量边界、基线、间距锚点、逐角圆角与主体轮廓，区分原图测量和实现参数。**先在原图上记录参考边界，再采集浏览器 DOM。** 文字、按钮及标为重要背板/图标的层必须有独立的 `referenceBounds`；`bounds` 是实现 DOM 的当前边界。文字还有两个不同的边界：截图中可见字形的 ink bounds，以及 CSS 元素的 layout bounds。`referenceBounds` 对文字表示从原图字形、基线及目标行高推导并独立记录的目标 layout box；可见字形另记为 `referenceInkBounds`，不能直接把 OCR 字形框与 DOM 行盒比较。严格校验比较目标 layout box 与浏览器边界，字形本身依靠源图/截图 OCR 辅助、局部差异和人工核对。不能把写入 CSS、DOM audit 或仅有 OCR 猜测的值反称为原图实测。测量方法见 [reference-geometry.md](references/reference-geometry.md)。

每个文字层的 `referenceInkBounds` 同时填写 `referenceInkMethod` 与 `referenceInkEvidence`。OCR 记录须绑定锁定原图 SHA 和对应观测框；箭头等合并文字改用紧 ROI 的高对比像素核心，保存来源、ROI、阈值、结果，严格校验会从源图重新计算。OCR/像素核心只证明字形可见范围，不替代 `referenceBounds` 的行盒推导，也不证明字体轮廓已相同。

创建 design-tokens.json 及对应 CSS variables：字体/字重/字号/行高/颜色、间距、圆角、描边、渐变、模糊、阴影、图标尺寸/线宽、控件状态。视觉阈值须在实现前按 [acceptance.md](references/acceptance.md) 冻结为 `one_to_one` 档，不得仅让两份 JSON 的宽松值相等。按 [layer-manifest.md](references/layer-manifest.md) 创建图层合同，每层有唯一 DOM selector；覆盖全部可见文字与控件，不仅列标题和植物。已有 HTML 而合同缺失时，可运行 `node scripts/inventory_page.cjs /absolute/path/to/page /absolute/path/to/playwright` 采集实现侧文字、控件、图片、形状的 selector/边界/样式与原生截图；它只生成 `evidence/implementation-inventory.json` 草稿，不创建 `referenceBounds`、合同或验收结果。逐项对原图测量并补齐，避免从 DOM 自动值虚构原图坐标。

多页批量转换时，先从**全部参考图目录**冻结 `expected-pages.json`（页面目录名数组）；批量门槛拒绝缺页或遗漏参考图。默认可逐页闭环；**若用户要求先铺齐全部基础 HTML，就采用两阶段流程**：第一阶段为每张参考图建立独立、可打开的 HTML、可编辑 DOM 文字、语义按钮、独立图像/背景资产与原生浏览器截图，逐页核对图片加载、参考截图未进入运行时、基础交互和原图尺寸，并输出基础报告。此阶段允许暂缺精修合同，但不得称为视觉验收通过。第二阶段再逐页补 design tokens、源图测量、图层合同、具名 ROI、局部修复及严格验收。

已有全页基础稿时，不因某个页面暂时无法取得原始素材或未通过严格验收而停住整批；记录该页差异并转向下一页可推进的精修，随后回访。`triage_batch.py` 的 `nextAcceptanceCandidate` 是建议队列，不是阻止跨页推进的锁；同时参考其 `visualRepairOrder` 和用户优先级。OCR 提词和通用模板仅是基础稿手段，不能把“28 页可打开”当成 28 页视觉通过。

## 3. 资产与轮廓

读取 [reconstruction.md](references/reconstruction.md)。
- 在精修 CSS 前做关键资产门槛：对照原图可见轮廓、透视、裁切、透明边缘。主体或大面积装饰不匹配时，优先取得同源素材或重新提取/重建；代用图只能用于结构调试，不能进入最终视觉验收截图。
- 新素材先替换真实 HTML 中的独立图层，保持其他代码与截图环境不变，用 [visual-convergence.md](references/visual-convergence.md) 的浏览器截图 A/B 对照并核对素材 ROI；合同未齐时可用 `scripts/compare_candidate.py`，合同齐后用冻结 ROI 的 `compare_iteration.py`。不因为 imagegen 输出看起来像同一种植物就接受，必须确认局部和全图都改善。A/B 改善仍不代表严格验收通过。
- 原资产优先；照片可裁切复用，植物需干净透明边缘，不连背景板或文字一起切入。
- 编辑和去背景默认使用可用 imagegen 工具；用户明确指定其他处理方式时遵从。生成资产是重建，不保证逐像素恢复；记录 prompt、来源和轮廓对照。
- 缺字体时测试本机候选与真实 CJK fallback，比较字形、基线、换行；缺 SVG 时描绘轮廓并校准线宽。不能以无源文件为由放弃整个重建。
- 不规则背板描绘为闭合 Bézier path，保留顶部台阶、斜边、圆角变化和遮挡关系；随手画一个异形矩形不算通过。

## 4. 实现分层页面

按 [html-css-contract.md](references/html-css-contract.md) 实现。UI 文字能选择、替换；文字、背板、照片、投影可分别隐藏。按钮和导航需要可见状态及结果，不只是隐藏播报、console 或 data-clicked。

保留参考中的排列规则：例如相机横排、普通导航上下排、选中胶囊大小；图标语义、线宽、形状都对齐。先锁定基准视口，再测小/大屏及长文案，允许滚动，不压缩文字过关。

## 5. 浏览器校准循环

读取 [acceptance.md](references/acceptance.md) 与 [visual-convergence.md](references/visual-convergence.md)。
- 等待字体、图像解码，固定数据、时钟、滚动、动画，记录实际环境。
- 用 `node scripts/capture_native.cjs /path/to/prototype /path/to/playwright <state-id>` 从当前 `index.html` 一次性采集原生截图、DOM audit 与源码哈希收据；收据和截图/DOM 哈希必须一致。不要手写或复用旧截图的收据。脚本默认本地 `file://` 独立页面、1 参考像素 = 1 CSS px、DPR=1；其他坐标策略先按 render-contract 明确转换。
- 此脚本的 `state-id` 只标记证据，**不会自动导航、点击或注入该状态**；它也不会自动应用 render-config 中的全部环境参数。仅在入口真实呈现目标状态时直接使用。弹层、选中项、表单及多路由状态须在同一浏览器会话执行真实触发、验证 landmark 后再采集截图和 DOM；不能把同一初始页改名为多个状态的证据。
- 采集基准截图、隐藏照片后的 UI 截图、逐层开关和修改文字后的截图；scripts/audit_dom.js 收集真实 DOM 文本与几何。
- 输出原图/实际并排、叠加和差异图。运行 `scripts/diagnose_visual.py`，读取失败 ROI、最差局部块和 RGB 偏差；按错误贡献选择下一处修复，不凭整体观感随意微调。每轮只改一类因素，重截并记录该 ROI 与全图误差变化。
- 每轮修复前保存上一次浏览器原生截图；新截图用 `scripts/compare_iteration.py` 对照冻结 ROI。它给出全图、各区域 MAE 和变化像素比例的前后差异；有关键区域回退时检查原因，再决定保留或撤销。截图必须来自实际页面，不得把参考图当作候选截图。
- 全图 MAE 不能替代局部验收；按 ROI 检查关键区域，阈值调试前固定。禁止为通过改基准、放宽阈值或排除整块 UI。
- ROI 合计覆盖至少 75% 的原图，且每个文字、按钮及占画面至少 1% 的可见图层中心必须处于某个 ROI 内。按 `subject`、`panel`、`typography`、`controls`、`icon` 等视觉角色建立具名局部区域；不要用一个整页 ROI 代替局部测量。每个 ROI 同时检查 MAE、变化像素比例与轮廓/边缘差异；异形背板、主体轮廓、底栏和图标单独设紧 ROI。浏览器实际字族、颜色、透明度与字体尺寸都要核对；DOM 中出现未登记的可见文字/控件也不能记为通过。
- 对照 `referenceBounds`、DOM 边界与叠加图核对文字、按钮、重要背板和图标。数字检查只覆盖边界框；背板 Bézier 轮廓、植物透明边缘、前后遮挡、圆角和阴影仍要逐层人工核对，并在关键 ROI 中用边缘差异约束。若一页尚无源图测量，不把 DOM 自动盘点填入 `referenceBounds` 来消除失败。
- 人工视觉复核必须查看**当前源码对应**的原图、浏览器截图、叠加图、原始差异图及隐藏图层证明，并在 `acceptance.json.manualReview.states[]` 对素材身份、背景、字体、轮廓、层级与控件逐项写具体观察；不能只填一个 `passed` 标志。任何一项仍明显不符，该项和页面保持 `pending`。
- 若一个失败区域连续两轮没有改善，改变素材来源或重建方法，重新核对参考测量；不要继续叠加 CSS 补丁。主体/背景/字体轮廓未匹配时不得跳到小图标抛光。
- 主交互验证可见结果和返回/关闭；未设计的目标页可用明确标为演示的 sheet，不能声称业务已接入。

## 6. 验收和交付

运行 skill 目录内：
```sh
python3 scripts/validate_manifest.py /path/to/prototype/layer-manifest.json
python3 scripts/validate_prototype.py /path/to/prototype
```

--structure-only 只用于开发诊断，不代表最终通过。

严格验收失败时，保留冻结阈值和失败证据，继续 [visual-convergence.md](references/visual-convergence.md) 的修复循环。`validate_prototype.py` 对 `one_to_one` 档设有不可放宽的数值上限，还要求逐状态的结构化人工视觉记录；即使 token 与 acceptance 同步扩大、或只把人工字段改成 `passed`，也不能通过。数值上限是必要条件，不代表脚本能自动判断植物品种、素材真伪或美感。只有严格校验与实际并排复核都通过，才把视觉状态记为 `passed`。多页请求对每页执行同一门槛；任一页面 pending，整批状态仍为 pending。使用冻结清单运行 `python3 scripts/validate_batch.py /path/to/pages --expected-pages /path/to/pages/expected-pages.json --out /path/to/pages/batch-acceptance.json`，从每页严格校验的退出结果生成整批报告；不能用索引图或平均误差代替。缺合同的批次先运行 `python3 scripts/triage_batch.py /path/to/pages --expected-pages /path/to/pages/expected-pages.json --out /path/to/pages/visual-triage.json`；按基础/精修阶段和用户优先级选择下一页，不把 `nextAcceptanceCandidate` 视为单页阻塞。若已穷尽可用素材/工具仍无法匹配，明确写出阻塞的资产或源信息、尝试过的修复及当前误差；不能靠扩大阈值或隐藏区域取得通过。

交付 index.html、CSS/JS、独立 assets、reference、design tokens、layer/asset manifests、render config、state matrix、geometry/typography tables、interaction map，以及 evidence/ 中的 DOM 报告、截图、diff、图层证明和 acceptance.json。机器校验字段见 acceptance。需要 Flutter 时读取 [flutter-mapping.md](references/flutter-mapping.md)。

哈希收据防止误用过期截图，但不等于证明视觉相似；原图与实际图仍要逐页并排审阅。生成图缺少可提取的原始素材时，继续尝试同源提取/重建，不能通过放宽误差掩盖差异。

分别报告结构可编辑、视觉还原、交互、适配。只有四项都有证据且关键差异清零才说完成。关键资产、轮廓或字体明显不符就继续校准；确有工具/信息限制时交付当前状态、具体未通过项和已尝试方案，不退回整屏贴图。格式校验和文件存在不是视觉验收。

## 调用示例

- “用 $image-to-layered-html-prototype 从这些已认可图片提取设计标准，再实现全部页面；文字、图标、异形背板独立可编辑，给真实浏览器截图。”
- “用 $image-to-layered-html-prototype 先通过 imagegen 设计这个产品，再拆分素材并做分层 HTML；沿用已选方向，逐页记录差异。”
- “用 $image-to-layered-html-prototype 修复当前 HTML：优先核对植物遮挡、背景板轮廓和底栏选中态，保留参考图并输出修复前后对比。”
