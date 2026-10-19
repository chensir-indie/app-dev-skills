# 原图测量与实现边界分离

`referenceBounds` 是从原图独立推导的目标元素布局框；`bounds` 是当前 HTML 元素的浏览器布局框。文字还必须区分原图可见字形的 `referenceInkBounds`：字形墨迹不包括 CSS 行高留白，不能直接拿 OCR 框与 DOM 行盒比较。严格验收核对布局框，再用源图/实际截图的字形测量、局部差异和人工复核检验墨迹。

## 测量顺序

1. 锁定未经缩放的原图、尺寸和 SHA-256。用原图、放大裁图、网格/标尺或图像查看器，在原图坐标中标出文字、按钮、重要背板/图标的左上角及宽高。不要从实现截图反推参考坐标。
2. 在 `geometry-table.md` 记录元素 ID、`x/y/width/height`、测量锚点、轮廓/圆角、`measured` 或 `inferred` 及不确定原因。透明影子与发光不是内容边界；说明是否包含描边。对文字先记录原图可见字形的墨迹框，再依据该字形、基线与预期行高独立推导目标 CSS 行盒；不要把整块父卡片当文字框，也不要把墨迹框冒充行盒。
3. 把目标行盒或控件/背板布局框写入对应 layer 的 `referenceBounds`，把文字原图墨迹框写入 `referenceInkBounds`。每处文字再登记 `referenceInkMethod`（`apple-vision-ocr` 或 `high-contrast-pixel-core`）和指向原图测量 JSON 的 `referenceInkEvidence`。独立记录 DOM 的 `bounds`，它可以来自真实浏览器 audit。文本层需要独立的 DOM 包裹元素；它的 box 应对应目标行盒。只有 OCR 字形框而无可靠行盒推导时保持 `pending`。
4. 使用 reference/actual 叠加图确认锚点。若边界框匹配但轮廓仍不同，继续修轮廓和材质；通过边界框不等于通过视觉验收。

在 macOS 上可以用 `swift scripts/measure_text_ink.swift /absolute/path/to/reference.png zh-Hant 返回 繁體中文 > evidence/reference-ink-ocr.json` 和同一命令测浏览器截图。可选的词语参数会附带 OCR 合并行中指定词语的字形框，用于把文字与邻近箭头分开。这个只读工具记录图片 SHA、原生尺寸、OCR 文本与字形墨迹框；需要人工核对漏识、合并的图标/文字和标点。OCR 只辅助墨迹测量，不会自动生成 `referenceBounds`，也不自动判定验收通过。

若 OCR 把箭头、标点与文字并成一行，可以在原图上先选一个只含文字的紧 ROI，再用 `python3 scripts/measure_ink_core.py /absolute/path/to/reference.png --box 590 640 735 725 --mode dark` 测高对比像素核心。浅色字用 `--mode light`。结果含图像 SHA、ROI、颜色阈值和像素外框；边缘抗锯齿不会计入核心，所以它是第二份定位证据，仍需与原图放大视图核对，不能直接充当 CSS 行盒。

```json
{
  "id":"page-title", "type":"text", "selector":"#page-title",
  "referenceBounds":{"x":42,"y":195,"width":204,"height":64},
  "referenceInkBounds":{"x":43,"y":204,"width":200,"height":48},
  "bounds":{"x":44,"y":195,"width":203,"height":64}
}
```

这些数字仅演示格式，不是 任何实际页面测量值。`referenceBounds` 对所有文字、按钮以及 `visualRole` 为 `panel` 或 `icon` 的层必填。严格阈值默认最多 2 CSS px；参考图不能可靠测出边界时保持该页 `pending`，说明素材或测量阻塞，继续修可确定的区域，不要将实现值复制成“实测”。

对不规则背板，外接框只约束摆放范围。另记录 SVG path、参考拐点/切线、遮挡关系和具名 `panel` ROI；对含透明边缘的植物，外框只作粗定位，使用 `subject` ROI、透明边缘与参考叶片的局部对照判断。文字还要检查字形、基线、字重、字距、行距与颜色；按钮还要检查内部图标、选中态、圆角和层级。
