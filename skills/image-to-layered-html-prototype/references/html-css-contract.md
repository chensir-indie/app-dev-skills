# 可编辑实现

## 结构
背景使用 CSS 或独立无 UI 装饰资产；背板使用 CSS / SVG；图片只承载照片与主体；文字使用 DOM；可见按钮使用 button / a。禁止整屏 raster/canvas、UI 大切片和隐藏文字盖在截图上。

所有交付图层带稳定 id / data-layer-id。文本与控件映射 manifest selector；图片带 data-asset-role="subject|photo|decoration|logo"。不允许用 data URI 隐藏参考整图或把截图放入 SVG image。参考整图仅用于独立 review.html，不能被 index.html 请求。

## 排版与层级
固定基准坐标后可以采用 absolute、grid 或 flex；选能复现测量值的方式。禁止不经测量的 space-between。
层级显式表达 background < decor < backplate < subject < content < navigation < dialog；不是强制固定数值。
overflow、transform、filter、opacity 都会影响堆叠；用逐层隐藏和交叉点检查，不只看 z-index 数字。
规则圆角逐角记录。不规则背板 SVG path 需要测量转折点和曲线，禁止用大圆角矩形代替。
文字使用显式字族/真实 fallback、字重、字号、px 行高、字距、颜色、对齐、换行；清除 button 等浏览器默认样式。
导航记录每项自己的形状、图标与文字方向、选中/未选中状态，不能默认等分或默认横排。

## 交互
可见控件有实际反馈：导航切换可见内容及 aria-current，添加操作更新列表/按钮状态，详情可打开关闭。
仅写 data-clicked、console、隐藏 aria-live 不算完成。不可用的生产行为明确为演示，不能写用户真实数据。

## 可编辑证明
用浏览器修改标题并截图；分别隐藏 subject 与 backplate 再截图；隐藏全部 photo/subject 后，标题/背板/导航/按钮仍存在。这些是检查步骤，不是最终页面功能开关。
