# Rendering coordinates and reproducibility

Default reconstruction checks use 1 reference pixel = 1 CSS px, DPR=1, screenshot scale=css.
For a 591×1280 reference, set viewport=591×1280 and produce a 591×1280 capture.
A 393×852 logical viewport at DPR=3 yields a 1179×2556 device capture. Declare the mapping and match the reference; do not multiply reference width by DPR again.

render-config.json records actual browser.version(), viewport, deviceScaleFactor, screenshotScale, locale, colorScheme, scroll, font sources/SHA, animation state, timezone and fixture data.
When pages share CSS/JS/images, each page's render-config.json may declare `"sharedRuntimeDirs":["../shared"]`. The validator permits only explicitly listed sibling shared directories. Record every runtime image/SVG in that page's asset-manifest.json using relative paths such as `../shared/assets/plant.png` and its SHA. Shared CSS/JS/fonts and registered assets are covered by capture receipts and final hashes. Do not disguise another page, reference or evidence directory as shared runtime resources.
A package version is not the browser version. Do not attribute an arbitrary measured one-level color difference to JPEG decoding without an experiment.

Before capturing, await document.fonts.ready, all img.decode() calls and the application ready marker. Freeze transitions, animations and caret; use a fixed date and local fixture.
An imagegen reference may have no source browser. Compare against frozen pixels without inventing its runtime environment.

A desktop preview may uniformly scale the whole artboard, but update its wrapper dimensions too, preventing transform-induced blank space and horizontal scrolling.
Record compact / baseline / wide and long-copy adaptation tests separately. Uniformly shrinking the canvas is not responsive acceptance.
