# App Publish Skill

[English](README.md) · [Agent 工作流](SKILL.md)

复用项目 Fastlane，将本地打包与商店交付拆成可独立执行的阶段。先按平台和框架选择构建适配：原生 iOS Swift/SwiftUI/UIKit/Objective-C、Flutter、具有受支持本地 native 工程的 React Native/Expo，以及原生 Android Kotlin/Java/Gradle。实时商店基线、精确源码、签名、最终制品校验、TF 回执、多语言元信息、截图封面和审核共用阶段合同；Android 交付使用本地签名包与已认证 Chrome Play Console。其他框架需先识别项目已验证的 native/export adapter，不宣称全部都已实测。

本技能负责发布编排。可编辑封面制作可接封面生成技能或项目现有工具；只想设计封面时无需执行整条发布链。

## 输入 → 流程 → 交付

![发布流程示意：源码身份、本地打包、制品检查与阶段证据](docs/workflow.svg)

*上图是证据记录示意，不含真实版本、上传结果或服务商回执。*

### 准备哪些输入

| 输入 | 需要提供什么 |
| --- | --- |
| 项目 | 可信 App 仓库、当前发布合同及已有构建/Fastlane adapter。 |
| 意图 | 平台、轨道、目标源码/功能及准确终点：构建、TestFlight 上传、资料修改或后续阶段。 |
| 环境 | 本地工具链及已批准的签名/凭证配置；只引用秘密文件路径，不把秘密值粘入报告。 |
| 实时身份 | 可按授权读取商店基线的环境；README 中的旧版本不是本次候选身份。 |

### 一次 TestFlight 上传如何完成

| 步骤 | 处理什么 | 产生什么 |
| --- | --- | --- |
| 1. 发现入口 | 读当前项目合同、包装脚本与 Fastlane lane，检查相关工具。 | adapter/工具链诊断与明确授权终点。 |
| 2. 冻结身份 | 读取新鲜商店基线，按项目策略决定候选，验证干净且已推送的源码。 | 意图、基线时间、commit、版本/build、平台和轨道。 |
| 3. 本地构建 | 通过必要预检与测试后，使用项目签名及构建 lane。 | 本地 archive/IPA 与构建证据。 |
| 4. 检查制品 | 检查最终包身份、内容、签名/配置和必要素材/数据，对实际文件计算哈希。 | 与冻结源码关联的制品检查和 SHA-256。 |
| 5. 上传记账 | 使用项目按回执结束的 Fastlane 路径，保存精确 Apple 成功回执。 | 此制品/版本/build 的 `uploaded` 状态，上传任务到此结束。 |

### 如何阅读交付记录

结果写明完成阶段、源码 commit、包/Bundle ID、版本/build、制品路径和哈希、适用的服务商回执、检查结果与未完成门禁。沿用项目记录格式；[证据合同](references/evidence-contract.md)说明随包离线工具。

仅元信息任务交付已有候选的多语言字段/文件差异、预览、准确 allowlist 与绑定评审，不人为增加二进制重建。Android 使用本地打包与已认证 Chrome Play Console 执行授权商店阶段，不套用 Apple 上传路线。

**完成标准：** 请求终点有直接证据。TestFlight 成功回执表示 `uploaded`；处理中、provider-valid、测试分发、可安装、审核及公开可用各自独立。本页配图不证明商店交付。[只读诊断](#只读诊断与离线工具)可以在不真实上传的情况下执行。


## 输入与产出

提供目标仓库、平台/轨道和本次终点。技能读取项目合同与真实 adapter，记录源码/制品身份，完成已授权阶段并说明剩余门禁，沿用已有会话中的明确授权。

```text
使用 $app-publish-skill，为这个 App 通过项目 Fastlane 构建并上传 TestFlight。
收到 Apple 成功回执后结束，记录版本/build、源码 commit 和 IPA SHA-256。
```

```text
使用 $app-publish-skill，为已有候选准备多语言元信息和完整截图封面矩阵。
交付预览、字段/文件差异与检查记录，本次先不上传商店资料。
```

TF 上传必须明确点名 TestFlight；直接请求已构成该阶段授权，预检通过后不重复确认。元信息、截图、法律/订阅字段、测试分发、提审仍各有范围，不能相互推导。Apple 公开发布默认由 owner 手动操作。

先读 [SKILL.md](SKILL.md)。首次使用、Fastlane 缺失或项目 gems 不完整时，先完成 [Fastlane 检测、安装与恢复](references/fastlane-setup.md)，再按阶段进入 [构建/TF](references/fastlane-build-testflight.md)、[元信息/截图](references/metadata-screenshots.md)、[验收/提审/Android](references/acceptance-review-android.md)。[工作区适配与历史经验](references/workspace-adapters.md) 保留历史逻辑，但不把旧版本或 lane 参数当成当前事实。

## 单一源码安装

已有 [集合源码链接](https://github.com/chensir-indie/app-dev-skills#1-connect-codex-to-one-source-checkout) 会自动发现新增技能。单独使用时，将整个技能文件夹保留在 discovery 目录外的一份源码 checkout，仅建立一个发现链接；保留既有入口和本地修改，并验证只有一个发现条目解析到该目录。不要维护第二份复制安装或额外静态注册表。

## 只读诊断与离线工具

在技能目录执行：

```sh
sh scripts/doctor.sh
sh scripts/doctor.sh --project /path/to/app --platform ios
sh scripts/doctor.sh --project /path/to/app --platform android
# monorepo 或多个 Fastlane 入口时明确选择一个项目内目录：
sh scripts/doctor.sh --project /path/to/app --platform ios --fastlane-dir /path/to/app/ios/fastlane
python3 scripts/release_evidence.py --help
python3 -m unittest discover -s tests -p 'test_*.py'
```

工具只依赖 Python 3.9+ 标准库，无 pip/npm 依赖。缺失或版本过旧时，选择 [python.org](https://www.python.org/downloads/) 的受支持 Python，重新打开终端后重试。

默认 doctor 检查包资源与 Python。`--project` 还在实际 adapter 目录执行 Ruby/Bundler 版本、`bundle check` 和项目 `bundle exec fastlane --version`；已有无 Gemfile 配置则实际检查 standalone Fastlane，并提示未锁定版本。`--platform` 选择 iOS 或 Android，多个入口用 `--fastlane-dir` 明确选择，避免猜错。只检查所选框架的相关工具，原生 iOS 或 React Native 工程不要求安装 Flutter。只对受信任项目运行此检查，因为 Bundler 会评估其 Gemfile。doctor 不认证、不安装、不构建或上传，不读取 secret，也不证明源码同步或发布资格。按 [安装指南](references/fastlane-setup.md) 保留现有 Ruby/依赖固定版本、安装缺少的依赖，或在授权范围初始化真正的新配置，之后重跑检查。实际构建仍需对应平台/框架工具链与签名；Android 交付另需已认证 Chrome 会话。

[证据合同](references/evidence-contract.md) 说明 `plan` 和 `verify-artifact`：前者只从提供的新鲜规范化基线计算离线候选提案，不读取商店或预留 build；后者只比较文件 SHA，不检查包内内容、签名或平台接收。测试仅使用临时合成 fixture，不写真实商店。

本包采用 [MIT](LICENSE)。创建或验证技能不代表已打包或上传任何 App。
