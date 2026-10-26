# Preserve the original app across Duo environments

Read during whole-app analysis, recommendation handoff, and HTML review. This is the collection's migration and review contract; it does not prescribe a new Apple product style or certify a framework's native support. Keep **whole-app layout analysis → adaptation recommendations → complete HTML prototype**.

## Original design authority and the smallest necessary change

Use the target app's observed UI, approved design references, shared components, tokens, copy, and content hierarchy as the primary design authority. Record their source/build or file identities and distinguish observed behavior, source inference, and unknowns. If an approved reference differs from the running app, identify that conflict and the authorized target instead of silently combining them. A generated concept or the previous prototype is supplementary evidence unless the user explicitly adopts it as the design target.

Extract enough of the current design to reuse it: type scale and weights; semantic colors; spacing and density; radii and materials; row/card/button/input families; icons and labels; navigation/back behavior; fixed/scroll boundaries; important component states; asset crop and content rules. Preserve the original page stack and single-column presentation wherever they remain usable. More space alone does not require an extra column, side navigation, a new toolbar, new icons, new copy, or additional features. Offer optional enhancements separately, with project attribution, rather than making them migration defaults.

Maintain a concise retain/adapt/change record alongside the page matrix. Shared-component decisions can cover several named pages, but every proposed page-level change must trace to one:

| Field | Required content |
| --- | --- |
| Page/state/component | Existing identity and affected task, including shared-component consumers |
| Original reference | Actual screenshot/build/source/design location and its identity; observed/inferred/unknown |
| Treatment | `retain`, `adapt`, or `change` |
| Delta and reason | Smallest necessary modification, current conflict, relevant rule/source, and why a lower-impact treatment is insufficient |
| Affected environments | Named review environments, available-space conditions, and relevant stress states |
| Preservation and verification | Original tokens/content/interactions retained, planned checks, then actual same-state before/after evidence and results |

`retain` keeps a working arrangement; `adapt` adjusts the existing component's geometry, insets, wrapping, placement, or state ownership; `change` replaces a pattern only when evidence establishes that smaller adjustments cannot meet platform, accessibility, or task requirements. A justified defect repair or explicitly authorized redesign remains possible; record its scope. Keep product choices in [project conventions](project-conventions.md) rather than attributing them to Apple.

Compare the **same page and state** before and after: matching content, selected object, draft/task progress, text scale, and relevant scroll/overlay state. Identify the original capture's actual viewport; if its geometry differs, explain the comparison rather than claiming a pixel-identical setup. Keep source captures separate from reconstructed baseline previews. A missing original is a recorded gap or proposed design, never a generated substitute presented as the real app.

## Named environment coverage

Generic responsive widths are necessary checks but do not by themselves demonstrate a Duo migration. Define the following named environments before implementation. Read the [device-presentation contract](device-presentation.md) to collect the actual Device Hub/simulator or official reference and freeze exterior/display calibration alongside this matrix. Record applicability and reasons for exclusions against the actual app, target system, and orientation contract; do not silently omit an environment or force native capabilities the app does not support. The matrix names review contexts, not a list of official device sizes.

A current limitation that conflicts with applicable guidance is an adaptation gap, not a reason to declare that guidance inapplicable. Distinguish an HTML simulation from a confirmed supported native configuration.

| Environment | Review purpose |
| --- | --- |
| Closed outer display, portrait | Existing compact iPhone tasks, readable density, insets, and continued navigation |
| Closed outer display, landscape | Short-height behavior, preserved actions, and supported orientation handling |
| Open inner display, portrait | Expanded available space and applicable horizontal-bar behavior |
| Open inner display, landscape | Wider content and applicable side-control placement without gratuitous new columns |
| Side-by-side, app on the left | Narrow app window and controls at the app's outside edge |
| Side-by-side, app on the right | Same tasks with the opposite outside edge, not just a renamed preset |
| Partial fold: book, tabletop, or standing | Applicable partial-fold configurations and usable regions; record each relevant orientation rather than treating all partial folds as one geometry |

Keep **Closed / PartiallyOpen / Open** as physical posture states when matching those controls in the supplied Device Hub. Rotation is independent; inner portrait and inner landscape can be orientations of the same open device. When outer portrait, inner portrait and inner landscape are the requested main views, make them easy to compare while retaining applicable partial-fold and app-window checks. Determine each view's actual bounds and appearance from capture/calibration; do not turn three review views into three invented official sizes.

Keyboard visibility, large text, RTL, dark mode, menus, and sheets are **stress states**, not physical poses. Apply them to relevant named environments. Keep continuous resizing and intermediate widths in the test plan; do not implement a different bespoke product layout for every preset.

Apple's [Design for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111466/) describes the outer/inner displays, partial-fold poses, two-app side-by-side use, and pose-related control placement. Most poses use side controls; inner portrait retains horizontal bars. In side-by-side use, app controls follow its outside edge. Partial-fold portrait targets favor the lower usable area; an optional tabletop arrangement preserves control hierarchy and function. Recheck decision-relevant details against the [Duo HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) and maintained [official basis](official-basis.md).

For custom navigation, review applicable native targets without claiming automatic framework behavior. [Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462/) distinguishes the edge detail column from other columns, allows appropriate compound/title controls to remain horizontal, and keeps keyboard accessories with the keyboard. Preserve those distinctions when deciding whether an existing component needs rearrangement. Follow actual view geometry and safe areas; [Prepare](https://developer.apple.com/iphone-duo/prepare/) warns against device identity inferred from size class, orientation, or idiom. HTML demonstrates the proposed treatment; native bars and region delivery need their own target-build evidence.

For each review preset, record its stable name, physical posture, display, orientation, app-window placement, applicability, source, app-frame dimensions and coordinate units, available content bounds, four-edge inset assumptions, active/reserved regions and their ownership, expected control placement, and native unknowns. Keep source screenshot pixels/UI zoom, logical points/display scale, CSS pixels/browser pixel ratio, shell coordinates and preview magnification separate under the [calibration record](device-presentation.md#establish-the-device-reference-before-drawing-the-shell). Use actual simulator/host values when available. Otherwise label dimensions and regions **review assumptions**, with provenance; do not invent official display dimensions, a fixed center hinge/gap, camera cutout, or folding curve. A decorative device outline is not geometry evidence. Partial-fold simulations must expose which region is active and what remains unknown; content does not need a mechanically inserted center split.

## Usable review and continuity

Provide a large active device and compact comparison cards for the required main views, with concise posture/view controls **outside the product canvas**. Keep the comparison views on the same page/task state; editable views share app state and captured cards identify freshness. Put detailed dimensions, coordinates, stress controls and evidence in a collapsed secondary inspector, retaining a short visible indication of material uncertainty. Include the original-versus-adapted comparison. All in-scope pages and tasks must remain reachable across applicable environments. A layout family can share representative captures if the matrix still maps every page and state to its treatment and check.

Pose switches change the running app container and applicable region assumptions. Keep one app state: route, selection, draft/composition where modeled, semantic reading anchor, media, and ongoing tasks survive transitions. Do not reload the app or switch to disconnected datasets to mimic continuity. Reflow must use the live app container, not a scaled screenshot or a fixed layout shrunk to fit. Optional canvas magnification is separate from layout dimensions.

Verify both the review controls and their actual effects: measured container/content bounds, control reachability and placement, overlay anchors, scrolling, and same-state task completion. A selected pose label alone is not evidence that the app adapted. Capture the device reference and matched rendered exterior separately from the original and adapted app page/state. Review shell fidelity and original-app visual quality independently from functional results; neither a plausible frame nor passing task counts can establish both. Explain retained design and necessary deltas, and record failures and repairs. Browser evidence, simulated regions, native-host checks, and physical-device acceptance retain separate scopes under [validation](validation.md).
