# 原型设计质量流程复核

日期：2026-10-21。范围：`image-to-layered-html-prototype` 的指令、参考和导航；不改脚本、机器 schema、依赖或像素阈值。遵循 skill-creator 的渐进披露原则，将详细评审与来源放入技能内 references，独立安装仍可使用。

## 场景桌面推演

以下是阅读修订后指令的分支推演，不是 Agent 实际完成八个设计任务，也不是实际页面视觉测试。

| 请求 | 预期行为与完成边界 | 指令依据 |
| --- | --- | --- |
| “一比一，背板不是矩形，植物压错层了” | 保留认可参考，测量轮廓/透明边界，修正图层；用原冻结门槛与实际截图验证，不换成指南推荐卡片 | SKILL 选择起点；design-quality-review 第 1、2 节；原 geometry/acceptance 合同 |
| “继续优化，还原得还是不对” | 从既有复刻上下文判断为还原修复；不因出现“优化”就解除锁定 | SKILL 工作意图区分 |
| “页面太普通，在现有品牌下提升质感” | 查看页面与规范，列关键问题，依层级/布局/字体等顺序改共享组件，留前后图；不默认添加玻璃和动效，不强迫生成新图 | design-quality-review 第 1–4 节 |
| “只评审，不改代码” | 检查真实页面，给区域/源码定位、观察、影响与建议；没有写操作，也不声称已修复 | SKILL 起点表与评审完成条件 |
| “给我两个方向和提示词，先不要 HTML” | 输出所请求的概念；没有浏览器或可选上游也能完成，不启动合同或校验器 | imagegen-workflow 入口；design-sources 工具边界 |
| “按 HIG 优化 Flutter 页面”但本次交付只是 HTML 原型 | 确认采用的主规范与平台约束；不因 Flutter 自动混入 Material 视觉；输出范围仍为原型，原生实现另行处理 | design-quality-review 主规范选择；原 flutter-mapping 交接 |
| 原图对比不足、缺少加载状态 | 原参考视觉还原与可访问性问题分别报告；无参考状态沿组件规范推导并单列，不能伪造源图对照通过 | design-system 第 3、4 节；design-quality-review 第 1、3、4 节 |
| 未安装 Impeccable / UI/UX Pro Max，或浏览器不可用 | 上游是可选辅助；继续本地设计判断。浏览器缺失保留草稿，真实截图与交互验收仍待完成，不用 imagegen 冒充 | design-sources；SKILL doctor 与证据边界 |

复核未发现需要新增审批、解除像素约束或强制安装第三方工具的分支。实际审美效果、执行中的误路由仍需后续真实任务验证，不能用此推演证明消除。

## 已执行检查

- `sh scripts/doctor.sh --scope collection`：通过，只读环境检查。
- `npm run check:docs`：通过，集合元数据、独立技能链接和文档路径有效。
- `quick_validate.py skills/image-to-layered-html-prototype`：通过。
- `python3 -m unittest discover -s tests -p 'test_skill_discovery.py'`：5 项通过。
- Codex app-server `skills/list`，`forceReload: true`：在维护者产品工作区和技能集合工作区均确认三个本地技能各出现一次、启用且解析到同一 canonical source；其中包含另一个尚未提交的技能，此观察不代表本次提交包含三个技能。

本次仅指令/文档修改，未新增镜像文字断言的测试，也未运行产品截图验收或全套浏览器回归；上述检查不证明界面审美或 WCAG 合规。上游来源与访问限制在技能的 [design-sources](../skills/image-to-layered-html-prototype/references/design-sources.md) 记录。

## 发布整理

初次编辑时，维护者 checkout 的 `.git` 指向已不存在的旧 common repository。用户授权修复与推送后，先备份工作文件及旧指针，再从 GitHub 的完整可达历史恢复独立 Git 元数据，保留工作文件不变。无法由远端恢复的本地未推送 Git 对象不在此恢复证明范围内。

本次从远端 `eca25e1` 建立隔离分支，用修改前副本提取本轮的 12 个文件差异。其他尚未提交的技能、安装说明和脚本改动保留在原工作区；涉及这些改动的上下文按远端现状适配，不纳入本次提交。仅推送本轮设计质量流程、参考文档、调用入口与此复核记录。
