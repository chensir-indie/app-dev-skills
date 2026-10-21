# 六级设计标准

本文件补充设计决策；机器字段继续采用 layer-manifest、render-contract 和 acceptance 中的现有格式。不要创建与这些文件竞争的第二套验收 schema。

设计探索或用户要求优化时，先按 [设计质量评审](design-quality-review.md) 明确任务、主设计系统与改动范围；复刻时从认可图提取规范。共享标准优先复用项目已有文件，页面例外明确记录，不另建竞争的 token 源。选规范与工具时查 [来源](design-sources.md)。

## 0. 视觉方向

用可执行描述明确视觉主角、主要动作、背景明暗、文字对比、材质、内容密度、留白以及参考中的关键识别特征。例如“植物超出半透明异形背板，底部有独立浅色选中胶囊与深色相机按钮”。不要只写“高级、大气、清新”。这是示例，不限定所有项目为植物或玻璃风格。

## 1. 基础变量

从参考采样并写入 design-tokens.json，生成或同步 CSS variables。记录每项值的来源为 measured / inferred / unresolved，以及关联参考与测量说明。

| 类别 | 必须明确的参数 |
| --- | --- |
| 颜色 | 背景、主次文字、图标、描边、选中、禁用；颜色与 opacity 分开 |
| 字体 | 字族、实际 CJK fallback、字体文件及授权来源、weight、size、line-height、tracking |
| 布局 | 基准画布、边距、模块间距、对齐锚点、内容宽度、系统栏区域 |
| 形状 | 逐角圆角、描边粗细、异形路径和 viewBox、按钮光学边界 |
| 材质 | 渐变方向与 stops、透明度、blur、shadow 偏移/扩散/颜色 |
| 图标 | 来源、viewBox、可见边界、线宽、端点、连接、填充/描边、光学位置 |
| 状态 | default、selected、pressed、focus、disabled，以及相关 loading/error |
| 动效 | 实际交互需要的时长/缓动、减少动态效果模式；静态图无法推断的值标 inferred |

使用 primitive → semantic → component 的引用关系，例如调色板 → navigation.selectedSurface → 底栏选中胶囊。同一语义值不在每页重复微调；参考确实不同时记录组件变体，不强行“统一”成与参考不同的图。

从有透明叠加的截图采样得到的是最终合成颜色，并不等于 CSS 原色。以实际合成结果校准，不能把采样色再次叠加原透明度而变淡。

## 2. 图层和资产

在 layer-manifest 为背景、纹理、装饰、背板、主体、文字、图标、控件、浮层建立独立项。记录 parent/stacking-context 关系到 geometry-table；z-index 数字本身不证明遮挡正确。

背板拆解记录：顶边台阶、斜边两端、曲率转折、各角切点、闭合路径、填充/描边/阴影。测量可见段，被主体遮住的段注明 inferred。不要为了好写 CSS 将不规则轮廓换成矩形。

植物使用可见 alpha 边界定位。PNG 大量透明留白会让相同 width 产生不同视觉比例；记录 intrinsic size、alpha bounds、目标可见矩形，校准 object-fit/object-position。

不把跨级需求混为一谈：页面层级表示导航关系，视觉图层表示遮挡关系，DOM 层级表示实现结构；三者都需明确。

## 3. 组件标准

仅定义本次范围实际出现的组件，并在 component-spec.md 记录以下项目：

- anatomy：背景、图标、文案、状态标记各自的图层和 selector。
- geometry：外框、内部 padding、间距、文字基线、图标可见大小、圆角/路径。
- states：每个已要求状态的颜色、尺寸变化、语义属性、可见反馈。
- interaction：触发、结果、返回/关闭、键盘操作，演示数据与真实服务的边界。
- content：文案来源、最大/长文案策略、本地化、空值处理。
- evidence：使用该组件的页面/状态、参考区域、截图与未解决差异。

底栏专项检查：外壳和内嵌选中块分别量尺寸与边距；普通项目可上下排，相机按钮可横排；选中胶囊、未选中项、主动作不必等宽。分别定义当前页面选中与按钮按下反馈，不把 selected 和 pressed 当同一种状态。图标用同源 SVG 或精确描绘，emoji 不能作为最终替代。

可见尺寸与点击目标分别记录；扩展 hit area 不能遮挡相邻控件。像素还原稿与可访问性/适配修订应分别展示差异；原图存在低对比时明确记录，不悄悄改图后声称完全一致，也不把有缺陷的稿当生产可访问性通过。

## 4. 页面和状态

在 page-map.md 列出页面层级、入口、退出、主要操作与目标路由；用 state-matrix.json 绑定每个参考状态。首页、列表、详情、设置、表单、弹层只有在本次范围内才纳入，不为“完整”擅自增加业务功能。

有用户参考的状态执行像素对照。没有参考但实际需要的 loading/empty/error/权限状态沿用组件标准，注明 designed/inferred，只验收可用性和风格一致性，不能伪造它们的原图或宣称已经通过源图对照。现有严格验证器要求带参考的状态；这类无参考状态单独写入 supplemental-states.md 及交互证据，不能提交到原图对照状态表冒充已有参考。

组件共用修改后检查全部消费者；尤其详情页、编辑页和弹层复用的文本、输入框、按钮。批量报告逐页写状态，不用平均值掩盖某一页失真。

## 5. 验收与移交

先复现基准视口，再检查窄/宽视口、长文本和键盘/滚动。锁定图不等于响应式产品；两者单独验证。页面浏览入口应明确区分“参考图”和“实际 HTML”，默认打开实际 HTML，另页显示并排/叠加比较。

每页交付：可运行 HTML/CSS/JS、独立素材、可编辑设计变量、图层/组件/页面标准、真实截图、差异与交互证据。完整目录可按下列结构组织；验证器要求的文件名以现有 references 为准。

```text
prototype/
  index.html, styles.css, app.js
  assets/                       # 独立主体、照片、字体、纹理
  reference/                    # 锁定原图，运行页不加载
  design-tokens.json, layer-manifest.json, asset-manifest.json
  render-config.json, state-matrix.json
  geometry-table.md, typography-table.md, interaction-map.md
  component-spec.md, page-map.md
  evidence/                     # 浏览器截图、DOM、收据、对比、图层证明
  acceptance.json
```

Flutter 移交复用这些标准与资产，再按 flutter-mapping.md 校准原生实现。获得 HTML 通过不自动授权修改/发布应用，也不等于 Flutter 或真机已通过。
