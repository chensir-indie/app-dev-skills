# App Dev Skills

[English](README.md)

研究竞品、还原界面、适配布局、制作商店封面、交付应用。按任务选一个技能，提供材料后直接提需求。

## 选择技能

| 你想做什么 | Skill | 用法与产物 |
| --- | --- | --- |
| 分析竞品 | [app-competitor-analysis](skills/app-competitor-analysis/SKILL.md) | [报告与产品建议](skills/app-competitor-analysis/README.zh-CN.md) |
| 还原或优化界面 | [image-to-layered-html-prototype](skills/image-to-layered-html-prototype/SKILL.md) | [可编辑 HTML 与浏览器对比](skills/image-to-layered-html-prototype/README.zh-CN.md) |
| 适配 iPhone Duo | [iphone-duo-adaptation](skills/iphone-duo-adaptation/SKILL.md) | [布局分析、建议与交互原型](skills/iphone-duo-adaptation/README.zh-CN.md) |
| 制作多语言商店封面 | [app-store-cover-generator](skills/app-store-cover-generator/SKILL.md) | [可编辑封面与 PNG](skills/app-store-cover-generator/README.zh-CN.md) |
| 打包或上传应用 | [app-publish-skill](skills/app-publish-skill/SKILL.md) | [本地制品与指定阶段回执](skills/app-publish-skill/README.zh-CN.md) |

## 使用

安装后，在 Codex 中附上截图、文件或项目路径，直接输入：

```text
用 $image-to-layered-html-prototype 把这些截图还原成可编辑 HTML，
保留原设计与主要交互，提供浏览器对比。交付说明使用中文。
```

各技能用法页提供可复制示例。说明目标和结束阶段即可；Agent 会按任务读取指令、检查所需环境。

## 安装

已连接本仓库的 Codex 无需重复安装。

<details>
<summary>首次安装或迁移时展开</summary>

### 连接一个源码目录

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
# Skip cloning if you already have a checkout; set its path above.
mkdir -p "$(dirname "$APP_DEV_SKILLS_DIR")"
git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
mkdir -p "$HOME/.agents/skills"
if [ -e "$HOME/.agents/skills/app-dev-skills" ] || [ -L "$HOME/.agents/skills/app-dev-skills" ]; then
  printf '%s\n' 'Existing entry: preserve edits and inspect before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills" "$HOME/.agents/skills/app-dev-skills"
fi
```

适用于 macOS/Linux/WSL。已有源码时修改路径并跳过 clone。维护源码，通过一个软链接发现技能，不向 `~/.codex/skills` 复制。迁移前保存修改，将重复副本移出发现目录；必要时新开 Codex 会话，确认每个技能只出现一次。其他 Agent 保留所选技能完整目录并加载 `SKILL.md`。

</details>

[环境排查](docs/runtime.zh-CN.md) · [贡献](CONTRIBUTING.md) · [MIT](LICENSE)
