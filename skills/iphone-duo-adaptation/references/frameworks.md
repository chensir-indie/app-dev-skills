# Identify the iOS UI framework

Read this before layout analysis. Determine **which framework draws the current interface**, then open its contract. General HIG guidance, the workspace ledger, and the HTML prototype apply across frameworks; the sources of size, safe-area, keyboard, bar, and folding-region data differ.

## Identification order

Cross-check repository manifests, entrypoints, and source code, and record the version source. When dependencies overlap or names are ambiguous, classify each screen by its actual rendering layer rather than the project's marketing label.

| Evidence | UI framework | Read next |
| --- | --- | --- |
| SwiftUI views form the page body | SwiftUI | [Apple frameworks](apple-frameworks.md) |
| `UIViewController`, Storyboard, XIB, or custom `UIView` forms the page body; language may be Swift or Objective-C | UIKit | [Apple frameworks](apple-frameworks.md) |
| `pubspec.yaml` and Dart UI form the page body | Flutter | [Flutter adaptation](flutter-adaptation.md) |
| A `react-native` dependency, or RN components in an Expo project, form the page body | React Native | [React Native](react-native.md) |
| Visible UI is HTML/CSS inside WKWebView; the shell may use Capacitor, Cordova, Ionic, uni-app, Taro, or a custom host | WebView shell | [WebView shells](webview-shells.md) |

Record mixed projects by layer: for example, Flutter embedded in a native shell or a native screen inside React Native. Each layer uses its own contract. A plugin, native module, or Swift/Objective-C host file does not change the page's UI framework. When the user requests changes to those native files, also use the UIKit/SwiftUI contract and the exported Apple App Resizability guidance.

Identify Kotlin/Compose Multiplatform, .NET MAUI, and Unity in the baseline when present. They have no dedicated implementation contract here. Continue with general HIG guidance and HTML without transplanting SwiftUI, Flutter, or React Native APIs. Before changing product code, establish that project's own layout, safe-area, and window APIs from its documentation.

Keep the framework unknown when evidence is insufficient. General guidance, layout analysis, and HTML can proceed without assigning unsupported framework APIs or test gates.

## Ledger applicability

Keep the [rule catalog](../assets/official-rules.json) complete. Mark another framework's dedicated rules `not_applicable`, naming the identified framework and evidence location. Retain the rule; distinguish inapplicability from work that has not been done.

Product implementation and device acceptance begin only when requested. Under `FRAMEWORK-IMPL-001`, use the identified framework's own execution and tests. The HTML prototype does not depend on these product toolchains.
