# App Store 封面生成 Skill

[English](README.md) · [Skill 入口](SKILL.md)

把 **AI 视觉素材、可编辑网页排版、多语言批量导出** 组合成可复用的工作流。

做这个 skill 的目标，是解决“概念图好看，但落到网页后字体、比例和细节对不上”的问题。AI 负责难以用代码表现的材质与画面，网页负责准确的文字、语言和设备几何，审计负责找到裁切、溢出与缺图；视觉复核再判断最终效果。

![原创示例预览](docs/demo-contact.png)

这是原创矢量素材与虚构 UI 的可运行示例，不是实际 App 截图，也不是所有产品必须采用的风格。[NextNote 原始案例与效果展示](https://x.com/NextNote_App/status/2100984993619366199)。

## 这次完善了什么

- 参考图分层、等比例对比、材质和光影提示词。
- 字号一致性、字体回退、长文案、CJK、RTL、多设备排版。
- 动态封面不同相位、动态表情不同姿态的细节方法。
- 3 种语言 × 手机/平板 × 2 页的独立 HTML/CSS/JS 模板。
- 本地预览、批量导出、完整矩阵检查、图片哈希与接触表。
- 有故障注入的单元和浏览器测试。
- 明确自动检查的局限，不把“脚本通过”描述成视觉一致或商店已审核。

不再把 NextNote 的九页故事、私人路径和历史送审数据当成通用规则。AskMATT 是可选集成，只有环境真正提供并且能力适用时才调用。

## 安装

```sh
git clone https://github.com/chensir-indie/app-store-cover-generator.git ~/.codex/skills/app-store-cover-generator
```

已有同名目录时，先备份或合并自己的修改。不要直接覆盖。必要时新开一个 Codex 任务，让 skill 被发现。

示例请求：

> 使用 $app-store-cover-generator，根据我提供的参考图和真实 App 截图制作封面。先匹配一张主视觉，再扩展到指定语言和 iPhone/iPad 尺寸。标题保持可编辑，动态封面和动态表情需要复刻细节，导出后检查所有文字，停在本地交付阶段。

## 运行模板

需要 Node.js 22+、npm、Chromium。Linux 可使用 `npx playwright install --with-deps chromium` 安装系统依赖。

```sh
npm ci
npx playwright install chromium
node scripts/init.mjs /tmp/my-covers
node scripts/serve.mjs /tmp/my-covers
# 打开命令打印的地址，编辑项目中的 project.json 与 style.css。
node scripts/export.mjs /tmp/my-covers /tmp/my-covers-output-01
node scripts/verify.mjs /tmp/my-covers-output-01
npm test
npm run test:browser
```

每次导出使用新的输出目录。生成独立 PNG、各语言设备接触表、manifest.json。自动通过后仍然标记 `visualReview: pending`，需要人工或具备视觉能力的 agent 逐格检查。

生产用途请换成真实截图和有授权的本地字体。示例使用系统字体，因此不承诺跨系统像素完全一致。尺寸以当前 App Store Connect 的目标展示槽位为准。

## 文档

- [参考拆解与提示词](references/art-direction.md)
- [字体、本地化与动态细节](references/localization.md)
- [数据格式、模板接口和命令](references/template-contract.md)
- [质量检查覆盖范围与故障排查](references/quality-gates.md)
- [商店交付与公开案例](references/delivery.md)
- [NextNote 经验](references/nextnote-case-study.md)

本仓库代码、文档和原创示例 SVG 采用 MIT。NextNote 品牌、外部图片和第三方素材不随仓库重新授权。查看 [LICENSE](LICENSE) 与 [第三方说明](THIRD_PARTY_NOTICES.md)。
