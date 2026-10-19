# 渲染坐标与可复现性

默认重建检查使用 1 参考像素 = 1 CSS px、DPR=1、screenshot scale=css。
例如参考 591×1280，viewport=591×1280，输出也应是 591×1280。
若用 393×852 logical、DPR=3，则设备截图为1179×2556；必须明确映射并匹配原图，禁止把参考图宽度又乘一次 DPR。

render-config.json 记录实际 browser.version()、viewport、deviceScaleFactor、screenshotScale、locale、colorScheme、scroll、字体来源与 SHA、动画状态、时区、样例数据。
多页共用 CSS/JS/图片时，每页的 render-config.json 可声明 `"sharedRuntimeDirs":["../shared"]`。校验器只允许该页同级、明确列出的共享目录；运行时图像/SVG 仍须在本页 asset-manifest.json 用相对路径（如 `../shared/assets/plant.png`）逐项记录 SHA。共享 CSS/JS/字体与已登记资产会进入截图收据和最终哈希覆盖。不能把另一页、参考图或 evidence 目录伪装成共享运行时资源。
软件包版本不等于浏览器版本；不得把任意测得的 1 级颜色差异未经实验归因于 JPEG 解码。

截图前等待 document.fonts.ready、全部 img.decode() 和应用 ready 标记。冻结过渡、动画、光标，使用固定日期与本地 fixture。
参考图可能来自 imagegen，并不存在“相同源浏览器”；对照的是已冻结像素，不编造其运行环境。

桌面预览可整体等比缩放，必须同步包装容器尺寸，避免 transform 造成空白与横向滚动。
适配测试独立记录 compact / baseline / wide 及长文案。不把整体缩小画布当响应式通过。
