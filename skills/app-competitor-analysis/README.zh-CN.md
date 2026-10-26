# App 竞品分析

[English](README.md) · [Agent 工作流](SKILL.md) · [运行辅助脚本](#运行辅助脚本)

从证据解释竞品的 UI、任务流程与技术能力，再形成适合自己产品的决策。每个竞品交付一份独立可读的 HTML 报告，多竞品另附可搜索的索引。

详细界面分析另交付每个竞品的 `Design.md`：逐区域元素、语义视觉规则、组件状态，以及目标、选择、反馈、恢复和完成条件的 UX 评审。HTML 与 Markdown 共用同一份分析记录，见[设计规格合同](references/design-specification.md)。


生成的阅读器采用统一的产品研究画册布局：左侧可搜索竞品库、宽幅证据封面、可深链接的独立分析视图与连续阅读、图像目录，以及有区别的功能/任务/技术图。视觉重做包含真实“参考 / 原版 / 新版”HTML 对照，并将共享排版应用到全部指定报告。具体参考如何转成布局、如何实页评审，见[报告设计合同](references/report-design.md)；原图与明确记录的裁片保持可检查。

## 从你的问题开始

| 现有材料 | 分析起点 |
| --- | --- |
| 截图或录屏 | 可见设计规则、任务状态与重要分支 |
| 多个竞品 | 完整身份清单、逐 App 报告，再按用户任务比较 |
| 获准检查的安装包或源码样本 | 固定版本的静态发现、调用路径与候选实现解释 |
| 证据不完整 | 有依据的发现、明确未知项与下一步有效观察 |

提供目标竞品、自己的产品问题和已有材料即可开始。阅读所提供的证据无需 Python，也不以设备访问为前提。

```text
使用 $app-competitor-analysis 分析这些截图、任务录屏与官方资料。
解释 UI 规则、核心交互分支和有证据支持的技术机制，并联系我的产品需求。
为每个竞品交付完整、独立可读的 HTML 报告和总索引，区分事实、假设与证据缺口。
```

问题较窄时，说明需要哪些分析维度。要求覆盖已收集的全部竞品时，请明确范围；深度抽样仍需保留每个竞品的独立报告。

## 安装

Codex 优先使用[合集安装方式](https://github.com/chensir-indie/app-dev-skills#1-connect-codex-to-one-source-checkout)：一个软链接让所有技能直接从源码目录生效。已有合集链接时，本技能无需再次安装。若只需要本技能，先将仓库克隆到技能发现目录之外，再将下面变量设为它的绝对路径：

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
CODEX_SKILL_LINK="${HOME}/.agents/skills/app-competitor-analysis"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' '技能入口已存在，请检查后再调整。'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/app-competitor-analysis" "$CODEX_SKILL_LINK"
fi
```

迁移前，将 `~/.agents/skills` 和 `~/.codex/skills` 中已有入口与源码比较，保存本地修改，再把淘汰的副本移出技能发现目录。后续直接更新源码仓库。发现尚未刷新时开启新的 Codex 会话，确认本技能只出现一次且解析到源码 `SKILL.md`。以上 shell 示例适用于 macOS/Linux 和 WSL。

其他 Agent 或独立范围可通过 [Skills CLI](https://github.com/vercel-labs/skills)（需要 Node.js 22.20+）安装：

```sh
npx skills@latest add chensir-indie/app-dev-skills --skill app-competitor-analysis
```

选择不与 Codex 链接重复的 Agent 和范围，更新前保留本地修改。安装器需要 Node.js/npm，分析和内置辅助脚本本身无需它们。

## 交付内容

索引和每份报告共用可搜索的左侧竞品列表，高亮当前产品；增强阅读器切换竞品时保留章节，手机端使用可展开的选择器。每份报告仍可通过独立链接离线打开。

每份竞品报告先解释产品的主要任务、独特体验和关键结论，有已检查的图像时，以清晰可读的画面支持分析。四张可追溯证据的图拆解功能层级、带方向的任务流程、页面关系和技术数据流。详细分析覆盖所需维度、使用限制、优势与代价、产品决策和未知项；较长的证据记录可按需查阅，不占据主要阅读篇幅。默认阅读包把图像、样式和脚本保存在同目录 `assets/` 文件夹中，保留原始证据字节，供多份报告共用与缓存。请完整保留或打包整个目录，即可离线阅读；需要单文件交换时使用 `--format standalone`。

[分析深度契约](references/analysis-depth.md)要求重要发现串起证据、机制与状态、因果解释及替代假设、代价、产品决策，以及能够改变决策的验证。文档包含使用同一份证据深化分析的原创示例，并检查换个产品名仍然成立的套话、章节重复和通用占位图。缺少运行证据时保留边界，同时继续有依据的条件推理；字数、图谱数量和自动审计不能证明分析深入。

默认采用[参考 Apple 原则的网页设计契约](references/apple-web-design.md)，明确系统字体层级、中性背景、统一间距、可操作控件和响应式图表。它把官方设计原则转成具体网页选择，包括默认浏览器比例下 17px 正文、至少 13px 的注释，以及 44px 的独立触控目标；实际报告还需检查桌面、手机、文字放大、键盘和打印状态。用户明确要求时可调整视觉方向；这些网页参数不代表 Apple 原生界面认证。

截图支持可见外观判断，运行证据支持记录条件下的行为；官方声明、静态发现与假设分别标注。覆盖矩阵保留证据缺失项。HTML 生成、来源覆盖完整度和浏览器检查分别验收。

需要简洁的研究阅读版时，填写产品 `brief` 和章节 `summary_blocks`，完整分析与协议仍可展开查阅。参见[阅读稿编辑](references/design-quality-review.md#edit-the-reading-copy)。

阅读版把四类完整图谱放在对应说明旁边。在图谱 `reading` 与节点 `caption` 外，填写 `features.priority`、`journey.focus` 和 `dataflow.contract`，分别表达所选任务下的能力主次、含分支的重点路径，以及带具体边界的技术职责。全部原节点、关系与证据状态仍可核对。[图谱设计规范](references/diagram-design.md)包含数据格式、响应式表达和整套报告检查方法。

## 运行辅助脚本

研究可以直接开始。渲染报告或审计记录前，先**在此 skill 目录内**运行只读检查：

```sh
sh scripts/doctor.sh
```

它依次检查 `python3`、`python`，选择可运行的 **Python 3.9+**。下面示例中的 `python3` 应替换为检查实际输出的命令。核心渲染与审计脚本仅使用标准库，无需 pip 依赖、Node.js 或浏览器下载；可选的本地预览图准备命令使用当前解释器中的 Pillow。

缺少 Python 或版本太旧时，检查以非零状态退出，并给出[官方安装入口](https://www.python.org/downloads/)和重试步骤。按所在平台安装受支持的 Python 3，重新打开终端后再次检查。Windows 可在 Git Bash 或 WSL 中执行 shell 检查，并确保该 shell 能找到 Python。准备环境时可继续证据研究，依赖脚本的交付保持待完成。

将内置的**合成示例**渲染到技能目录之外的新文件夹：

```sh
python3 scripts/render_reports.py assets/report-bundle.example.json --output /tmp/teardown-demo --format linked
```

若该目录已存在，换一个新路径；渲染器拒绝覆盖已有内容。用浏览器打开 `/tmp/teardown-demo/index.html` 查看示例。正式工作需替换示例中的分析和证据，将输出放入项目目录。渲染器负责排版，不会寻找来源或撰写结论。

需要结构化研究记录时：

```sh
python3 scripts/audit_evidence.py /absolute/path/to/evidence.json
python3 scripts/audit_acquisition.py /absolute/path/to/acquisition.json
```

前者检查来源关联与覆盖矩阵，后者检查证据缺口的采集记录；两者均不会联网取证或判断结论真伪。格式见[证据模型](references/evidence-model.md)和[采集记录示例](assets/acquisition.example.json)。

浏览器检查使用 Agent 已有工具或人工浏览器。若无法使用浏览器，保留生成结果并明确浏览器交付检查仍待完成；渲染成功本身不能替代这一步。

图片较多时，可先运行 `python3 scripts/prepare_previews.py INPUT.json --output NEW_MEDIA_DIR --bundle-output NEW_BUNDLE.json`，再渲染新 bundle。该可选命令需要 Pillow，保留原图字节并记录派生图哈希，不自动安装依赖。没有该能力时，索引使用符合预算的小图或功能概览。具体定位、返回、原图保留和实测要求见[导航与性能](references/html-delivery.md#navigation-and-performance)。

## 按任务阅读

| 当前任务 | 参考文档 |
| --- | --- |
| 界定结论范围和来源 | [证据模型](references/evidence-model.md) |
| 深化发现或修复浅层报告 | [分析深度](references/analysis-depth.md) |
| 检查像素与设计规则 | [UI 分析](references/ui-analysis.md) |
| 重建任务和状态 | [交互分析](references/interaction-analysis.md) |
| 评估技术机制与替代解释 | [技术分析](references/technical-analysis.md) |
| 跨竞品比较与产品决策 | [综合与报告](references/synthesis-and-report.md) |
| 编写、渲染和检查 HTML | [HTML 交付契约](references/html-delivery.md) |
| 改善报告展示并评审实际页面 | [设计质量评审流程](references/design-quality-review.md) |
| 应用默认设计和浏览器检查 | [参考 Apple 原则的网页设计](references/apple-web-design.md) |
| 验收分析完整度 | [评估准则](references/evaluation.md) |

工作流止于分析与报告交付。应用实现、真机验收和发布分别处理；访问竞品账号或检查文件遵循用户已有授权。

继续进入设计或实现时，引用已有报告与证据，附用户已采用的决策、未验证假设和下一产物。推荐结论本身不代表设计已获认可，也不代表已取得我方 App 的真实截图。

## 研究方法与任务记录

[按决策选择研究方法](references/research-methods.md)，执行同任务比较、启发式检查、指标口径、商业场景、可选评分与决策实验。用[记录工作簿](assets/research-workbook.md)填写真实记录，保留原有功能图、任务图与技术拆解。

```sh
python3 scripts/study_metrics.py assets/study-record.example.json --output study-summary.json
```

示例完全虚构。脚本核对每名用户每产品每任务的首次有效尝试及统计口径，不验证招募真实性、任务等价性或可用性。未执行研究的结果为 null；示例结果不能进入真实竞品结论。
