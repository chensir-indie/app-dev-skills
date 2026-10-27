# Image to Layered HTML Prototype

[English](README.md) · [Agent 指令](SKILL.md)

把认可的 App 截图还原为可编辑、可交互的 HTML，也可评审或修复已有页面。

## 直接使用

```text
用 $image-to-layered-html-prototype 把这些页面还原成可编辑 HTML。
保留原设计，接通主要交互，提供真实浏览器对比。
```

**提供：** 各页面原图、已有素材／字体、需要的交互；修复时附上现有 HTML。

**得到：** 可编辑 HTML/CSS/SVG、独立素材、可用交互和逐页对比证据。

也可明确只要概念、提示词或评审。忠实还原时保留认可参考；整屏图片加点击热点不算可编辑结果。

<details>
<summary>安装（已安装合集可跳过）</summary>

合集已安装时无需再安装。仅安装此技能时，先克隆仓库到发现目录之外；将下方路径设为已有源码目录。

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
# Clone here first if you have no checkout:
# git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
CODEX_SKILL_LINK="${HOME}/.agents/skills/image-to-layered-html-prototype"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing entry: preserve edits and inspect before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/image-to-layered-html-prototype" "$CODEX_SKILL_LINK"
fi
```

直接维护源码，不复制到 `~/.codex/skills`。迁移时保留本地修改，将重复副本移出发现目录；必要时重开 Codex，确认仅发现一个入口。其他 Agent 保留完整技能目录并加载 `SKILL.md`。

</details>

<details>
<summary>手动运行工具或排查环境时展开</summary>

## 环境检查与安装

在本技能目录运行。截图需要 Python 3.9+、Node.js 22+、npm、Playwright 和浏览器；测量／校验另需 Pillow、PyYAML。仅做概念无需渲染环境。

```sh
sh scripts/doctor.sh
# For a standalone installation when dependencies are missing:
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
npm install
npx --no-install playwright install chromium
sh scripts/doctor.sh
```

合集源码在仓库根目录使用 `npm ci`，替代独立安装的 `npm install`。可选 `--scope python` 或 `--scope browser`，两者都需要 Python。已有 Chrome 可在 doctor 和截图命令前设置 `PLAYWRIGHT_CHANNEL=chrome`。使用 macOS/Linux 或 WSL，按 doctor 输出修复运行时或浏览器库；依赖检查未完成时验收仍待完成。

</details>

[MIT](LICENSE) · [素材与依赖声明](THIRD_PARTY_NOTICES.md)
