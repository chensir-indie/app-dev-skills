# Competitor Design.md and UX review

Read for detailed interface analysis, a requested `Design.md`, or UI/UX depth repairs. The deliverable describes the competitor's evidenced design system, not the visual system of our report. Use [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) as a decomposition reference; its brand-specific tokens are third-party interpretations and must not be transplanted into another product.

## Inspect, inventory, then explain

1. Inventory available screens and states with source IDs, platform/version, theme, locale and pixel dimensions. Separate promotional framing from the app viewport. Inspect every image used for a material finding; missing screenshots require [evidence acquisition](evidence-acquisition.md).
2. Work through each visible region: navigation, title/status, content, primary action, secondary controls and overlays. Record each distinguishable element's label/shape, role, grouping, state and evidence. Mark illegible detail. A declared feature has no known visual form until pixels establish one.
3. Recover semantic rules for surfaces/ink/accent/semantic colors, text roles, spacing/alignment, proportions, shape/borders, elevation, icons, imagery, density, motion, responsive behavior and accessibility. Values are measured with units/method, visibly described, source-declared, inferred or unknown. Screenshot pixels are not logical points; unknown font families and timings stay unknown.
4. Explain component anatomy, variants and default/selected/disabled/loading/error/success states, trigger/feedback and what survives navigation. Record unknown states with a targeted observation route. A still supports the depicted state only.
5. Challenge the explanation with another screen, contrary evidence or a plausible alternative. Derive a reusable principle and its cost; keep proposals apart from observed competitor facts.

## Artifact contract

For a detailed UI deliverable, write `design/<product-id>/Design.md` with:

- Product identity, evidence scope and an honest completeness statement.
- Design intent and the main task it serves.
- Screen/state inventory; inspected image links and the app-versus-promotion boundary.
- Full visible-region/element inventory and hierarchy, not a few selected widgets.
- Semantic tokens/rules for every category above; unknowns with specific observation routes.
- Component anatomy and state matrix, including known and unobserved states.
- Layout/imagery/content/motion/responsive/accessibility rules at supported precision.
- UX findings, task decisions, feedback, recovery, repeated use and completion contract.
- Transferable choices, tradeoffs, counterexplanations and discriminating validation.
- Source register and consequential gaps.

Complete coverage of available material differs from a complete reconstruction of every app screen. Put that distinction near the document title. Unsupported token values stay null; do not fill a CSS theme with guesses. Use the requested casing `Design.md`. Export from the same authored records as the HTML. Do not claim to recover a full specification by extracting prose keywords or applying category-wide defaults.

## What the UX reviewer contributes

Use the [NN/G heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) as diagnostic lenses, not scores or proof of user success:

| Concern | Product-specific record |
| --- | --- |
| Goal and entry | User task, prerequisite, starting state, discoverable entry and first meaningful value |
| Mental model and choice | Core object, vocabulary, choices, alternatives, defaults and recognition/memory burden |
| Feedback and control | What changes after each consequential action; waiting, cancellation, undo, selected state and agency |
| Recovery and continuity | Failure/permission/interruption branches, retained object, retry cost, return and repetition |
| Completion and trust | Durable result, preview/output agreement, save/export boundary, access/paywall/privacy constraints |
| Inclusion and evaluation | Relevant reachability/legibility/assistive behavior, friction, severity rationale and a falsifying test |

Each important finding needs observation with sources → consequence (hypothesis when untested) → alternative explanation → decision → protocol. The protocol states starting conditions, action, observable pass/fail result and what would reverse the decision. Preserve unknown metrics. The task graph remains complete; highlights support reading, not replace it.

## Reading hierarchy

The interface view shows inspectable imagery, the decisive design observation, a concise element/rule overview and a visible `Design.md` link. The interaction view shows the user goal and consequential UX findings beside the full task graph. The document retains the entire inventory and state/protocol detail.

Every small line must identify the product, explain a decision, qualify evidence or enable an action. Remove repeated chapter indices, decorative English labels, generic instructions, debug-like counts and duplicate platform/category lines from the main area. Keep source access and uncertainty adjacent to the affected claim. Put packaging notes and acquisition metadata in the delivery/source record. Author the reading layer and shared components; do not merely shrink or hide content with CSS.

## Reapply and verify

Update the Skill contract and generator before regenerating the collection. Check each Design.md link, artifact identity, cited evidence, element/state coverage and HTML agreement. Negative tests cover missing sources, measured tokens without methods, absent UX reversal criteria and missing dimensions. Review image-rich, sparse and dense reports at desktop/phone sizes. Report missing runtime evidence separately from successful export.
