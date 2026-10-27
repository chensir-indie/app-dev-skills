# App Competitor Analysis

[English](README.md) · [Agent 指令](SKILL.md)

分析竞品 App，把界面、交互和技术证据转成产品建议。

## 直接使用

```text
用 $app-competitor-analysis 分析这些竞品，回答我的产品问题。
每个 App 交付一份 HTML 报告，并提供对比索引，标明证据缺口。
```

**提供：** 竞品名称／链接、截图或录屏，以及你希望解决的产品问题。

**得到：** 各 App 的 HTML 报告、对比索引、四类地图和有证据的建议；详细 UI 分析另附 Design.md。打开报告时保留旁边的 assets 目录。

只需局部分析时直接说明问题；未获得的证据会明确标注。

<details>
<summary>查看产物示例</summary>

![使用虚构 Example Notes 数据的真实渲染结果。](docs/report-example.png)

2026-10-27 在 Chrome 中实际截取的 `assets/report-bundle.example.json` 渲染结果，使用虚构 Example Notes 数据。原创示例与图片采用 [MIT](LICENSE)；系统字体仅渲染到图片中，不分发字体文件。

</details>

<details>
<summary>安装（已安装合集可跳过）</summary>

合集已安装时无需再安装。仅安装此技能时，先克隆仓库到发现目录之外；将下方路径设为已有源码目录。

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
# Clone here first if you have no checkout:
# git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
CODEX_SKILL_LINK="${HOME}/.agents/skills/app-competitor-analysis"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing entry: preserve edits and inspect before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/app-competitor-analysis" "$CODEX_SKILL_LINK"
fi
```

直接维护源码，不复制到 `~/.codex/skills`。迁移时保留本地修改，将重复副本移出发现目录；必要时重开 Codex，确认仅发现一个入口。其他 Agent 保留完整技能目录并加载 `SKILL.md`。

</details>

<details>
<summary>手动运行工具或排查环境时展开</summary>

## 运行辅助工具

仅内置渲染／审计工具需要 Python 3.9+。在本技能目录运行，使用 doctor 检出的解释器；核心工具不需 pip 依赖。

```sh
sh scripts/doctor.sh
python3 scripts/render_reports.py assets/report-bundle.example.json --output /tmp/teardown-demo --format linked
```

此命令把合成示例渲染到**新目录**，随后打开其中的 index.html。真实任务按 [HTML 交付说明](references/html-delivery.md)由 Agent 先完成分析，再渲染并检查浏览器结果。

</details>

[MIT](LICENSE)
