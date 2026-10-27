# App Publish Skill

[English](README.md) · [Agent 指令](SKILL.md)

本地打包移动应用，完成指定的 TestFlight 或商店资料交付阶段。

## 直接使用

```text
用 $app-publish-skill 通过项目自有 Fastlane 本地构建并上传 TestFlight。
拿到 Apple 成功回执即停止，报告版本／build、源码 commit 和 IPA 哈希。
```

**提供：** App 仓库、平台／轨道和明确终点：仅打包、上传 TestFlight、更新商店资料或提审。签名凭据保留在已配置的本地环境中。

**得到：** 所需制品或商店操作结果，附精确版本／build／源码身份、哈希、回执和剩余检查。

通过项目适配器支持原生 iOS/Android、Flutter、React Native/Expo。回执代表已上传；处理、测试者可访问和公开发布分别确认。仅改商店资料时复用已有候选。

<details>
<summary>安装（已安装合集可跳过）</summary>

合集已安装时无需再安装。仅安装此技能时，先克隆仓库到发现目录之外；将下方路径设为已有源码目录。

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
# Clone here first if you have no checkout:
# git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
CODEX_SKILL_LINK="${HOME}/.agents/skills/app-publish-skill"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing entry: preserve edits and inspect before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/app-publish-skill" "$CODEX_SKILL_LINK"
fi
```

直接维护源码，不复制到 `~/.codex/skills`。迁移时保留本地修改，将重复副本移出发现目录；必要时重开 Codex，确认仅发现一个入口。其他 Agent 保留完整技能目录并加载 `SKILL.md`。

</details>

<details>
<summary>手动运行工具或排查环境时展开</summary>

## 只读环境检查

在本技能目录针对可信项目运行。辅助工具需要 Python 3.9+；App 使用自身构建和签名环境。

```sh
sh scripts/doctor.sh --project /path/to/app --platform ios
# For Android, use --platform android.
```

此命令检查项目工具，不构建或上传。缺少 Fastlane 或 gems 时按[安装与恢复](references/fastlane-setup.md)处理。具体流程见[构建／TestFlight](references/fastlane-build-testflight.md)、[商店资料](references/metadata-screenshots.md)和[提审／Android](references/acceptance-review-android.md)。

</details>

[MIT](LICENSE)
