# Analyze the current app's whole layout

Read this first for a default adaptation task. Understand the existing app's organization and recurring layout problems so page-specific decisions and the complete prototype have evidence. The original app is the design authority; follow the [migration-review contract](migration-review.md) to preserve its working arrangements and justify the smallest necessary changes.

## Map pages and tasks

Cross-check routes, navigation shells, shared components, screenshots/recordings, and available runtime entrypoints. Include primary destinations, secondary pages, detail/edit, search, settings, existing onboarding, and necessary overlays. Follow real entrypoints to identify conditional routes and important states; names alone do not establish that a path runs.

Maintain a coverage matrix in the project's existing artifact directory with at least:

| Field | Content |
| --- | --- |
| Page/state and source | Stable identifier, route/entrypoint, screenshot or code location, observed/inferred/unknown label |
| User tasks and relationships | Page relationship map, navigation hierarchy, access path, primary task, back/close, cross-page dependencies |
| Existing layout anatomy | Navigation, content, tools/input, fixed and scrollable regions and boundaries, overlays and anchors |
| Shared rules | Original typography, semantic colors, materials, spacing/density, radii, icons/copy, component families/states, and existing inconsistencies; approved source identity |
| Spatial baseline | Actual narrow/wide/low-height captures, available container and pane sizes, keyboard/large-text states, missing views and reasons |
| Adaptation risks | Excessive width/density, low-height overflow, safe-area/input obstruction, unreachable actions, state resets |
| Treatment and prototype entry | Retain/adapt/change decision and smallest necessary delta, affected named Duo environments, target layout/state, reachable HTML path, same-state before/after evidence |

For the default whole-app scope, every known page belongs in the matrix. A layout family may share analysis and component rules, but each page still needs its own task, content, and entrypoint. One representative screen cannot establish complete coverage.

## Analyze at app and page scales

**Across the app:** check navigation hierarchy and back behavior, stable destinations, content/action priorities, existing iPhone/iPad/landscape foundations, and consistency of theme, type scale, spacing, and bars. Explain relationships among features and pages; a control inventory alone is not whole-layout analysis.

**Within each page:** identify what users read and do first. Compare reading width, density, alignment, whitespace, media focal points, and primary-action placement. Inspect scrolling containers, fixed toolbars, keyboard, and overlays. Record specific conflicts at different sizes and structures that work and should remain.

Extract the existing visual/component contract before proposing new layouts. A working single-page stack remains a valid expanded presentation; additional columns, navigation chrome, new icons, or new features need their own evidence and authorization. Map each proposed modification to the migration record, and distinguish an optional product improvement from required adaptation.

Where the app can run, capture narrow/wide/low-height views representing every layout family, including important input, overlay, and scrolling states. Record app/build identity when available, window and local pane sizes, text scale, and source. If the current app fails at a layout, retain the actual failure or evidence gap; save adapted captures separately. Source inspection can locate problems and infer uncaptured branches, but does not become a runtime observation. Screenshots alone support visible-layout analysis; keep navigation, state, and dynamic behavior unknown where evidence is missing.

Record global inventory scope separately from the current redesign scope. Modules explicitly excluded from redesign still need their navigation and layout relationships documented. Inventory does not automatically authorize redesign. Message, calendar, and editing behavior for apps such as IMX belongs in [project conventions](project-conventions.md).

## Use technical scans to explain layout

Follow the [identified framework's contract](frameworks.md) to find geometry, safe-area, keyboard, navigation, and region entrypoints, shared components, and state lifetimes. Flutter searches can include `Scaffold`, `Navigator`, routers, `LayoutBuilder`, `MediaQuery`, `SafeArea`, `viewInsets`, `OverlayEntry`, and controllers. SwiftUI/UIKit searches cover current-view geometry, safe areas, keyboard, and reserved regions. React Native searches cover window metrics, safe-area libraries, and keyboard handling. WebView searches cover viewport, `env(safe-area-inset-*)`, and startup-cached screen widths. Inspect a platform host when SDK, native-bar, or region behavior affects a decision.

Explain the user impact: for example, cached width leaves a gallery with the wrong column count after unfolding. API lists, regex match counts, or blanket replacement proposals without context are insufficient.

## Missing material

First try the existing repository, page materials, and runtime capabilities. For each missing page, record acquisition attempts, known entrypoints, and impact. An unobserved design may be an explicit proposed option, not a claim about the current app. If critical gaps permit only a partial prototype, deliver the useful result with its scope and keep whole-app completion open.

This stage should let a reviewer answer: what layout rules does the current app follow, what can remain, where are its problems, why is each adaptation needed, and how will final HTML cover all known pages/tasks and applicable named Duo environments?
