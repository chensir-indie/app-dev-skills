# App Store Cover Generator

[简体中文](README.zh-CN.md) · [Skill instructions](SKILL.md)

An open-source agent skill for creating editable, localized App Store screenshot covers from visual references and app screenshots.

The skill guides reference analysis, HTML/CSS implementation, localization, export and review. It works with the target app’s assets and visual direction; layout, branding, slide count, languages and device sizes are configurable.

## Capabilities

- **Reference-guided design:** translate typography, composition, spacing and visual layers into an editable cover project.
- **Reusable templates:** separate content and assets from HTML/CSS layout, with a consistent slide order across outputs.
- **Localization:** use App Store locale presets or custom BCP 47 tags, script-aware font stacks and right-to-left layouts.
- **Batch export:** render native-size PNGs across configured languages, devices and slides, with contact sheets and a hash manifest.
- **Validation:** check missing copy, text overflow, element collisions, asset loading and export integrity; retain separate visual review records.

Deliverables include the editable project, exported images and review artifacts. Automated checks support human review of visual fidelity and translation quality. Image generation is optional and uses tools available to the agent; store upload is outside this skill’s scope.

## Install

Run the [Skills CLI](https://github.com/vercel-labs/skills) from your project directory:

```sh
npx skills@latest add chensir-indie/app-dev-skills --skill app-store-cover-generator
```

Choose your agent when prompted. Installation is project-local by default. For global Codex installation:

```sh
npx skills@latest add chensir-indie/app-dev-skills --skill app-store-cover-generator -a codex -g
```

Update a Skills CLI installation with:

```sh
npx skills@latest update app-store-cover-generator
```

<details>
<summary>Manual Codex installation</summary>

Clone into a new directory:

```sh
git clone https://github.com/chensir-indie/app-dev-skills.git
# Ensure the destination does not already exist before copying.
mkdir -p ~/.codex/skills
test ! -e ~/.codex/skills/app-store-cover-generator && \
  cp -R app-dev-skills/skills/app-store-cover-generator ~/.codex/skills/
```

Update the source clone, review local edits, then refresh the individual skill directory intentionally. Use one installation method per agent and scope.

</details>

Installation adds skill instructions and supporting files. Running the bundled rendering toolkit additionally requires Node.js 22+, npm and Playwright Chromium; setup commands are in the [toolkit guide](references/template-contract.md#commands). Open a new agent session if the installed skill is not yet available.

## Use

Provide app screenshots, a visual reference, target languages and device dimensions, then ask your agent:

> Use $app-store-cover-generator to create App Store covers from these assets. Keep the design editable and export the configured language and device variants.

For an existing project:

> Use $app-store-cover-generator to review this cover project and fix layout or localization issues while preserving its approved design.

The agent uses [SKILL.md](SKILL.md) for the workflow and loads supporting references as needed.

## Documentation

- [Art direction and reference analysis](references/art-direction.md)
- [Localization and typography](references/localization.md)
- [Project format, preview and export commands](references/template-contract.md)
- [Quality checks and review](references/quality-gates.md)
- [Delivery scope](references/delivery.md)
- [Contributing and development](CONTRIBUTING.md)

## License

[MIT](LICENSE). External app screenshots, trademarks and third-party fonts retain their own rights; see [third-party notices](THIRD_PARTY_NOTICES.md).
