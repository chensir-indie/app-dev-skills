# UI style: from pixels to a design explanation

Apply [analysis-depth.md](analysis-depth.md) to turn regional observations into task mechanisms, bounded causal hypotheses and product decisions. A color/type inventory alone does not satisfy a detailed UI analysis.

Use [design-quality-review.md](design-quality-review.md#choose-authority-before-choosing-style) to select the relevant platform/system lens. Explain the competitor's actual choices before judging them against a convention. Keep a screenshot-supported finding separate from a runtime accessibility claim; our HTML report's Apple-guided presentation is not evidence that every competitor should resemble Apple.

## Establish what the image is

Inspect the actual image. Record native dimensions, crop/scale, light/dark theme, locale, page/state and whether it is an app capture, promotional mockup or concept. Separate the app viewport from phone frames, headings and marketing decorations. If only promotional images exist, limit findings to the depicted state.

When the image's official attribution comes only from the user's description or a supplied metadata file, retain that provenance separately from the pixels you inspected. Missing attribution verification does not erase visible UI evidence, and viewing pixels does not verify attribution.

Use regions or an annotated contact sheet to connect claims to visible elements. Keep originals immutable. Crops and annotations are derivative evidence with their own provenance. Exact measurement is useful for a concrete layout question, not a requirement to extract every pixel.

## Inspect the system, not just adjectives

| Dimension | Questions that produce useful findings |
|---|---|
| Hierarchy | What attracts attention first? What is the primary action? Are navigation, content and status distinguishable? |
| Typography | Which semantic roles differ by size/weight/line length? How does dense or localized text behave in the shown state? |
| Color | What roles do base surfaces, accents, selection, warning and disabled treatments play? Is brand color competing with content? |
| Geometry | What alignments, spacing rhythm, component proportions, corners and margins recur? Does the layout protect the user's working area? |
| Layering | Which elements cover content? What separates modal, sheet, toolbar and background? Is the active task obvious? |
| Components | What stays stable across pages/states? How are selection, loading and errors represented where shown? |
| Imagery | Does photography, illustration or diagram teach, inspire, identify or decorate? What information is lost in a simplified thumbnail? |
| Information architecture | Where do browsing, creating, editing and reviewing live? Are labels about user goals or internal implementation? |
| Motion | If a recording exists: what changes, persists, enters/exits, and signals completion? A still cannot answer this. |
| Accessibility | Visible contrast/legibility, color-only signals and text crowding; touch targets, semantics and text scaling need appropriate runtime evidence. |

Describe `visible pattern → role in the task → benefit/cost → transferable principle`. Example: “The selected image retains a persistent accent border while secondary actions are neutral; this keeps the editing target identifiable.” This is more actionable than “premium, clean, modern”.

## Measurement discipline

- Identify screenshot pixels versus logical layout units. Do not turn an image width into an exact iOS point or Android dp value without scale evidence.
- Color sampling is a rendered approximation affected by gradients, antialiasing and compression. Use ranges/roles unless exact values matter.
- Font appearance supports “sans serif, heavy heading” or a candidate family; actual font identity needs assets/code or official specification.
- Distinguish visible icon size, component bounds and interactive hit region.
- A multi-phone composite can support hierarchy and sequence depicted by the publisher; it usually cannot support exact native typography or animation timing.
- When no pixels are available, write a visual evidence gap and continue the interaction/technology work. Never substitute a generated reconstruction for competitor evidence.

## Deliverable

For detailed analysis, follow [design-specification.md](design-specification.md) and deliver an individual `Design.md` alongside the HTML. The record covers every distinguishable element in the inspected states and keeps unsupported dimensions explicit.

For a detailed UI pass, provide representative regions/states, a role-based style table, recurring component rules, concrete friction hypotheses, and the observations needed to validate them. For each important region explain what it prioritizes or defers, which neighboring elements compete for attention, and the consequence for the task. Relate visual rules to the state and object being manipulated. If the evidence cannot establish cross-state consistency, say so. Avoid inferring “easy to use” from attractive screenshots alone.
