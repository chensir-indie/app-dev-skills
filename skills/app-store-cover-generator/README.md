# App Store Cover Generator

[Simplified Chinese](README.zh-CN.md) · [Agent instructions](SKILL.md)

Turn real app screenshots and a visual reference into editable, localized App Store covers. The toolkit exports native-size PNGs across your locale/device/slide matrix, contact sheets, file hashes and review records.

## Input → workflow → output

![Cover workflow illustration from app captures and a brief to a coordinated set of editable covers](docs/workflow.svg)

*Illustrative covers with fictional UI; the actual bundled toolkit export appears below.*

### Prepare the input

| Input | What to provide |
| --- | --- |
| App content | Real captures, evidenced feature claims and approved copy; label concept-only work explicitly. |
| Art direction | Visual reference, brand palette, font/asset rights and any approved master cover. |
| Export matrix | Exact locale IDs, device slot/dimensions, slide IDs/order and intended destination. |
| Existing work | Current project, configuration and approval history when requesting fixes. |

### Follow one complete task

Example request: “Use these real captures and this reference. Create three editable slides in en-US and zh-Hans at the supplied phone and tablet dimensions. Inspect all 12 images and deliver locally.” The matrix is 2 locales × 2 targets × 3 slides; dimensions remain project inputs.

| Step | Work performed | Inspectable result |
| --- | --- | --- |
| 1. Freeze | Confirm claims, capture provenance, story order, locales and dimensions. | Brief and exact target matrix. |
| 2. Match | Render one representative cover and compare its composition, type and crop with the chosen reference. | Editable master and recorded visual differences. |
| 3. Expand | Adapt localized copy and layout deliberately, including long text and RTL where requested. | Complete configured source matrix. |
| 4. Export | Render native-size PNGs into a fresh output directory, then verify assets, geometry and file integrity. | PNGs, contact sheets, manifest/hashes and automated results. |
| 5. Inspect | Inspect every contact sheet and native PNG; fix cells, export again and bind review to final hashes. | Reviewed delivery with remaining translation/rights/eligibility limits. |

### See and use the actual output

![Actual synthetic toolkit export contact sheet with English, Chinese and Arabic phone and tablet covers](docs/demo-contact.png)

*Real toolkit export using synthetic app UI and draft translations. The sample illustrates localization and layout variants; it does not establish production translation approval or current store-slot eligibility.*

Open contact sheets to compare the matrix, then inspect full-size PNGs. Edit the source project's HTML/CSS, media and `project.json`; re-export after changes because the earlier review is bound to the old export. PNGs are delivery files, not the editable source. Use [initialize, preview, export and review commands](references/template-contract.md#commands). The starter is a scaffold: replace its synthetic UI with your app's actual captures.

**Done means:** the requested cells are exported, checked and visually reviewed, with source and bound evidence included. A contact sheet is not an upload asset; store upload is a separate endpoint. Direction-only requests end with the concept.


## Choose your starting point

| You have | Ask for | Result |
| --- | --- | --- |
| A reference or early idea | Direction and prompts | A cover concept; no rendering setup required |
| App captures and target dimensions | Build editable covers | HTML/CSS project and exported matrix |
| An existing cover project | Audit or focused fixes | Cell-specific findings and reviewed changes |

Layout, branding, slide count and languages are project inputs. Automated checks find copy, geometry, asset and integrity failures; visual fidelity and translation still require inspection. Store upload and social publishing need separate authorization.

This skill produces marketing covers. For a clickable reconstruction of an app screen, read `image-to-layered-html-prototype` when available and follow that goal instead. Directions or prompts alone stop at the requested concept and need no rendering setup.

## Install and invoke

For Codex, use the [collection installation](https://github.com/chensir-indie/app-dev-skills#1-connect-codex-to-one-source-checkout) to expose every skill from one source checkout. If that collection is already linked, this skill is ready without another installation. To expose only this skill, clone the repository outside skill discovery directories, set the variable to that clone's absolute path, then create a symlink:

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
CODEX_SKILL_LINK="${HOME}/.agents/skills/app-store-cover-generator"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing skill entry: inspect it before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/app-store-cover-generator" "$CODEX_SKILL_LINK"
fi
```

Before migration, compare existing entries in `~/.agents/skills` and `~/.codex/skills` with the source, preserve local edits, and move superseded copies outside discovery directories. Maintain and update the source checkout; Codex reads it directly. Open a new session if discovery has not refreshed, and check that the skill resolves to the source `SKILL.md` only once. Shell examples support macOS/Linux and WSL.

For other agents or a separate installation scope, [Skills CLI](https://github.com/vercel-labs/skills) requires Node.js **22.20+** and npm/npx (the toolkit itself requires Node 22+):

```sh
npx skills@latest add chensir-indie/app-dev-skills --skill app-store-cover-generator
```

Choose the intended agent/scope without duplicating the Codex link. Preserve local edits before using `npx skills@latest update app-store-cover-generator` on a CLI installation.

Minimum input: app/feature claims, real captures (or an explicitly requested concept), a reference or design direction, target locales and device dimensions, and the stage you want completed. Example:

> Use $app-store-cover-generator with these screenshots and reference. Create editable covers for zh-Hans and en-US at the supplied iPhone dimensions, export the matrix and complete the visual review. Stop at local delivery.

## Before running the toolkit

Installation adds instructions and files; rendering additionally needs **Node.js 22+, npm, Playwright and a usable browser**. The bootstrap uses POSIX `sh` (macOS/Linux; use WSL on Windows). From the installed `app-store-cover-generator` directory:

```sh
sh scripts/doctor.sh
# Runtime and packages only, without certifying browser readiness:
sh scripts/doctor.sh --scope core
```

The shell entrypoint works even when Node/npm are missing. It lists actual checks and exact repair steps, exits nonzero for missing requirements, and never installs software automatically. For an independently installed skill, follow its `npm install` instruction in this directory; a collection source checkout uses `npm ci` at its repository root. Browser setup, Linux library guidance and `PLAYWRIGHT_CHANNEL=chrome` support are in the [toolkit setup guide](references/template-contract.md#environment-check-and-setup).

Once the doctor passes, [initialize, preview and export](references/template-contract.md#commands). Deliver editable source, PNGs, contact sheets, manifest/hashes and a review bound to that export. A successful automated export still needs visual review.

Initialize from the starter only for a new project. For an existing project, retain its configuration, assets, matrix and approval history, modify the requested cells or shared source, and regenerate affected evidence. A handoff references the project/export and records the app, next stage, matrix, capture provenance, final hashes, bound review and pending cells. Concept and prototype captures keep those labels through export.

## Continue by task

- [Reference matching and art direction](references/art-direction.md)
- [Locale expansion, fonts and RTL](references/localization.md)
- [Setup, project schema and commands](references/template-contract.md)
- [Quality gates, visual review and troubleshooting](references/quality-gates.md)
- [Store handoff and publication boundaries](references/delivery.md)
- [Development and contribution](CONTRIBUTING.md)

[MIT](LICENSE). External captures, trademarks and fonts retain their own rights; see [third-party notices](THIRD_PARTY_NOTICES.md).
