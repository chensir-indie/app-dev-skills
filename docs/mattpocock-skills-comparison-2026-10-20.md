# mattpocock/skills 对照调查与本仓库改进

调查日期：2026-10-20。上游快照为 [`5beb35b040e3de97e54fa9e386d7e42d15c295c2`](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2)，提交日期为 2026-10-19。本文所有上游源码链接均固定到该提交，避免把后续 `main` 的变化算入本次结论。

## 调查结论

最值得借鉴的是一套让技能保持可发现、可组合和可维护的约束：按用户现状导航、推荐前读取实际技能、分开人读说明和 Agent 执行步骤、按分支加载参考、为每个阶段定义可观察的完成条件，并在技能变更时同步导航和元数据。

本仓库的执行工具更重：它必须生成和检查 HTML、浏览器截图、图像差异、语言与设备导出矩阵。因此，不能从上游以提示词为主的形态推导出“本仓库应该删脚本”“只用一种语言”或“只做文档检查”。既有证据约束、环境检查和真实浏览器回归应保留，改进重点是入口、概念、阶段交接与防漂移检查。

调查开始时，原工作区包含三项技能、八份中英文 README，以及环境 doctor、竞品报告相关的未提交修改。这些是比较的基础，不应全部归因于本轮。按用户最终选定的提交范围，本文随两项既有技能（分层原型、商店封面）及六份 README 的改进提交；并行的 `app-competitor-analysis`、其验证文档和竞品报告测试不在本次提交内。下文涉及竞品分析的内容保留为原工作区的本地未发布观察，不代表此次提供该技能。

此前的 [README 设计说明](readme-design-notes.md) 记录了其他项目的介绍方式；本文补充对 mattpocock/skills 的源码级比较、取舍和落地追踪，不替换该说明。

## 对照范围和判定方法

已读取上游根 README、`SCOPE.md`、`CLAUDE.md`、`GLOSSARY.md`、`.agents/` 约定、`ask-matt`、`writing-for-agents`、`prototype`、`research`、`tdd`、`code-review`、`diagnosing-bugs`，并核对插件清单、脚本、Changesets 和 GitHub workflows。原工作区核对根及技能 README、三个 `SKILL.md`、Agent 元数据、环境文档、集合检查器、测试及 CI；最终提交追踪仅覆盖两项既有技能及集合维护工具。

判定分为三类：

| 判定 | 含义 |
| --- | --- |
| 采纳 | 对本次两项技能及集合维护有直接收益，能在现有安装和交付合同下实现 |
| 条件采用 | 原则有价值，但需要规模、发行方式或用户任务满足条件 |
| 不采用 | 依赖上游的产品定位或工作流，照搬会增加负担、破坏独立安装，或降低现有验收标准 |

“上游事实”只描述固定快照的内容；“本仓库判断”是基于当前需求的工程取舍。文档和自动检查只能证明各自的覆盖范围，不证明技能在所有模型、平台或真实产品上的效果。

## 详细比较

### 1. 定位和范围：用边界减少无效扩张

**上游事实。** README 将技能定位为小而可组合的日常工程实践；`SCOPE.md` 用真实会话中的失败和是否符合项目方向来筛选变更，并区分维护中、试验中和冻结技能。它明确不接受新增技能提案，理由包括目录、文档、路由和插件清单的持续维护成本。[定位](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/README.md#L11-L23) · [范围规则](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/SCOPE.md) · [新增技能的取舍](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.out-of-scope/new-skills.md)

**当前差距。** 调查时的根 README 已明确三个本地技能的输入和产物；本次提交的[根 README](../README.zh-CN.md)仅列两项既有技能。[CONTRIBUTING](../CONTRIBUTING.md) 有打包与测试要求，但本轮开始时没有一个专门说明“为什么增加一项技能、什么属于当前范围、什么必须保留独立授权”的简短入口。

**本仓库判断：采纳范围约束，不照搬关闭贡献。** 新技能应解决独立且反复出现的任务，已有技能的一个分支优先留在原技能内。增加 `SCOPE.md`，把本次分层原型、商店封面及其证据边界写清楚；本地竞品研究不纳入此次发行。上游个人精选库拒绝所有新技能的政策不适合直接复制。提交范围只有两项技能，无须预先创建多层 bucket 目录和空的 deprecated/in-progress 分类。

### 2. README：先让读者判断，再让读者安装和开始

**上游事实。** 根 README 先解释定位，安装部分按 Agent 和更新方式分支，随后给出初次配置和按问题选技能的说明，末尾提供全目录。`.agents/install-block.md` 将安装口径集中管理，并区分托管更新和用户自行维护的文件，要求同一 Agent 选一种路径。[README](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/README.md#L25-L107) · [安装口径](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.agents/install-block.md)

**当前差距。** [中英文根 README](../README.md) 和各技能 README 已有“输入 → 技能 → 产物”、安装、调用和 doctor 引导，基础优于从功能清单开始的介绍。原工作区八份 README、本次提交保留的六份 README 都存在与默认提示、工具命令分别维护而漂移的风险。远程安装与本地未推送版本也必须继续明确区分。

**本仓库判断：采纳入口顺序和一致性约束。** 根 README 负责选择与组合；技能 README 负责独立安装、依赖、首次运行、可观察产物和故障支持；技能指令负责执行。安装路径、完整复制范围和更新时保留本地修改是当前项目的必要信息，不能因上游官网有安装组件而删除。把“选择后先读实际 SKILL”写入维护入口，并对 README 中的技能入口做一致性检查。

### 3. 触发和路由：目录摘要不能替代实际合同

**上游事实。** `ask-matt` 按用户当前情境组织主流程、进入路径、独立工具和底层词汇；文件开头要求在说明某技能行为或建议跳过步骤前，读取该技能实际 `SKILL.md`。`.agents/invocation.md` 区分用户显式调用和模型可自动调用，并要求 Claude frontmatter 与 Codex policy 保持一致。[路由和读取要求](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/ask-matt/SKILL.md#L1-L15) · [调用模式](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.agents/invocation.md#L1-L22)

**当前差距。** 原工作区三个技能本身已能按任务自动触发，但其目录说明、`description` 和 `agents/openai.yaml` 的覆盖范围不完全一致。本次涉及的原型支持截图还原和已有稿修复，而旧的 picker 文案更偏向 imagegen 输入。原有集合检查器验证元数据格式和 `$skill-name`，未验证双端调用策略或完整的目录登记。

**本仓库判断：采纳真实合同与元数据同步，不增加专门路由技能。** 两项既有技能用 README 选择表足够。它们都有明确的自然任务入口，维持模型和用户均可调用；不为了模仿上游而全部设置为只许用户调用。维护规则应区分自然语言导航和真正执行：推荐是索引，执行仍以所选技能的实际步骤和当前授权为准。新增、改名或改变适用范围时同步 README、SKILL 描述与 Agent 默认提示。本次自动检查覆盖元数据类型、格式和完整调用 token；尚未实现 Claude/Codex 双端调用策略冲突检查，若未来引入显式禁用自动调用配置，再补相应场景。

### 4. 按需展开：精简入口，不削弱要求

**上游事实。** `writing-for-agents` 将材料分为执行步骤、同文件参考和通过带条件指针加载的参考。每条指针既解释内容，也说明在什么分支读取。`prototype` 把逻辑与 UI 两种输出分开，入口只留下选择条件和共用规则。[信息层级](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/writing-for-agents/SKILL.md#L10-L43) · [按分支组织原型](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/prototype/SKILL.md#L10-L17)

**当前差距。** 两项既有 SKILL 已有大量本地 references 和按起点选择的表格；原型的具体几何、文字、素材、状态采集和逐页验收要求本身很密集。继续按字数裁剪，容易把冻结阈值、真实状态触发或人工复核删出可见执行路径。README 和 SKILL 中也存在安装概览与环境解释重复的风险。

**本仓库判断：采纳按条件读取和单一权威位置。** 共用起点、执行顺序和完成条件留在 SKILL；字段、算法和边界案例留在 references；环境安装与修复留在 README/runtime。保留会改变执行正确性的硬门槛，尤其是参考哈希、独立测量、真实截图和未通过状态。对入口长度使用维护者可解释的预算，防止无意识膨胀；预算不能成为删验收条款的理由。

### 5. 共享术语：缩短重复解释，防止同词不同义

**上游事实。** 根 `GLOSSARY.md` 定义 Issue tracker、Issue、Decision ticket 等概念、关系和避免使用的近义词；`domain-modeling` 进一步规定术语和 ADR 的记录方式。README 将共享词汇与减少沟通歧义联系起来。[项目术语](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/GLOSSARY.md) · [术语与决策格式](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/domain-modeling/SKILL.md)

**当前差距。** 证据、reference、原型、素材、自动通过、视觉通过、人工审查和发布等概念分布在各技能合同中，根目录没有便于维护者核对的共同词表。尤其“原型完成”“导出通过”和“App 已交付”不能在跨技能交接时互相替换。

**本仓库判断：采纳小型术语表。** 增加 `GLOSSARY.md`，只放跨技能、易混淆的词和状态边界；各技能字段仍由自己的 schema/reference 负责。独立安装的技能不能强依赖仓库根术语表，否则只复制一个技能就失去合同。因此词表是集合维护入口，必要的执行定义仍由技能内部自足承载。无需为此新增一个 domain-modeling 技能或复制上游 issue 领域模型。

### 6. 阶段交付：一个产物通过，不代表下一个阶段成立

**上游事实。** `ask-matt` 区分研究、澄清、原型、规格、实现和复盘；`PHASE-BOUNDARIES.md` 比较继续、清空、交接、子代理和压缩上下文的代价。`prototype` 明确实验回答的问题和之后移交的决策，研究技能要求留下有来源的文件。[阶段路由](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/ask-matt/SKILL.md#L15-L40) · [阶段边界](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/ask-matt/PHASE-BOUNDARIES.md) · [研究产物](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/research/SKILL.md)

**当前差距。** 原工作区曾区分“竞品证据 → 分层原型 → App 实现 → 商店封面”，但跨阶段需要传什么、哪些结论还未验证，仍主要隐含在单个技能合同里。竞品分析是此次未发布的本地研究；其假设若被当成产品事实，仍可能进入封面的功能卖点。对本次两项技能，分层 HTML 若被当成真实 App 截图，同样会破坏素材来源声明。

**本仓库判断：采纳明确交接合同。** 为每个阶段列出输入、交付、通过证据、未决项和下一步进入条件。转入封面阶段需要真实产品素材及有证据的功能文案；实验图和合成素材继续明确标注。保留当前用户上下文与已授权方向，不照搬上游 `/clear`、固定上下文 token 数或默认创建分支/issue 的规则。上游轻量 `prototype` 的“跳过测试”也不适用于本仓库承诺测量和视觉验收的分层重建。

### 7. 仓库维护约定：让一次技能变化有完整影响面

**上游事实。** 根 `CLAUDE.md` 要求正式技能同步顶层 README、bucket README、用户文档与插件列表；新增、改名、移除或适用范围变化时更新 `ask-matt`。安装口径与文档编写规则有各自的权威位置。`AGENTS.md` 是指向 `CLAUDE.md` 的链接，避免维护两份相同约定。[维护规则](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/CLAUDE.md#L1-L25) · [文档同步规则](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.agents/writing-docs.md#L1-L19)

**当前差距。** 当前 `CONTRIBUTING.md` 已约束独立打包、文档对齐和 doctor，但缺少一个短的仓库 Agent 入口，明确遇到什么任务读什么维护文件。原工作区的三项技能列表还曾同时存在于 shell doctor、Python doctor 和检查器逻辑中，增加后可能漏掉检查；本次改为从最终提交实际存在的两个目录发现。

**本仓库判断：采纳维护入口和从文件发现。** 新增短 `AGENTS.md`，把编写规则、范围和术语放在各自文件并按任务引用；发现技能以磁盘上实际 `skills/*/SKILL.md` 为准，发现后校验目录与声明名称，而不是静默跳过坏条目。新增、改名需覆盖 README、Agent 元数据、独立 doctor、tests 和工作区配置。只采用本仓库需要的维护规则，无需复制禁止破折号、作者个人写作偏好或其整套目录体系。

### 8. 自动化检查：把机械错误变成失败信号

**上游事实。** `scripts/sync-plugin-version.mjs --check` 以只读方式检测 package/plugin 版本漂移。`ask-matt` 的复盘部分建议把机械错误转成确定性检查。该快照的根 npm scripts 主要用于 Changesets 和版本同步，三条 workflow 分别处理发行 PR、triage 标签和 needs-info 关闭；它们没有运行本仓库这一类浏览器、图像和独立技能回归。[版本检查器](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/scripts/sync-plugin-version.mjs) · [复盘方向](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/ask-matt/SKILL.md#L32-L34) · [npm scripts](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/package.json) · [workflows](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.github/workflows)

**当前差距。** [check_collection.py](../scripts/check_collection.py) 已验证发现、frontmatter、元数据、许可证、doctor、本地链接和技能外依赖；[CI](../.github/workflows/check.yml) 已执行完整 `npm run check`。本轮开始时，文档登记、元数据异常类型、完整调用 token 和新增技能漏检等问题尚未完整变成可失败的测试。入口规模采用维护者评审的软预算，不作为自动失败项。

**本仓库判断：采纳确定性防漂移，保留现有执行回归。** 对确有风险的约束加检查，并用临时 fixture 验证破坏后会失败。自然语言语义、翻译质量、证据真实性和视觉好坏继续由真实任务与审查负责，不伪装成几个字符串检查就能完全验证。只有新增测试能捕获独立的失效模式时才扩充，不为文档微调堆重复断言。

### 9. 测试和审查：采用行为反馈，调整流程强度

**上游事实。** `tdd` 主张通过公共边界测可观察行为，避免私有实现、同义反复和测试中重新计算实现；它也要求先与用户确认测试边界。`code-review` 将规范符合与需求符合分开审查。`diagnosing-bugs` 要求先建立能复现具体症状的反馈，再定位和修复。[测试准则](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/tdd/SKILL.md) · [双轴审查](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/code-review/SKILL.md) · [诊断闭环](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/diagnosing-bugs/SKILL.md)

**当前差距。** 当前提交已有命令退出码、doctor 缺失依赖和视觉工具浏览器行为测试；竞品报告 HTML 测试属于未发布的本地研究。新增集合规则需要同时检查“合法技能通过”与“出错被发现”；否则检查器本身也可能一直绿却漏检。文档改动则需要检查真实链接、示例命令和英中一致性，而不是给每段文字增加测试。

**本仓库判断：采纳行为测试和两类审查，条件采用 TDD。** 执行校验逻辑变化可先加反例，再修实现；普通文案和可逆低风险修改不强制 TDD，也不增加每项测试都要用户批准的步骤。最终评估分别看是否符合当前打包/证据约束，以及是否确实解决用户这次的 README、技能清晰度和环境支持需求。

### 10. 发行和插件打包：先证明需要，再增加分发面

**上游事实。** 上游有显式技能清单、marketplace、Changesets、自动建立版本 PR 的 workflow，以及 package/plugin 版本同步。ADR 记录了从清单表达能力限制到重新验证 Codex/Copilot 安装的变化；历史决策带日期更新，没有把旧结论当永久事实。[插件清单](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.claude-plugin/plugin.json) · [发行流程](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.github/workflows/release.yml) · [发行决策及更新](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.agents/adr/0002-ship-as-a-claude-code-plugin.md)

**当前差距。** 当前根 package 为私有维护工具，技能通过目录复制或 Skills CLI 独立安装，没有相应插件合同，也没有已验证的托管自动更新链路。

**本仓库判断：条件采用，当前不新增插件或发行自动化。** 当用户确实需要一整套托管订阅安装，且能在目标 Agent 上验证发现、更新、卸载和技能完整性，再增加清单和版本同步检查。先保持真实可用的独立安装；不复制上游自动更新承诺、不建立空壳 Changesets，也不因为新增文档而自动发版。此处讨论的是技能仓库发行，不能延伸为授权移动 App 的 GitHub Actions 打包或上传。

### 11. 依赖和 Python/JavaScript：按任务检查，区分硬依赖与软依赖

**上游事实。** ADR 0001 区分不配置就无法正确执行的硬依赖和只改善输出的软依赖，避免所有技能都要求先 setup。上游也不是单语言仓库：其维护脚本有 Shell 和 JavaScript，部分技能携带 Shell 模板与 CJS 配置；package 的 Node 依赖主要用于发行维护。`prototype` 允许按已有项目选择运行命令。[依赖决策](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.agents/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md) · [维护脚本](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/scripts) · [运行选择](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/prototype/SKILL.md#L19-L26) · [wizard 模板](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/wizard/template.sh)

**当前差距。** 本次两项技能中，Python 负责图像/结构检查，JavaScript 负责浏览器与封面运行，Shell 提供在这些运行时尚未就绪时仍可进入的诊断入口。两项技能依赖不同，要求每个使用者一开始安装整个仓库环境会过重。原工作区的竞品研究还展示了无专用运行时也可先读证据的边界，但该技能不随本次提交。已有 doctor 分 scope 检查和 [环境支持](runtime.zh-CN.md) 正是应保留的基础。

**本仓库判断：采纳按任务前置检查，不执行语言迁移。** 研究、阅读或构思可以先做；即将执行渲染、浏览器或图片校验时检查对应硬依赖。诊断明确缺什么、影响什么、如何修复以及重跑命令；缺失时保持失败退出码，安装与凭证操作不夹在只读检查内。只在真实替代方案能生成同等证据时使用替代方案。用户此次没有要求统一运行时，不能把“上游以 Markdown 为主”或“Node 安装更熟悉”当迁移 Python 的理由。

### 12. 不照搬的实现和项目偏好

| 上游做法与来源 | 当前处理及原因 |
| --- | --- |
| 开始工程流程前配置 issue tracker、triage labels 和文档布局：[setup](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/setup-matt-pocock-skills/SKILL.md) | 不新增前置问卷或远程 issue 依赖。当前工作是文件与视觉证据交付，不必让用户先选择工单系统。 |
| 个人维护脚本会移除同名的非 symlink 安装目录后重建链接：[link-skills.sh 第 55–59 行](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/scripts/link-skills.sh#L55-L59) | 不借用该安装实现。当前复制方式应遇到既有目录时停止，保留用户本地修改。上游自己也将它标记为维护者脚本，不是受支持安装器。 |
| setup 的 verify 模式被列入不接受范围：[取舍记录](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.out-of-scope/setup-skill-verify-mode.md) | 不把该立场泛化为禁用 doctor 或合同检查。提示词配置检查与本仓库实际 Python/Node/浏览器可执行性是不同问题。 |
| 外部官网负责渲染安装组件，所以人读 docs 不写安装命令：[writing-docs](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.agents/writing-docs.md#L13-L19) | 不删除独立技能 README 的安装/依赖说明。当前没有替代其职责的官网组件。 |
| bucket 分类和用户调用/模型调用两轴：[CLAUDE.md](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/CLAUDE.md#L1-L19) | 保持本次两项明确任务入口，维护调用范围和元数据一致性。未来目录变大时再评估分类，不制造空目录和新的学习成本。 |

## 候选行动与验收

以下是本次调查形成的实施范围。状态以末尾的落地追踪为准，候选项不等于已经实现。

| ID | 行动 | 应解决的问题 | 可检查的结果 |
| --- | --- | --- | --- |
| A01 | 增加范围与短 Agent 维护入口 | 新增技能、授权和维护影响面没有集中入口 | 维护者能按任务找到规则；独立技能继续自足 |
| A02 | 增加跨技能小词表与阶段交接说明 | 同词异义和上阶段产物被误当下阶段证据 | 事实/假设、原型/App、导出/发布分别定义；交接记录未决项 |
| A03 | 完善本次六份 README 的选择、结果信号与下一步 | 用户知道安装但不知道如何判断有用或是否完成 | 英中版本含等价任务边界、调用、输出、环境和失败支持 |
| A04 | 对齐本次两项技能描述和 Agent 元数据 | 自动发现或 picker 描述与实际分支不一致 | 输入与任务范围一致，默认提示指向正确技能 |
| A05 | 技能动态发现与校验 | 增加技能后 doctor 或集合检查仍只检查旧列表 | 临时加入合法技能可发现，坏条目显式失败，不静默忽略 |
| A06 | 集合完整性与元数据回归 | 文档、metadata 和独立文件漏同步 | 合法 fixture 通过；遗漏注册、缺文件、错误字段类型或不完整调用 token 有具体失败；不含双端调用策略检查 |
| A07 | 编写准则与入口软预算 | 重复说明回流到 SKILL、按字数误删验收 | 分支参考有触发条件，关键门槛保留；建议低于 500 行，必要时解释例外，无自动行数 gate |
| A08 | 保留并复核 doctor 支持链 | 缺运行时直接 traceback，或全量依赖阻塞可独立工作 | 缺运行时/包/浏览器有修复引导，必需项失败退出，不自动安装 |

未纳入本次：新增路由技能、移植完整 spec/ticket/TDD 工作流、远程工单、插件市场、自动发版和 Python 到 JavaScript 的迁移。出现具体需求和验证计划后可重新评估。

## 落地追踪

下表仅追踪此次提交的两项技能、六份 README 与集合维护工具，区分本轮实际落地和此前已有的基础。并行竞品分析及其本地测试不计入交付；运行结果以隔离提交目录的最终回执为准。

| 行动 | 本轮落实 | 范围和限制 |
| --- | --- | --- |
| A01 | 新增 [AGENTS.md](../AGENTS.md)、[SCOPE.md](../SCOPE.md)；扩充 [CONTRIBUTING.md](../CONTRIBUTING.md) | 短入口按任务指向维护材料；不引入新 router、issue tracker 或授权步骤 |
| A02 | 新增 [GLOSSARY.md](../GLOSSARY.md)、[中英文阶段交接](workflows.zh-CN.md)；两个 SKILL 增加最小交接字段 | 记录来源、产物身份、状态、未决项和下一动作；技能内部 schema 仍为权威 |
| A03 | 两份根 README 与四份技能 README 对齐任务分支、完成信号和下一步；根 README 增加实际 SKILL 入口 | 六份 README；沿用已有安装与 doctor 基础；概念任务、完整重建和已有项目修复分别说明 |
| A04 | 修订两个 SKILL；更新原型和封面的 `agents/openai.yaml` | 原型不再仅指 imagegen；封面触发限定商店素材；竞品分析改动不在此次提交内 |
| A05 | 新增 [list_skills.py](../scripts/list_skills.py) 与 `npm run list:skills`；[doctor](../scripts/doctor.py) 和 Shell 定向入口移除固定技能列表；新增 [发现回归](../tests/test_skill_discovery.py) | 列举来自当前 checkout；合法新增目录可发现；损坏目录由集合检查器明确报错 |
| A06 | 增强 [集合检查器](../scripts/check_collection.py) 与 [回归测试](../tests/test_collection.py) | 覆盖 slug、重复/异常 YAML、元数据类型、完整 token、根 README 登记、独立 README/LICENSE/doctor、本地链接和锚点；不含双端调用策略检查 |
| A07 | CONTRIBUTING 增加按需引用、变更影响面、低于 500 行的软预算和可说明例外；新增 [六场景推演](skill-routing-evaluation-2026-10-20.md) | 不是自动行数 gate；六场景为桌面推演，其中竞品分析保留为未发布的本地观察，没有让 Agent 实际执行六个完整任务 |
| A08 | 更新 [双语环境说明](runtime.zh-CN.md)，补动态发现和缺 Python 时定向检查 Node 技能的说明；让三个封面浏览器测试文件的四处启动遵守 `PLAYWRIGHT_CHANNEL` | doctor、缺运行时/包/浏览器修复链是此前已存在基础；本轮补齐 doctor、工具与测试的浏览器选择一致性，保留原断言，默认仍为 Chromium；没有统一语言或自动安装依赖 |

### 最终提交验证

2026-10-20，在仅包含本次两项技能和公共工具改动的隔离提交目录执行 `PLAYWRIGHT_CHANNEL=chrome npm run check`，退出状态为 0。环境 doctor、文档检查、158 项单元回归（集合 31、封面 44、原型 83）、13 项封面浏览器测试和原型 DOM 集成检查全部通过；两项技能的 `quick_validate.py` 与 `git diff --check` 也通过。原三技能工作区的测试及竞品报告测试未计入本次结果。

本报告的上游源码路径和行号锚点已在调查时对照固定提交核查，所有上游链接固定到同一 SHA。本次保留的浏览器选择修复仅涉及封面 [demo](../skills/app-store-cover-generator/tests/demo.browser.mjs)、[pipeline](../skills/app-store-cover-generator/tests/pipeline.browser.mjs)、[render](../skills/app-store-cover-generator/tests/render.browser.mjs) 三个文件四处启动，未删除断言。验证使用已安装的 Chrome `155.0.8059.85`；默认 Chromium 缓存缺失，安装器曾返回 `ECONNRESET`，因此本次结果不声称默认 Chromium 环境已修复。

本报告的源码调查不构成安装所有 Agent 的端到端验证，也不代表新增产品页面、真实设备验收、商店提交或内容发布。相关阶段仍遵守各技能的合同与用户授权。
