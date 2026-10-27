# HTML report delivery

## Final artifact contract

Deliver `index.html` and one HTML file per requested product identity. Each report opens directly via `file://` without a build, server, CDN, remote font or script. Embed available images with their provenance and useful captions. Keep report material in the project output folder, not in the installed skill. A sparse product still gets its own report, with all useful evidence analyzed and specific gaps; report-shell completeness is not research completeness.

Each product report contains:

**Make the product understandable before asking the reader to inspect the research.** The opening identifies the product, its core user task and a finding tested against the material, with useful inspected imagery where available. Prominent navigation exposes four maps: (1) product → modules → atomic capabilities, (2) the supported task path, including acquired actions, branches and continuation, (3) identifiable screen/region containment and known routes, and (4) technical input/processing/storage/output relationships. Distinguish real UI organization from analytical grouping. When navigation evidence is incomplete, title the bounded screen view accordingly and show route breaks; generic task categories are not replacement pages. These maps need not occupy four consecutive screens. Make nodes clickable for explanations and evidence, retain uncertainty labels in print, and keep lengthy arguments outside nodes. Completeness is bounded by source coverage, not node count. Preserve analysis of:

1. Product identity, version/date, user task, positioning and conclusion.
2. UI style and hierarchy: actual images/regions, visual rules and task implications; missing pixels are explicit.
3. Core interaction: main flow, key objects and state transitions, continuation and consequential failure paths.
4. Core technology: input/output/data flow, supported mechanisms, alternative explanations and distinguishing tests.
5. Business and operational constraints affecting the main task.
6. Strengths, costs and limitations, separated from untested assumptions.
7. Adopt/adapt/defer decisions tailored to the user's product.
8. Important unknowns, actual acquisition attempts/results, evidence added to diagrams, and ordered next actions or concrete resumption conditions. Distinguish unattempted work from blocked work using [the acquisition record](evidence-acquisition.md).
9. Inspectable evidence sources, dates, versions and locators, cited near findings.

Keep readable line lengths, semantic headings, accessible contents, responsive tables, clear evidence labels and print CSS. Let images and concrete flows explain the analysis. Do not make every product's prose identical, inflate page length with repeated caveats, or generate competitor UI to fill a gallery.

Apply [analysis-depth.md](analysis-depth.md) to authored content before rendering. Each consequential finding must explain a mechanism and its decision relevance within its evidence boundary. Four maps and nine chapters are delivery structures; their presence does not establish complete reasoning. Report unresolved evidence and actual analytical review separately from file generation or structural checks.

## Editorial and visual quality

Apply the [visual report contract](report-design.md) for shared composition and visual tokens, with [Apple-guided usability](apple-web-design.md) for component behavior and concrete browser checks. Keep platform principles distinct from authored CSS choices. An explicit user request may change the visual direction; preserve the readability, evidence and interaction requirements. The principles below explain how to compose the report's actual content within that system.

Use [design-quality-review.md](design-quality-review.md) to establish one working design contract and review the actual report through critique, typesetting, layout, hardening, polish and relevant code checks. Record concrete defects and final evidence rather than listing external skills as if they had run. Helpful heuristics do not override the user's system or introduce new installation requirements.

### Collection navigation

Render the same text-only competitor list on the index and every product report. On desktop, keep it in a bounded, independently scrolling left rail with name/category search and exactly one `aria-current="page"` product. Local report chapters belong in a separate, labeled contents control; chapter tracking must not overwrite the current-product state. On phones, use an operable disclosure rather than putting all competitors before the report.

Use native relative links to independent HTML files. The enhanced switcher can preserve a shared chapter/map context, search query and rail position, while node/source IDs remain specific to their product. Keep optional session storage collection-scoped, bounded and failure-tolerant; `file://` or privacy-mode storage denial must not disable links or report content. Load one report at a time and reuse shared assets. Avoid rendering/preloading the whole collection to make switching appear immediate.

Verify actual product changes, highlight, search/empty/clear behavior, rail scrolling, same-chapter switching, browser Back, cold deep links, mobile selection, keyboard access and the no-script fallback. Retain independent report URLs, source/back history and all diagrams.

### Structure the reading experience

- **Orient first.** A reader entering a report should quickly understand what the product does, what is distinctive, and why it matters to the user's decision. Put the most explanatory product image or concise task representation beside that argument when useful. Build/version strings, evidence coverage and acquisition counts support this opening; they should not displace it.
- **Give each section a job.** Explain the competitor's known organization and behavior before its tradeoffs and possible application. Keep recommendations and future tests in their own analytical role rather than filling the interaction chapter with how a system “should” work. A summary can recall a finding; later sections add evidence or explanation.
- **Separate reading from inspection.** Keep concise findings and material qualifications visible. Put raw acquisition attempts, long source locators, extended status histories and exhaustive evidence matrices behind descriptive disclosures or in an appendix. Their summaries must say what remains uncertain and where the detail is. Never collapse the sole explanation of a consequential limit.
- **Use the right form.** Use a diagram for relationships, an image for visible interface evidence, connected prose for an argument, and a table for genuinely comparable fields. A six-column ledger or many identical text cards is not a default chapter layout. Do not pad sparse evidence with empty galleries or repeated generic advice.
- **Make the index useful for choosing.** Distinguish products by task, mechanism and a specific finding. Use consistent thumbnails only when meaningful evidence exists; a concise alternative is preferable to a misleading placeholder. Search/filter and card links should aid comparison without hiding the full inventory.

### Make images and maps carry information

- Display the relevant app region large enough to inspect its controls and hierarchy at the report's normal reading size. A browser capture with a tiny centered phone and large black margins needs a better presentation window or an accurately labeled enlargement; displaying the full desktop capture as a thumbnail does not make UI evidence readable.
- Preserve the original evidence and provenance. A crop or display window may remove irrelevant margins, but must not remove a material control, qualifier or promotional frame without showing that context elsewhere. Label the region and offer access to the complete source when a close-up is used. Do not redraw, enhance or generate missing app controls as evidence.
- Pair the image with observations anchored to visible regions: selected categories, named tools, current values, object previews and action boundaries often explain more than palette descriptions. Use readable enlargements or annotations where useful. Keep publisher decoration, an app screen, an annotated reconstruction and an analysis diagram distinct. Visible pixels establish the inspected state, not an unseen transition.
- Give every map a clear reading direction, concise labels, legible connectors and a meaningful default view. Separate the main path from optional branches and return paths. Larger maps need a readable overview plus navigation or focused detail; shrinking everything until it fits sacrifices the analysis.
- Preserve all four maps, node explanations and source access. Tabs, disclosures or section navigation may control screen density, but must not make undisplayed maps disappear from no-script or print output. Evidence status must remain intelligible without color alone.

### Establish hierarchy and responsive behavior

Create a clear distinction between report title, conclusion, section heading, finding, supporting explanation, caption and provenance. Use the [current reader tokens](report-design.md#one-system-implemented-once), with spacing and grouping to show their relationship; do not give every block the same border, background and prominence. Limit prose width independently of diagrams and imagery. Captions, source controls and evidence labels retain the contract's readable size and contrast on phones.

At narrow widths, recompose the reading order instead of merely shrinking the desktop page. Keep the product argument and useful imagery early; avoid a full-page contents list before the report begins. Wide diagrams or tables may scroll within labeled regions, with a visible means to inspect their content; the entire page should not overflow. Controls, disclosures and source links must remain operable by touch and keyboard. Use animation only when it helps orientation, and respect reduced-motion preferences.

When the user reports poor visual quality, inspect the generated page and its authored content before editing styles. Identify whether the failure is reading order, repetitive writing, missing imagery, image scale, diagram layout or responsive behavior, then repair that cause. Preserve evidence and product identity while changing presentation. Do not treat a palette change, extra decoration or a successful render as proof that the complaint is resolved.

When the user reports shallow analysis, challenge the main product model against its strongest available counterexample. Reinspect original material for omitted capabilities, control values, known paths and conflicts, then repair the explanation and acquire the consequential missing evidence. Review the repaired representative report before scaling. Another visual redesign or longer test plan does not resolve an incorrect model.

## Reusable renderer

[Example preview](../docs/report-example.png): an actual Chrome capture of the original synthetic `assets/report-bundle.example.json`, generated on 2026-10-27. The example and image use [MIT](../LICENSE); host-system fonts are rendered, not redistributed as font files.

The standard-library renderer consumes **authored analysis**; it does not infer findings from a ledger or discover missing evidence. Start with [the original example bundle](../assets/report-bundle.example.json), replace its synthetic content, and run from the skill directory:

```sh
sh scripts/doctor.sh
python3 scripts/render_reports.py path/to/report-bundle.json --output path/to/new-report-folder --format linked
```

Use the Python command reported by the doctor (`python3` or `python`). Missing or unsupported Python blocks rendering, while evidence research can continue; activate or install Python 3.9+ and rerun doctor before retrying. The helper needs Python 3.9+ and no third-party packages. Keep browser review pending if browser access is unavailable.

The CLI defaults to `--format linked`: per-product HTML, a searchable/filterable index, content-addressed local images/CSS/JS in `assets/`, and a hash manifest. Keep and zip the entire folder. Shared resources can be cached across reports, and HTML editors/previews avoid large inline base64 strings. `--format standalone` explicitly embeds resources into each HTML for single-file exchange. The Python `render_bundle` API retains its historical standalone default for compatibility; pass `delivery_format="linked"` for the normal reading bundle. Use an empty/new output directory; the renderer refuses to overwrite existing work. No network requests occur during rendering. Its completion message proves generation, not source truth or browser quality.

The bundle has `title`, `date`, `summary`, optional `lang` (default `zh-CN`), and `products`:

- Each product has stable safe `id`, `name`, `category`, `platform`, `identity`, `version`, `tagline`, `verdict`, `scope`, `coverage`, `sources`, **`visuals`** and `sections`. Product IDs determine filenames; use distinct identities for similarly named apps.
- Optional product `brief` contains nonempty `headline` and `deck`: an authored short product promise and a bounded primary-task description. It enables the editorial layout; the index uses `deck`. See [reading-copy review](design-quality-review.md#edit-the-reading-copy).
- Optional `presentation.lead` supplies a concise opening finding suited to the reading layout. It must preserve the substance and confidence of `verdict`; a shorter display copy is not permission to strengthen the claim.
- `coverage` has one row each for `ui`, `interaction`, `technology`, `business`, with `status` (`supported`, `partial`, `missing`, `out_of_scope`) and a specific `detail`.
- Each source has `id`, `title`, `kind`, `date`, `locator`, `context` and optional HTTP(S) `url`. Source kinds follow [the evidence model](evidence-model.md). Treat a historical note quoting an official source as secondary until rechecked; its original URL may remain a reference link.
- `sections` contains IDs `overview`, `ui`, `interaction`, `technology`, `business`, `strengths`, `decisions`, `validation`, each with a localized `title` and nonempty `blocks`. Sources render as the ninth chapter automatically.
- Optional section `summary_blocks` uses the same block schema and citation checks as `blocks`. It is the authored reading copy; complete unique analysis in `blocks` remains in a disclosure. Optional nonempty `summary_title` and `detail_label` name those two layers. Include consequential qualifications in the reading copy, not only in the disclosure.
- Optional section `lead_blocks` is an integer count of opening blocks to show before a supporting-detail disclosure. Choose the boundary from meaning, not a fixed page-length target; material qualifications must remain beside their finding. Acquisition detail in `validation` uses a compact lead and an expandable record.
- Every block may include `status` (reader-facing evidence label) and `sources` (IDs within this product). Text is escaped; raw HTML is not accepted.

| Block type | Content fields |
|---|---|
| `paragraph`, `callout`, `heading` | `text` |
| `list` | `items`: nonempty text array |
| `table` | `columns`: text array; `rows`: arrays of equal-length text cells; optional accessible `label` |
| `flow` | `items`: objects with `title` and `detail`; label whether edges are observed or reconstructed |
| `image` | `path`: local PNG/JPEG/WebP relative to the bundle (absolute paths also accepted for private research); `alt`; `caption`; cite source/region and distinguish app UI from promotional framing; optional `viewport` describes a display window |

Images are limited to 20 MiB each. Linked delivery copies each unique image once without changing its bytes; standalone export embeds data URLs. Respect task authority and redistribution rights; the renderer is for local report delivery and does not publish assets. External source links work online; all report prose and illustrations remain readable offline.

In the UI chapter, an image immediately followed by a three-column region/observation/interpretation table becomes an image-and-notes composition. All column labels, cell text and citations remain available; display-window images sit beside the notes on wide screens, while full-context images and phone layouts stack. Author those rows as specific visual observations, not unrelated comparisons.

An image `viewport` has numeric `x`, `y`, `width`, `height`, `source_width` and `source_height` in source-image pixels. Record the actual inspected dimensions and bounds; the window must fit inside the original. This changes display framing, not the evidence file or its pixels. Explain what region is shown and keep the complete source inspectable. A browser screenshot's margins may be omitted for reading, but image context must remain available when it changes interpretation.

### Visual atlas schema

An optional product `positioning` object contains a nonempty `summary` and local `sources` IDs. It states the product's primary task as a bounded research synthesis, separately from `verdict`/`presentation.lead` (the study finding). Use that primary task on the index. Categories are analysis labels, not automatically the app's navigation, market segment or validated customer positioning.

`visuals` requires exactly `features`, `journey`, `screens`, `dataflow`. Each has `title` and a concise `summary` describing evidence scope. These diagrams are original analysis, never fabricated app screenshots.

Read [diagram design](diagram-design.md) for visual grammar and collection review. Each map may include an authored `reading: {text, sources}` introduction; citations must join existing source IDs. Nodes may include a nonempty `caption` of at most two SVG lines. Keep the full `detail`, evidence status and sources. The `brief` layout places the full maps with their corresponding explanation, linked by a four-map directory; other inputs retain the compatible tab layout. The enhanced phone reader offers an adjacency list and a switch to the full spatial drawing. Disconnected components are drawn separately without changing the authored relationships.

- `features.modules` is a nonempty array of `{label, features}`. Each feature is a node. Retain supported atomic capabilities when grouping; a broad “editing” or “AI” node must not erase distinct tools. State whether grouping follows visible UI or an analytical taxonomy. Include supported auxiliary/return capabilities and precise gaps, not standard app modules assumed from other products.
- The other three maps have nonempty `nodes` and `edges`. Nodes use distinct nonnegative integer `col` and `row` grid coordinates (each 0–12). Prefer two or three columns; move long explanations to details. Keep labels to a few words (at most three rendered lines). The renderer draws directed orthogonal arrows and retains all diagrams offline.
- Each node has `id`, `label`, `detail`, `status`, `sources`. Status is `observed`, `declared`, `static`, `reported`, `inferred` or `unknown`. Factual statuses require source IDs. Apply the status narrowly: declared capability presence does not make inferred UI placement or lifecycle factual. Distinguish them in details or separate nodes. A historical report remains `reported` until its underlying evidence is inspected; reformatting does not upgrade it.
- Each edge has `from`, `to`, `label`, `status`, `sources`, with the same evidence rules. Label trigger/condition rather than simply “next.” A transition into an unknown state can be supported even when the state's internal behavior is unknown. Do not give a real route status to a conceptual task progression. Show absent implementation knowledge explicitly in the technical map; plausible architecture stays inferred.

The included original notes fixture demonstrates all fields. Feature trees reflow on phones; wider SVG graphs scroll internally at a readable size and offer zoom. An accessible node/edge text index supplements the diagram. Without JavaScript, all diagrams remain visible. Printing includes all four maps and restores the reader's previously collapsed disclosures afterwards.

## Check actual delivery

### Navigation and performance

Measure the user-visible operation on actual output before tuning: file bytes, image dimensions/decoded pixel budget, navigation-to-settled-target time, layout shift and long tasks or frame gaps when relevant. Use the same report, viewport, cache/CPU conditions and action for the comparison. Keep synthetic/slow-CPU results distinct from real-device measurements. Do not call an unchanged passing layout check a performance benchmark.

- Diagnose the actual reader and entry route, including embedded previews and `file://` versus loopback HTTP when relevant. A fast Chrome page does not establish that an editor preview can process megabyte base64 lines smoothly. Measure HTML bytes separately from lazy media transfer and decoded pixels. Keep the default reading bundle linked; a smaller total ZIP alone does not prove interactive responsiveness.
- Check the document already loaded in the reader's existing tab against the delivered manifest and resource URLs before measuring. The same URL or updated disk file does not establish that the live document or a back/forward-cache entry has changed. Refresh an outdated report under the existing authorization and verify its actual content. Hand off a revision-specific entry URL or folder so the reader can identify the artifact; keep relative report/resource links within that revision. Retain compatible old entry points when useful, while resolving a fresh visit to the current revision.
- Match the input path to the complaint. Test desktop wheel/trackpad scrolling for a desktop complaint; a synthetic touch gesture is a distinct sample. Measure directory clicks through a stable destination, including reading while a previous scroll is settling. Keep untested browser engines explicit, and verify each product landmark after navigation before collecting its geometry.
- Give same-page navigation one owner. Reveal the target's actual disclosure/map before one final scroll; avoid native hash scrolling plus delayed duplicate scrolling. Preserve modified-click behavior, real link targets, browser history and keyboard focus. Long automatic smooth scroll is not required to convey a destination.
- Verify the destination after layout settles, including cold direct hashes and large images above it. Derive the sticky offset from the rendered header, including enlarged text; do not assume its height is always 72px. The active directory item must follow the actual reading position.
- A node inspector belongs to its selected context. Close it when leaving that context, clear its old selection and preserve Escape focus return. Source/back should restore the real reading position and selected node, not merely the atlas heading. If the page owns history restoration, coordinate it with native restoration and page/bfcache lifecycle events. Repeat source/back and index/report/back checks; a single successful return can hide a restoration race.
- Keep default map switching free of unnecessary layout measurements after hiding/revealing panels; measure only when the user explicitly asks to fit. Avoid per-frame geometry polling when a native intersection observer can track reading sections. Offscreen-rendering optimizations must retain correct cold-hash geometry, browser find, keyboard/source access, history and print; reject changes that break those operations.
- Reserve intrinsic image dimensions before decode and use asynchronous decoding. A small index tile must not decode a full camera poster. The renderer uses `thumbnail_path` when supplied and otherwise falls back to a capability summary if a source exceeds its catalog budget (120 KiB or 960×960 pixels). Those limits are project choices, not a platform standard.
- Optional image fields `thumbnail_path` and `preview_path` point to truthful local reading derivatives. The renderer retains the exact `path` original in an expandable full-source view; captions distinguish reading previews. Preserve source bytes, provenance, aspect ratio, meaningful qualifiers and full context. Derivatives are not new app evidence. No-script users can still expand original images.
- For an existing documented `viewport`, prepare the reading derivative from that region before reducing it; shrinking an entire desktop capture first can make its small phone region unreadable. The helper sets `thumbnail_framed` / `preview_framed` only for such derivatives, so the renderer does not apply the source window twice. Keep the complete original and the crop's disclosure. Unframed derivatives retain the original geometry.
- If available, `scripts/prepare_previews.py INPUT --output NEW_MEDIA_DIR --bundle-output NEW_BUNDLE` prepares bounded derivatives and a hash receipt without modifying inputs. This optional command needs Pillow in the current interpreter. Core rendering/auditing remains standard-library-only. Missing optional tooling does not justify automatic installation or fabricated screenshots; use existing authorized image tooling or the bounded fallback.
- Set an aggregate catalog budget for the actual inventory. Record total payload and decoded pixels, not merely per-file limits; forty individually small originals can still be expensive. Keep required originals and full maps available rather than deleting evidence to meet an arbitrary score.

Record final artifact hashes, before/after values, exact actions and remaining limits. Remove temporary instrumentation from shipped assets. A warm machine showing no long task is evidence for that sample, not proof that the user's reported stall was imaginary or that every device is now smooth.

- Match inventory count and stable identities to generated reports; open deep links from the index and source references inside reports.
- Apply the [design completion checks](apple-web-design.md#completion-checks) to representative dense, image-based and sparse reports and the index before applying a presentation change to the full set. Review the final generated files again after the change. Record the reports, viewport sizes, enlargement methods and states actually inspected; fixture checks do not establish that the user's reports look good.
- Judge the opening viewport and the reading sequence, not just the existence of all chapters. Can a reader identify the product's main task and finding, inspect its relevant UI, and locate the core flow without wading through metadata, repeated conclusions or logs? Does each following section add useful information?
- Inspect images at their actual displayed size. Check for illegible app controls, excessive capture margins, misleading crops, distorted aspect ratios, invented screenshots and captions that overstate source/version certainty. Open any enlargement or full-context view.
- Check broken images, horizontal viewport overflow, cropped text, keyboard navigation, disclosure and source access, and index search/filter/empty state. Verify the no-image and no-JavaScript cases as distinct presentation states, rather than filling them with fabricated evidence.
- Inspect the rendered connectors as well as the nodes: branches must not look like a mandatory sequence; return arrows must not pass through unrelated nodes or hide labels. Check feature coverage against the source, not just graph counts. Sparse evidence must produce a visibly bounded map, never the same invented app architecture repeated across products.
- Review print rendering for readable tables, content order and visible evidence/scope disclosures even if collapsed on screen. Restore the reader's disclosure state after printing. The browser's print action can save PDF; PDF is optional, HTML is primary.
- Review the main claim against a concrete counterexample before checking chapter coverage. Confirm that source details have not been lost, acquired actions survive in the task path, and a chapter of proposed tests has not replaced an explanation of the competitor.
- Apply the [depth review](analysis-depth.md#review-depth-before-delivery) to actual findings. Shared category principles belong in synthesis; each report retains the evidence and mechanism that distinguish its case. A repetition flag directs review but does not justify padding. Formatting must not strengthen the conclusion beyond its sources.

Use an available, authorized browser route for this review. If access is denied or unavailable, do not bypass the restriction; report the exact unperformed checks and continue checks that remain possible. Do not mark visual review complete based on source-code inspection.

Automated tests can check escaping, source joins, filename safety, inventory preservation and offline dependencies. They cannot decide whether the report is thoughtful, readable or visually coherent, or whether a source actually supports a finding. Report structural checks, observed browser behavior and visual judgment separately.

When a research chapter contains a finding, limiting evidence and decision before a long protocol, set its explicit `lead_blocks` to keep those blocks visible. The renderer honors that choice in `validation`; its compact default applies only without an explicit hint. Keep conclusion-changing qualifications beside the finding rather than inside a closed acquisition disclosure.

## Design and UX authoring schema

Optional product `design` is required when delivering a detailed UI specification. Existing narrow/legacy inputs remain renderable without it; their lack of this field is not a completed detailed design pass. Read [design-specification.md](design-specification.md) for acquisition, analysis and completion criteria.

- `scope`, `intent`: authored nonempty text; `coverage`: `partial`, `available_material_complete` or `no_ui_pixels`. None means the entire app has been runtime-verified.
- `regions`: `{name, elements: [text], role, status, sources}` for every distinguishable region in inspected states. Empty only when no app pixels support a visible-element inventory. Separate promotional packaging explicitly.
- `rules`: exactly one each of `color`, `typography`, `spacing`, `shape`, `iconography`, `imagery`, `motion`, `responsive`, `accessibility`; fields `{category, value, status, sources, method?, verify?}`. Unknown `value` is null with a concrete `verify`; measured values require a method, units and context. Described values do not pretend to be exact design tokens.
- `components`: `{name, anatomy, shown, unknown, verify, status, sources}`. Inventory known anatomy and states; `unknown` identifies absent variants/behavior. A visible icon does not prove its click result.
- `ux`: `{goal, entry, object, choice, feedback, recovery, completion, findings}`. Each finding has `{title, observation, consequence, alternative, decision, status, sources, protocol}`. Protocol has `{start, action, pass_result, reverse, status: "not_run"}`; actual execution belongs in the study record, not a template flag changed to “passed”.
- Evidence states: `observed`, `declared`, `reported`, `inferred`, `unknown`, `measured`. Source IDs must join the product source register; factual states require evidence. Qualify static records in the text and cite the exact static source.

The renderer writes `design/<id>/Design.md`, includes source images as local content-addressed assets, and records document hashes in `manifest.design_documents`. The interface heading links the document; UI/UX panels use the same data. Retain the whole folder when moving Markdown so relative evidence/report links work. Even a standalone HTML export has companion files when Design.md was requested.

For an authorized local preview, `python3 scripts/preview_reports.py REPORT_FOLDER --port 8000` serves a hash-checked immutable snapshot bound only to `127.0.0.1`. It includes Design.md and refuses files outside its manifest allowlist. Restart after regenerating and use the printed revision URL. Stop with Ctrl-C; it installs no persistent service.

## Reading workspace runtime

Apply [reader-interactions.md](reader-interactions.md) for the shared interaction contract. HTTP links enhance to same-origin, on-demand report loading with a three-report cache; native file links remain the no-script/file fallback. The preview helper permits `connect-src self` for these manifest-listed reads and does not serve arbitrary files. `reader.js` owns navigation/history/inspection; legacy `report.js` exits when that controller is active. `workspace.css` styles its native dialog and mobile chooser. `design_reader.py` renders the exact exported specification into an inert template, preserving original Markdown downloads. Keep element/event cleanup, cancellation and retry as part of each report transition.
