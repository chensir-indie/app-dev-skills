# App Dev Skills

**Turn design references into editable interfaces and create multilingual store artwork.**

[简体中文](README.zh-CN.md) · [Choose a skill](#choose-a-skill) · [Get started](#get-started) · [Runtime help](docs/runtime.md) · [Contributing](CONTRIBUTING.md)

[![Checks](https://github.com/chensir-indie/app-dev-skills/actions/workflows/check.yml/badge.svg)](https://github.com/chensir-indie/app-dev-skills/actions/workflows/check.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-193d34)](LICENSE)

A collection of independently installable **agent skills with runnable tools**. Start from the material you have and the outcome you need; you can use one skill without running the whole sequence.

## Choose a skill

| Your starting point | Skill and guide | What you receive |
| --- | --- | --- |
| A design question, approved screenshots or an existing reconstruction | [Image to Layered HTML Prototype](skills/image-to-layered-html-prototype/README.md) · [Agent instructions](skills/image-to-layered-html-prototype/SKILL.md) | A concept/prompt, or editable HTML/CSS/SVG with assets, design standards and browser comparisons, according to the requested branch |
| Real app captures, a visual reference, target languages and dimensions | [App Store Cover Generator](skills/app-store-cover-generator/README.md) · [Agent instructions](skills/app-store-cover-generator/SKILL.md) | Editable covers, a locale × device × slide PNG matrix, contact sheets and hash/review records |

```text
Product brief → design direction or image prompts
                                 ↓ when reconstruction is requested
Approved design → editable prototype + visual evidence
                                 ↓ app implementation and device testing
Real app captures → localized covers + export review
```

A prototype does not ship an app. Exporting artwork does not upload or publish it. Each stage has its own evidence and completion criteria.

Read the selected `SKILL.md` before starting or recommending a workflow. For branch completion and passing artifacts between skills, use the [workflow guide](docs/workflows.md). In a local checkout, `python3 scripts/list_skills.py` lists the actual entrypoints without installing anything; append `--json` for automation.

## Get started

### 1. Install only the skill you need

With [Skills CLI](https://github.com/vercel-labs/skills) (Node.js 22.20+), list the remote skills and choose one:

```sh
npx skills@latest add chensir-indie/app-dev-skills --list
npx skills@latest add chensir-indie/app-dev-skills --skill image-to-layered-html-prototype
```

Replace the name with `app-store-cover-generator` for store artwork; repeat `--skill` to select both. Choose your agent when prompted. Append `-a codex -g` for global Codex installation. Remote installation uses the published revision; use a local copy for changes that have not been pushed.

<details>
<summary>Manual Codex installation, including environments without Node.js</summary>

Clone outside the agent's skills directory, then copy an individual skill:

```sh
git clone https://github.com/chensir-indie/app-dev-skills.git
mkdir -p ~/.codex/skills
# Copy only if this destination does not already exist.
test ! -e ~/.codex/skills/image-to-layered-html-prototype && \
  cp -R app-dev-skills/skills/image-to-layered-html-prototype ~/.codex/skills/
```

Use the same pattern for another skill. Keep `SKILL.md`, `scripts`, references and assets together. Preserve local edits when updating. Install each skill once per agent/scope; the collection root is not itself a skill. Start a new agent session if discovery has not refreshed.

</details>

### 2. Provide inputs and invoke the skill

Use the prompt matching your task, replacing the example scope with your own:

**Reconstruct an interface**

```text
Use $image-to-layered-html-prototype with these approved screenshots.
Build all pages as editable layers, preserving typography, panel contours and
occlusion. Show real browser captures, regional differences and remaining gaps.
```

**Produce store artwork**

```text
Use $app-store-cover-generator with these real app captures and this reference.
Create six covers in English, Chinese and Japanese at the dimensions I provide.
Match one master before expanding the matrix, then export and review.
```

### 3. Check the environment before running tools

Installing a skill adds instructions and files. Its Python/browser dependencies are separate. From the **installed skill directory**, run:

```sh
sh scripts/doctor.sh
```

The check reports missing runtimes/packages/browser support, gives repair commands, and exits unsuccessfully until required checks pass. It installs nothing. Browser tools need Node.js 22+, npm and Playwright; the layered prototype's image and structure checks also need Python 3.9+ and its documented packages. Concept-only work can proceed without the rendering environment.

Use the selected skill's README for setup, scoped checks and its first command. If you are working on this repository, follow [repository runtime setup](docs/runtime.md), then run `npm run check`.

## Example output

![Exported synthetic starter contact sheet in English, Chinese and Arabic, with phone and tablet variants](skills/app-store-cover-generator/docs/demo-contact.png)

An actual toolkit export of the bundled original demo. Its app UI is synthetic and its translations are drafts. The cover toolkit provides 50 locale presets and custom rendering targets; production copy and store eligibility still need review. See the [template contract](skills/app-store-cover-generator/references/template-contract.md).

## Continue from here

- [Runtime setup and troubleshooting](docs/runtime.md): missing Python/Node/packages/browser, standalone versus repository installation, platform support and focused checks.
- [Contributing](CONTRIBUTING.md): packaging rules, tests and safe fixtures.
- [Workflows and handoffs](docs/workflows.md): choose a branch, recognize completion and carry evidence into the next stage.
- [Scope](SCOPE.md) and [shared terms](GLOSSARY.md): maintenance boundaries; the [mattpocock/skills comparison](docs/mattpocock-skills-comparison-2026-10-20.md) records the source, decisions and implementation.
- [Prototype design standards](skills/image-to-layered-html-prototype/references/design-system.md): geometry, layers and component contracts. Missing assets/fonts can prevent exact pixel identity; keep measured gaps visible.
- [Cover localization](skills/app-store-cover-generator/references/localization.md): locale copy, fonts and RTL. Image generation is optional and uses the agent environment's tools and access conditions.

This repository continues the history of `chensir-indie/app-store-cover-generator`. Existing clones should update their remote and run the toolkit from `skills/app-store-cover-generator`. Migrate old whole-repository skill installations to individual skill directories, preserving local edits.

Code, documentation and original demo artwork use [MIT](LICENSE). User screenshots, generated artwork and third-party fonts have separate rights; see [third-party notices](THIRD_PARTY_NOTICES.md).
