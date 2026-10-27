# 环境配置与故障支持

[English](runtime.md) · [合集说明](../README.zh-CN.md)

技能指令与脚本依赖分别安装。阅读参考、竞品研究和概念设计不需要提前装齐全部渲染工具；准备执行哪个任务，就检查对应环境。

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

独立安装的技能，在该技能目录运行 `sh scripts/doctor.sh`；更小的检查范围见该技能 `SKILL.md` 链接的环境说明。shell 入口会先判断运行时是否存在，避免连 Python/Node 都没有时直接执行失败。`npm run doctor` 仅在 Node/npm 已可运行时作为快捷入口。

目录命令与完整 doctor 从当前 checkout 的 `skills/*/SKILL.md` 发现技能。`--skill` 定向检查直接进入对应技能的 shell 入口，因此只需要 Node 的技能不必先安装合集 Python。集合校验另行检查不完整的技能目录及缺失的文档入口。

### 各技能环境

| 任务 | 所需环境与配置说明 |
| --- | --- |
| 竞品报告辅助工具 | Python 3.9+ 标准库；[渲染器配置](../skills/app-competitor-analysis/references/html-delivery.md#reusable-renderer) |
| 可编辑 HTML 截图 | Python、Node 和浏览器；[截图环境](../skills/image-to-layered-html-prototype/references/render-contract.md#environment-check-and-setup) |
| 商店封面导出 | Node 和浏览器；[导出环境](../skills/app-store-cover-generator/references/template-contract.md#environment-check-and-setup) |
| iPhone Duo 工作区规则 | Python 3.9+ 标准库；[规则工具](../skills/iphone-duo-adaptation/references/workspace-rules.md)。布局与 HTML 工作不需要 Xcode；浏览器验收需要浏览器。 |
| 应用发布 | 离线辅助工具需要 Python 3.9+；构建／上传使用[项目工具链](../skills/app-publish-skill/references/fastlane-setup.md)。在技能目录运行 doctor 时追加 `--project /path/to/app --platform ios` 或 `android`。 |

doctor 不安装、认证、构建或上传；浏览器检查会启动空白无头浏览器。按提示修复并重跑同一命令；通过只说明环境可运行，不代表产物质量或任务验收通过。

## 配置完整仓库

使用 macOS、Linux 或 Windows WSL 中的 POSIX shell。完整检查需要 **Node.js 22+、npm、以 `python3` 命令可用的 Python 3.9+、Pillow、PyYAML 和 Playwright Chromium**；单个技能可能只需要其中一部分。可选 Swift/Vision OCR 仅支持 macOS，不阻塞跨平台核心流程。移动打包另有目标项目的平台要求。

在仓库根目录执行：

```sh
npm ci
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r skills/image-to-layered-html-prototype/requirements.txt
npx playwright install chromium
npm run check
```

仓库 checkout 使用带锁文件的 `npm ci`；只安装单个 skill 时，使用其 `SKILL.md` 链接的环境说明。Python 包必须安装到当前检查所用的解释器中；装到另一个 Python 环境不会解决当前问题。每次开启新终端都要重新激活对应虚拟环境。

## 按缺项修复

| 检查失败 | 处理方式 |
| --- | --- |
| Python 缺失或版本过低 | 从 [python.org](https://www.python.org/downloads/) 安装受支持版本，重开终端，再创建/激活 `.venv`。完整 npm 测试使用 `python3`。 |
| 缺 `venv` 或 `ensurepip` | 安装系统发行版对应的 Python venv/pip 包，例如 Debian/Ubuntu 的 `python3-venv`，再创建虚拟环境。 |
| Node/npm 缺失或 Node 低于 22 | 按 [Node.js 官方安装选项](https://nodejs.org/en/download)配置 Node.js 22+ 与 npm，重开终端。没有 Node 时也可以先手动安装并阅读技能。 |
| Pillow/PyYAML 无法导入 | 激活 `.venv`，执行 `python -m pip install -r skills/image-to-layered-html-prototype/requirements.txt`，避免往系统 Python 全局安装。 |
| 缺 Playwright/pngjs | 在仓库根目录运行 `npm ci`；独立安装的技能若含 `package.json`，在其目录执行 `npm install`。 |
| 找不到 Chromium 可执行文件 | npm 依赖安装完成后，在对应包/仓库目录运行 `npx playwright install chromium`。 |
| Linux 缺浏览器系统库 | 在有权限的环境运行 `npx playwright install --with-deps chromium`，可能需要系统管理员权限；无法安装时换到受支持主机采集，浏览器验证保持待完成。 |
| 希望使用现有 Chrome | 对 doctor 和截图/导出命令同时设置 `PLAYWRIGHT_CHANNEL=chrome`，例如 `PLAYWRIGHT_CHANNEL=chrome sh scripts/doctor.sh`。主机须已安装 Chrome，证据中记录实际版本。 |
| 下载失败或环境受管理 | 保留诊断输出，检查网络和包源策略，请环境维护者提供明确缺少的运行时/依赖；不要反复重跑失败流程或修改安全设置。 |

原生 PowerShell 无法执行 POSIX bootstrap。本文 shell/npm 流程在 Windows 上使用 WSL；自行适配的原生 Windows 流程可直接运行 `.py`/`.mjs` 工具，但不属于当前合集 shell 测试覆盖路径。

## 缺少能力时如何继续

继续不依赖失败工具的研究、源码检查或概念工作。依赖它的截图、渲染或校验步骤保持待完成，并说明具体缺少的能力。其他浏览器/检查工具只有能提供同等证据时才可替代；缺运行环境不能用虚构截图或未经验证的通过状态补齐。

请求支持时附上命令、运行目录、系统、实际解释器/版本、doctor 输出与失败范围。公开分享前移除私有路径和敏感项目内容，勿附 token、cookie、签名文件或账号凭据。

## 定向验证

```sh
npm run check:docs
python3 -m unittest discover -s tests -p 'test_*.py'
npm test -w image-to-layered-html-prototype
npm test -w app-store-cover-generator
npm run test:browser
npm run demo
```

迭代时运行相关范围即可；合集/工具改动交付前运行 `npm run check`。demo 使用合成 UI；CI 只验证本仓库，不打包或上传移动应用。
