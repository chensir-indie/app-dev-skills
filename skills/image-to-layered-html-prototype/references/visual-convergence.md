# 视觉收敛：从失败截图走到通过

这份流程用于 `validate_prototype.py` 的视觉检查失败时。它不能保证任意扁平图都能逐像素还原；它要求先消除可修复的差异，并以同一套冻结标准复测。结构通过、可点击或总体 MAE 下降都不是视觉通过。

已有 HTML 尚缺合同时，先保存原始源码与修改前截图。首次运行 `inventory_page.cjs` 需要 `index.html`、`reference/source.png` 和目标画板根元素的 `data-artboard`；只在现有根元素补属性，沿用已有布局，不重建 wrapper。盘点结果只描述实现，不能代替独立参考测量。

## 1. 先处理决定性素材

在排版精修前检查占比大的主体、照片、纹理与装饰。把参考与候选素材并排看：叶片/物体数量、可见轮廓、孔洞、透视、光向、裁切、阴影和透明边缘。**语义相同不等于资产相同。** 找到同一次生成的独立素材时优先使用；否则按 [reconstruction.md](reconstruction.md) 用 imagegen 对参考做局部提取/编辑，保留未经修改的参考。若提取后的可见轮廓仍错，继续重建或换方法，不用另一个“差不多”的植物压过整页。

候选照片/主体必须先放入真实 HTML 图层并用同一浏览器、同一视口截两版页面，不能直接比较原始素材与参考的整页。若页面合同尚未建好，先用 `scripts/compare_candidate.py` 做局部 A/B：

```sh
python3 scripts/compare_candidate.py \
  --reference /abs/page/reference/source.png \
  --baseline /abs/page/evidence/previous-browser.png \
  --candidate /abs/page/evidence/candidate-browser.png \
  --roi LEFT TOP RIGHT BOTTOM \
  --out /abs/page/evidence/asset-candidate.json
```

该脚本要求原图和两版**浏览器全屏实拍**尺寸一致，列出全图及素材区域的 MAE、轮廓差异和 RGB 偏差；候选必须改善素材 ROI，同时不能让全图退步。`keep for further visual review` 只表示值得继续检查，绝不是视觉通过。检查候选资产本身没有携带文字、按钮、卡片边框或菜单，再登记来源、prompt、SHA 和局限。若完整合同已存在，仍以冻结 ROI 的 `compare_iteration.py` 和最终严格校验为准。

背景另作无 UI 的图层：先从无遮挡位置采样色场/明暗，再匹配渐变停靠点、纹理、模糊和装饰路径。不能把截有文字、按钮或背板的参考块当作独立背景资产。没有可用原字体时比较多个实际渲染的候选字族，选择字形和基线更接近者；记录尚未恢复的字体来源不确定性。

## 2. 冻结验收目标并定位误差

原图 SHA、尺寸、状态、具名角色 ROI 和 `design-tokens.json` 中的 `one_to_one` 阈值在调参前冻结；阈值还必须满足 [acceptance.md](acceptance.md) 的不可放宽上限。每轮先用 `capture_native.cjs` 从当前 HTML 重采截图、DOM 和哈希收据，再运行：

批量草稿尚无合同时，先按下文「多页推进」运行分诊，补齐选定页面合同后转入冻结 ROI 诊断。triage 的分数不是验收成绩；全图 MAE 低也不能跳过文字、按钮和轮廓。

```sh
python3 scripts/diagnose_visual.py /path/to/prototype --state <state-id> \
  --out /path/to/prototype/evidence/visual-diagnosis.json \
  --overlay-out /path/to/prototype/evidence/visual-overlay.png \
  --heatmap-out /path/to/prototype/evidence/visual-heatmap.png
```

脚本返回非零表示至少一个冻结视觉指标未过。报告按「超标 MAE × ROI 面积」排序，同时列出最差 128px 局部块、变化像素比例、边缘不一致比例及 `actual - reference` 的平均 RGB。排序用于先处理影响面积最大的差异；相互重叠的 ROI 误差不能直接相加。数值用于定位，不自动判断差异属于哪种图层；必须看原图/实际/叠加/热图和独立图层截图。保留零阈值原始差异，不能只看容差后的结果。

轮廓差异独立参与每个 ROI 的通过判定；异形背景板、植物边缘、按钮和图标应分别看轮廓叠加，不能靠相近的均色掩盖形状错误。

## 3. 一次只修复一类成因

按最差区域和图层证据选择：

| 观察 | 首先检查 |
|---|---|
| 大块实色或明暗偏差 | 背景/面板颜色、透明度、混合模式、模糊与阴影 |
| 物体两侧都出现高差异 | 主体素材、透明边界、尺度、裁切、旋转、层级 |
| 字附近呈双边缘 | 字族、字重、字号、基线、行高、字距和抗锯齿环境 |
| 细线或拐角局部高差异 | SVG 路径、描边宽度、圆角及光学校准 |
| 整页似乎平移 | 参考坐标、视口/DPR、状态栏、安全区或截图滚动位置 |

每轮修改一类因素，重载当前源码，等待字体和图片解码，截原生尺寸。保留前一轮截图，运行：

```sh
python3 scripts/compare_iteration.py /path/to/prototype --state <state-id> \
  --before evidence/iteration-before.png --after evidence/native.png \
  --out evidence/iteration-report.json
```

报告列出全图和每个 ROI 的前后误差；若全图改善但关键区域明显回退，查看叠加图后再决定是否保留。先解决大面积与高对比区域，再解决小图标。不要以 CSS 色块掩盖错误素材；不要通过缩放文字躲避错误字体。`compare_iteration.py` 是收敛建议，不是最终验收门槛；最终仍以严格 `validate_prototype.py` 和人工轮廓/层级检查为准。

同一类别连续两轮无改善，就停止局部微调，重新检查资产/测量/渲染方法。若关键素材无法从参考可靠提取，记录具体缺失、失败尝试和受影响 ROI；仍可交付结构，但视觉状态必须为 `pending`。不要将该状态说成“验收通过”。

## 4. 通过门槛

对每个请求的页面和状态重新运行原生尺寸采集、DOM/图层证明、`diagnose_visual.py` 与严格 `validate_prototype.py`。ROI 并集至少覆盖 75% 原图，并以对应角色覆盖至少 80% 的文字、按钮、主体和重要面板/图标图层；全图及关键 ROI 都低于原先冻结的阈值和固定上限。打开原图、当前浏览器截图、叠加图、原始差异图和图层开关证明，逐项核对主体身份、背景、字形、轮廓、遮挡和控件，再按 [acceptance.md](acceptance.md) 将具体观察记录到 `manualReview.states[]`；六项任一未过就保持 `pending`。`--structure-only` 仅说明 HTML 图层合同有效。

多页交付以逐页状态表收尾；一页失败不等于整批通过。若当前回合没有完成所有被请求页面，列出仍未通过的页面及各自最主要的差异，不以索引页或首个试点充当完成品。

## 多页推进

从全部参考图目录冻结 `expected-pages.json`（页面目录名数组）。基础稿尚无合同时运行：

```sh
python3 scripts/triage_batch.py /absolute/path/to/pages \
  --expected-pages /absolute/path/to/pages/expected-pages.json \
  --out /absolute/path/to/pages/visual-triage.json
```

它报告每页缺件、已有原生截图的全图 MAE 与最差局部块。默认可先把最接近完整的一页严格闭环，再推进下一页；`nextAcceptanceCandidate` 仅是建议，结合 `visualRepairOrder` 和用户优先级选择，不把某页缺素材变成整批停工条件。

用户要求先铺齐时，用两阶段流程：第一阶段逐页建立独立可打开 HTML、可编辑 DOM 文字、语义按钮、独立素材与原生截图，检查图片加载、参考图不进入运行时、基础交互与尺寸，报告基础状态；第二阶段逐页补 tokens、源图测量、合同、具名 ROI 和严格验收。不能把页面可打开数量当作视觉通过数量。

最终运行：

```sh
python3 scripts/validate_batch.py /absolute/path/to/pages \
  --expected-pages /absolute/path/to/pages/expected-pages.json \
  --out /absolute/path/to/pages/batch-acceptance.json
```

批量结果来自每页严格检查退出码；遗漏 HTML 或已有参考目录均失败。索引图、平均误差和首个试点不能替代逐页结果。记录仍未通过页面、主要差异和已尝试修复；关键受阻页保持 `pending`，继续其他可推进页，随后回访。
