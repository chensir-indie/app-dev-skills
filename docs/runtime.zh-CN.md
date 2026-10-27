# 环境配置与故障支持

[English](runtime.md) · [合集说明](../README.zh-CN.md)

安装技能后就能读取它的指令，运行脚本可能还需要安装其他工具。阅读参考资料、规划竞品分析或做概念设计时，不必先装齐渲染工具。准备执行哪个任务，就检查它需要的环境。

## 选择检查范围

在仓库根目录运行：

```sh
python3 scripts/list_skills.py                            # 实际技能入口；可追加 --json
sh scripts/doctor.sh                                      # 合集和全部技能环境
sh scripts/doctor.sh --scope collection                   # 合集元数据与检查前置条件
sh scripts/doctor.sh --skill app-competitor-analysis      # Python 标准库工具
sh scripts/doctor.sh --skill app-publish-skill            # Python 3.9+ 离线发布辅助工具
sh scripts/doctor.sh --skill iphone-duo-adaptation        # Python 标准库工作区规则工具
sh scripts/doctor.sh --skill image-to-layered-html-prototype
sh scripts/doctor.sh --skill app-store-cover-generator
```

如果只安装了一个技能，在该技能目录中运行 `sh scripts/doctor.sh`。更具体的检查选项见它的 `SKILL.md` 和所链接的环境说明。shell 脚本会先检查 Python 或 Node 是否可用，再尝试运行。已经装好 Node/npm 时，也可以用 `npm run doctor`。

技能列表命令和完整 doctor 会读取当前仓库中的 `skills/*/SKILL.md` 来查找技能。指定 `--skill` 后，doctor 直接运行该技能的 shell 脚本。因此，检查只依赖 Node 的技能时，无需先为整个合集安装 Python。合集校验还会检查技能目录是否完整、文档入口是否缺失。

### 各技能环境

| 任务 | 所需环境与配置说明 |
| --- | --- |
| 竞品报告辅助工具 | Python 3.9+ 标准库；[渲染器配置](../skills/app-competitor-analysis/references/html-delivery.md#reusable-renderer) |
| 可编辑 HTML 截图 | Python、Node 和浏览器；[截图环境](../skills/image-to-layered-html-prototype/references/render-contract.md#environment-check-and-setup) |
| 商店封面导出 | Node 和浏览器；[导出环境](../skills/app-store-cover-generator/references/template-contract.md#environment-check-and-setup) |
| iPhone Duo 工作区规则 | Python 3.9+ 标准库；[规则工具](../skills/iphone-duo-adaptation/references/workspace-rules.md)。布局与 HTML 工作不需要 Xcode；浏览器验收需要浏览器。 |
| 应用发布 | 离线辅助工具需要 Python 3.9+；构建／上传使用[项目工具链](../skills/app-publish-skill/references/fastlane-setup.md)。在技能目录运行 doctor 时追加 `--project /path/to/app --platform ios` 或 `android`。 |

doctor 只检查环境，不会安装工具、登录账号、构建或上传。检查浏览器时，它会启动一个空白无头浏览器。按提示修复后，重新运行同一命令。检查通过表示所需工具已就绪，产物质量和任务验收还需要分别验证。

## 配置完整仓库

在 macOS 或 Linux 中使用 POSIX shell，在 Windows 中使用 WSL。运行合集的全部检查需要 Node.js 22+、npm、可通过 `python3` 调用的 Python 3.9+、Pillow、PyYAML 和 Playwright Chromium。单个技能可能只需要其中一部分。可选的 Swift/Vision OCR 仅支持 macOS，跨平台流程可以在没有它的情况下运行。移动应用打包还需要目标项目所用平台的工具。

在仓库根目录执行：

```sh
npm ci
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r skills/image-to-layered-html-prototype/requirements.txt
npx playwright install chromium
npm run check
```

在仓库中使用 `npm ci`，按锁文件安装依赖。如果只安装一个技能，请按它的 `SKILL.md` 所链接的环境说明操作。Python 包要装到运行检查的那个环境中，每次新开终端也要激活同一个虚拟环境。装到其他环境里，无法解决这里的导入错误。

## 按缺项修复

| 检查失败 | 处理方式 |
| --- | --- |
| Python 缺失或版本过低 | 从 [python.org](https://www.python.org/downloads/) 安装受支持版本，重开终端，再创建/激活 `.venv`。完整 npm 测试使用 `python3`。 |
| 缺 `venv` 或 `ensurepip` | 安装系统发行版对应的 Python venv/pip 包，例如 Debian/Ubuntu 的 `python3-venv`，再创建虚拟环境。 |
| Node/npm 缺失或 Node 低于 22 | 按 [Node.js 官方说明](https://nodejs.org/en/download)安装 Node.js 22+ 与 npm，然后重开终端。没有 Node 时，也可以先手动安装和使用技能指令。 |
| Pillow/PyYAML 无法导入 | 激活 `.venv`，执行 `python -m pip install -r skills/image-to-layered-html-prototype/requirements.txt`，避免往系统 Python 全局安装。 |
| 缺 Playwright/pngjs | 在仓库根目录运行 `npm ci`；独立安装的技能若含 `package.json`，在其目录执行 `npm install`。 |
| 找不到 Chromium 可执行文件 | npm 依赖安装完成后，在对应包/仓库目录运行 `npx playwright install chromium`。 |
| Linux 缺浏览器系统库 | 在有权限的环境运行 `npx playwright install --with-deps chromium`，这可能需要系统管理员权限。如果无法安装，换到受支持的主机采集，并将浏览器验证标为待完成。 |
| 希望使用现有 Chrome | 对 doctor 和截图、导出命令都设置 `PLAYWRIGHT_CHANNEL=chrome`，例如 `PLAYWRIGHT_CHANNEL=chrome sh scripts/doctor.sh`。主机上须已安装 Chrome，并在证据中记录实际版本。 |
| 下载失败或环境受管理 | 保留诊断输出，检查网络和软件包源的使用限制，再请环境维护者提供缺少的运行环境或依赖。不要反复运行同一失败流程，也不要修改安全设置。 |

在 Windows 上，请用 WSL 执行本文的 shell/npm 检查，原生 PowerShell 无法运行 POSIX 启动脚本。你也可以自行适配 Windows 流程，直接运行 `.py`/`.mjs` 工具，但合集的 shell 测试不覆盖这种配置。

## 缺少能力时如何继续

可以继续做不依赖该工具的研究、源码检查或概念设计。说明缺少什么工具，并将依赖它的截图、渲染或校验步骤标为待完成。如果其他浏览器或检查工具能提供所需证据，可以替代使用。不要用虚构截图填补缺口，也不要把未经验证的结果写成通过。

寻求帮助时，请附上运行命令、工作目录、操作系统、实际使用的解释器及版本、doctor 输出，以及哪项检查失败。公开分享前，移除私有路径和敏感项目内容，不要附上 token、cookie、签名文件或账号凭据。

## 定向验证

```sh
npm run check:docs
python3 -m unittest discover -s tests -p 'test_*.py'
npm test -w image-to-layered-html-prototype
npm test -w app-store-cover-generator
npm run test:browser
npm run demo
```

修改过程中，先运行与当前改动相关的检查。交付合集或工具改动前，再运行 `npm run check`。demo 使用模拟界面；CI 只检查本仓库，不会打包或上传移动应用。
