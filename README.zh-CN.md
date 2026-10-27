# App Dev Skills

[English](README.md)

研究竞品、还原界面、适配布局、制作商店封面、交付应用。按任务选一个技能，提供材料后直接提需求。

## 选择技能

| 你想做什么 | Skill | 产物 |
| --- | --- | --- |
| 分析竞品 | [app-competitor-analysis](skills/app-competitor-analysis/SKILL.md) | 报告与产品建议 |
| 还原或优化界面 | [image-to-layered-html-prototype](skills/image-to-layered-html-prototype/SKILL.md) | 可编辑 HTML 与浏览器对比 |
| 适配 iPhone Duo | [iphone-duo-adaptation](skills/iphone-duo-adaptation/SKILL.md) | 布局分析、建议与交互原型 |
| 制作多语言商店封面 | [app-store-cover-generator](skills/app-store-cover-generator/SKILL.md) | 可编辑封面与 PNG |
| 打包或上传应用 | [app-publish-skill](skills/app-publish-skill/SKILL.md) | 本地制品与指定阶段回执 |

## 产物预览

**竞品分析：HTML 报告**

![Example Notes 竞品报告，包含研究导航和四步用户旅程图](skills/app-competitor-analysis/docs/report-example.png)

基于虚构 Example Notes 数据生成的报告，图片为实际浏览器截图。

**商店封面：多语言、多设备**

![英语、中文和阿拉伯语的 iPhone 与 iPad 商店封面](skills/app-store-cover-generator/docs/demo-contact.png)

使用示例应用界面和翻译草稿，由工具实际导出。

## 使用

安装后，附上材料或项目路径，选择下面的示例提需求。说明目标和结束阶段即可；Agent 会读取指令、检查所需环境。需要中文产物时，在请求中说明。

- `用 app-competitor-analysis 技能 分析这些竞品，回答［产品问题］。输出各应用 HTML 报告与对比索引，标明证据缺口。`
- `用 image-to-layered-html-prototype 技能 把这些截图还原成可编辑 HTML，保留原设计与主要交互，提供浏览器对比。`
- `用 iphone-duo-adaptation 技能 分析［项目路径］的 iPhone Duo 适配，以最小布局改动给出建议并制作完整交互 HTML 原型。`
- `用 app-store-cover-generator 技能 根据这些截图和文案，制作［语言和设备尺寸］的可编辑商店封面与 PNG。`
- `用 app-publish-skill 技能 将［项目路径］打包上传 TestFlight，拿到 Apple 上传回执后结束。`

## 安装

选择你使用的工具。安装完整技能目录，保留其中的脚本、参考文档和资源；后续统一在源码目录更新。

先克隆一次，已有仓库直接使用原路径。以下终端命令适用于 macOS/Linux；只有 Agent 也运行在同一个 WSL 环境时才在 WSL 执行。后续命令在同一终端运行。

```sh
APP_DEV_SKILLS_DIR="$HOME/src/app-dev-skills"
# Already cloned? Set the existing path above and skip git clone.
mkdir -p "$(dirname "$APP_DEV_SKILLS_DIR")"
git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
```

<details>
<summary><b>Claude Code</b></summary>

选择一个技能，链接后可在本机所有项目中使用：

```sh
APP_DEV_SKILL="iphone-duo-adaptation" # Choose a name from the table.
APP_DEV_SKILL_LINK="$HOME/.claude/skills/$APP_DEV_SKILL"
mkdir -p "$(dirname "$APP_DEV_SKILL_LINK")"
if [ -e "$APP_DEV_SKILL_LINK" ] || [ -L "$APP_DEV_SKILL_LINK" ]; then
  printf '%s\n' 'Already exists: inspect it; existing files are preserved.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/$APP_DEV_SKILL" "$APP_DEV_SKILL_LINK"
fi
```

新开会话，输入 `/iphone-duo-adaptation` 或直接描述任务。安装其他技能时替换上方名称。[Claude Code 技能目录](https://code.claude.com/docs/en/skills#choose-where-skills-load)。

</details>

<details>
<summary><b>Codex</b></summary>

通过一个链接安装整个合集。已连接本仓库时跳过此步。

```sh
APP_DEV_SKILL_LINK="$HOME/.agents/skills/app-dev-skills"
mkdir -p "$(dirname "$APP_DEV_SKILL_LINK")"
if [ -e "$APP_DEV_SKILL_LINK" ] || [ -L "$APP_DEV_SKILL_LINK" ]; then
  printf '%s\n' 'Already exists: inspect it; existing files are preserved.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills" "$APP_DEV_SKILL_LINK"
fi
```

新开会话，通过 `$` 选择技能，例如 `$iphone-duo-adaptation`。保留一个合集链接，不再向 `~/.codex/skills` 安装单独副本。[Codex 技能发现](https://developers.openai.com/codex/skills)。

</details>

<details>
<summary><b>Cursor</b></summary>

本地 Cursor 也读取 `~/.agents/skills/`。已为 Codex 安装合集时直接复用，否则运行：

```sh
APP_DEV_SKILL_LINK="$HOME/.agents/skills/app-dev-skills"
mkdir -p "$(dirname "$APP_DEV_SKILL_LINK")"
if [ -e "$APP_DEV_SKILL_LINK" ] || [ -L "$APP_DEV_SKILL_LINK" ]; then
  printf '%s\n' 'Already exists: inspect it; existing files are preserved.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills" "$APP_DEV_SKILL_LINK"
fi
```

新开会话，输入 `/` 选择技能。已发现同名技能时，不再向 `.cursor/skills` 或 `.claude/skills` 重复安装。以上适用于本地 Agent；云端会话需要单独配置技能。[Cursor 技能目录](https://cursor.com/docs/skills)。

</details>

<details>
<summary><b>WorkBuddy</b></summary>

1. 打开 **专家·技能·连接器 → 技能 → 添加技能 → 上传技能**。
2. 选择仓库内的一个完整技能文件夹，例如 `skills/iphone-duo-adaptation`。导入技能目录，不选整个仓库或单独的 `SKILL.md`。
3. 在「已安装」中确认技能存在且已启用，然后直接说「用 iphone-duo-adaptation 技能……」。

不使用终端也可以在 GitHub 点击 **Code → Download ZIP**，解压后选择对应技能文件夹。源码更新后重新导入。[WorkBuddy 导入说明](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)。

</details>

确认每个所选技能只出现一次。安装技能不会安装渲染或移动应用构建依赖；Agent 会在任务需要时检查环境。

[环境排查](docs/runtime.zh-CN.md) · [贡献](CONTRIBUTING.md) · [MIT](LICENSE)
