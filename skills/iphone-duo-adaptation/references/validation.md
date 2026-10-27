# Validate runtime behavior and final output

For a default adaptation task, validate the HTML in a browser and review its actual rendering. Product implementation checks apply only when the user requests that later stage and only under the identified framework's contract. Xcode, a Duo simulator, and physical devices are not prerequisites for independent HTML work.

## Default HTML acceptance

| Acceptance area | Actual checks and evidence |
| --- | --- |
| Whole-app analysis | Page relationships, navigation hierarchy, fixed/scroll regions, original tokens/components/copy, and working arrangements appear in the baseline matrix. Layout families have narrow/wide/low-height evidence or explicit gaps; original captures, reconstructions, source inference, and unknowns are distinct. |
| Complete workspace rules | Every catalog ID has exactly one binding; general rules and project conventions are separate, with applicability, decisions, actual paths, and evidence. JSON/Markdown match and the completion check passes. |
| Adaptation recommendations | Important issues trace to current evidence and Apple HIG sources. The retain/adapt/change record justifies the smallest necessary delta and accounts for every proposed change. Page-level treatment and shared rules agree; extra columns, new chrome, icons, copy, or features have no automatic mandate. |
| Pre-implementation handoff | Before this iteration's first implementation edit, freeze populated applicability, decisions, planned targets, adopted project conventions, original-design references, migration/environment matrix, device-reference/calibration record and design handoff. Inspect content and chronology; initializing a pending ledger or completing it later does not pass this gate. |
| Builder runtime | Record the selected builder, actual Skill path/source/version/hash, handoff inputs, commands/actions, and resulting files. Read the [BUILD WEB APPS handoff](build-web-apps.md); distinguish actual use from an unavailable-builder fallback. Preserve the three-stage order and the authorized local/deployment boundary. |
| Page coverage | Every matrix page and necessary state has a reachable prototype entry; back/close/navigation have no dead ends or generic placeholders. |
| Complete tasks | Enter through actual navigation and obtain semantic visible results from editing, saving, selecting, searching, menus, and overlays where applicable. |
| Named Duo environments | Exercise applicable outer portrait/landscape, inner portrait/landscape, side-by-side app-left/app-right, and partial-fold configurations under [migration review](migration-review.md). Check actual app bounds, applicable control placement, insets/regions, usable tasks, and reasoned exclusions; a selected preset label alone is insufficient. Verify Closed / PartiallyOpen / Open physical controls and independent rotation against the supplied Device Hub reference, where applicable; three main review views do not establish three official sizes. |
| Device presentation | Under the [device-presentation contract](device-presentation.md), compare actual rendered exterior/display crops against identified references: silhouette, proportions, aperture/corners, finish/skin, buttons/cutouts and required postures/orientations. Inspect the scale/calibration record and app-container measurements; screenshot pixels, UI zoom, logical points/display scale, CSS pixels/browser pixel ratio and preview magnification remain distinct. Unverified geometry and unseen hardware remain open; a generic shell cannot pass real-device matching. |
| Continuous adaptation | In one session, named pose switches, narrow → wide → narrow, low height, and breakpoint crossings preserve route, selection, drafts, and semantic reading anchors. Verify one running state without reload or disconnected datasets. Keyboard/large text/overlays are separate stress states applied to relevant environments. |
| Rich content | At the actual pane width, long text/links, code, tables, quotations, media, and attachments wrap or scroll locally. Overlapping media load, history pagination, and resizing retain the reading anchor and product-defined follow-bottom behavior. |
| Accessibility and state | Check applicable large text, RTL/themes, labels, contrast, and reachability. Complete primary keyboard tasks and record focus after hiding a pane, restoring an overlay, and reflow under Reduce Motion. |
| App visual quality | Independently of shell fidelity and task counts, compare the same original and adapted page/state for hierarchy, typography, spacing, density, alignment, media crop, and component consistency. Identify retained design and necessary deltas; generated concepts cannot replace original authority. Repair shared defects and revisit affected pages. |
| Review presentation | Inspect the opening view and controls: the active device and compact main-view comparison cards are readable, share current page/task state and remain operable; rotation is distinct from physical posture. Coordinates, detailed dimensions, stress controls and evidence are collapsed secondary tools outside the app UI. |
| Execution and resources | Open the actual final entrypoint. Check console errors, missing resources, overflow, obstruction, overlay anchors, and all navigation; keep review controls separate from the app UI. |

Record browser/version, final HTML/resource identity and hashes, named environment and actual container/viewport sizes, task steps, results, and capture locations in the coverage matrix. Attribute original and adapted captures independently, with matching page/content/task state and any geometry differences explained. Check usable review controls outside the product canvas and their effects inside it. Mark all unverified preset geometry/regions as review assumptions; no invented official dimensions, center hinge, or camera cutout. Separately record text-input/IME focus, keyboard-navigation focus, and assistive-reading focus during reflow, target removal, and overlay dismissal. Passing one focus type does not establish the others. Use VoiceOver or an actually available assistive technology to complete primary tasks and name the browser/platform. Native Full Keyboard Access evidence is separate; DOM or ordinary Tab tests do not establish it. Use available Agent browser tools, existing Playwright, or manual execution; this package does not mandate a renderer. Mark simulated keyboard/safe-area/system-region/service behavior as assumptions rather than native runtime proof.

Record device-shell fidelity, app visual quality and functional results separately. A passing build, selector or quantity of functional tests cannot close a shell or app visual failure. Without a browser, retain HTML source and report browser/visual acceptance pending. Missing pages, broken primary tasks, evident layout faults, unresolved requested real-device matching, or absent visual review prevent a claim that a complete high-quality prototype passed.

## End-to-end Skill evaluation

When evaluating this Skill itself, separate instruction/validator checks from actual Agent behavior and the produced interface:

1. **Freeze inputs and independent expectations.** Use an original or redistribution-cleared multi-page app fixture with representative content, source, original visual/component references, current-layout evidence, and scope constraints. Record fixture/Skill hashes, tools, model configuration, and environment. Before execution, an independent evaluator records known pages, main tasks, important states, applicable named environments, minimal-change boundaries, and expected retained design. Keep its answer checklist separate from the generating Agent's task brief.
2. **Run a fresh Agent.** Supply the Skill, raw fixture, and a realistic user request without inherited conversation or a scripted answer. Allow artifact writes only in the isolated evaluation workspace. Keep input/product files unchanged unless the task explicitly permits edits. Preserve observable tool calls, stage artifacts, builder discovery/read/use, and final results; a statement that a step ran is not evidence that it did.
3. **Audit the process.** Establish that framework identification and whole-app original-design baseline preceded recommendations, and that populated applicability/decisions/planned targets/project conventions plus migration/environment/design inputs were frozen and passed to the selected builder before its first implementation edit. Inspect hashes and timestamps, not only stage labels. Check honest creation/refinement routing, original-design authority, minimal deltas, explicit narrower requests, and that missing native tools did not block independent HTML. Record actual unavailable capabilities, fallbacks, and late gates.
4. **Independently test final output.** Use the frozen page/task/environment checklist against the final artifact. Run browser tasks, physical posture and independent rotation transitions, and continuous resizing in one stateful session; inspect same-state original/adapted screenshots across layout families, significant stress states, large text, low height, and reduced motion. Compare the device shell and scale mapping against its actual reference separately from the original-app comparisons. Verify actual app layout, applicable bar/overlay placement, shared comparison state and state retention independently of review-control labels. Bind screenshots and logs to final resource hashes. Assess baseline coverage, original-design preservation, necessary changes, shell fidelity, functionality, app visual quality and review usability separately, with unresolved calibration/accessibility/native checks visible.
5. **Test the checks, then repair and repeat the affected scope.** Introduce representative known failures in disposable copies, such as a missing page/resource, a dead primary action, discarded draft on pose switch, a label-only pose selector, rotation mislabeled as partial fold, a generic shell claimed as measured hardware, conflated screenshot/CSS dimensions, stale comparison cards, unexplained token/style replacement, a late/empty handoff, stale capture, missing rule, or unrelated project convention. Confirm the applicable automated or independent manual check detects them; do not imply the structural validator detects visual or chronology failures. Retain failing and repaired observations rather than selecting only a successful run. One complete run demonstrates that fixture and environment; broader reliability needs independent repeats and different app/task types.

A ledger validator checks structure and file existence, not whether a screenshot or log proves a particular claim. Independently inspect the linked evidence. A packaging test, synthetic fixture, browser result, and actual native acceptance each support their own declared scope.

## Later product implementation: route by framework

Execute this section only when the user requests product implementation or device acceptance. Use [framework identification](frameworks.md) and the project's own runner. Build a matrix from modes actually supported by the target version rather than guessed device sizes.

- SwiftUI/UIKit: follow [Apple frameworks](apple-frameworks.md) for current-view geometry, four-edge safe areas, keyboard, and custom-interface reserved regions; run Apple App Resizability checks when the export is available.
- React Native: follow [its contract](react-native.md) for live windows, the installed safe-area library, and keyboard handling; folding regions remain unverified without an evidenced native module.
- WebView shells: test both page viewport and native host. Record browser-page and WKWebView-host results separately.
- Flutter: use the following matrix, layered checks, and `integration_test`. That gate applies only to Flutter pages.
- Other frameworks: establish their own layout API evidence before product changes.

## Later Flutter implementation: size and state matrix

Apply only after identifying Flutter and receiving a product/device request. Use the target project's runner and supported modes:

| Scenario | Operation and checks |
| --- | --- |
| Continuous resizing | Same-session narrow → wide → narrow, wide/short, and breakpoint crossings; no overflow, clipping, unreachable actions, or unintended restart |
| Duo outer/inner displays | Simulator folding/unfolding, supported orientations, and partial-fold postures; correct layout, regions, reachability, and content movement |
| Side-by-side/split | Where the target system provides it, exercise actual app-window changes; an iPad/desktop resize is not Duo region evidence |
| Resizing during input | With keyboard, unsaved text, and selection active, resize and continue editing/submitting; no lost text, duplicate inset, or obstruction |
| Navigation and scrolling | Open detail, select an object, scroll, and cross breakpoints in both directions; retain object/route, semantic position, and back path |
| Resizing with overlays | Open menus, dialogs, sheets, or sharing and resize; correct anchors, bounds, dismissal, and continuation |
| Ongoing tasks | Resize during requests, saving, capture, or playback; check duplicate execution, result ownership, progress, and output consistency |
| Accessibility and regression | Independently complete applicable selection, reading, edit/submit, and overlay-close tasks using VoiceOver or Full Keyboard Access alone. Focus has a visible destination after pane/target removal and sensible restoration after dismissal. Reduce Motion and ordinary iPhone/iPad tasks remain usable. |

Mark unavailable or unsupported modes unexecuted/not applicable with reasons. Empty `displayFeatures` does not prove absence of iOS reserved regions; region sources and bridges need independent evidence.

## Later Flutter implementation: layered checks

1. **Static review:** inspect affected call chains, effective configuration, state lifetimes, and new debug-only APIs. Search hits alone do not establish a defect.
2. **Automated regression:** use existing widget tests to exercise metric/constraint changes and state retention within one element session, not just separately launched screenshots. Extend relevant route/edit/task integration coverage. Every new page needs an `integration_test` entering through production navigation/routing, with stable `ValueKey`/`Semantics` identifiers, a page landmark, at least one primary interaction, and its visible result. For display-only pages, check content and back/close. Register it with the existing runner and run on a supported target. A test-only example entrypoint cannot replace the production path.
3. **Runtime evidence:** run narrow checks on a supported target and record commands/results. Use Duo simulators for platform postures and identify state/build in captures. A generic resizable target can test layout but cannot replace platform-region tests.
4. **Production mode and hardware:** record Debug/Profile/Release. Check debug-only API contracts in all three modes and guard access correctly. Device-sensitive changes need a Profile or Release smoke test. Verify the actual iOS hardware flow where camera, rendering, sharing, plugins, or lifecycle differs. Without Duo hardware, report only actual simulator and other-device coverage.

A new Flutter page without its integration test, with a skipped test, or with a failing test remains incomplete. For technical blockage, record the exact cause and obtain the explicit follow-up authority required by project rules before exception delivery. This gate does not require inventing Flutter pages or tests for HTML prototypes.

## Record prototype and product results separately

```text
Requested endpoint and scope:
Source commit; relevant dirty diff/new-file identity or hashes; app version/build when applicable:
UI framework/version, runtime/engine/host, Xcode, linked SDK, OS/device/simulator, build mode:
Builder identity, actual Skill read, handoff artifacts, execution and fallback if any:
Pre-implementation handoff identities/timestamp; first implementation event; any late gate:
Original-design references; retain/adapt/change decisions; same-page/state original/adapted captures:
Named Duo environments, applicability, preset geometry provenance/assumptions; orthogonal stress states:
Device reference/capture identity; exterior/display calibration and units; posture/orientation; CSS mapping/magnification:
Separate shell fidelity, original-app visual quality, functional and review-usability results:
Current view/local sizes, four-edge insets, keyboard/text scale, region source:
Initial task state → size/posture operation → expected state → actual state:
Commands/exit results, screenshots/recordings/log paths:
General/project rule IDs; Apple guidance/framework contract/engineering boundary/project choice and source:
Passed/failed/unexecuted/unknown capabilities and next action:
```

HTML results use the browser, container sizes, page coverage, task steps, and captures. Framework/build/device fields apply only to actual product implementation. A check supports only what it executed. Plans are not observations, and Skill packaging is not prototype or product acceptance.
