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

## Commands

```sh
npm ci
npx playwright install chromium
node scripts/init.mjs /tmp/my-covers
node scripts/locales.mjs list
node scripts/locales.mjs check /tmp/my-covers
node scripts/serve.mjs /tmp/my-covers
node scripts/export.mjs /tmp/my-covers /tmp/my-covers-output-01
node scripts/verify.mjs /tmp/my-covers-output-01
node scripts/review.mjs init /tmp/my-covers-output-01 /tmp/my-covers-review.json
# Fill after visual inspection, then:
node scripts/review.mjs check /tmp/my-covers-output-01 /tmp/my-covers-review.json
npm run check
```

Run these commands from the skill/repository directory. To customize, edit the copied project, not the installed skill assets. Output must be a fresh directory outside the source. Preflight failures stop before rendering; an interrupted rendering run can leave an incomplete manifest and should not be reused; inspect it, fix the cause and choose a new output directory.

## Output

`locale/device/01-semantic-id.png`, one contact sheet per locale/device, and manifest.json. The manifest records project copy, input file hashes, per-cell text checks, PNG dimensions/SHA-256, browser metadata, contact sheet hashes, limitations and `visualReview: pending`. A changed PNG or missing/duplicate/extra matrix cell fails verification. A valid manifest is local integrity evidence, not a signature or a remote-store receipt.

The verifier checks an export against its own manifest, not a trusted external signature or the current source tree. Source changes require a fresh export. Review records bind to the entire manifest hash, so any export change invalidates an earlier review.
