# Image to Layered HTML Prototype

[Simplified Chinese](README.zh-CN.md) · [Agent instructions](SKILL.md)

Turn approved UI images into editable HTML/CSS/SVG. Use this skill to rebuild a screenshot, turn an imagegen concept into an interactive prototype, repair a visual mismatch, or keep multiple pages consistent through shared tokens. Text, controls, panels and subjects remain independent layers.

## Choose your starting point

| You have | Provide | Result |
| --- | --- | --- |
| A request for directions, prompts or a reference image only | Product purpose, page/task and visual constraints | The requested concept artifact; no automatic HTML reconstruction |
| Approved screenshots | Original files, page/state names, viewport and language if known | Measured layers, runnable prototype and comparison evidence |
| A product direction and a request for a complete prototype | Product purpose, required pages and visual constraints | A reference design using available image-generation tools, followed by reconstruction |
| Existing HTML | Prototype directory and the approved reference for each page | Preserved source/assets/interactions, initial browser inventory, targeted repairs and refreshed evidence |
| Multiple references | All page images and any implementation priorities | Shared tokens, per-page status and batch acceptance |

For full reconstruction, deliverables include HTML/CSS/JS, separate assets, design tokens, geometry and typography tables, layer/asset manifests, interaction/state contracts, and real browser captures with diffs and review observations. Full screenshots remain comparison references; they do not replace editable UI.

## Review and improve design quality

Choose faithful reconstruction, active refinement or review only. Approved references stay locked during reconstruction; a review does not authorize editing. For authorized improvements, inspect the existing page, select one primary design system and work through hierarchy, layout, typography, icons/materials and relevant edge states. Keep shared tokens and compare actual before/after browser captures.

[Design quality workflow](references/design-quality-review.md) provides the review sequence and evidence format. [Sources and optional tools](references/design-sources.md) explains how Impeccable, UI/UX Pro Max, Vercel guidelines and platform standards fit without requiring installation or mixing visual systems. This complements the existing pixel checks; it does not guarantee aesthetic quality or full accessibility conformance.

> Use $image-to-layered-html-prototype to improve this existing HTML within its current design direction. First identify the largest hierarchy, layout and typography issues, then refine the shared components and show real before/after captures. Preserve any explicitly locked reference geometry.

## Install and invoke

For Codex, prefer the [collection installation](https://github.com/chensir-indie/app-dev-skills#1-connect-codex-to-one-source-checkout): one symlink exposes every skill from the source checkout. If the collection is already linked, this skill needs no additional installation. To expose only this skill, first clone the repository outside discovery directories and set its absolute path below:

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
CODEX_SKILL_LINK="${HOME}/.agents/skills/image-to-layered-html-prototype"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing skill entry: inspect it before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/image-to-layered-html-prototype" "$CODEX_SKILL_LINK"
fi
```

Compare existing `~/.agents/skills` and `~/.codex/skills` entries with the source, preserve local edits, and move superseded copies outside discovery directories before migration. Maintain and update the source checkout directly. Open a new Codex session if discovery has not refreshed, then check that this skill resolves to the source `SKILL.md` only once. Shell examples support macOS/Linux and WSL.

For other agents or a separate scope, [Skills CLI](https://github.com/vercel-labs/skills) needs Node.js 22.20+ and npm (the toolkit itself requires Node.js 22+):

```sh
npx skills@latest add chensir-indie/app-dev-skills --skill image-to-layered-html-prototype
```

Choose an agent/scope that does not duplicate the Codex link and preserve local edits before updating. Then ask your agent:

> Use $image-to-layered-html-prototype to rebuild these approved UI images as editable HTML. Extract shared tokens, verify the layers and interactions with real browser screenshots, and report each page's visual status.

For an existing page:

> Use $image-to-layered-html-prototype to compare this HTML with its reference, repair the panel contours and typography, and retain before/after evidence.

An agent can follow the design workflow without running this toolkit. Image generation comes from the agent environment and is optional when approved references already exist. Generated assets cannot recover hidden source pixels reliably.

For directions or prompts only, the workflow ends with those artifacts and needs no rendering setup. Marketing covers belong to `app-store-cover-generator`; evidence-based competitor decisions belong to `app-competitor-analysis`. Read the relevant skill when available before guiding that work; a separate skill installation is not a prerequisite for discussing the next step.

## Environment check and setup

Open the installed skill directory (the folder containing this README). Check before running helpers:

```sh
sh scripts/doctor.sh
```

If requirements are missing, follow the reported repairs, retain the draft and continue independent design work. Script-dependent checks and visual acceptance remain pending until the environment is ready and the checks run.

The checker detects Python 3.9+ using `python3` or `python`, imports Pillow/PyYAML, checks Node.js 22+ and npm, resolves Playwright and launches a real browser. It prints the detected directory and exact repairs; it never installs anything. Use `--scope python` for measurement/validators or `--scope browser` for browser capture. The checker itself needs Python in every scope; the browser scope does not need Pillow/PyYAML. Exit codes: `0` ready, `1` missing/broken runtime, `2` invalid arguments. Swift/Vision OCR is optional and macOS-only; its absence does not block core checks.

If Python is missing, install it from [Python downloads](https://www.python.org/downloads/), enable PATH where offered and reopen the terminal. Install Node.js/npm from [Node.js downloads](https://nodejs.org/en/download). For Python dependencies, from the skill directory:

```sh
python3 -m venv .venv  # use python if python3 is unavailable
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Install JavaScript dependencies using the route matching your copy:

| Copy | Command and location |
| --- | --- |
| Repository checkout | `npm ci` at the repository root; the workspaces share that install |
| Independently installed skill | `npm install` in this skill directory |

Then, from the skill directory:

```sh
npx --no-install playwright install chromium
sh scripts/doctor.sh
```

On Linux, browser launch may also require `npx --no-install playwright install --with-deps chromium`; that command installs system packages, so follow the local administrator policy. To use installed Chrome, run `PLAYWRIGHT_CHANNEL=chrome sh scripts/doctor.sh --scope browser` and use the same variable for browser helpers. Record the actual browser version in evidence.

On Windows, WSL is the recommended POSIX shell route; Git Bash may also run the launcher. Native PowerShell activation is `.venv\Scripts\Activate.ps1`; after Python is installed, it can run `python scripts/doctor.py --scope all`. These are setup routes, not a claim that the full native Windows workflow has been tested. Python examples below use `python3`; use `python` if that is the interpreter reported by doctor, and keep the same environment for validation. If package downloads fail, retain the failed check and fix the network/package-manager issue before rerunning; helpers do not change registry or proxy configuration.

## Shortest working path

For existing HTML, preserve the original source and save before-change screenshots. Add `data-artboard` to the existing target artboard root if absent; retain the element and layout rather than building a new wrapper. Then run the inventory below before adding missing measurements/contracts; inventory observes the implementation, not reference coordinates.

```sh
node scripts/inventory_page.cjs /absolute/path/to/prototype
```

1. Freeze reference images, state names and shared tokens; measure the reference independently of DOM. Read [geometry measurement](references/reference-geometry.md) and freeze the [acceptance contract](references/acceptance.md).
2. Build editable layers and visible interactions using the [layer manifest](references/layer-manifest.md).
3. When the required manifests are complete, capture the entry state and validate:

   ```sh
   node scripts/capture_native.cjs /absolute/path/to/prototype playwright home
   python3 scripts/validate_manifest.py /absolute/path/to/prototype/layer-manifest.json
   python3 scripts/validate_prototype.py /absolute/path/to/prototype
   ```

4. Inspect the reference, screenshot, overlay, raw diff and layer proofs. Repair failed regions using [visual convergence](references/visual-convergence.md), then recapture and revalidate each page.

Inventory requires `index.html`, `reference/source.png` and `[data-artboard]` on the target root; it drafts implementation observations only. Capture's state id labels evidence and does not click, navigate or open dialogs. Non-entry states require real interactions and a verified landmark before capture. The helper defaults to DPR=1 and does not apply every render-config field automatically; see [render contract](references/render-contract.md).

## Read next

| Stage | Guide |
| --- | --- |
| Generate or isolate assets | [Imagegen workflow](references/imagegen-workflow.md), [reconstruction](references/reconstruction.md) |
| Define shared styles | [Design system](references/design-system.md) |
| Measure fonts and contours | [Typography](references/typography-contract.md), [geometry](references/geometry-contract.md) |
| Build and verify evidence | [Acceptance](references/acceptance.md), [visual convergence and batches](references/visual-convergence.md) |
| Hand off to Flutter | [Flutter mapping](references/flutter-mapping.md) |

Validators detect missing layers, stale evidence, geometry and image differences. They need real browser evidence and independent reference measurements; `--structure-only` is diagnostic. Human visual review remains required for asset identity, glyphs, contours and layer order. A page stays pending while a key difference remains; a batch passes only when every requested page passes. Flutter handoff does not establish native-device acceptance.

For downstream work, reference the existing artifacts and include the next task, selected reference paths/hashes, page/state IDs, source entry point and editability/visual/interaction/responsiveness status with remaining gaps. Keep prototype captures labeled as such; a store cover using real app UI needs actual app captures.

To check toolkit changes, activate the Python environment, then run `npm test` and `npm run test:browser` from this directory. Synthetic fixtures verify checker behavior; they are not reconstructed product screenshots.

[MIT](LICENSE) · [Dependencies and asset rights](THIRD_PARTY_NOTICES.md)
