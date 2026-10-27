# App Store Cover Generator

[English](README.md) · [Agent 指令](SKILL.md)

根据真实 App 截图和视觉参考，制作可编辑、多语言 App Store 封面。

## 直接使用

```text
用 $app-store-cover-generator 根据这些截图和参考图制作 3 张封面，
覆盖 en-US、zh-Hans，使用给定尺寸。导出并逐张检查，停在本地交付。
```

**提供：** 真实截图、功能说明／文案、视觉参考、语言、尺寸和张数；修改时附上现有项目。

**得到：** 可编辑 HTML/CSS、目标语言／设备／页面的 PNG、总览图和审查记录。

也支持只做概念或局部修复，保留现有项目。上传商店需另行指定。

<details>
<summary>查看产物示例</summary>

![使用合成界面和草稿译文的真实导出样例。](docs/demo-contact.png)

使用合成界面和草稿译文的真实导出样例。

</details>

<details>
<summary>安装（已安装合集可跳过）</summary>

合集已安装时无需再安装。仅安装此技能时，先克隆仓库到发现目录之外；将下方路径设为已有源码目录。

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
# Clone here first if you have no checkout:
# git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
CODEX_SKILL_LINK="${HOME}/.agents/skills/app-store-cover-generator"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing entry: preserve edits and inspect before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/app-store-cover-generator" "$CODEX_SKILL_LINK"
fi
```

直接维护源码，不复制到 `~/.codex/skills`。迁移时保留本地修改，将重复副本移出发现目录；必要时重开 Codex，确认仅发现一个入口。其他 Agent 保留完整技能目录并加载 `SKILL.md`。

</details>

<details>
<summary>手动运行工具或排查环境时展开</summary>

## 执行脚本前检查环境

渲染需要 Node.js 22+、npm、Playwright 和可用浏览器。在本技能目录运行：

```sh
sh scripts/doctor.sh
```

doctor 给出修复方式，不自动安装。独立技能使用 `npm install`，合集源码在根目录使用 `npm ci`。详见[环境配置](references/template-contract.md#environment-check-and-setup)与[初始化／预览／导出命令](references/template-contract.md#commands)。仅新项目套用模板，导出后实际查看图片再记录审查。

</details>

[MIT](LICENSE) · [素材与依赖声明](THIRD_PARTY_NOTICES.md)
