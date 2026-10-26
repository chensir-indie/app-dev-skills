# 上手指南

[English](getting-started.md) · [文档导航](README.zh-CN.md) · [选择技能](../README.zh-CN.md#选择技能)

从一个具体任务和已有材料开始。Agent 需要能够读取 `SKILL.md`；执行工具时再配置对应依赖。阅读指令或规划任务不必安装全部运行环境。

## 安装与发现验证

按[首页安装步骤](../README.zh-CN.md#1-让-codex-直接读取一个源码目录)链接同一份源码；只安装单个技能时，使用对应独立 README。

其他 Agent 或独立安装范围可使用 [Skills CLI](https://github.com/vercel-labs/skills)：`npx skills@latest add chensir-indie/app-dev-skills --list` 列出技能，`--skill <name>` 选择技能（需要 Node.js 22.20+）。选择不与 Codex 合集链接重复的范围；远程安装使用已发布版本，更新前保留本地修改。

### 检查安装结果

在源码 checkout 运行 `python3 scripts/list_skills.py`，查看实际打包入口。它检查的是**源码目录，不是 Agent 的实时发现状态**。新开 Codex 会话，检查可用技能，确认所需技能都只出现一次并解析到此 checkout。发现不到技能与缺少 Python／浏览器依赖是两个不同问题。

| 现象 | 下一步 |
| --- | --- |
| 看不到合集 | 检查软链接是否指向 checkout 的 `skills/`，再在新会话刷新发现结果。 |
| 同一技能出现两次 | 对照两个发现目录中的合集与单技能安装，保留修改后把冗余副本移到发现目录外。 |
| 已有链接指向别处 | 先检查那个 checkout 及其修改；安装命令有意保留已有链接。 |
| 能发现技能，但命令失败 | 运行该技能对应范围的 doctor，按[环境排查](runtime.zh-CN.md)处理。 |

## 完成首次任务

1. 从[目录](../README.zh-CN.md#选择技能)选择技能，读取独立指南与 `SKILL.md`。
2. 提供源文件或项目目录、范围、约束、交付语言及结束阶段。产品和输出使用独立目录，避免把生成成果写入安装的技能。
3. 执行工具前，在技能目录运行 `sh scripts/doctor.sh`；适用时按指南缩小检查范围，只安装所需依赖。
4. 参考下面的示例调用技能，说明不可改动的参考或决定，保留已有可用文件。
5. 按对应工作流检查结果与证据。环境检查、产物生成、视觉审查及平台状态分别判断，明确剩余问题。

例如，界面还原应交付可编辑源码、独立素材和真实浏览器对比；只要概念时止于概念。这两类结果都不能证明原生 App 行为。

## 任务示例

用对应技能名说明材料、约束、交付语言与结束阶段；完整示例和输出合同见[独立技能指南](../README.zh-CN.md#选择技能)。

| 任务 | 请求示例 |
| --- | --- |
| 竞品研究 | `$app-competitor-analysis`：围绕我的产品问题分析这些截图，区分事实和推断，交付逐竞品报告与比较索引。 |
| 界面还原 | `$image-to-layered-html-prototype`：将已认可页面还原为可编辑图层，保留设计并提供浏览器对比。 |
| 商店封面 | `$app-store-cover-generator`：使用真实截图和参考，导出并审查指定的语言／设备／页面矩阵。 |
| iOS 适配 | `$iphone-duo-adaptation`：分析现有应用，提出最小改动并交付完整 HTML 原型和浏览器证据，原生验收单独说明。 |
| TestFlight 上传 | `$app-publish-skill`：遵循当前发布合同和项目本地 Fastlane 流程，取得精确产物的成功上传回执后停止。 |

## 更新与迁移

维护源码 checkout 即维护安装。更新前先检查并保留已有工作：

```sh
cd "$APP_DEV_SKILLS_DIR"
git status --short
git remote -v
```

checkout 干净且跟踪预期上游分支时，使用 `git pull --ff-only`。存在本地修改、分叉提交或非预期 remote 时，先明确处理，再更新；不要直接重置或覆盖。更新后重跑对应 doctor，并检查 Agent 发现结果；依赖变更还可能需要执行[环境指南](runtime.zh-CN.md)中的配置命令。

从旧 `app-store-cover-generator` 仓库迁移时，先确认 `origin` 是你准备跟踪的上游。若它仍指向旧上游，可执行：

```sh
git remote set-url origin https://github.com/chensir-indie/app-dev-skills.git
```

若使用自己的 fork，保留符合该工作流的 remote 配置。封面工具现在从 `skills/app-store-cover-generator` 或根目录 npm workspace 命令运行。旧版整仓库和单技能复制安装应迁移到一个源码链接；修改先保存在发现目录之外。已有脚本依赖的兼容路径可以保留为指向同一源码的软链接，前提是确认每个技能只被发现一次。

要从 Codex 断开合集，先检查 `~/.agents/skills/app-dev-skills`，只移除该软链接。保留源码、项目产物及仍需使用的兼容链接；解除链接不会改变账号或服务配置。
