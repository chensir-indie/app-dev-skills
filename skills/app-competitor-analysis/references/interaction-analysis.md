# Core interaction and state

Start with a user intent and a concrete terminal result: a saved photo, exported document, accepted order, completed lesson, etc. Define entry and finish before counting steps or discussing friction.

Apply [analysis-depth.md](analysis-depth.md). Explain the decisions and persistent objects that produce the flow, including their costs and conditions; a sequence of page names is descriptive, not sufficient interaction analysis.

## Follow the task

Retain concrete steps obtained from recordings, official tutorials or authorized call paths: control names, start conditions, observed/documented feedback and source locators. Do not replace them with generic verbs when formatting the report. An official tutorial establishes a documented route, not a test performed by the analyst.

Use a state table or graph with these fields where supported:

| State/context | User action | System work | Visible feedback | Next state / durable result | Evidence and unknowns |
|---|---|---|---|---|---|

Inspect first use versus repeat use; what must happen before value; what the user chooses versus what happens automatically; whether the main action changes meaning; and whether a successful attempt leaves the user ready for another task. Explain the available path before proposing how it should work. Stop where the source stops; a guessed save, return or retry edge does not complete the teardown.

Cover the most consequential alternatives, proportionate to the request and evidence:

- Empty versus populated, loading versus ready, canceled versus failed.
- Permission denied, unavailable hardware/network, interrupted operation, retry and return.
- Free versus paid entitlement, anonymous versus logged in, first versus repeat session.
- Selection stability, edits/drafts, undo and preservation across navigation/backgrounding.
- Actual persistence/export versus an animation, toast or transient preview.

Do not run a huge device matrix or intentionally destructive failure campaign just to fill a template. Mark unobserved branches and choose the one most likely to change the product decision.

## Recover the core object and invariant

Ask what persists while operations repeat: reference, project, draft, cart, transaction or session. What updates it, clears it, commits it, or restores it? What must remain independent?

For example, “choose a target once, perform multiple attempts” is a reusable mechanism; “always skip photo review” is a product-specific choice. Explain lifecycle and dependency rather than just counting screens.

Test the proposed task model against actual containment and entry points. A tool using the same technology as another tool can belong to a different user task; a category called “mode” may combine style, input format and audience. Closed controls may expose the selected value or object, making state inspectable without opening the panel. Separate those visible facts from unknown persistence or reset behavior.

Keep runtime routes, documented routes, static paths and analytical reconstructions distinguishable. Conditions such as entitlement are not screens. When only isolated screens exist, map their visible regions and mark route breaks rather than chaining hypothetical workspaces. Label supported edges with trigger and condition, distinguish optional work, and explain which object survives. Task and screen graphs describe different relationships.

## Friction and outcome

Distinguish effort to find the feature, decide, enter data, wait, correct mistakes and recover. Count only observed interactions under stated conditions. Distinguish perceived waiting (an interaction hypothesis) from measured latency (timed observation with start/end, conditions and sample count).

Assess whether the interface teaches the task, preserves context, supports repetition and makes successful completion discoverable. Do not infer completion rates, retention or preference without suitable user/telemetry evidence.

Output the supported flow and states first, then explain strengths and friction hypotheses. Keep recommendations and targeted next checks separate. Expanding the list of unperformed failure tests does not substitute for understanding a known transition.

## Visible UX review

For a detailed report, apply [the UX concern and finding contract](design-specification.md#what-the-ux-reviewer-contributes). Show the user goal, consequential choices, feedback/completion and recovery in the reading layer; provide the concrete observation, alternative explanation, decision and falsifying protocol in the same record. Keep complete task diagrams and existing technical analysis.
