# 设计来源与可选工具

核对日期：2026-10-21。以下是来源导航和本技能的应用方式，不是这些项目的安装包、全文副本或效果保证。具体规则执行时读对应官方章节，记录日期；无法获取时标明未核验，不编造规则或宣称已调用工具。

## 可选技能

| 来源 | 本技能采用的方法 | 调用边界 |
| --- | --- | --- |
| [Impeccable](https://github.com/pbakaus/impeccable) | 将设计判断拆为 critique、layout、typeset、polish、harden 等针对性工作，先明确产品任务再迭代 | 当前上游入口为 `/impeccable <command> <target>`；只有环境中实际提供时，先读安装版本的技能说明再调用。这里的评审流程可独立执行，不要求安装、初始化新项目文档或运行全部命令 |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 按场景检索风格、排版与技术栈规则；共享设计系统配合明确的页面变体 | 用于未定方向或缺失规范的区域。检索结果是候选，不覆盖已批准参考；沿用项目既有 tokens，不并行维护一份竞争规范 |
| [Vercel Web Design Guidelines](https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md) / [规则源](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) | HTML 交付前检查语义、焦点、内容、交互与资源，问题定位到文件/组件 | 面向 Web 实现质量，不能证明审美或像素还原；按项目语境判断具体建议，不把它当原生平台规范 |

不根据对话中的技能名假定已经安装；先看当前可用技能。缺少任一上游时，继续执行本地 [设计质量评审](design-quality-review.md)，不阻塞复刻、不自动安装、也不伪造工具结果。用户只要提示词时不运行 HTML 审计。

## 选一套主设计系统

| 官方来源 | 何时查阅 | 使用方式 |
| --- | --- | --- |
| [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/) | Apple 平台交互、布局、材质与可访问性 | 核对目标平台和控件章节；保留品牌与已选设计，明确原生约束和视觉修订的区别 |
| [Material Design 3](https://m3.material.io/get-started) | Android 或已选择 Material 的产品 | 从官方组件与样式章节提取实际采用的角色、状态与变量，不因使用 Flutter 就默认套用全部 Material 外观 |
| [Carbon 2x Grid](https://www.carbondesignsystem.com/building-blocks/foundations/2x-grid/overview) | 密集内容与业务界面的网格、对齐和节奏 | 借鉴适用的布局原则；不强制把移动消费类产品改成企业界面 |
| [Ant Design](https://ant.design/docs/spec/introduce-cn/) | 中文业务界面的组织与一致性 | 查相应设计模式与组件状态；已有主规范时仅补充具体问题，不混搭另一套皮肤 |
| [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) | Web 可访问性的可检查要求 | 按适用成功准则与级别评审；可访问性标准作为质量约束，不是视觉风格选择 |
| [Refactoring UI](https://refactoringui.com/) | 学习具体界面调整与视觉判断 | 可选学习资料，引用可访问的官方公开内容；不要求购买，不复制或推测付费章节 |

本次 HIG 页面返回 JavaScript/Markdown 导航，Material 入口返回 JavaScript 占位，未据此声称已核验其全部正文或具体尺寸。任务实际依赖某条平台要求时必须取得相应章节。其他来源也只证明查看到的内容，不代表整体审计。

Web 常用规则的直接入口：[文字对比 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)、[文字缩放 1.4.4](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)、[回流 1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)、[目标尺寸 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)。包含例外和适用条件，不能将速记数值当作所有页面无条件门槛。

以上方法由本技能结合分层重建约束重新编写；没有复制上游 skill 或付费教材，也没有增加运行时依赖。若未来引入上游代码或文本，另行核对相应版本许可证与归属要求。
