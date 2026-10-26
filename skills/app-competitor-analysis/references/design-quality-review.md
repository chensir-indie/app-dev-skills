# Design quality: one system, concrete findings, rendered proof

Use this when delivering visual reports or repairing weak presentation. It supplements the [visual report contract](report-design.md) and [Apple-guided usability baseline](apple-web-design.md); it does not replace evidence analysis with styling. Review the competitor's interface and the authored report as separate surfaces: the former is evidence to explain, the latter is a page we can repair.

## Choose authority before choosing style

Preserve the user's design direction and existing project system. Select one primary design system for the surface, then use other references to answer specific questions. Do not combine several component languages because they are available.

| Surface | Primary reference | Useful supplementary lens |
| --- | --- | --- |
| This skill's HTML reports | [visual report contract](report-design.md), or the user's selected direction | Web semantics, keyboard behavior and WCAG criteria; no native Apple certification |
| iOS/macOS competitor | [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/) | The observed product's own conventions and accessibility evidence |
| Android competitor | [Material 3](https://m3.material.io/) | Platform conventions; do not assume a Flutter app uses Material defaults |
| Dense enterprise product | Its actual design system; [Carbon](https://carbondesignsystem.com/) or [Ant Design](https://ant.design/docs/spec/introduce-cn/) when relevant | Task density, grids, table hierarchy and state clarity |
| Web interaction/accessibility | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines/blob/main/command.md) as implementation heuristics |

Read the relevant official section before attributing a requirement or claiming current conformance. A screenshot can reveal hierarchy and crowding, but cannot prove hit regions, keyboard access or text scaling. State the scope rather than assigning a compliance score.

External design skills are aids, not authorities over the user. [Impeccable](https://github.com/pbakaus/impeccable) supplies useful critique, typesetting, layout, polish and hardening vocabulary. [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) can help explore options when an appropriate installed capability is available. Their style recommendations remain proposals. For example, a font suggestion must not override this report's chosen local display/body pairing; a suggested glass theme must not replace its opaque reading surfaces.

Do not make installation, another skill, paid material or a remote service a prerequisite. Use available tools or perform the review directly. [Refactoring UI](https://www.refactoringui.com/) can supply optional explanatory examples from publicly available material; do not require purchasing or accessing its paid content.

## Establish the report's working design contract

For a report set, record the following once in its existing project notes or delivery record. Reuse the contract across products, allowing evidence density to change the composition.

- Reader and task: understand this product, inspect its mechanism, compare a consequential choice.
- Primary system and sources: distinguish official principles from this project's CSS choices.
- Type, space, color and density: use the shared tokens; identify any justified override.
- Components and states: navigation, four-map switcher, node inspector, source disclosure, search/results, evidence imagery.
- Composition: opening finding and explanatory image/map; concrete mechanism before research metadata; detailed evidence progressively disclosed.
- Validation scope: representative dense, image-based and sparse reports plus the index; actual final files, viewports and states.

This is a small implementation contract, not another specification to write instead of repairing the page. Inspect the existing source and rendered result first. Preserve useful work and change the shared cause when several reports have the same defect.

Check the opening against the revised analysis: title, category, core-task strip, index card and default map must describe the same product. A rewritten chapter does not repair a stale opening that still omits its main task. For example, a photography business workflow must not retain a pose-library-only task strip after client documents and delivery have been established.

## Review in the order that changes the result

These are review lenses, not commands that must all run for every small edit. On a full or rejected delivery, examine the affected lenses and repair substantive defects before final polish.

| Lens | Inspect in the actual page | Actionable outcome |
| --- | --- | --- |
| **Critique** | Can the reader identify the product, task and distinctive finding? Does the strongest evidence support the headline? Can they find all four maps? | Name the blocking comprehension problem and affected region; strengthen the argument or reading order before decoration |
| **Typeset** | Chinese/Latin mixing, paragraph measure, heading rhythm, long names/versions/URLs, caption and source legibility | Repair semantic type roles, wrapping and spacing; do not shrink all text to fit a dense page |
| **Layout** | Evidence at usable scale, image/observation proximity, repeated containers, excessive empty bands, graph connectors and information density | Group by meaning, enlarge the relevant source region truthfully, and give diagrams internal space without widening the document |
| **Harden** | Long text, no image, zero search results, narrow widths, unavailable external links, offline/no-script, keyboard/focus and print | Preserve the task and source context in these states; keep unavailable evidence explicit instead of adding fictional UI |
| **Polish** | Token consistency, alignment, repeated labels, icon meaning, selected/hover/focus states and source controls | Fix shared component inconsistencies after structure and content work |
| **Audit** | Semantic HTML, image sizing, accessible controls, reduced motion and state announcements in the relevant code | Link a real defect to its source and retest the affected rendered behavior |

Do not treat a list of passes as proof that they were performed. A useful finding connects **location → visible defect → reader/task impact → repair → retest evidence**. Avoid taste-only findings such as “not premium enough.”

Examples: “The scene-reference control is unreadable because the full desktop capture is displayed at phone-thumbnail width; show the documented app region and retain the full source.” “Two feature nodes repeat the same capability under different names; consolidate them when their contracts match, but preserve a real version difference.” “The inspector opens, then an old hash scrolls away from its node; respect the handled click and verify that focus/context remain.”

Treat citations as part of reading design: attach the actual supporting source to its finding instead of repeating a chapter-wide source dump after every paragraph. Keep useful locators in the source record and a working return path. Do not remove necessary qualifications or citations merely to make a cleaner screenshot.

## Edit the reading copy

Give each finding one primary home. Write what the competitor does in direct language, then explain its consequence; challenge only an interpretation that matters to the decision. A chain of invented misconceptions followed by corrections makes the reader do unnecessary work.

Author a short headline and purpose for the opening, a distinct finding for the overview, and a concrete action for the decision. These have different jobs. Merge exact duplicates and repeated process notes; keep a material limitation beside the claim it limits. Store exhaustive acquisition history once. Repeated statements of unavailable runtime data can become one clear scope statement plus the affected specific uncertainty.

Use the renderer's product `brief` and section `summary_blocks` for the reading layer. Keep unique causal reasoning, counterevidence and the full protocol in `blocks`, behind a descriptive disclosure. An automatic truncation cannot make that editorial choice. Preserve complete feature/route inventories and source references; a shorter reading page still needs to explain the mechanism.

Review the [diagram grammar and chapter composition](diagram-design.md) as part of the same page. Give capabilities a visible role, put technology beside its actual inputs/outputs, and keep full maps in the reading path. Folding prose does not fix a wall of labels, disconnected explanations or misleading connectors.

Let imagery do useful work: use an inspected source at a readable scale, obtain a better official rendition when the existing image is too small, and retain its original. Show the same image again only when the second view adds information. For sources, group a short argument's references in a compact disclosure rather than a repeated row of prominent buttons. Mobile steps should read as steps; a long table does not automatically need every column header repeated above every cell.

Compare the actual old/new reading experience. Check whether the opening explains the app, the finding fits a short paragraph, and the reader can reach complete reasoning without losing context. Measure text/height changes as descriptive evidence only; fewer characters alone do not prove better analysis or design.

## Apply web rules proportionately

Use semantic actions and navigation, persistent form labels, visible focus, meaningful image alternatives, understandable status and reduced motion. Fix overflow at its cause; hiding page-wide overflow must not clip diagrams or source metadata. Native gestures and web controls have different evidence requirements.

Do not import a framework-specific checklist wholesale. A standalone offline report does not need React hydration work, remote font preload, CDN preconnect, an animated hero or list virtualization merely because a web checklist mentions them. Browser back/forward, link opening and keyboard alternatives should keep their normal meaning.

Keep numeric standards distinct: WCAG 2.2 target-size minimum (2.5.8) is 24 CSS pixels with stated exceptions; this report chooses 44×44 CSS pixels for standalone controls. Neither is a conversion from Apple's native points. Assess the relevant criterion and actual scope before claiming accessibility conformance.

## Close the review against final artifacts

Use [completion checks](apple-web-design.md#completion-checks) for the browser matrix, zoom, keyboard, reduced motion, print and offline states. Record the methods actually exercised. A narrowed viewport is not a browser-zoom test; a screenshot file is not evidence it was inspected.

Keep a concise review receipt in the report project: file/hash and region, checked lens, original finding, implemented correction, final screenshot/state, remaining limitation. If a route cannot be exercised, retain the precise pending check. Distinguish design review, structural checks, source verification and competitor runtime validation. Do not infer analytical depth, aesthetic approval or WCAG certification from a detector count.

The source links and workflow vocabulary above were reviewed on 2026-10-21. Impeccable and UI/UX Pro Max are reference projects, not bundled dependencies or commands claimed to have run. Refresh a source when its exact rule is needed; keep third-party manuals and report-specific artifacts out of this skill package.
