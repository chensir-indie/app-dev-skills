---
name: iphone-duo-adaptation
description: Adapt an existing iOS app for iPhone Duo or resizable windows through whole-app layout analysis, minimal-change HIG recommendations and a complete interactive HTML prototype. Supports SwiftUI, UIKit, Flutter, React Native/Expo and WKWebView shells.
---

# iPhone Duo Adaptation

Follow **whole-app layout analysis → adaptation recommendations → complete HTML prototype**. Preserve the original app's identity, tasks and usable design with the smallest justified changes. An explicit module boundary or audit/advice-only request narrows the endpoint; native implementation and release are separate stages.

## Scope and starting point

Read project instructions, design material and runtime entrypoints. Use [framework identification](references/frameworks.md) to establish rendering layer, versions and mixed-framework boundaries, then read only the matching contract:

| UI framework | Contract |
| --- | --- |
| SwiftUI / UIKit, Swift or Objective-C | [Apple UI frameworks](references/apple-frameworks.md) |
| Flutter | [Flutter adaptation](references/flutter-adaptation.md) |
| React Native / Expo | [React Native](references/react-native.md) |
| Capacitor, Cordova, Ionic, uni-app, Taro or other WKWebView UI | [WebView shells](references/webview-shells.md) |

For other frameworks, continue shared design/HTML work while establishing their actual layout APIs. This community workflow is distinct from Apple's App Resizability Skill; target-build support requires evidence. Keep workflow/rule prose in English unless requested otherwise, and preserve the app's localization contract.

## 1. Analyze the current whole-app layout

Follow [layout analysis](references/layout-analysis.md) and the framework contract. Inspect actual captures, runnable UI, routes and shared components. Inventory every in-scope page, relationship and significant state, including hierarchy, actions, scrolling/fixed regions, panes/overlays, typography, input and narrow/wide/low-height behavior. Record excluded-module relationships without expanding scope.

Extract original components, tokens, copy and interactions. Establish the [retain/adapt/change record and named Duo environments](references/migration-review.md). For device references, apply [device presentation](references/device-presentation.md) to source exterior/display geometry and scale before drawing a shell. Attempt to acquire missing material; distinguish observations, source inference and unknowns.

**Stage gate:** a reviewable original-app baseline and coverage matrix account for every known page with evidence or an explicit gap. Every proposed change and prototype page traces to that baseline. Preserve usable arrangements; extra width alone does not justify new styling, navigation or features.

## 2. Recommend adaptations grounded in iPhone guidance

Read [official basis](references/official-basis.md) and verify relevant current HIG/framework facts. Materialize **every catalog rule** under the [workspace-rule contract](references/workspace-rules.md), with attributable [project conventions](references/project-conventions.md) separate. Add a conditional pointer in the project's Agent entrypoint.

For each recommendation, connect **baseline evidence → general/project rule ID and source → decision → affected pages/components → prototype check**. Cover layout/hierarchy, navigation/back/close/actions, visual accessibility, content/input/insets/overlays and continuity of route, selection, drafts, composition, reading anchors, media and async work.

Keep Apple guidance, framework facts, collection policy and product choices distinct. Split views, sidebars, breakpoints and center gaps need product-specific reasons. Mark other-framework rules `not_applicable` with evidence; defer native-only work with reasons. Missing Xcode, bridges or hardware does not block independent HTML work.

**Stage gate, before the first prototype implementation edit:** follow the [pre-implementation handoff gate](references/workspace-rules.md#pre-implementation-handoff-gate). Populate applicability, decisions, planned targets, exclusions/deferrals and adopted conventions. Freeze JSON/generated Markdown, original-design references, migration record, page/pose coverage and design handoff with hashes/timestamps. Verification may remain pending; an empty catalog passing structural checks is not ready for implementation. Preserve actual chronology when repairing an existing prototype.

## 3. Build and deliver the complete HTML prototype

Read [HTML requirements](references/html-prototype.md), [migration review](references/migration-review.md) and the [BUILD WEB APPS handoff](references/build-web-apps.md). Prefer the actual builder's matching creation or existing-design refinement/rendered-QA route. Read its real contract, record source/version/hash and execution mode, and pass the frozen stage-1/2 inputs. Apply its Image Gen requirements and exceptions only when their conditions hold. Generated concepts supplement the original app; they do not authorize redesign. Record an unavailable builder and an honest equivalent fallback. Keep local delivery separate from hosting.

Deliver editable source and runnable `index.html` with relative assets, or a project with reproducible static build. Cover every scoped page, task, shared component and important state. Reuse original components and record each necessary change.

Apply [device presentation](references/device-presentation.md): a device-focused active preview, compact comparison cards and secondary/collapsed diagnostics. Match sourced exterior/display geometry; label assumptions and calibration gaps. Keep Closed / PartiallyOpen / Open separate from rotation. External review controls expose applicable outer-display, inner portrait/landscape, side-by-side left/right and partial-fold contexts. Preserve one running app state and same-page/state original-versus-adapted comparisons. Browser width or a decorative frame alone does not prove real-device matching.

Use an actual browser and [validation.md](references/validation.md) for connected tasks, continuous resizing, low height, large text, rich content, input, overlays and focus. Inspect final screenshots against the adaptation design, retain mismatches, repair shared causes and repeat affected checks. Unavailable browser tools leave visual/interaction acceptance pending.

**Default delivery gate:**

- Framework identity, original baseline, minimal-change recommendations and populated pre-implementation handoff are available. Applicable rules and adopted project conventions pass the workspace completion check.
- The actual builder route or labeled fallback is evidenced; the complete prototype opens and all scoped tasks/states remain usable across named applicable environments.
- Independent shell-fidelity, original-app visual and functional reviews record source-to-browser scale, original/adapted captures, justified changes and unresolved calibration/native limits.
- Return a clickable HTML entry, source/assets, opening instructions, key tasks and validation records bound to final artifacts and source/local changes.

A later native implementation uses its own framework/build/SDK/runtime identities, production-navigation tests, production-mode smoke tests and required physical-device checks. HTML or fixture success does not establish native acceptance.
