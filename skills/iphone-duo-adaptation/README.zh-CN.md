# iPhone Duo Adaptation

[English](README.md) · [Agent 指令](SKILL.md)

为现有 iOS App 做 iPhone Duo 适配，尽量保留原设计。

## 直接使用

```text
用 $iphone-duo-adaptation 分析这个 App，提出最小必要改动。
交付覆盖全部页面的交互 HTML 原型，展示 Duo 形态，并对比原设计与适配结果。
```

**提供：** App 仓库或可运行界面、当前截图／录屏，以及页面范围和设计约束。

**得到：** 整体布局分析 → 适配建议 → 完整 HTML 原型，附浏览器证据和规则记录。

支持 SwiftUI、UIKit、Flutter、React Native/Expo、WKWebView 壳。只要建议时请明确说明；原生实现和真机验证是独立任务。本技能由社区维护。

<details>
<summary>安装（已安装合集可跳过）</summary>

合集已安装时无需再安装。仅安装此技能时，先克隆仓库到发现目录之外；将下方路径设为已有源码目录。

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
# Clone here first if you have no checkout:
# git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
CODEX_SKILL_LINK="${HOME}/.agents/skills/iphone-duo-adaptation"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing entry: preserve edits and inspect before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/iphone-duo-adaptation" "$CODEX_SKILL_LINK"
fi
```

直接维护源码，不复制到 `~/.codex/skills`。迁移时保留本地修改，将重复副本移出发现目录；必要时重开 Codex，确认仅发现一个入口。其他 Agent 保留完整技能目录并加载 `SKILL.md`。

</details>

<details>
<summary>手动运行工具或排查环境时展开</summary>

## 环境与验证

布局分析和 HTML 制作无需 Xcode 或真机。规则工具需要 Python 3.9+，不需要 pip 依赖。在本技能目录运行：

```sh
sh scripts/doctor.sh
```

Agent 使用可用构建工具和浏览器制作、验证原型；缺少浏览器时验收保持待完成。如需手动管理规则，见[工作区规则](references/workspace-rules.md)，正常使用时由 Agent 处理。

</details>

[MIT](LICENSE)
