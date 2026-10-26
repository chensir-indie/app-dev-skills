---
name: iphone-duo-adaptation
description: Help adapt and optimize an existing iOS app for iPhone Duo across SwiftUI, UIKit, Flutter, React Native/Expo, and WKWebView shells. Preserve its original design with minimal necessary changes through whole-app layout analysis, Apple HIG-linked recommendations, and a complete interactive HTML prototype demonstrating named Duo environments with sourced device exteriors and display geometry, preferably through BUILD WEB APPS. Use for app-wide layout migration or fold/unfold adaptation.
---

# iPhone Duo Adaptation

The goal is to **help adapt and optimize the existing application for iPhone Duo**, preserving its product identity, usability, and task continuity across supported display and window configurations. Follow **whole-app layout analysis → adaptation recommendations → complete HTML prototype** to make the necessary improvements concrete and reviewable. The original app is the design authority: use the smallest changes needed for supported Duo environments. Identify the rendering framework first; framework discovery supports these stages and does not replace them.

| UI framework | Read when identified |
| --- | --- |
| SwiftUI or UIKit in Swift/Objective-C | [Framework identification](references/frameworks.md), [Apple UI frameworks](references/apple-frameworks.md) |
| Flutter | [Framework identification](references/frameworks.md), [Flutter](references/flutter-adaptation.md) |
| React Native, including Expo | [Framework identification](references/frameworks.md), [React Native](references/react-native.md) |
| Capacitor, Cordova, Ionic, uni-app, Taro, or other WKWebView UI | [Framework identification](references/frameworks.md), [WebView shells](references/webview-shells.md) |

For Compose Multiplatform, .NET MAUI, or Unity, identify the actual rendering layer and continue with shared HIG/design/HTML requirements until its own layout APIs are established. This community workflow is distinct from Apple's App Resizability Skill; framework support must be demonstrated on the target build.

## Scope and starting point

Read project instructions, design material, and available runtime entrypoints. Establish rendering layer, versions, and mixed-framework boundaries using [framework identification](references/frameworks.md). By default inventory every known page, relationship, shared component, and relevant state. Honor explicit module boundaries or an analysis/advice-only endpoint and state coverage gaps.

Preserve the app's tasks, content, brand, components, tokens, copy, and effective interactions. Keep an existing arrangement wherever it remains usable; adjust geometry, insets, navigation placement, or continuity only where baseline evidence and platform guidance require it. A larger display does not itself justify new styling, features, icons, or information architecture. Product implementation, SDK/scene migration, and release follow the user's scope and framework toolchain; they do not replace the prototype. Native investigations can run alongside independent design work. Write workflow documentation and rule prose in English unless requested otherwise; preserve the app's localization contract.

## 1. Analyze the current whole-app layout

Read the [layout-analysis contract](references/layout-analysis.md) and relevant framework contract. Combine actual screenshots/recordings, runnable UI, routes, and shared components into an inventory of pages, navigation, states, and layout families. Analyze hierarchy, content/actions, fixed and scrolling regions, panes/overlays, typography, density, input, and narrow/wide/low-height constraints.

Produce a reviewable baseline and coverage matrix before designing adaptations. Extract the original app's visual/component contract and establish the [retain/adapt/change record](references/migration-review.md). Read the [device-presentation contract](references/device-presentation.md) when collecting the supplied Device Hub/simulator or official device references: establish the actual exterior, display/app geometry and scale provenance before drawing the review shell. Account for every known page with evidence or an explicit gap. Distinguish observed UI, source inference, and unknowns; attempt to acquire missing material. Record relationships to excluded modules without expanding their scope.

**Stage gate:** repository evidence identifies the framework; the baseline covers page relationships, navigation hierarchy, fixed/scrolling regions, original visual/component rules, and narrow/wide/low-height evidence or gaps. Every prototype page and proposed change traces to the original app. Define applicable named Duo environments under the [migration-review contract](references/migration-review.md).

## 2. Recommend adaptations grounded in iPhone guidance

Read the [official basis](references/official-basis.md) and verify relevant current HIG and framework facts. Materialize the entire catalog using the [workspace-rule contract](references/workspace-rules.md); keep attributed [project conventions](references/project-conventions.md) separate. Bind decisions to the baseline, an existing `Design.md` or equivalent, prototype targets, and actual evidence. Add a short conditional pointer in the project's Agent entrypoint.

Keep Apple guidance, framework facts, collection policy, and product choices attributable. Mark another framework's specific rules `not_applicable` with the identified framework as the reason. IMX permission, sending, unread, and draft behavior belongs only to the applicable project. Native-only checks may be deferred with reasons during HTML work; missing Xcode, a native bridge, or hardware does not block independent layout/design/HTML work.

| Decision | Explain |
| --- | --- |
| Layout and hierarchy | What is retained or changed, which levels appear at each available size, and how this improves the main task |
| Navigation and actions | Destinations, back/close, primary actions, toolbar grouping, overflow, and continued reachability |
| Visual and accessible behavior | Shared typography, semantic colors, materials, spacing, hit areas, large text, and focus |
| Content and input | Readable widths, rich content, dynamic insets/regions, keyboard accessories, and anchored/window-level overlays |
| Continuity | Route/selection, draft/selection/composition, logical reading anchor, media, and asynchronous work across layout changes |

Trace each key recommendation through **current evidence → general/project rule ID and source → decision → affected pages/components → prototype check**. Split views, side navigation, breakpoints, and a fixed center gap require product-specific reasoning; they are not universal Apple mandates. One framework's APIs or native-bar behavior cannot establish another framework's support. Label simulated system regions and native unknowns.

**Stage gate, before creating or editing prototype implementation in this iteration:** record applicability for every catalog rule; fill applicable decisions and planned target paths, reasoned exclusions/native deferrals, and adopted project conventions. Verification may remain pending until execution. Freeze the populated JSON/Markdown ledger, original-design references, retain/adapt/change record, page/pose coverage, and design handoff with identities and timestamps. An empty pending catalog copy is not a completed handoff. Follow the [pre-implementation gate](references/workspace-rules.md#pre-implementation-handoff-gate), then continue to HTML.

## 3. Build and deliver the complete HTML prototype

Read the [HTML contract](references/html-prototype.md), [migration-review contract](references/migration-review.md), and [BUILD WEB APPS handoff](references/build-web-apps.md). Prefer the actual BUILD WEB APPS construction/refinement and rendered-QA Skills. Select their creation or existing-design refinement route honestly, read the real entrypoints, record source/version/hash and execution mode, and pass the frozen original-app and stage-1/2 contracts. Keep this package self-contained; link to the external builder rather than vendoring it.

Follow the selected contract, including Image Gen where that route requires it. Generated concepts supplement the original app and cannot become authority for an unrequested redesign. Reuse original tokens/components; make justified changes explicit in the migration record. Apply actual creation/refinement exceptions only when their conditions hold. If the builder cannot run, record the precise limit and use an equivalent available path; never claim it ran when it did not.

Deliver editable source and a runnable `index.html` with relative assets, or a framework project plus its reproducible static build. Cover every in-scope page, task, shared component, and important state. Follow the [device-presentation contract](references/device-presentation.md): lead with a device-focused active preview and compact main-view comparison cards; keep diagnostics and stress/evidence controls secondary. Reproduce the actual referenced exterior and display aperture without redesigning the app. Separate Closed, PartiallyOpen and Open physical controls from rotation, and derive required views from calibrated evidence rather than claiming three official sizes. Explicitly showcase applicable outer-display, inner-portrait/landscape, side-by-side left/right, and partial-fold environments through usable review controls outside the app canvas. Keep one running app state across switches and provide same-page/state original-versus-adapted comparisons. Label unknown geometry and simulations; a generic frame or browser width cannot establish real-device matching. Keep local delivery separate from optional hosting.

Use a real browser and the [validation contract](references/validation.md) to check page coverage, connected tasks, continuous resizing, low height, large text, rich content, input, overlays, and focus. Review actual final screenshots against the accepted adaptation design, save mismatches, repair shared problems, and repeat affected checks. Keep browser/visual acceptance pending if its required tools are unavailable.

**Default design/prototype delivery gate:**

- Framework identity, original-design baseline, minimal-migration record, recommendations, and populated pre-implementation handoff are available; applicable rules and adopted project conventions pass the completion check.
- The preferred builder's actual execution or an accurately labeled fallback is evidenced, including design and rendered review.
- The full prototype opens, named applicable Duo environments are reviewable, and all in-scope tasks/states remain usable across them; independent shell-fidelity and app-visual checks accompany functional results. Source-to-browser scale mapping, real-reference matching or specific open calibration gaps, original-versus-adapted captures, necessary changes, and platform limits are explicit.
- Provide a clickable HTML entry, source/assets, opening instructions, key tasks, and validation records.

An explicit narrower request may end at its requested stage. Bind evidence to source/dirty changes and final artifacts. Later product implementation records framework/build/SDK/runtime identities and runs its own production-navigation, production-mode, and hardware checks. HTML, fixture entrypoints, and real native-device acceptance remain distinct evidence scopes.
