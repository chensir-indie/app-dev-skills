# Report design: visual product studies

Read before rendering a collection or repairing rejected presentation. The reader should recognize the product, inspect its evidence, read its main task and understand its technical limits before opening the full research record. Treat the cover, evidence spread, diagrams and collection shelf as one composition.

## Inspect concrete references

Preserve the user's direction. Open the actual current report and specific reference pages; record the section, URL, capture date and layout mechanism. A repository, brand name or style adjective alone cannot define a redesign. Community analyses such as [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) help locate references; they are third-party interpretations, not official design specifications. Compare them with the actual page when accessible. Keep any inaccessible live-page check pending.

The implemented composition was tested against these concrete pages. Reinspect when relying on their current geometry; use another reference when it better fits the task.

| Page / section | Useful mechanism | Adaptation to research |
| --- | --- | --- |
| [Runway homepage](https://runway.com/) | A dominant visual and short argument establish the first focal point | Give actual product evidence most of the opening's visual area; keep identity, task and finding distinct |
| [Oura homepage](https://ouraring.com/), product hero and interface sequence | Intentional image/text proportion; several related images make one visual statement | Pair an inspected image with the observation it supports; use real material from distinct categories in the collection cover |
| [Linear Plan](https://linear.app/plan), milestones/dependencies and prediction | Relationships are the main picture; headings and captions explain rather than crowd it | Put the selected task or technical chain before long analysis; distinguish primary path, supporting objects and limits |

Borrow composition, not brand assets, marketing claims, measurement results or internal technical facts. A promotional image remains promotional evidence. Keep reference screenshots and product-specific conclusions in the report project, outside the reusable Skill. [Apple-guided usability](apple-web-design.md) remains the baseline for readable controls, focus, native navigation, responsive behavior and print; the report's typefaces and colors are authored choices.

## Compare reference, old and new

When the user asks for a reference comparison or rejects the visual direction, deliver a project-local `design-review.html` beside the reports. Show actual reference / old report / new report captures together at matched report viewport sizes. Cover every requested surface, normally the opening, image/text spread, collection hierarchy, capabilities, task and technology. Each comparison records the borrowed mechanism, original defect, structural correction and evidence boundary, with direct links to the source page and complete new report. Keep original-sized captures inspectable. Make the comparison itself responsive, local and lazy-loaded; use neither live iframes nor hidden loads of the collection.

Review macro composition before color and type: image versus prose area, dominant focal point, reading width, sequence, grouping and graph meaning. Measure actual visible image content when claiming a size change; a larger padded frame is not a larger image. Scope measurements to the checked sample. A screenshot's existence or a test count does not establish that the design was inspected or approved.

## One system, implemented once

`scripts/reader_shell.py` owns the product reader frame and seven URL-addressable content views. `assets/reader.css` owns shell geometry, product navigation, the view bar, collection frame and responsive/print layout; its `reader-*` / `app-*` vocabulary avoids dependence on legacy document layout. `assets/reader.js` owns visible-view state and the continuous-reading option. `assets/report.js` owns anchors, browser history, source/inspector restoration and diagram controls, calling the reader API before measuring or restoring hidden content. `scripts/design_spec.py` validates authored element/rule/component/UX records, exports per-product Design.md and renders its UI/UX reading panels. `assets/design-spec.css` owns those panels. `scripts/render_reports.py` renders authored research components and passes them to the frame. `assets/editorial.css` owns evidence and diagram composition; `assets/report.css` supplies semantic base components and `assets/atlas.css` graph geometry. `scripts/semantic_atlas.py` renders diagram meaning; `scripts/visual_composition.py` renders bounded excerpts and responsibility glyphs. Repair shared causes and replace obsolete rules rather than appending another theme. Index, reports and supporting pages must resolve to the same current stylesheet hash.

| Role | Default | Purpose |
| --- | --- | --- |
| Surface / ink | Warm neutral `#f6f5f0`, dark `#232a27`, secondary `#626b65` | Quiet navigation and readable evidence |
| Action / selected state | `#28664f`, pale `#edf3ed` | One action language across reader and diagrams |
| Uncertainty | Written state, dashes and restrained warning color | Certainty remains independent of prominence |
| Type | System sans body; local Georgia/Songti display; mono indices | Distinct argument, body and provenance without font downloads |
| Type hierarchy | Product identity about 24px, authored opening claim 36–48px, sections 22–24px, body 15–16px | Emphasize the product's defining experience rather than an oversized name alone |
| Containment | Broad evidence surfaces, original module containers, plain leaf lists | Each region expresses a relationship; controls remain compact |

## Page composition

- **Desktop:** a searchable left product library, broad content workspace and sticky view bar: Overview, Capabilities, Interface, Interaction, Technology, Decisions and Sources. Each view is an addressable content surface, with its complete relevant diagrams and evidence. The continuous-reading link reveals the whole report. Native anchors, not simulated tab buttons, own the URL; only one view is laid out in focused reading. Product and view selections have independent current states.
- **Phone:** a native product chooser, horizontally scrollable view navigation, full available content width and reflowed diagrams. Search, clear/empty state, Escape, focus and browser back retain their normal meaning.
- **Opening with imagery:** place the authored task/argument beside a generous real-evidence stage. Large covers use bounded reading previews, not small catalog thumbnails. An adjacent excerpt may show the first actual connected task stages and their edge labels. Qualify promotional framing and unobserved behavior.
- **Opening without imagery:** show a clearly labeled task excerpt from the authored `journey.focus.path`, or an authored capability extract when no path exists. State excerpt/total stage count. Preserve evidence states and actual directed edges; the drawing is not an app screenshot or proof of a complete loop.
- **Evidence spreads:** pair each image with observations that it can support. A single short observation uses a deliberate image/short-comment composition; several observations use a wider text column. Reflow based on material density, preserving every qualification and source. Avoid leaving a large empty column or adding generic observations to fill it.
- **Collection:** use a few existing inspected images from distinct categories as one cover composition. Keep each linked identity visible. Below it, two large-screen report columns put image/task excerpt before identity and task; phones use one. A category or image choice is not a ranking.
- **Research:** keep complete analysis and protocols reachable under descriptive disclosures; a qualification that changes the conclusion stays with the affected claim. Retain independently inspectable original images. Each crop/preview must match its documented source and aspect.

## Diagram composition

Read [diagram-design.md](diagram-design.md) for data contracts and evidence semantics. All four complete maps stay outside research disclosures, with node details, relationship indexes and sources preserved.

- **Capabilities:** original modules are containers within authored task tiers. Repeat a module heading once per tier, then show every original atomic capability and its status. Give the task-critical region more width than support; place extensions below. A node-count distribution may help orient the reader, but explicitly measures collected nodes rather than importance, usage or market coverage. Group modules by identity/index, not equal display labels.
- **Task:** lead with large numbered actions and an actual directed spine. Edge labels name the transfer or condition; missing evidence stays dashed and labeled. Keep branches, returns and disconnected routes explicit. Phones use the same order vertically.
- **Technology:** lead with the selected input/transform/control/state/output path using responsibility glyphs. Put its specific evidence boundary beside a short chain; use full width for a longer chain and place the boundary below. Preserve the complete dependency drawing beneath it. Glyphs encode responsibility, never inferred deployment, vendor or framework.
- **Screens:** retain observed surfaces, containment, navigation wording, disconnected groups and provenance. Keep screen chrome different from processors; put relationship/zoom controls by the drawing.

Surface changes, scale, alignment and sequence express meaning together. Reduced prose alone cannot replace a readable functional or technical model.

## Render, inspect, repair, apply to the set

Review an image-based report, a sparse report, a dense capability landscape, a long technical chain, the collection and the comparison page at desktop and phone widths. Inspect the opening and each diagram separately. Repair clipped long chains, wrong crops, tiny evidence, repeated module names, competing labels, blank columns and stale CSS before rebuilding the full requested set.

Then verify every report's identity/current marker, native product switch, four map links, all original nodes/edges/statuses, sources, image decode and document overflow. Exercise all seven view links, direct map/source deep links, continuous reading, product switching at the same view, browser back/forward, source/back and node/Escape focus behavior. Hidden-view content must be revealed before anchor measurement, history restoration or node inspection. Without JavaScript, all research stays readable; print must reveal every view. Save the current view with the existing scroll/inspector state rather than creating a second history owner. Test enlarged text, reduced motion and print. Keep the independent local-file model: no framework, full-collection preload, canvas engine, remote font or animation is required.

For performance complaints, use [navigation/performance checks](html-delivery.md#navigation-and-performance). Record exact final file hashes, browser, viewport, measured operation and untested conditions. Layout checks do not establish Safari scroll smoothness. Save captures and the review receipt with the report project; distinguish rendered review, structural integrity, analytical depth, source truth and competitor runtime evidence.

## Main-area copy budget

Apply [the design specification reading hierarchy](design-specification.md#reading-hierarchy). Keep identity once in the view bar, chapter titles without decorative indices, and a concise report footer. Design-document access belongs in the interface heading. A capability count distribution is not a finding about usage or priority; omit it from the main chart. Preserve meaningful task-step numbers, evidence states and uncertainty.
