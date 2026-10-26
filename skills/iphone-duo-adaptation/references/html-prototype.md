# Complete HTML adaptation prototype contract

Read for the default final deliverable. The HTML is an operable app prototype: adaptation decisions must appear in its pages and interactions. The current app's coverage matrix defines scope, and the [workspace ledger](workspace-rules.md) connects the complete catalog to project decisions, components, and verification under shared rule IDs. The prototype does not run SwiftUI, UIKit, Flutter, React Native, or a WebView shell, so it cannot establish those frameworks' receipt of iOS window, safe-area, or folding data.

Preserve **whole-app layout analysis → adaptation recommendations → complete HTML prototype**, with browser and visual review before final acceptance. Read the [BUILD WEB APPS handoff](build-web-apps.md) at this stage and prefer that construction workflow when its actual Skill is available. Discover and read its real instructions, record its identity, and give it the completed analysis, design decisions, coverage matrix, and applicable general/project rules. Record an honest fallback when it is unavailable rather than claiming it ran. Installation, hosting, and deployment are separate actions, not implicit requirements of this prototype stage.

The [migration-review contract](migration-review.md) defines original-app authority, minimal deltas, same-state comparison, and named Duo environment coverage. The [device-presentation contract](device-presentation.md) defines the referenced exterior, calibrated display/app geometry, distinct physical posture and rotation controls, and a device-focused review surface. Pass their populated records and the [pre-implementation handoff](workspace-rules.md#pre-implementation-handoff-gate) to the selected builder before editing prototype implementation. Generated concepts are supplementary; compare final UI to the original and authorized adaptations.

Native region/bridge investigations may proceed in parallel where needed, constraining the prototype with explicit assumptions and capability gaps. Xcode, bridge implementation, and device acceptance are not prerequisites for independent HTML work. Product implementation and native acceptance follow the user's requested scope.

## Structure and editability

- Deliver an openable `index.html` and necessary relative assets, either as a single file or portable directory. State whether direct opening or a local server is required and provide a working entrypoint. Use existing project conventions and only necessary dependencies. Include editable source and reproducible instructions rather than leaving the runtime only on the author's computer.
- Organize HTML/CSS/JS around shared tokens, components, and pages. Every in-scope page is reachable, through multiple files or reproducible single-page routes, with consistent navigation, back/close behavior, and state. Framework-built prototypes must include their source and a reproducible local build/output.
- Keep text, bars, buttons, lists, cards, input, and overlays as editable interface structures. Screenshots may provide media or comparison evidence, not an uneditable full-page substitute.
- Use representative current-app content and legally usable assets. Attribute substitutes and missing media without inventing product photos or user data. Repeated placeholders do not establish page coverage.

## Layout and visual quality

Reuse the original tokens, components, icons, copy, navigation, density, and effective interactions. Apply iPhone guidance through evidence-required adaptations to hierarchy, geometry, insets, reachability, and continuity. Keep a working arrangement, including a single-column page, when it fits. Record required deviations and separately attribute optional improvements rather than imposing a generic website style. Check accessible names, hit areas, contrast, large text, keyboard focus, and Reduce Motion.

Verify these **layout categories** in one browser session. Derive sizes from actual material or content constraints and record them; unsupported presets are review dimensions, not claimed official device geometry:

- Narrow-window/outer-display presentation and ordinary iPhone regression.
- Expanded wider presentation, including readable content width, media, and multiple hierarchy levels where appropriate.
- Wide and short windows, both sides of breakpoints, and continuous narrowing/widening.
- Input, overlays, large text, RTL, or dark mode relevant to the original app.

Also implement usable named selectors for applicable **outer portrait/landscape, inner portrait/landscape, side-by-side app-left/app-right, and partial-fold book/tabletop/standing** environments as defined in the migration record. Account for exclusions and unsupported orientations. Match a supplied Device Hub's **Closed / PartiallyOpen / Open** physical controls and keep rotation independent. Outer portrait, inner portrait and inner landscape may be the three main review views when requested and evidenced; do not call them three official sizes. Keyboard/text controls are independent stress states. Provide same-page/state original-versus-adapted comparison; a generic width dropdown, static montage, or decorative device outline does not satisfy this showcase.

Adapt to the app preview container's actual available space. If a review page embeds a device canvas, its responsive behavior must follow that container; resizing the frame or scaling a fixed screenshot is insufficient. Derive the exterior, display aperture/corners, skin, buttons and cutouts from actual references, with a recorded scale mapping and visible uncertainty for missing evidence. Lead with an active device and compact comparison cards sharing the current task state. Keep device/view controls outside the app canvas; collapse coordinates, calibration details, stress controls and evidence into a secondary inspector so the device and original app remain the primary surface.

Keep one running app state across named switches and continuous resizing; review controls must not reload the page, discard work, or substitute separate datasets. Record and test actual app bounds, applicable control placement, insets/regions, and usable task results rather than only the selected preset label. Mark unverified geometry as review assumptions; do not hardcode an invented official hinge, camera gap, or pose-specific native behavior.

HTML may simulate safe areas, keyboard obstruction, and system regions with attributed sources or explicit assumptions. It cannot validate native SDK bars, an iOS reserved-region bridge, the real software keyboard, camera, or sharing plugins.

## Rich content and reading continuity

For content types actually used by the app—rich text, long links, code, tables, quotations, images/video, and attachments—define reading width, wrapping, local horizontal scrolling, media proportions, and scaling from the live pane width. A locally scrollable code block/table must preserve navigation, input reachability, and vertical reading without expanding the whole page horizontally.

Use meaningful task samples to test semantic reading anchors when asynchronous media loading, history pagination, and continuous resizing overlap. Define expectations for following the bottom, reading history, and explicitly returning to the bottom. Message bubbles, Markdown semantics, sending/read status, and draft lifetime belong to [project conventions](project-conventions.md); the general contract preserves the target app's content semantics and continuity.

## Complete pages and real interactions

Map the coverage matrix to pages and states. Primary destinations, secondary pages, detail/edit, necessary settings, and existing overlays all need entrypoints. Cover applicable loading, empty, error, selected, disabled, and success states. Explain inapplicable states rather than mechanically adding them.

Users must complete actual tasks: browse → choose → detail → back; input → edit → save → see the update; or open a menu → execute an action → receive feedback. Primary actions need semantic visible results. A common placeholder page, “coming soon” message, dead link, or button-color change alone does not implement a task. Model simulated services/system actions with local state, credible feedback, and a usable continuation path.

Narrow → wide → narrow transitions preserve route, selected item, drafts, semantic reading anchor, and applicable task progress. Changing layout must not switch to an unrelated copy of the data. Verify continuity through interaction.

Enter through real prototype navigation and complete primary tasks with a keyboard. Record where focus moves when a pane closes or a target is hidden/removed, and restore a visible trigger or sensible successor after a menu/overlay closes. Keep reflow and feedback stable under Reduce Motion. Complete browser-supported accessibility checks, and record actual platform/scope for VoiceOver and Full Keyboard Access under [validation](validation.md).

## Browser checks and visual review

Open the actual final output in a real browser and follow [validation](validation.md). At minimum, test primary tasks, every navigation entry, same-session resizing, important input and overlays, and inspect console errors, overflow, cropping, obstruction, missing resources, and unreachable controls.

Save actual captures representing layout families, named applicable Duo environments, relevant sizes/stress states, and important changes. Review shell fidelity separately against its device reference, including physical postures, silhouette, display aperture and scale mapping. Compare the same original and adapted app page/state for hierarchy, typography, density, whitespace, asset focal points, component states, and consistency; identify original capture provenance and reconstructed views separately. Explain each material change through the retain/adapt/change record. Repair shared components/rules and revisit affected pages when a defect repeats. Functional success and test counts do not establish either shell or app visual quality.

Deliver the completed matrix, source-linked recommendations, design rules, editable HTML and assets, captures, and verification records together. Analysis may live in separate documents; the operable app prototype remains the primary deliverable. Without a browser, preserve source and leave browser/visual acceptance pending. Missing key pages, broken primary tasks, clear layout defects, or absent visual review keep complete high-quality prototype acceptance open.
