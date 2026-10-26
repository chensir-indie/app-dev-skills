# 文档导航

[English](README.md) · [合集首页](../README.zh-CN.md)

按当前任务选择文档。根 README 是技能目录，各技能的 `SKILL.md` 定义执行规则；本页只连接这些入口，不另建一份技能注册表。

## 使用合集

| 你需要…… | 阅读 |
| --- | --- |
| 按材料和目标选择技能 | [技能目录](../README.zh-CN.md#选择技能) |
| 安装、验证发现、完成首次任务或迁移旧安装 | [上手指南](getting-started.zh-CN.md) |
| 修复缺失的运行时、依赖包或浏览器 | [环境配置与故障支持](runtime.zh-CN.md) |
| 确定结束阶段或向其他技能交接 | [工作流与交接](workflows.zh-CN.md) |
| 理解证据或完成状态 | [共用术语](../GLOSSARY.md) |
| 提问或反馈可复现问题 | [问题反馈](../CONTRIBUTING.md#questions-and-bug-reports) |

具体 schema、设计规则与工具命令，从所选[技能指南](../README.zh-CN.md#选择技能)进入，再按 `SKILL.md` 查阅引用。详细合同由各独立技能维护，本页不重复列出。

## 贡献与维护

- [贡献指南](../CONTRIBUTING.md)：开发配置、包结构、变更清单与验证。
- [合集范围](../SCOPE.md)：职责、重叠边界与新增技能的条件。
- [安全政策](../SECURITY.md)与[第三方声明](../THIRD_PARTY_NOTICES.md)：报告方式和来源。

## 验证与设计历史

<details>
<summary>展开历史记录；日常使用无需逐份阅读</summary>

这些记录描述特定日期、文件、环境和任务，不是支持矩阵、实时 CI 面板，也不能证明新产品已经通过验证。部分记录引用未随仓库分发的私有本地产物或忽略的测试输出；有公开命令时可按记录复现，不可访问的证据仍应标为不可访问。历史记录保留原有语言。

| 领域 | 记录 |
| --- | --- |
| 合集文档与路由 | [2026-10-26 文档审查](documentation-review-2026-10-26.md)；[2026-10-26 英文指令](english-skills-validation-2026-10-26.md)；[2026-10-20 路由场景](skill-routing-evaluation-2026-10-20.md)；[2026-10-20 合集对照](mattpocock-skills-comparison-2026-10-20.md) |
| 竞品分析 | [2026-10-20 初始交付](app-competitor-analysis-validation-2026-10-20.md)；[2026-10-21 研究方法](app-competitor-analysis-methods-validation-2026-10-21.md)；[2026-10-22 报告设计](app-competitor-analysis-design-validation-2026-10-22.md)；[2026-10-22 设计规格](app-competitor-analysis-design-spec-validation-2026-10-22.md)；[2026-10-23 交互](app-competitor-analysis-interaction-validation-2026-10-23.md) |
| 分层原型 | [2026-10-21 设计质量](prototype-design-quality-evaluation-2026-10-21.md) |
| iOS 适配 | [初始工作流与框架修订](iphone-duo-adaptation-validation-2026-10-23.md)；[2026-10-26 构建流程](iphone-duo-adaptation-build-web-apps-validation-2026-10-26.md)；[2026-10-26 最小迁移](iphone-duo-adaptation-minimal-migration-validation-2026-10-26.md)；[2026-10-26 设备展示](iphone-duo-adaptation-device-fidelity-validation-2026-10-26.md) |
| 商店素材 | [工具验证](../skills/app-store-cover-generator/docs/validation.md)；[语言区域验证](../skills/app-store-cover-generator/docs/global-locales-validation.md)；[2026-10-12 工作流审计](../skills/app-store-cover-generator/docs/workflow-audit-2026-10-12.md) |
| 应用发布 | [2026-10-26 工具与场景检查](app-publish-skill-validation-2026-10-26.md) |

本地环境是否就绪，以对应 `doctor.sh` 为准；自动化是否通过，以实际执行的检查为准。二者都不能替代针对最终产物的审查或平台证据。

</details>
