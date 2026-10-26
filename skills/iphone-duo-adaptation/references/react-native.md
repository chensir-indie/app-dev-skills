# React Native

Read when React Native draws the target interface; Expo apps use the same UI contract. The React Native documentation for `useWindowDimensions`, built-in `SafeAreaView`, and `KeyboardAvoidingView`, and Expo safe-area guidance, were checked on 2026-10-26. Dependency versions come from the target project's lockfiles.

## Window dimensions

Use `useWindowDimensions()` for layout. It updates `width`, `height`, `scale`, and `fontScale` when screen dimensions or font scale change. Search for `Dimensions.get("window")` cached at module load or in startup effects; avoid treating that one result as a permanent size.

Use current width and height to determine columns, reading width, and bar presentation. Orientation and device labels such as `Platform.isPad` cannot substitute for available space.

## Safe areas and keyboard

First identify the safe-area implementation actually installed:

- The built-in `react-native` `SafeAreaView` documentation describes iOS 11+ support and a padding-based implementation; padding styles applied to that view are ignored.
- Expo and React Navigation use `react-native-safe-area-context`. It needs a root `SafeAreaProvider`. `useSafeAreaInsets()` returns four values relative to the nearest provider and excludes the software keyboard. The official window example also imports `SafeAreaView` from this library.

Handle the keyboard separately. Give `KeyboardAvoidingView` an explicit `behavior`; iOS and Android respond differently to it. Whether `keyboardVerticalOffset` applies depends on the current navigation-bar height. Avoid compensating the same edge through both safe-area padding and keyboard height. Retain a keyboard library already validated in the project rather than replacing it merely to match this reference.

## Navigation bars and folding regions

Native containers such as `react-native-screens` and native stack differ from JS-rendered top bars. Verify Duo posture behavior in the iOS host for native bars; validate JS bars as ordinary RN layout.

The React Native documentation checked here provides no counterpart to SwiftUI `reservedRegions` or UIKit `UIView.reservedRegions`. Without a versioned native module and actual device data, claim only window-size adaptation and keep folding regions unverified. An empty JS geometry object cannot prove the absence of an iOS reserved region.

Product implementation uses the target project's iOS build. Flutter's `integration_test` and SwiftUI APIs do not apply to this path. Enter new screens through the app's existing navigation and record the Metro/native build type and simulator/device used.
