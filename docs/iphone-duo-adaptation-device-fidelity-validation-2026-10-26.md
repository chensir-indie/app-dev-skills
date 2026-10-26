# Actual Device Hub exterior and display geometry — 2026-10-26

The user required the prototype to use the actual iPhone Duo appearance and dimensions shown in Device Hub. The [Skill](../skills/iphone-duo-adaptation/SKILL.md) now routes to a [device-presentation contract](../skills/iphone-duo-adaptation/references/device-presentation.md): identify the source exterior and screen geometry, distinguish posture from rotation, foreground the active device/application, collapse diagnostics, and review device fidelity separately from app design and functionality. Its objective remains helping adapt and optimize the existing app, through whole-app analysis → recommendations → complete HTML prototype.

## Actual source and calibration

The user-supplied Device Hub view was inspected directly. Parent-operated Closed, Partially Open and Open controls produced separate reference captures. The installed Duo device profile and stable CoreDevice display reads independently established:

| Physical posture | Active display | Native pixels | Scale | Logical display in the captured orientation |
| --- | --- | --- | --- | --- |
| Closed | Outer | 1398 × 2034 | 3 | 466 × 678 pt |
| Partially Open | Inner | 2007 × 2853 | 3 | 951 × 669 pt, landscape |
| Open | Inner | 2007 × 2853 | 3 | 951 × 669 pt, landscape |

Inner portrait is 669 × 951 pt. The three posture buttons do not establish three native display sizes. Rotation, app-window placement and preview magnification are separate controls. The source is a **simulated** iPhone Duo on iOS 27.1, not physical hardware.

The local evidence retains source profiles, per-posture display reads, actual device captures, exact vendor mask transcriptions, measured screen contours and source hashes. Screenshot pixel measurements have ±2 px uncertainty from antialiasing and JPEG compression. Captures initially saved with `.png` names actually contain JPEG bytes; runtime asset copies use `.jpg` without reencoding. Screenshot pixels, native pixels, logical points, CSS pixels and preview scale are recorded separately. No physical millimeter dimensions or native safe areas were inferred.

## Prototype and execution

The new local `workspace/index.html` composes byte-preserved Device Hub hardware images with measured SVG display apertures. The original Safari/system-screen content is removed by the aperture mask. A single editable Pocket Notes App iframe occupies the logical display; the Closed camera remains a source-derived hardware overlay. Closed preserves the asymmetric edge, hinge and camera; Partial preserves the observed bowed perimeter; Open preserves the captured full exterior. Enlarging or fitting scales the composed device without changing its logical App viewport.

The interface leads with the active device, three current-state posture cards and separate rotation/window controls. Raw dimensions, calibration, stress conditions, rules and canonical comparisons are in a collapsed inspector. The application remains the supplied **synthetic Pocket Notes fixture** with original styling and tasks. This revision verifies its device presentation; it is not a real target-product migration.

Before implementation, the author froze the current 69-rule catalog, 39 applicable populated rule decisions, 30 reasoned native/framework exclusions, eight project conventions, source references and calibrated geometry at **12:09:58 UTC**. The parent observed no prototype files before first implementation at **12:10:17 UTC**. A later generated vendor-SVG close-path correction was recorded in an input addendum; the original raw vendor files, captures and first freeze were preserved. The operative builder was the actual BUILD WEB APPS existing-reference refinement/testing contract, using installed Playwright and Chrome; no AI device concept, package installation, native app build or deployment was performed.

## Rendered checks and repaired findings

Independent comparison aligned the three actual source hardware crops with browser-rendered hardware at reference scale. Outside the display aperture, with a 3 px edge guard, mean RGB difference was **0.0** for Closed (20,540 pixels), Partial (35,184) and Open (29,051), including the Closed camera. This establishes matching of those captured exteriors, not whole-interface or physical-device pixel identity. Actual screenshots were also inspected for aperture alignment, shape, buttons, camera, app readability and layer separation.

Disposable proof checks hid each layer independently: hiding the iframe left a blank aperture and the hardware camera, with no Safari/system content; hiding hardware left editable App DOM, where creating and saving a note produced a visible new card. Source files were unchanged by these checks.

The review retained and repaired these actual findings:

- Early posture thumbnails were positioned outside their visible boxes; their scale/position was corrected.
- Fitting an inner display into a narrow mobile page made text too small. A visible **Enlarge / Fit** control now magnifies the device and App together, supports keyboard panning, and preserves viewport, session and draft. Twelve independent targeted checks and rendered before/after evidence confirmed the repair.
- Rotating a half-window context requested missing comparison images, while rotated Standing used landscape images with portrait labels. Comparison identity now uses actual viewport width, height and navigation edge. Independent coverage of all 12 named contexts, independent rotation and seven canonical states passed 170 checks without resource/script errors; the repaired 335 × 951 and 669 × 951 pairs have matching decoded dimensions. Capture reuse is explicit where geometry/design are identical.

Functional, source-app visual and continuity checks cover all existing surface families, primary tasks, initial versus cleared Search, draft/selection, dialogs, reading anchors, large text, modeled keyboard/regions, optional hierarchy, desktop/mobile and direct-file operation. These checks support their declared HTML scope and do not replace visual review.

Final runtime files were frozen at **12:32:56 UTC**. The author passed 24 grouped checks and 728 reachable comparison checks across enabled posture/rotation/window contexts, inspector states and HTTP/file opening. There are 126 canonical images across nine distinct viewport/edge profiles including the original baseline; twelve named contexts explicitly reuse matching geometry. Independent acceptance passed 249 checks with zero failures and reconciled all 27 source-freeze files plus eight reviewed runtime files. All three independent findings were retained and resolved. The target-fixture ledger completion check passed: 69 general rules and eight conventions, with 47 prototype-scoped verified items, 15 native-only deferrals and 15 framework exclusions.

The parent's final image inspection found an evidence-binding issue: the author's `review-open.png` still showed Partial while its later JSON record said Open. Both modes share the same viewport, and the capture runner had waited only for viewport/route, allowing the image to precede asynchronous shell/heading settlement. The frozen artifact remains preserved and is excluded from Open proof. Independently valid Open evidence was rechecked. Three additional parent captures now wait for the selected posture, visible heading, actual hardware-image source, live App viewport/content, source-image decode and two paint frames; all passed with source hashes unchanged. Their source-bound capture receipt and images are retained under the local bundle's `review/final-presentation/`, with an independent evidence addendum. No runtime modification was required.

## Collection checks and evidence boundary

The catalog contains **69 rules and 43 sources**, adding `WORKFLOW-DEVICE-001` without changing previous IDs. The collection workspace ledger was reconciled with all previous decisions/evidence preserved. Thirty-seven focused tests and Skill-format validation passed. Collection documentation checks passed after an unrelated in-progress skill's missing documents became available. The full collection command passed doctor/docs and 342 unit checks but remains failed on the existing competitor-image crop assertion at `tests/competitor_html.browser.cjs:69` (root browser 8/9, portrait bottom `-95.96875px`). No competitor renderer/test was changed.

The [evidence manifest](iphone-duo-adaptation/device-fidelity-evidence-2026-10-26.json) binds the current instruction files and relative local research, calibration, source, captures, findings and verification artifacts. Historical prototype revisions remain separate.

Physical body millimeters, native safe-area/bridge behavior, real IME/assistive technology, compiled target-app behavior and physical-device acceptance remain unverified. The partial-fold live HTML surface uses a planar projection inside the measured curved aperture; it does not reproduce the native nonplanar 3D content warp. No product repository, account, release, staging, commit or push was changed.
