# WKWebView interface shells

Read when the visible interface is HTML/CSS inside WKWebView. This contract covers Capacitor, Cordova, Ionic, uni-app, Taro, and custom shells. Validate page layout and native-container behavior separately.

## Lay out within the current visible area

Search for startup-cached `screen.width`, `window.innerWidth`, window width from system information, and rpx/upx/rem bases converted once from a design width. Use the current `visualViewport` or actual container width and update it when the window changes. Orientation and device names cannot replace the visible area.

Use CSS `env(safe-area-inset-top)`, `env(safe-area-inset-right)`, `env(safe-area-inset-bottom)`, and `env(safe-area-inset-left)` for safe areas. Check whether the viewport declares `viewport-fit=cover`; without it these environment variables generally do not expose four edge values. Consume each edge independently; left and right need not match.

## Shell, keyboard, and folding regions

Status-bar, keyboard, and native safe-area plugins belong to the shell, not page CSS. Record whether a plugin already adds a WebView inset. If CSS also compensates that same edge, remove the duplicate and state which layer owns it.

Page styles do not provide iOS reserved-region data. Avoidance requires a bridge delivering kind, identifier, frame, active state, coordinate-owning view, and units, with updates when folding changes. Without that data, HTML prototypes may declare assumptions; the product page cannot claim verified fold avoidance.

Check the shell's `UIView`, scene, safe areas, and orientation policy under [Apple frameworks](apple-frameworks.md). For changes to a Swift or Objective-C host, the exported Apple App Resizability checks can run in parallel.

Opening the page directly in a browser validates page layout and tasks, not WKWebView viewport behavior, plugin insets, or folding on hardware. Preserve both evidence scopes.
