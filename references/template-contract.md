# Runnable template contract

## Project data (schemaVersion 1)

See [project.json](../assets/starter/project.json) for a complete example.

| Field                 | Meaning                                                                           |
| --------------------- | --------------------------------------------------------------------------------- |
| app                   | Display label; plain text                                                         |
| minTextScale          | 0.60–1 inclusive; project design minimum                                          |
| locales               | Unique IDs and direction ltr/rtl                                                  |
| devices               | Unique ID, kind phone/tablet, integer width/height (320–5000)                     |
| slides                | Ordered, unique semantic IDs                                                      |
| slides[].copy[locale] | Nonempty headline, support, uiTitle, uiBody; newline is an intentional line break |
| slides[].art          | shared local media path, optionally overridden by locale ID                       |
| slides[].phases       | Optional 2–4 local art paths for distinct static motion phases                    |
| slides[].provenance   | Capture/illustration source and permissions note                                  |

The validator checks the executable starter contract, **not** store size eligibility. Device IDs and dimensions are configuration, not universally valid Apple slots. Confirm the current destination before using them. The demo uses portrait canvases; redesign the layout for landscape or other platforms before export.

All asset paths must be relative media paths inside the project. Remote art/fonts are rejected by the exporter. No symlinks. No credentials in the project: source-file hashes are recorded in the manifest. The local server rejects filesystem traversal, including escaped paths and symlinks outside the root. It is a local trusted-project preview, not a multi-user hosting service.

## Rendering contract

The project exposes index.html with query parameters locale, device, slide and export=1. #cover is exactly the configured canvas. Set window.coverReady=true only after fonts, decoded images and fitting settle. [data-text-box] contains one [data-text] element and reports data-text-scale plus data-overflow. The exporter enumerates the matrix from project.json; selectors alone are not proof of correct rendered copy.

To use an existing Next/React template, adapt its export route and selectors or port this small contract. Do not copy the demo's visual skin over an approved design. Native-size export uses deviceScaleFactor=1 so configured dimensions equal PNG dimensions. A reduced-motion context and disabled screenshot animations stabilize capture, but real animations must be deliberately frozen at a chosen frame.

## Commands

```sh
npm ci
npx playwright install chromium
node scripts/init.mjs /tmp/my-covers
node scripts/serve.mjs /tmp/my-covers
node scripts/export.mjs /tmp/my-covers /tmp/my-covers-output-01
node scripts/verify.mjs /tmp/my-covers-output-01
npm test
npm run test:browser
```

Run these commands from the skill/repository directory. To customize, edit the copied project, not the installed skill assets. Output must be a fresh directory outside the source. An interrupted export leaves an incomplete manifest and should not be reused; inspect it, fix the cause and choose a new output directory.

## Output

`locale/device/01-semantic-id.png`, one contact sheet per locale/device, and manifest.json. The manifest records project copy, input file hashes, per-cell text checks, PNG dimensions/SHA-256, browser metadata, contact sheet hashes, limitations and `visualReview: pending`. A changed PNG or missing/duplicate/extra matrix cell fails verification. A valid manifest is local integrity evidence, not a signature or a remote-store receipt.
