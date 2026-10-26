# Flutter handoff

Use the layered HTML as the Flutter migration baseline only after its visual and interaction acceptance passes.

| HTML | Flutter |
| --- | --- |
| CSS background/material | DecoratedBox / Gradient / explicit filters |
| SVG backplate | CustomPainter or existing SVG support |
| Separate plant/photo assets | Image.asset / actual product images |
| DOM text | Text with calibrated semantic TextStyle |
| Semantic buttons/navigation | Existing shared controls, Semantics, ValueKey |
| Layout constraints | LayoutBuilder / SafeArea / Stack / Flex |

Do not package the full-screen reference as app UI. System bars belong to the device; a fake clock in a static calibration draft is not a production status bar.
Map CSS px to logical px, then calibrate fonts, safe areas, materials and image-sampling differences. Fixed canvases are for baseline verification; use constraint-based production layouts for long copy and system text sizes.
Prototype data is a test fixture. Follow the target repository's new-page integration-test and device-validation requirements; HTML screenshots are not Flutter physical-device evidence.
