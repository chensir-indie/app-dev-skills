# Runnable template contract

## Project data (schemaVersion 1)

See [project.json](../assets/starter/project.json) for a complete example.

| Field                 | Meaning                                                                               |
| --------------------- | ------------------------------------------------------------------------------------- |
| app                   | Display label; plain text                                                             |
| minTextScale          | 0.60–1 inclusive; project design minimum                                              |
| locales               | Canonical BCP 47 base IDs and matching direction ltr/rtl; optional fontFamilies array |
| devices               | Unique ID, kind phone/tablet, integer width/height (320–5000)                         |
| slides                | Ordered, unique semantic IDs                                                          |
| slides[].copy[locale] | Nonempty headline, support, uiTitle, uiBody; newline is an intentional line break     |
| slides[].art          | shared local media path, optionally overridden by locale ID                           |
| slides[].phases       | Optional 2–4 local art paths for distinct static motion phases                        |
| slides[].provenance   | Capture/illustration source and permissions note                                      |

The validator checks the executable starter contract, **not** store size eligibility. Device IDs and dimensions are configuration, not universally valid Apple slots. Confirm the current destination before using them. The demo uses portrait canvases; redesign the layout for landscape or other platforms before export.

All asset paths must be relative media paths inside the project. Remote art/fonts are rejected by the exporter. No symlinks. No credentials in the project: source-file hashes are recorded in the manifest. The local server rejects filesystem traversal, including escaped paths and symlinks outside the root. It is a local trusted-project preview, not a multi-user hosting service.

## Real captures and optional branding

The starter's synthetic UI is a demo. A cover built around an actual app screenshot can use:

```json
{
  "textFields": ["headline", "support"],
  "showBrand": false
}
```

`textFields` is an optional project-wide unique subset of headline/support/uiTitle/uiBody and must include headline. It controls translation requirements, DOM rendering, exporter copy comparison and required audit boxes. All fields remain required by default for existing projects. Extra copy keys may be retained but are not rendered or audited. Put the real capture in the locale's `art` path and adapt the image sizing/frame CSS to its aspect ratio; this configuration does not itself create a realistic device mockup. Raster UI still requires manual language/content review.

`showBrand` is an optional boolean, default true, with a per-slide override. A first-slide lockup and later feature-first pages can share the same template. When true, the brand box is required and audited; when false, the starter removes it. This changes branding only, not the declared feature headline.

## Rendering contract

The project exposes index.html with query parameters locale, device, slide and export=1. #cover is exactly the configured canvas. Set window.coverReady=true only after fonts, decoded images and fitting settle. Audited IDs come from project.textFields (default headline, support, uiTitle, uiBody), plus brand when enabled. Each must contain exactly one [data-text]. Keep declared markers when adapting the template. [data-text-box] contains one [data-text] element and reports data-text-scale plus data-overflow. The exporter enumerates the matrix from project.json; selectors alone are not proof of correct rendered copy.

To use an existing Next/React template, adapt its export route and selectors or port this small contract. Do not copy the demo's visual skin over an approved design. Native-size export uses deviceScaleFactor=1 so configured dimensions equal PNG dimensions. A reduced-motion context and disabled screenshot animations stabilize capture, but real animations must be deliberately frozen at a chosen frame.

## Environment check and setup

Run from the **skill source directory**, not a generated cover project. In a linked Codex collection, this is `skills/app-store-cover-generator` inside the source checkout, exposed through `~/.agents/skills/app-dev-skills/app-store-cover-generator`. A single-skill link or another installer may use a different discovery path. The bootstrap requires POSIX `sh` (macOS/Linux; use [WSL](https://learn.microsoft.com/windows/wsl/install) on Windows). It also works via an absolute path from any working directory:

```sh
sh scripts/doctor.sh
# Check runtime and packages without launching the browser:
sh scripts/doctor.sh --scope core
```

The doctor checks Node >=22, working npm, actual imports and required APIs of the declared packages, and (by default) a real headless browser launch with a local-page smoke check. Missing requirements return nonzero. `--scope core` skips browser readiness explicitly. No installation or configuration changes are performed. Running `doctor.mjs` directly bypasses the shell's runtime/npm checks; use `doctor.sh` as the public entrypoint.

Follow the printed repair for your installation type:

- **Missing Node/npm:** install or select Node 22+ with npm using the [Node.js installer](https://nodejs.org/en/download) or [npm setup guide](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm). Reopen the terminal/agent if its PATH has not refreshed. If package installation is unavailable, preserve the project and report the blocker; direction/prompt work can continue without rendering.
- **Independently installed skill:** run `npm install` in this skill directory. Dependencies resolve relative to the skill, not the generated cover project.
- **Collection source checkout:** run `npm ci` at the collection repository root. The doctor prints that exact path; keep the root lockfile authoritative.
- **Missing bundled browser:** after package setup, run `npx --no-install playwright install chromium` in this skill directory. This intentional command downloads the browser matching the installed Playwright package.
- **Missing Linux libraries:** review the reported library error and [Playwright OS dependency guidance](https://playwright.dev/docs/browsers#install-system-dependencies). The explicit repair is `npx --no-install playwright install-deps chromium`; it changes OS packages and may need administrator access. The doctor never executes it.

To use an existing Google Chrome instead of bundled Chromium, select the same channel for the check **and** export:

```sh
PLAYWRIGHT_CHANNEL=chrome sh scripts/doctor.sh
PLAYWRIGHT_CHANNEL=chrome node scripts/export.mjs /tmp/my-covers /tmp/my-covers-output-01
```

Chrome must already be installed. Without that environment variable (or with `PLAYWRIGHT_CHANNEL=chromium`), bundled Chromium is used. Other channel values fail with a correction. Environment success establishes local execution readiness, not cover quality or store eligibility.

## Commands

After the default doctor passes, run these commands from this skill directory:

```sh
node scripts/init.mjs /tmp/my-covers
node scripts/locales.mjs list
node scripts/locales.mjs check /tmp/my-covers
node scripts/serve.mjs /tmp/my-covers
# Open the printed loopback URL; Ctrl+C closes the preview. Edit the copied project.
node scripts/export.mjs /tmp/my-covers /tmp/my-covers-output-01
node scripts/verify.mjs /tmp/my-covers-output-01
node scripts/review.mjs init /tmp/my-covers-output-01 /tmp/my-covers-review.json
# Fill only after visual inspection, then:
node scripts/review.mjs check /tmp/my-covers-output-01 /tmp/my-covers-review.json
```

To customize, edit the copied project, not installed skill assets. Initializer/exporter refuse existing targets. The server binds to loopback and serves only the selected project. Output must be a fresh directory outside the source. Missing packages and browser-launch errors include repair commands; a browser-launch failure happens before output creation. Later rendering failures retain an incomplete report: inspect it, fix the cause and choose a new output directory. Source edits during export require a fresh export. External requests and failed local assets fail even when a browser fallback appears usable; store approved local artwork/fonts with provenance.

For development checks, read [Contributing](../CONTRIBUTING.md).

## Output

`locale/device/01-semantic-id.png`, one contact sheet per locale/device, and manifest.json. The manifest records project copy, input file hashes, per-cell text checks, PNG dimensions/SHA-256, browser metadata, contact sheet hashes, limitations and `visualReview: pending`. A changed PNG or missing/duplicate/extra matrix cell fails verification. A valid manifest is local integrity evidence, not a signature or a remote-store receipt.

The verifier checks an export against its own manifest, not a trusted external signature or the current source tree. Source changes require a fresh export. Review records bind to the entire manifest hash, so any export change invalidates an earlier review.

## Full-language demo

`npm run demo` serves a temporary project with all 50 App Store locale presets; Ctrl+C closes the server and removes the temporary files. `node scripts/init.mjs NEW_PROJECT --locales app-store` creates a persistent copy. A selected comma-separated preset list is also accepted. Without `--locales`, the initializer keeps the lightweight three-locale selection.

The optional `demo` metadata labels sample copy as draft and records intentional regional wording reuse. It is informational; it grants no translation approval. Real product expansion continues to use `locales.mjs add` and leaves missing translations empty.

[Example export](../docs/demo-contact.png) · [Asset and dependency notices](../THIRD_PARTY_NOTICES.md).
