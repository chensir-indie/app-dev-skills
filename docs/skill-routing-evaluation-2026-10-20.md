# 技能路由与交接评估

日期：2026-10-20。

本记录对三个技能进行**桌面推演**：读取 README、SKILL.md 与相关参考，推导面对真实请求时应走的分支、使用的工具和完成边界。没有让 Agent 在六个场景中实际制作产品产物，不能将本记录视为六项行为测试通过。文末另列实际执行的结构检查；结构检查也不能证明 Agent 的路由或视觉判断正确。

## 比较依据

上游为 [mattpocock/skills](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2)，固定提交 `5beb35b040e3de97e54fa9e386d7e42d15c295c2`。本次借鉴四个机制：

- [ask-matt](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/ask-matt/SKILL.md)：按当前处境选择流程；推荐之前读目标技能。当前三个技能保留独立入口，在起点表中消除误路由。
- [prototype](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/prototype/SKILL.md)：问题决定产物。仅需方向或提示词时，应有自己的完成边界。
- [handoff](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/handoff/SKILL.md)：引用已有成果，携带下一任务需要的上下文。
- [writing-for-agents](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/writing-for-agents/SKILL.md)：引用同时说明内容和触发条件，步骤保留可判断的完成标准。

现有竞品采集闭环、原型独立测量与视觉门槛、封面矩阵及哈希绑定复核仍是当前技能的核心合同。本次不套用上游临时原型的“跳过测试/打磨”，也不增加第四个 router skill 或额外审批步骤。

## 场景 1：明确调用了错误技能

**请求**：用 `app-store-cover-generator` 把这张 App 首页一比一转成可点击 HTML，不加营销文案。

原有 cover 起点表没有界面重建分支，description 中未限定范围的 typography/overflow 也容易吸引普通页面修复；按 Build or refine 可能进入封面项目初始化，产物不符合用户目标。

修订后按目标产物纠偏：若当前环境有 `image-to-layered-html-prototype`，先读其 SKILL.md，再走 UI 重建。缺少该技能时说明目标与当前适用范围，利用已有能力继续指导，无须先安装新工具。cover 的排版触发词限定为 store-cover。

同时核对三个技能的 picker 元数据：prototype 的名称从 Imagegen 改为 Image，简介覆盖 UI 图重建和既有 HTML 修复，默认提示区分方向/提示词、重建和修复；cover 简介明确 App Store cover artwork，默认提示按概念、局部修复或导出矩阵结束；analysis 现有证据范围和采集提示保持不变。

**行为验收**：不初始化 cover 项目，不附加营销标题；选用 UI 重建路径后才按需读取 render、geometry、acceptance。方向纠偏本身不要求运行 doctor。终点是用户请求的原型及其真实状态，不是封面导出。

## 场景 2：缺少执行环境

**请求**：根据提供的 UI 图做完整原型；环境缺少 Python 或 Playwright/browser。

原有 prototype 在首次使用时即要求完整 doctor，且未明确缺项后的独立工作边界。修订后仅在执行依赖脚本前检查；按任务选择 `sh scripts/doctor.sh --scope python` 或 `--scope browser`。检查器本身仍需要 Python，browser scope 并不等于完全无 Python；其真实依赖没有被说明修改掩盖。

缺项按技能内环境说明和实际诊断提供修复路线，同时保存参考、页面清单和草稿，继续不依赖缺失环境的分析/设计。环境恢复后再运行所需脚本，不把静态设计进展当成浏览器证据。

**行为验收**：列出实际失败项、修复命令和待运行命令；独立工作有可交付产物；依赖脚本的检查与视觉验收保持 `pending`。doctor 不自动安装、不更改代理或软件源；没有实际截图时不声称视觉通过。

## 场景 3：修复既有 HTML

**请求**：现有页面及认可参考已提供，只修字体和背板轮廓，保留页面交互。

原有起点表说先盘点，正文却先进入全套参考/合同再介绍 inventory。修订后明确保留源码、素材、交互及修改前证据，先执行 `node scripts/inventory_page.cjs /absolute/path/to/page`，再补独立测量和合同。

inventory 要求 `index.html`、`reference/source.png` 和目标根元素的 `[data-artboard]`。首次盘点前保存原始源码与修改前截图；缺少标记时只在现有目标根元素补属性，保留已有布局，不重建 wrapper。它提供实现观察与真实截图，不生成参考坐标或验收结果。源图测量仍读取 reference-geometry；修复和收敛读取 visual-convergence；严格验收继续遵守 acceptance。CLI 的文件入口限制没有被扩大成任意网页应用支持。

**行为验收**：原项目得到保留，修改集中在请求的字体/轮廓；有修改前后证据。实现坐标没有反填为参考坐标，没有改参考图或放宽阈值来消除失败；最终分别报告可编辑、视觉、交互和适配状态。

补充命令实测：临时 `main`/标题/按钮 HTML 与 390×844 PNG 在没有 `data-artboard` 时返回退出码 1（`Missing [data-artboard]`）；保留原始文件、仅在现有 `main` 增加该属性后，Chrome `155.0.8059.85` 上同一 inventory 命令返回 0，生成截图和报告，识别到 1 个文字与 1 个按钮。该夹具验证首次盘点的前置条件，不是完整页面视觉验收或 Agent 场景实测。

另对 cover 的既有项目应用同一原则：原有 Build or refine 统一要求复制 starter，现改为仅新项目初始化；旧项目保留配置、素材、矩阵和审批历史，修改请求的单元或共享源码并更新受影响证据。

## 场景 4：竞品 → 原型 → 商店封面

**请求**：分析竞品，做我方 UI，再出商店封面；尚无我方真实 App 截图。

阶段箭头本身不足以传递证据身份。修订后每个技能只携带下一阶段所需字段，引用已有文件：

| 交接点 | 最小上下文 |
| --- | --- |
| 分析到设计 | 报告/证据入口、用户采用的决策、未验证假设、下一产物 |
| 原型到实现 | 采用参考路径与 SHA、页面/状态、源码入口、可编辑/视觉/交互/适配状态、未过项 |
| 封面到下一阶段 | 应用、目标阶段、语言/设备/页面矩阵、截图来源、最终哈希、绑定复核、待处理单元 |

分析建议不自动成为认可设计；HTML 原型截图不自动成为真实 App capture。按用户原有目标推进，在缺少真实 App 截图时可交付明确标注的概念封面，不把其描述为真实 UI 或 upload-ready。

**行为验收**：新阶段可从已有文件定位源证据和状态；不重新编造分析；不把竞品截图、概念图、原型截图改称我方 App 实拍；不因导出成功直接进入上传或发布。

## 场景 5：只要概念或提示词

**请求**：给我三个 UI 方向和生成提示词，暂时不要 HTML。

原有 prototype 的“只有产品方向”直接进入生成、锁定参考并重建，容易扩大任务。现在起点表区分仅概念、完整原型和既有修复；按 imagegen-workflow 只交付请求的方向/提示词即可结束。若用户仅请求参考图，实际生成后查看图片，但不自动进入 HTML 重建。

imagegen-workflow 的入口和后续章节也同步标明三个终点；资产追溯、HTML 核对及完整多页步骤只在完整重建时展开，避免入口与按需参考发生冲突。

**行为验收**：方向/提示词任务不运行 doctor，不初始化原型，不因缺少 Python/Node/browser 而阻塞；不消耗一次无关图像生成。实际生成图片遵循当前环境工具规则；草稿不写成 user-approved。cover 既有的概念终点也保留并在 README 说明。

## 场景 6：竞品关键证据不足

**请求**：分析竞品最新版离线、账户和重复使用行为，起始材料仅为营销页。

当前 app-competitor-analysis 已要求读取 evidence-model，并在关键证据不足时执行 evidence-acquisition 闭环：定义闭环证明、实际获取和查看、更新报告/关系图，再复核。此路径无需为借鉴上游而重写。

可用路线依授权与当前工具决定，包括官方来源、可查看的像素材料、录屏和本地授权文件。需要结构化审计时先 doctor，再用 `audit_evidence.py`、`audit_acquisition.py`；这些脚本验证记录结构，不能获取来源或证明结论为真。报告按 html-delivery 生成并实际浏览器检查。

**行为验收**：记录真实获取尝试及结果；营销图、官方声明、静态发现、运行时观察保持不同证据身份；没有依据的边保留未知，不为凑齐关系图编造。可继续的研究没有被未来任务清单替代；具体受阻时保留条件和下一观察。HTML 生成成功但缺少浏览器复核时，后者仍为 pending。

## 实际检查及其范围

三个技能的 `skill-creator/scripts/quick_validate.py` 均返回 `Skill is valid!`（退出码 0）。仓库 `scripts/check_collection.py` 在根导航补齐后返回 PASS；初次缺失的直接 SKILL.md 链接已修复。

完整集成命令 `PLAYWRIGHT_CHANNEL=chrome npm run check` 已通过（退出码 0）：根 Python 87 项、封面 44 项、原型 Python 83 项，共 214 项单元测试；竞品 HTML 3 项与封面 13 项浏览器测试全部通过，无跳过；原型 DOM 检查通过。实际浏览器为 Chrome `155.0.8059.85`。检查中发现四个浏览器测试文件未跟随环境选择，已修正五处 launch 参数，默认仍用 Chromium，未削弱断言。

默认 Chromium 缓存缺失，官方安装器下载出现 `ECONNRESET`；默认 `npm run check` 因而在 doctor 阶段失败，此环境缺口仍在。Chrome 结果不表示 Chromium 已安装，也不代表两种浏览器像素输出相同。最终文案复核另将原型的完整交付清单限定为重建分支，并把封面 doctor 移到首次代表渲染之前。

技能结构与文档检查覆盖 frontmatter、命名、占位内容、发现元数据和独立文件链接；自动回归覆盖样例上的工具行为。这些结果不验证上述六个场景的 Agent 行为，也不验证实际产品视觉。
