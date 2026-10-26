# Apple-guided report design

Use this as the interaction, readability and verification baseline when changing HTML presentation. The current reader composition and authored visual tokens live in [report-design.md](report-design.md); an explicit user direction takes precedence. Apply the chosen system through shared styles and inspect the actual output. A style name alone does not satisfy rendered review.

For choosing supplementary standards, reviewing weak pages and recording repairs, use [design-quality-review.md](design-quality-review.md). Keep the chosen report-design contract primary for composition; use these platform-derived principles and supplementary reviews for scoped checks.

## Authority and scope

Apple's Human Interface Guidelines describe Apple platform experiences. The principles below inform this skill's web reports; the CSS sizes, palette, spacing and browser checks are **our web implementation choices**, not an official Apple website specification, native component implementation or certification. Native points and CSS pixels are different units. A system font stack does not implement Dynamic Type or automatically inherit native semantic colors.

Official guidance reviewed on 2026-10-20:

| Source | Principle applied here |
| --- | --- |
| [Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles) | Consistent structure, recognizable interactions, clear feedback and preserved context |
| [Layout](https://developer.apple.com/design/human-interface-guidelines/layout) | Group related content, align elements and give essential information appropriate space |
| [Typography](https://developer.apple.com/design/human-interface-guidelines/typography) | Establish a readable type hierarchy, limit typefaces and adapt layout as text grows |
| [Color](https://developer.apple.com/design/human-interface-guidelines/color) | Use colors consistently by role; communicate meaning through labels as well as color |
| [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) | Support larger text, sufficient contrast, perceptible states and different input methods |
| [Materials](https://developer.apple.com/design/human-interface-guidelines/materials) | Keep navigation distinguishable from content; avoid applying Liquid Glass throughout the content layer |
| [Motion](https://developer.apple.com/design/human-interface-guidelines/motion) | Use purposeful, optional motion that does not obstruct frequent interactions |

Recheck the relevant official page when changing a source-dependent requirement or claiming current Apple guidance. Record which principles and implementation checks were applied; do not invent a compliance score or describe a browser report as a native Apple interface.

## Reading structure

The main experience is understanding a product. The opening presents its identity, primary task, defining finding and an inspected image or concise task map. One clear reading path leads into visual evidence, mechanisms and recommendations. Metadata supports this path; large status dashboards, long contents lists and acquisition logs must not occupy the opening instead.

For an authored editorial reading layer, apply [reading-copy review](design-quality-review.md#edit-the-reading-copy). The display title may use the upper end of the type scale; keep mechanism text and sources restrained and readable.

Use a stable section hierarchy and generous separation between chapters. Group related observations with proximity and alignment before adding a card, border or background. Use bordered surfaces for interactive maps, evidence groups or a genuine change of context; avoid wrapping every paragraph in the same card. Keep concise conclusions and material limitations visible, with descriptive disclosures for extended sources and acquisition records.

Desktop may place concise navigation beside the report. Phone layouts put the title and useful evidence early, then keep navigation compact and discoverable. Preserve the reading order when columns stack. The index prioritizes product identity, task, a specific finding and a meaningful preview; its search and filters help choose a report.

## Web tokens and typography

The following neutral Apple-guided palette/type scale is a reference implementation at a 16px browser root size. The current visual-report display, color and density roles are specified in report-design.md; preserve readable evidence when adapting those roles. HTML text uses relative font units and permits the browser root size to change; never disable zoom. Keep the same hierarchy across the report, index, diagrams and inspector.

| Role | Default |
| --- | --- |
| Font family | `-apple-system, BlinkMacSystemFont, system-ui, "Segoe UI", sans-serif`; use installed language fallbacks |
| Report title | Responsive 32–72px, semibold, compact but unclipped line height |
| Section heading | 24–32px, semibold; nested headings remain visibly subordinate |
| Main prose | 17px (`1.0625rem`), regular, line height about 1.65; adjust for the language |
| Supporting text / controls | 15px (`0.9375rem`), regular or medium |
| Captions / provenance / map status | At least 13px (`0.8125rem`) at the normal reading scale |
| Prose measure | Approximately 60–75 Latin characters; review Chinese and mixed-language line lengths visually |
| Spacing | Use a restrained 4/8px-derived rhythm; 16–24px within groups, 32–64px between major groups as space permits |
| Surfaces | White `#ffffff` and neutral background `#f5f5f7` |
| Main / secondary text | `#1d1d1f` / `#6e6e73`, with actual foreground/background contrast checked |
| Interactive accent | `#0066cc`; reserve it for interaction and meaningful selection |

Use regular, medium and semibold weights; tiny uppercase labels, thin text and excessive tracking do not create useful hierarchy. Captions and evidence controls remain readable on phones instead of shrinking to fit. Print may use its own readable type scale, checked in the actual print rendering.

The relationship diagrams use fixed SVG coordinates, with 16px node labels and 13px captions/status/edge text at their default reading scale. Card height reserves the actual label and caption lines. Enlarging these fonts independently would break node and connector geometry. Diagram zoom and browser zoom enlarge the whole drawing; the equivalent HTML node-and-edge index uses relative units and responds to root text enlargement. A root-font enlargement check does not prove that SVG labels enlarged. Test and report these routes separately.

Keep colors in semantic tokens shared by report and atlas styles. The hex values above are a web palette, not copies of native dynamic color APIs. Measure every rendered state: normal text needs at least 4.5:1 contrast, and meaningful control boundaries, focus indicators and diagram connectors need at least 3:1 against adjacent colors. Decorative separators need not compete with content. Status color always has a textual or shape-based equivalent; “unknown” must remain clear in grayscale and print.

The default report uses opaque reading surfaces. Do not add glass, blur, gradients or floating translucent cards merely to resemble a platform screenshot. If a user requests another appearance, preserve readable content and test its color combinations separately. Do not claim dark-mode support without implementing and inspecting it.

Use system fonts available on the reader's device; do not bundle downloaded SF fonts, Apple logos or platform artwork to manufacture authenticity. Product evidence remains attributed evidence, distinct from the report's own interface.

## Components and interaction

| Component | Required behavior |
| --- | --- |
| Navigation | Clear current location, meaningful link labels, keyboard access and visible focus; destination headings remain visible below any sticky controls |
| Search / filters | Persistent labels, visible results count or empty state, operable controls and no hidden inventory loss |
| Map navigation | Four discoverable destinations beside their explanation; compatible tab layouts name their selected view and preserve report context |
| Diagram | Readable default scale; large graphs scroll inside a labeled region and provide zoom/reset/fit controls plus equivalent node-and-edge text |
| Node inspector | Concise meaning, evidence status and source links; keyboard activation works, closing with Escape returns focus to its trigger |
| Disclosure | Its summary names the hidden material and relevant uncertainty; native keyboard behavior and visible expanded state |
| Sources | Inspectable provenance beside claims, useful link text and a return path to the reading context |

Standalone controls—including navigation items, map buttons, close buttons and source chips—have a target at least **44 × 44 CSS pixels**, using padding rather than oversized icons. This is this skill's touch-usability target, not a conversion of Apple's native point measurements. Inline prose links retain normal text flow, clear styling and comfortable separation from other links; a tiny isolated superscript is not an adequate source control.

Use semantic HTML before custom roles. Labels must explain symbol-only controls; focus must remain visible, including on graph nodes. Do not use color alone for current location or selection. Avoid moving focus unexpectedly during filtering or scrolling. Respect `prefers-reduced-motion`; animation must not be needed to understand a state change or finish before the reader can act.

## Images and complete maps

Display real inspected UI at a useful reading size, preserve aspect ratio, identify the source/state and retain access to its full context. An accurate display window can remove irrelevant capture margins; it cannot remove a meaningful qualifier without retaining that context elsewhere. Pair imagery with a few concrete, region-specific observations instead of surrounding it with repetitive prose.

All four maps remain complete and distinct: feature hierarchy, core task, screen relationships and technical data flow. Use concise node labels, clear directional connectors, visible branches and return paths. Give unknown edges their own labels. Keep node detail and sources outside the diagram's main reading path.

Use the [diagram composition rules](diagram-design.md) to connect these maps to adjacent evidence and explanations. Full maps remain visible in the authored reading layout; their sources and exhaustive research can use disclosure. Feature roles, graph captions, source controls and UI-image observations share the report's hierarchy.

Do not automatically shrink a graph until its text becomes unreadable. Let the reader pan, zoom or choose fit explicitly; provide an accessible textual equivalent with the same nodes, conditions and edges. On narrow screens, the graph region may scroll, while the document itself stays within the viewport. Without scripts and in print, all four maps and their evidence remain available.

## Completion checks

Review representative dense, image-based and sparse **final reports**, plus the index. Use these widths as practical web test cases, not as an Apple device certification matrix:

1. **1440px desktop:** opening hierarchy, readable imagery, restrained surfaces, aligned navigation and clear diagrams.
2. **390px and 320px phone widths:** useful reading order, readable captions, usable targets, no page-wide horizontal overflow, internal scrolling for genuinely wide content.
3. **200% text enlargement and browser zoom:** preserve HTML content, focus and interaction with wrapping/reflow instead of clipped labels or fixed-height text containers. Check whole-diagram enlargement through browser/diagram zoom and check the equivalent HTML index under text enlargement. Record each method actually exercised; neither changing the root font nor narrowing the viewport alone proves browser zoom behavior.
4. **Keyboard and reduced motion:** navigation, switcher, nodes, sources, disclosure, inspector close/focus return and search remain usable; essential information is available without animation.
5. **Print and offline/no-script:** complete chapters, all maps, provenance and useful disclosures remain legible; printing restores the prior on-screen disclosure state.

Record the report IDs, viewports, browser, checked states and observed defects. Fix actual failures before claiming the affected check passed. Automated style/geometry checks and synthetic fixtures provide regressions; they do not establish that a real report is visually clear or that its research is complete. If a browser route is unavailable, retain the outputs and state the unperformed checks without bypassing access restrictions.

For navigation, test cold deep links after image decode, rapid chapter changes, enlarged-header offsets, active-directory state and source/back restoration. Test leaving an open node inspector as well as opening it. For performance, record real-file payload, image dimensions and the same timed interaction before/after; use the [navigation and performance procedure](html-delivery.md#navigation-and-performance). Smooth motion and absence of overflow are not evidence of fast response.
