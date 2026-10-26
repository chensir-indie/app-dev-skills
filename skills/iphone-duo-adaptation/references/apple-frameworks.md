# SwiftUI and UIKit

Read this when SwiftUI or UIKit draws the target interface. Swift and Objective-C share the same UIKit layout contracts. Sources are [Prepare for iPhone Duo](https://developer.apple.com/iphone-duo/prepare/) and the SwiftUI/UIKit reserved-region documentation checked on 2026-10-26. Confirm API availability in the target SDK before writing product code.

## Measure the current space

Search for `UIScreen.main`, `UIDevice.current.orientation`, `statusBarOrientation`, `interfaceOrientation`, `userInterfaceIdiom`, `horizontalSizeClass == .regular`, and hardcoded model heights. Base layout on current available space:

- UIKit: use `view.bounds` or `window.bounds`. Put size-dependent layout in `layoutSubviews` or `viewDidLayoutSubviews`; use `viewWillTransition(to:with:)` when work must begin before a size transition. Read scale from `traitCollection.displayScale`. Create windows with `UIWindow(windowScene:)` rather than retaining a `UIScreen` as layout authority.
- SwiftUI: use `GeometryReader` or `onGeometryChange` for current geometry, and `@Environment(\.displayScale)` for scale. `GeometryReader` consumes the proposed size; place it in a `background` or `overlay` when measuring an existing view.
- Compare current width and height when the layout needs their relationship. Orientation, phone/pad labels, and tables of known device sizes cannot determine available space. `horizontalSizeClass == .regular` can also occur on iPhone.

Where the deployment target supports it, `containerRelativeFrame` is an optional way to allocate space relative to a container. System containers already account for safe areas; avoid subtracting them again based on unsupported assumptions.

## Safe areas, keyboard, and system bars

Handle all four insets independently; left and right need not match. Keep foreground controls inside the safe area while allowing full-bleed backgrounds behind it. SwiftUI places content in the safe area by default; use `ignoresSafeArea` explicitly for intentional bleed. Custom UIKit layout reads `safeAreaInsets` or constrains content to `safeAreaLayoutGuide`.

Prefer `keyboardLayoutGuide` for keyboard-related constraints. Check which safe-area portion it already includes before adding notification-derived heights or `additionalSafeAreaInsets`. SwiftUI input accessories use the current system safe-area or keyboard inset; verify actual behavior on the target version.

System navigation containers adapt their standard navigation, tab, and toolbars to Duo posture. Custom bars require separate checks for hit areas, titles, icons, grouping, and overflow.

## Reserved regions in custom interfaces

System containers such as split views and sheets handle their own folding and occlusion regions. Custom layouts query regions when needed:

- SwiftUI: call `reservedRegions(kind:options:layoutDirectionBehavior:)` on `GeometryProxy`. `.occlusion` represents obstructions such as cameras or Dynamic Island; `.division` represents a division caused by folding. The default query returns active regions intersecting the view.
- UIKit: call `reservedRegions(kind:options:)` on the queried `UIView`; the region type is `UIView.ReservedRegion`.

A region's `frame` is in the queried view's coordinates, measured in points, and already includes margins. Consumers must not add those margins again. A region can extend partly outside the view and therefore have negative coordinates. Duo's division is active only while partially folded; the default query does not return that division when fully open. Query inactive regions explicitly only when a design decision, such as column count, actually needs their presence. Distinguish that decision from avoiding an active fold.

HTML may simulate these regions with declared assumptions. A browser result does not prove that the product calls these APIs. For bulk Swift or Objective-C changes, also consult the actual exported Apple App Resizability Skill. A missing export remains a native-evidence gap while layout analysis and HTML work continue.
