# Competitor analysis — [scope and date]

This is an authoring outline, not a prescribed page layout. Deliver a separate complete HTML file for each product and an index for a multi-product study, following [HTML delivery](../references/html-delivery.md). Repeat the product-specific chapters for each identity; do not ship only this Markdown document or a shared comparison table. Open each report with the product, its main task and consequential finding, with readable inspected imagery when available. Keep extended inventories, source records and acquisition logs available as supporting detail.

## Decision and boundaries

Use the [research methods](../references/research-methods.md) and [workbook](research-workbook.md): decision and alternatives, falsifiable question, target situation, selection rationale and comparison mismatches. Record selected methods, actual inspection, artifacts and completion boundaries. Keep study plans distinct from executed studies.

## Product inventory and evidence coverage

| Product identity / platform / revision | User job / mechanism | Selection rationale | UI evidence | Interaction evidence | Technology evidence | Business evidence |
|---|---|---|---|---|---|---|

## Evidence index

| ID | Product / revision | Source type, date and context | URL / file / timestamp / region / function | Hash where relevant | What it can and cannot establish |
|---|---|---|---|---|---|

## Detailed findings

Repeat only to the depth justified for each product or mechanism. Apply [the depth contract](../references/analysis-depth.md): develop consequential findings from evidence through mechanism/state, causal alternatives, cost/boundary, a product decision and a discriminating check. Use the form that explains the argument clearly rather than repeating those labels in every section.

### Visual product atlas — make the relationships easy to inspect

1. Product → capability modules → subfeatures, including supported auxiliary features and explicit coverage gaps. This is not necessarily the real menu structure.
2. Directed task graph: entry, conditions, branches, result, repeat use and recovery. Keep optional features off the compulsory path.
3. Screen/route relationship graph. If only task states are known, label the graph conceptual and navigation edges inferred.
4. Technical/data-flow graph: inputs, processing, state/storage and outputs. Identify client/server or local/remote boundaries only where supported.

Use short node labels, readable connectors and linked explanations/sources. Preserve the evidence status of both nodes and edges. Complete the maps from available material without claiming unobserved app-wide coverage. Make all four maps easy to find without requiring four consecutive diagrams before the product explanation. Follow the structured `visuals` example in the HTML contract.

### UI style and structure

Representative images/regions, hierarchy, role-based typography/color/spacing, components, imagery, layering, state differences, visible accessibility concerns. Explain what each consequential region prioritizes or defers and the task tradeoff; a style inventory is supporting detail. State measurement units and uncertainties.

For a detailed UI analysis, follow [the Design.md contract](../references/design-specification.md). Inventory every distinguishable element in the inspected regions, then author semantic rules and component states with their evidence boundaries. Export `design/<product-id>/Design.md` from those same records and link it from the interface view. A complete document includes targeted acquisition routes for unknown values; it does not fill unavailable app screens with invented components.

### Core task and interaction

Add a source-linked capability-depth matrix where comparisons affect the decision. Distinguish a declared path from observed runtime completion. If a task study was executed, show its protocol, raw-attempt link and correct denominators; if not, state not_run and give the smallest discriminating protocol beside the affected finding.

Concrete user job; start/end; task/state graph or table; prerequisite, action, system work, feedback, durable result, continuation and recovery. Explain conditional decisions and what persists between actions. Label reconstructed versus observed paths.

Show the UX review in the reading layer: the user goal, key choice, feedback/completion and recovery. Tie each consequential risk to a source observation, impact hypothesis, alternative explanation, decision and test that could reverse it. Keep the complete task graph and protocols available. Do not repeat this overview as numbered filler in the adjacent interface summary.

### Core technology and data

Concrete input/trigger/transform/output/state/storage/consumer contracts. Separate static facts, official disclosures and hypotheses. Include alternatives, their conditional product consequences and distinguishing tests for uncertain mechanisms; an SDK list is insufficient.

### Commercial and operating conditions

Accounts, permissions, paywalls, network/cache, content supply and persistence as they affect the core task. Unknowns remain explicit.

## Cross-app synthesis

| User problem | Different mechanisms and supporting evidence | Strength / cost | What fits our constraints |
|---|---|---|---|

## Product decisions

Develop the consequential findings with actual source facts, causal alternatives, impact boundaries and reversal conditions. Use completed issue/experiment cards from the workbook when they change the decision. Show any score's anchors, common coverage, hard gates and sensitivity. Presentation quality does not establish usability or business outcomes.

| Adopt / adapt / defer | Supporting claims | Fit and prerequisites | Tradeoff | Discriminating observation and how it changes the decision |
|---|---|---|---|---|

## Conflicts, gaps and completion status

Version conflicts; missing dimensions; next observations prioritized by decision impact. Include the acquisition receipt below and update diagrams with new findings. Separate analysis delivered from research complete, runtime verified, implemented or released. If structured ledgers exist, link them and report their structural audits separately from manual review.

| Missing decision question / priority | Closure proof | Actual channel and result | New evidence and report update | Remaining question / next action or resumption condition |
|---|---|---|---|---|

Use the [acquisition workflow](../references/evidence-acquisition.md). Keep unattempted work distinct from blocked work and preserve the user-authorized research scope.
