# Present the actual Duo device and the original app

Read during stage 1 when collecting device references, freeze its decisions in the stage-2 handoff, and apply it during HTML construction and rendered review. This is a prototype-presentation contract. It adds no official hardware dimensions and does not establish native or physical-device acceptance.

## Establish the device reference before drawing the shell

Use the supplied Device Hub or simulator reference as the presentation target when the user provides one. Inspect the actual image or running surface rather than inferring its appearance from a filename or preset label. Where available, collect the corresponding Device Hub/simulator captures, exported screen images and runtime geometry; use current official device imagery or specifications for facts they actually establish. Record conflicts and the selected target instead of blending different devices or tool versions.

Capture or inspect each required physical posture and orientation. A single front view cannot establish the unseen back, side, hinge, inner display, or partial-fold perspective. Continue independent app/layout work while attempting to acquire missing views; keep the unsupported parts of the shell and their visual acceptance explicitly pending. Do not fill those gaps with a generic phone frame and describe it as the real iPhone Duo.

Keep a compact calibration record linked from the environment matrix:

| Record | Required evidence and boundary |
| --- | --- |
| Source identity | User reference or official URL; image/file identity and hash; capture date, tool/device/runtime identity and selected posture/orientation when known |
| Exterior | Observed silhouette, aspect ratio, body/bezel thickness, display placement, corner curvature, finish/skin, edge treatment, buttons, and visible cutouts; record what is hidden or unknown |
| Display and app | Display raster size, logical display/window/app bounds, display scale, safe areas and reserved regions, each with coordinate space, units and independent provenance |
| Capture transform | Screenshot raster dimensions, device/display crop, Device Hub/simulator UI zoom, host display scaling and perspective transform where established; unknown factors remain unknown |
| Browser mapping | Logical app bounds represented in CSS pixels, shell coordinate system, display aperture/mask, rotation, preview magnification and any projection; explain each conversion |
| Verification | Source-versus-rendered shell comparisons and measured landmarks, actual app-container bounds, matching page/state captures, differences, and unresolved evidence |

Separate **screenshot pixels, host UI scale, logical points, native display scale, CSS pixels, browser device-pixel ratio, and preview magnification**. They are different quantities. Do not infer a logical viewport or physical millimeter dimension from a scaled screenshot alone. Where the source establishes raster size, logical bounds and display scale, reconcile them; never assume a scale merely because a familiar device uses it. A 1 CSS-pixel-to-1-logical-point prototype mapping is a declared modeling choice, not a native runtime fact. The browser's device-pixel ratio does not establish the target device's display scale.

Measure the exterior and display aperture separately. Preserve the supplied reference's observable proportions even when its logical viewport is still unknown; call the result a reference-matched visual with unverified logical geometry. Keep profile values beside their source and uncertainty. Do not hardcode guessed official dimensions, corner radii, a center gap, crease, camera opening, button location, or folding angle into a reusable device profile.

## Keep physical posture, orientation, and app-window layout separate

When reproducing a Device Hub reference with **Closed**, **PartiallyOpen**, and **Open** controls, provide those three physical posture states. Preserve the source labels where they identify the tool's states. A rotation button changes orientation independently; selecting landscape does not substitute for PartiallyOpen. The partially open state must reflect the observed body/display arrangement and active usable area rather than merely changing a label, width, or decorative hinge line. If only its control is visible in the reference, its geometry is unverified until captured.

Derive the actual main review views from the user's scope and captured/calibrated configurations. Outer portrait, inner portrait and inner landscape can be three primary views when those are the requested and supported views; they are not three official device sizes. Bind each to the physical posture, display, orientation and app-window bounds it represents. Record additional applicable partial-fold and side-by-side configurations in the [migration matrix](migration-review.md), with unsupported or unknown combinations explicit.

Keep posture, orientation, display selection and app-window placement as separate state dimensions even if a convenient named-view button changes several together. Derive geometry from the selected calibrated profile and the live app container. A side-by-side window is not a new physical device, and a keyboard or large-text setting is a stress state rather than a fold state.

## Make the device and application the primary review surface

Lead with a large active device preview and compact comparison cards for the required main views. Show the current page/task state consistently across them; selecting a card changes the active view of the same app session. Editable comparison views must share the underlying app state; captured cards must identify their page/state and refresh or be marked stale when that state changes. Preserve route, selected item, draft, reading anchor, overlays and modeled task progress across posture and rotation controls.

Keep the active shell and app readable at the reviewer's available window size. Apply preview magnification to the composed shell and display together, separately from the app's logical layout dimensions. For a partial-fold projection, retain an operable display surface and distinguish its local app coordinates from the projected presentation. A perspective illustration alone does not demonstrate app adaptation.

Keep posture/view controls concise and outside the app canvas. Put coordinates, raw dimensions, calibration details, stress controls, rule/evidence tables and diagnostic output in a collapsed secondary inspector. A short uncertainty indicator may remain visible; its evidence belongs in the inspector. The prototype's opening view should present the device and the app, rather than a large debugging dashboard or implementation narrative.

The device exterior is a wrapper around the original application. Reproduce its observed shell without changing the app's visual language: retain original typography, colors, components, icons, density, copy and page relationships. Only recorded adaptation deltas may change the product. A realistic shell cannot compensate for an app redesign or missing pages.

## Review shell fidelity and app quality independently

Inspect final browser screenshots against the identified device reference and the original app references. Record separate results for:

- **Device presentation:** exterior proportions, display aperture and placement, corner masks, skin/finish, visible buttons/cutouts, each physical posture and orientation, and the source-to-browser scale mapping. Compare matched crops or aligned landmarks; preserve gaps where the source cannot establish a fact.
- **Original-app fidelity and adaptation:** same page/content/task state, retained design and justified deltas, typography, spacing, density, component consistency, readable content, reachability, and the actual app-container geometry in every required view.
- **Interaction and continuity:** real navigation/task outcomes, posture and independent rotation controls, shared state and comparison freshness, and relevant stress states.
- **Review usability:** a clear active device, readable comparison cards, unobstructed app interaction, and working secondary inspector controls.

Use actual rendered evidence at a useful inspection size, including full-size shell crops where needed. Repair material shell and app defects separately and recapture affected views. Functional test counts, a working selector, a successful build, or a visually plausible silhouette cannot pass the device or app visual gates. If real exterior/dimension matching was requested, unresolved calibration or shell fidelity remains a specific open acceptance item; do not report an illustrative frame as completed real-device matching. HTML evidence remains separate from native simulator behavior and hardware acceptance.
