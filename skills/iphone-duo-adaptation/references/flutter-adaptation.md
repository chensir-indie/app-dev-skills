# Flutter dynamic-layout implementation notes

Read only when [framework identification](frameworks.md) confirms that Flutter draws the interface. Use this contract for feasibility questions or later requested product implementation. It is not a migration prerequisite for the default HTML prototype and does not apply to SwiftUI, UIKit, React Native, or WebView shells. API availability depends on the target project's locked Flutter version. Sources and check dates are registered in the [official basis](official-basis.md). Validate these engineering recommendations against the target app's behavior.

## Space, navigation, and content

- Use `LayoutBuilder` for a component's parent constraints and `MediaQuery.sizeOf(context)` when current view size is needed. Avoid retaining startup dimensions, a global window, or physical pixels as long-lived layout inputs. Trace unbounded constraints to the parent; infinity is not a screen width.
- Derive breakpoints from the task content's minimum usable space and test both sides. Orientation can describe a camera task's semantics; portrait/landscape or phone/tablet labels cannot replace available geometry.
- A destination and action model can have narrow and wide presentations. Sidebars and list/detail layouts are choices. Wide, short windows still require a height strategy. Give reading content a suitable width and grids an appropriate column count; preserve image focal points and preview/export crop contracts.
- Flutter `AppBar`, `CupertinoNavigationBar`, `NavigationBar`, and custom toolbars are not native bars managed by Apple navigation containers. Test layout, hit areas, semantic labels, grouping, and overflow before deciding which actions change axis. Avoid mechanically rotating every control.
- Derive rich-content reading width, wrapping, local code/table scrolling, and media proportions from live pane constraints. Preserve a semantic reading anchor when media loading, pagination, and resizing overlap. The product defines follow-bottom and history-reading behavior; message-specific contracts belong to [project conventions](project-conventions.md).

## Safe areas, keyboard, and overlays

- Check updates to all four `padding`/`viewPadding`/`viewInsets` values and their consumption by nested `Scaffold`, `SafeArea`, and local `MediaQuery` instances. Left and right insets need not match. `SafeArea` does not guarantee avoidance of an arbitrary central region.
- Inspect `Scaffold.resizeToAvoidBottomInset` and existing keyboard handling before adding compensation. Avoid shrinking the body and manually adding the same inset. Input accessories follow the keyboard; verify composing text, caret visibility, submit reachability, and restoration after dismissal.
- For menus, dialogs, sheets, `OverlayEntry`, and native popover/share sheets, obtain current trigger geometry and identify local/global conversion and the target navigator. Recompute anchors after resizing or close the overlay according to product behavior; retain unfinished content and a usable continuation path.
- Text scaling, RTL, VoiceOver focus, and reachability can expose defects invisible in screenshots. Manage text-input/IME focus, keyboard-navigation focus, and assistive-reading focus separately. Complete primary tasks with VoiceOver and Full Keyboard Access, defining each focus destination after a pane is hidden, restoration after overlay dismissal, and reflow under Reduce Motion. Native hardware-sidebar RTL rules do not automatically apply to every Flutter custom navigation element.

## iOS folding regions and platform bridges

On its recorded check date, the `MediaQueryData.displayFeatures` contract guarantees population only on Android. If the target version changes that contract, record the engine/plugin version, implementation path, and actual iOS data before relying on it. Android hinge/fold examples are not Duo runtime evidence.

Check whether the current embedding/plugin exposes iOS reserved-region data. If a bridge is needed, design it against current Apple `ReservedRegion` documentation and record an explicit bridge contract:

| Field or semantic | Contract |
| --- | --- |
| `kind`, `id`, `isActive` | Region category, stable identifier, and whether it is currently active. Identify these as bridge fields rather than claiming they are identically named Apple API properties. |
| `frame`, coordinate-owning view, units | Identify the source UIView/scene and Flutter view, rectangle coordinate space, and point/logical-pixel conversion. Apple `ReservedRegion.frame` already includes margins; avoid adding them again. |
| Update timing/events | Define sampling/update timing, event order, and clearing after deactivation/removal. If the source has no timestamp, record a local time or sequence in the bridge. |

Verify ownership and coordinate conversion across folding, unfolding, rotation, window changes, and multiple scenes. Without region data, claim only ordinary size adaptation and leave region avoidance unverified. An empty `displayFeatures` list does not establish that iOS has no region.

`DisplayFeatureSubScreen` and a dialog's `anchorPoint` choose a subregion only from known feature data. An invented central hinge, fixed pixel gap, or posture guessed from width/height cannot establish native adaptation.

## State continuity

- Give routes, selected records, and editing sessions stable state ownership. Preserve controller, focus-node, request, and save lifetimes instead of recreating them in `build` or at every breakpoint transition.
- Use the project's existing keys, page storage/restoration, or state management. Moving content between containers can change element identity; test it rather than inferring preservation from copied key names.
- Pixel offsets may refer to different content when a list changes columns. Preserve a semantic visible-item anchor. Check draft text, selection, and composing state; editor undo/redo; media progress; and duplicate asynchronous operations.
- Platform focus or keyboard behavior may change during folding, but user tasks, content, and recoverability need an explicit contract. Resizing and process-restart restoration are separate tests.

## Runner and dependencies

Inspect the linked SDK, minimum deployment target, orientations, launch screen, and scene behavior in maintained source configuration. Fix evidenced defects within scope and preserve embedding/plugin lifecycle callbacks. An SDK or scene migration must not blindly replace the runner with a native template.

Guard debug-only render-object diagnostics before access using short-circuiting `kDebugMode && ...` or an early return; Profile mode may also lack the capability. Decide from the API contract rather than its name. Obtain hardware-specific evidence under the [validation contract](validation.md).
