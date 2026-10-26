# Analysis depth: recover the product, then explain the decision

Read this before detailed analysis or synthesis, and when a report is called shallow. Depth comes from explaining consequential product relationships. Length, graph size, caveat accuracy and an extensive future-test plan do not establish that the product has been understood.

## Recover the product before proposing a model

Begin with the material, not a familiar app taxonomy. Extract the named capabilities, visible controls and values, concrete actions, affected objects and outcomes. Keep atomic capabilities available in the feature tree even when the narrative groups them. A composite label such as “editing” must not erase distinct supported operations.

Separate three relationships:

- **Capability classification:** what operations the product offers and how the analyst groups them.
- **Visible organization:** which controls, categories and objects appear together in an inspected state.
- **Navigation and lifecycle:** what action moves between states, and what survives or commits.

These may disagree. A technical label such as “AI” can describe tools inside several ordinary tasks; it does not establish a separate workspace. A family called “modes” may mix output style, input format, audience and interaction method. Explain those axes before treating the family as interchangeable presets.

Before adopting a headline model, try to disprove it with the strongest available screenshot, entry point or documented path. Inspect the original material again for omitted details: selected categories, value summaries, nested tools, named subfeatures and conflicting terms or prices. Revise the model when a contrary detail matters; do not hide the detail in a source appendix while retaining the old conclusion. Absence from one list is not proof of removal.

For broad studies, deepen and challenge a representative report before scaling. Use comparable questions across products, but retain their actual structures and vocabulary. If a requested core path remains unknown after useful acquisition, make the gap precise and keep the supported analysis; do not invent a complete architecture to fill the report.

## Make the maps describe different relationships

| Map | Useful content | Failure to repair |
|---|---|---|
| Feature hierarchy | Supported capability groups and atomic operations, their prerequisites, objects and outcomes; distinguish analytical grouping from real menu placement | Collapsing distinctive tools into “AI/edit/export,” or adding standard account/cloud modules without evidence |
| Task flow | Acquired actions or documented steps, starting conditions, feedback, result, repetition and recovery where known | Replacing actual button sequences with “select → create → save,” or drawing an unobserved error path as fact |
| Screen relationships | Identifiable screens or visible regions and their supported containment/navigation relationships | Mixing permissions, jobs and hypothetical pages as equivalent nodes; copying the task graph under a new title |
| Technical data flow | Inputs, triggers, transformations, parameters, outputs, state/storage and consumers, with uncertain implementations explicit | Using quality goals or policy promises as if they were data objects; a generic “input → AI → output” chain |

Preserve the steps acquired from recordings, official tutorials or authorized static paths. Cite their screen, timestamp or locator and retain meaningful control names. Distinguish these evidence types; a tutorial is not a performed runtime test. Stop a path where its evidence stops. A conceptual relationship may be useful, but must explain its analytical purpose instead of pretending to complete navigation.

When only isolated screens are known, show their visible structure and route breaks. Do not imply that a sequence of unrelated promotional images establishes movement between them. A complete inventory of known material can coexist with an incomplete navigation model.

## Develop findings from the recovered product

Explain the competitor first. Recommendations and unperformed experiments belong after the finding they depend on, rather than replacing it with “the system should” or “we need to test.”

| Part of a finding | What the reader can inspect |
|---|---|
| Evidence and mechanism | Exact region, state, step or call path; the choice, object, constraint or data contract it establishes |
| Explanation | Why that mechanism may affect the task, the assumption linking cause and outcome, and a plausible alternative where uncertain |
| Cost and boundary | Who benefits under what conditions, and the effort, flexibility, resources or failure risk this imposes |
| Decision and unresolved discriminator | What changes for the user's product, and which missing observation would reverse that choice |

This is a reasoning discipline, not a template to repeat under every caption. An observed control, an inferred rationale and a proposed design can support one argument without sharing a certainty label. Cite claims beside the relevant clause or row; a chapter-level source list does not make all its reasoning factual.

### UI: explain what the control communicates

Read the region's role and current state, not only its appearance. A label plus a selected value can let a user inspect a setting without reopening its panel; a large preview may carry the object being edited while a smaller comparison preserves the input. Explain what competes for attention, what remains visible and what is deferred. Geometry, typography, color and spacing support that account.

Name the actual choices and values that matter. Preserve uncertainty about dynamic behavior without discarding static information already visible. Marketing decoration and an embedded UI fragment serve different purposes; neither establishes unseen defaults, navigation or measured touch targets.

### Interaction: explain changes to objects

Trace the task through actions and feedback, then explain what is selected, edited, temporarily accepted, durably saved or ready for another attempt. Keep conditions and state inheritance concrete. “Which parameters persist?” is a research question; it becomes a finding only when answered by a recorded transition or a clearly bounded inference from evidence.

Accounts, permissions and payment matter at their location relative to value and work already invested. A list of possible failures is not an interaction teardown. Prioritize the missing transition that could change the product model rather than expanding an undifferentiated test matrix.

### Technology: explain the work required by a capability

Separate classification, retrieval, segmentation, geometry, restoration, generation and rendering when they perform different jobs. Trace concrete inputs and outputs; explain which parts of the result should change and which should remain stable. Distinguish a disclosed implementation, a necessary capability constraint and a plausible architecture.

If several architectures can produce the observed result, explain their different implications for latency, consistency, offline use or cost. Do not name a private model or intermediate representation without evidence. A policy can bound a data use without establishing execution order or a dependency. Keep quality requirements and deletion/retention promises as annotations unless the evidence establishes actual operations in the path.

## Use incomplete evidence without substituting a research plan

Perform useful authorized acquisition using [evidence-acquisition.md](evidence-acquisition.md), then separate:

- **Answered:** the product-specific behavior, structure or capability established by the material.
- **Reasoned:** the conditional mechanism and alternatives that explain it.
- **Unanswered:** the exact observation needed to distinguish alternatives or continue the path.

“Unknown; needs testing” alone wastes evidence. Conversely, a longer table of hypothetical failures does not deepen a finding. Put detailed experiments and acquisition history in their own section; the analysis should still teach the reader something about this product.

## Compare mechanisms that could change a choice

Compare the same user job under sufficiently similar conditions: preparation versus repeated effort, selection versus automatic behavior, local completion versus remote work. Explain which constraint favors each approach. Keep principles already chosen for the user's product separate from decisions newly supported by this competitor. Repeating “simplify UI” or “preserve user work” does not show what the new evidence changed.

## Original worked example: challenge a plausible classification

This fictional audio-editor exercise is original teaching material, not a competitor finding or performed test. Suppose the supplied records are:

- **E1 — depicted editor:** the selected “Repair” tab contains “AI noise removal,” “De-click” and “Level.” A separate “Generate” tab is visible. The closed Level control reads “−3 dB.”
- **E2 — official tutorial excerpt:** from a selected clip, open Repair, choose De-click, preview, then Cancel. The tutorial shows the same clip selection after cancellation. It stops before export.
- **E3 — product description:** it names noise removal, de-click, loudness adjustment and music generation.

**Shallow:** “The product has editing and AI workspaces, offers clean controls, and should preserve drafts and export reliably.”

**Evidence-based analysis:** E1 contradicts the idea that all AI work is segregated: an AI-labeled tool sits inside Repair, while Generate is a separate category. The supported distinction is between repairing an existing clip and generating content, not AI versus non-AI. E3 supplies separate atomic operations; collapsing them into one “audio enhancement” feature would lose meaningful coverage.

The Level control exposes its value while closed, so it carries state as well as opening an action. This may reduce repeated panel opening to inspect the setting; live updates and cross-session persistence remain unknown. The visible value still belongs in the UI explanation.

E2 establishes a documented preview-and-cancel path returning to the selected clip. Keep those control names and that return edge. It does not establish undo history, saved drafts or successful export, so the diagram ends at the returned clip. Music generation remains a separate declared capability with no observed route connecting it to that clip.

For an original voice-note product, the useful choice is whether cleanup belongs on the current recording while generation has a different content-creation entry. That follows from the task/object distinction. Copying every tab, or putting all AI controls in one place, does not follow. A future comparison can investigate discoverability, but it is not needed to recognize the hierarchy already visible in E1.

## Review depth before delivery

Begin with the main claim, not the chapter checklist:

- **Counterexample:** which inspected pixel, entry or source detail most challenges the headline model? Reconcile it in the model and conclusion.
- **Source-to-report:** did grouping erase named capabilities, current values, actual steps or meaningful source conflicts? Can the reader distinguish real UI organization from the analyst's taxonomy?
- **Product explanation:** can the reader describe the competitor's task and consequential mechanism without reading the proposed implementation or future tests? If not, acquire or explain more; do not lengthen the test plan.
- **Decision and evidence:** what choice changes because of this product's evidence? Removing a material source should change the associated conclusion; substituting another app name should not leave every finding intact.
- **Cross-section and table roles:** each section adds a different explanation. A table row is one argument: its benefit and cost belong to the same mechanism, rather than unrelated lists zipped together.
- **Map and dependency:** follow one object through the supported path. Separate conditions, screens and objects; distinguish input from output, containment from navigation, and temporal/policy statements from data dependencies. Preserve evidence breaks.

Automated repetition, coverage and graph checks can direct review. They cannot establish causality, verify source support or certify depth. Record the findings actually reviewed and the unresolved path separately from structural and browser validation.
