# Shared terms / 共用术语

This glossary aligns collection documentation and handoffs. Each independently installed skill retains its own executable contract and schema; these definitions do not rename JSON fields or introduce new status values.

| Term / 术语 | Meaning and evidence boundary / 含义与证据边界 |
| --- | --- |
| Skill / 技能 | Instructions plus their packaged references, scripts and assets. Installation makes the workflow available; it does not install every runtime dependency. |
| Project / 项目 | The user's working product, report or artwork directory. It is distinct from the installed skill and its demo assets. |
| Concept / 概念 | A proposed direction or prompt. Generated UI is a design artifact until implemented and captured from the actual product. |
| Reference / 参考 | An explicitly selected source used for comparison. A frozen reference has recorded identity and hash; changing it changes the acceptance basis. |
| App capture / App 实际截图 | An image captured from the named app and state, with source/version recorded when known. A render of a prototype or synthetic demo is not an actual app capture. |
| Observed / 观察到 | Supported by a direct recorded observation within its tested scope. One screen does not establish all states or runtime internals. |
| Declared / 来源声明 | Stated by an attributable source, such as official documentation. Keep its source and date; it need not have been independently exercised. |
| Static evidence / 静态证据 | Supported by an inspected artifact or source file. Presence in a package does not by itself prove active runtime use. |
| Inferred / 推断 | A reasoned interpretation of evidence. Preserve the assumptions and a way to test them; do not promote it to a product claim during handoff. |
| Unknown / 未知 | Evidence is unavailable or insufficient. Record acquisition attempts and what remains unresolved. |
| Preflight passed / 环境检查通过 | Required runtimes and capabilities were available to the selected check. It does not validate the produced artifact. |
| Rendered or exported / 已渲染或导出 | The tool produced files for a recorded source/configuration. File creation alone proves neither visual acceptance nor store upload. |
| Verified / 已验证 | A named check passed for an identified artifact, browser, viewport and state. State the check and limits; avoid an unqualified “passed.” |
| Reviewed / 已审查 | The required content or visual judgment was performed against the identified final files. Automated checks cannot invent that judgment. |
| Delivered / 已交付 | The requested branch's outputs and evidence are available, with unresolved items visible. It does not imply app implementation, distribution or public release. |

For machine-readable states and required fields, use the selected skill's contract. For human stage transitions, use [workflows](docs/workflows.md) / [工作流](docs/workflows.zh-CN.md).
