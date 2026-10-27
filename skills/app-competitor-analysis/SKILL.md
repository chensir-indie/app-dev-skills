---
name: app-competitor-analysis
description: Analyze competitor app UI, UX and technology from evidence; deliver per-app HTML reports, Design.md specifications, visual maps and product recommendations with explicit gaps.
---

# App Competitor Analysis

Explain how a competitor works, why its experience takes that shape, and what the user's product could adopt. Match the requested decision, evidence scope and language.

## 1. Choose the scope

Identify the user's product/task, competitors, requested dimensions and available material. Read [research methods](references/research-methods.md) to frame a falsifiable question, comparable task subgroup and useful methods. Ask only for missing information that changes the work.

- **Single app:** trace its primary task and relate UI and implementation to it.
- **Landscape:** inventory the entire requested set and report on every product, even when deeper sampling varies. Group by user job and mechanism.
- **Limited access:** analyze what available artifacts establish and record the boundary. Sparse starting material calls for acquisition before a gap-only conclusion.

## 2. Establish evidence

Read [evidence-model.md](references/evidence-model.md). Pin product/platform, version, source date and account/device/state context. Inspect the underlying artifact for material claims; verify current behavior through current official sources. Distinguish observed, declared, static, inferred and unknown evidence.

Prefer supplied material and authorized acquisition. Missing device access limits runtime conclusions but permits screenshot/static analysis. For consequential gaps, follow [evidence acquisition](references/evidence-acquisition.md): define closure proof, acquire and inspect, reconcile, update reports/maps and recheck. Record actual attempts and distinguish unattempted, partial and concretely blocked questions. Text extraction cannot close a pixel/runtime question. Keep private artifacts out of the skill package; acquisition does not authorize purchases, protection bypasses or private-data uploads.

Record selected methods as completed, partial or not run using [the workbook](assets/research-workbook.md). Participant studies, runtime comparisons and cohort measurements need actual data; unknown measures remain null. Before bundled scripts, run `sh scripts/doctor.sh` and use its reported Python interpreter. For failures, follow [helper setup](README.md#run-the-helpers), continue independent research and keep dependent work pending.

## 3. Analyze only the needed dimensions

Read [analysis-depth.md](references/analysis-depth.md). Recover capabilities, visible organization and concrete task records before proposing changes. Challenge the product model with contrary pixels, entrypoints and source details. Preserve atomic capabilities, control states and known steps; caveats and future tests do not replace explanation.

| Dimension | Required reference | Result |
| --- | --- | --- |
| UI and information architecture | [UI analysis](references/ui-analysis.md); [design specification](references/design-specification.md) for detailed work | Element inventory, design rules/components and source-linked `design/<product-id>/Design.md` |
| Interaction and product logic | [Interaction analysis](references/interaction-analysis.md) | Tasks/states, choices, feedback, recovery and durable completion |
| Technology and data | [Technical analysis](references/technical-analysis.md) | Input → trigger → transform → output → storage → consumer, with artifact/call-path evidence |

Mark unrequested dimensions `out_of_scope`. Requested but unsupported dimensions retain a specific gap and next observation. Keep uncertain mechanisms conditional, with alternatives and a distinguishing check. Pixels do not prove unseen behavior or a technology stack. Record paywalls, permissions, accounts, offline and repeat-use constraints when they affect the main task; separate promotional framing and declared access from observed use.

## 4. Synthesize product decisions

Apply [synthesis and reporting](references/synthesis-and-report.md) and the [depth review](references/analysis-depth.md#review-depth-before-delivery). Compare mechanisms for the same user job and constraints. Each consequential adopt/adapt/defer recommendation needs evidence, the user's context, a tradeoff, an alternative explanation and a small test whose outcome could reverse it. Preserve existing user decisions unless new evidence warrants a change.

Keep the competitor's primary task distinct from the study's interesting finding. Platform/version scope and product classification must agree across index, opening and maps. Optional scoring requires declared anchors, comparable evidence, hard gates and sensitivity; otherwise compare mechanisms without a numeric winner.

## 5. Deliver and verify

Honor an explicit format or narrow endpoint. The default broad study delivers one complete HTML report per competitor and a searchable multi-product `index.html`, as a portable folder with shared local assets. Use single-file export only when requested. Each report includes four evidence-linked maps: feature hierarchy, directed task flow, screen relationships and technical data flow. Preserve known branches/loops and expose missing links instead of inventing transitions.

Follow these contracts at the relevant step:

| Step | Read and apply |
| --- | --- |
| Author and render reports | [HTML delivery](references/html-delivery.md) for schema, renderer, packaging and actual preview route; [report template](assets/report-template.md) for the outline |
| Compose the reading experience | [Report design](references/report-design.md), [design quality review](references/design-quality-review.md) and [Apple web usability](references/apple-web-design.md); preserve an explicit user direction |
| Author visual maps | [Diagram design](references/diagram-design.md); keep all four complete maps readable beside their explanations |
| Detailed UI/UX output | [Design specification](references/design-specification.md); author element/rule/component/UX records before rendering, link Design.md in the interface view and task findings in interaction |
| Change report interactions | [Reader interactions](references/reader-interactions.md); verify complete journeys and interrupted/failed report switches |
| Repair rejected presentation or compare a visual reference | [Report design](references/report-design.md); deliver actual reference/old/new captures in a local HTML comparison before applying the shared repair to the set |
| Diagnose navigation or speed | [Navigation and performance](references/html-delivery.md#navigation-and-performance); reproduce and measure the same operation on the actual final files |

Lead with product identity, its defining task, a distinct supported finding and useful imagery. Keep concise reading separate from detailed research using `brief` and `summary_blocks`; state a finding once and link back. Material qualifications stay beside claims. Long acquisition histories and exhaustive tables may use disclosures. Review a representative claim against its strongest counterexample, then inspect sparse, image-based and dense compositions before scaling.

Use shared styles/components and the existing reader: searchable desktop product library, URL-addressable views, native links/history, continuous reading and an accessible phone chooser. When changing reusable report behavior, update the canonical Skill/generator first and regenerate every requested report. Product-specific findings and imagery belong in the report project.

**Delivery gate:**

- Inspect the real generated HTML through an allowed browser route. Apply [design completion checks](references/apple-web-design.md#completion-checks): desktop/phone, enlarged text, keyboard, reduced motion and print; verify coverage, maps/connectors, details/sources, images, navigation, search and filters. Repair defects and verify the full set. Missing browser access leaves these checks pending.
- Include an acquisition receipt with real routes/results, evidence added, unresolved questions and next actions/resumption conditions. Broad studies run `scripts/audit_acquisition.py`; optional structured evidence audits follow [evidence-model.md](references/evidence-model.md). A readable table is sufficient for small work.
- For actual first-valid-attempt studies, run `scripts/study_metrics.py study.json --output summary.json` using [the schema example](assets/study-record.example.json), and separately inspect raw recordings and comparison conditions.
- Apply [evaluation.md](references/evaluation.md), including change-app-name, decision and cross-section checks. Structural tests, arithmetic and rendered files do not establish analytical depth, source truth or visual quality.

Return clickable reports and preferably a rendered diagram preview. State evidence completeness separately from HTML delivery, device validation, implementation and release. Later design/implementation handoffs carry report links, chosen decisions, unresolved hypotheses and the requested next artifact; recommendations do not establish an approved design or actual capture of the user's app.
