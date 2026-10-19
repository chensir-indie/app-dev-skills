# Flutter handoff

仅在分层 HTML 的视觉、交互验收通过后作为 Flutter 迁移基准。

| HTML | Flutter |
|---|---|
| CSS 背景/材质 | DecoratedBox / Gradient / 明确的滤镜 |
| SVG 背板 | CustomPainter 或已有 SVG 能力 |
| 独立植物、照片 | Image.asset / 实际业务图片 |
| DOM 文字 | Text + 经校准语义 TextStyle |
| 语义按钮/导航 | 现有共享控件、Semantics、ValueKey |
| 布局约束 | LayoutBuilder / SafeArea / Stack / Flex |

禁止将整屏参考图打包为应用 UI。系统栏由设备负责；静态校准稿中的假时钟不是生产状态栏。
先映射 CSS px 到 logical px，再校准字体、safe area、材质与图像采样差异。固定画布只用于基准验证，生产使用约束布局支持长文本与系统字号。
原型数据只作为测试 fixture；遵守目标仓库的新页面集成测试和设备验证要求，不把 HTML 截图当 Flutter 真机证明。
