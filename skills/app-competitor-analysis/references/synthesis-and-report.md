# Cross-app synthesis and reporting

Apply [analysis-depth.md](analysis-depth.md) before writing comparisons. A shared rubric makes questions comparable; it does not justify the same answer for every product.

## Breadth first, then justified depth

Build an identity inventory of the requested set, including unknown or inaccessible items. Do not count aliases, platform editions or cropped content variants as independent products/actions without stating the unit. Keep historical/unavailable leads separate from verified-current listings.

Group by user job and mechanism, not by identical feature names. Select deeper samples that answer different questions: a direct competitor, an adjacent task specialist, a platform baseline, or a different approach to the same outcome. There is no mandatory app count. Explain selection and coverage so the reader can see what was omitted and why.

Use the same questions across samples, but permit unequal evidence depth. Compare mechanisms that address the same job, showing which effort or risk each transfers to preparation, repeated operation, recovery or infrastructure. State when each approach is preferable and the condition that makes it fit the user's product. Do not give weakly evidenced products invented scores to make a ranking look complete.

## Synthesis dimensions

- Target user, context and promised outcome.
- Task entry and first value; preparation versus repeated operation.
- How content/data is obtained, structured, selected and refreshed.
- What stays stable while the user works; how corrections and failure recovery work.
- Design system and attention hierarchy supporting the task.
- Technical dependencies, computation/data boundaries and operational constraints.
- Entitlement and commercial interruptions; not speculative revenue claims.

## Adopt, adapt, defer

For each proposed decision record the supporting finding(s), fit to our user/task, conditions required, cost/tradeoff and smallest discriminating validation. Explain what possible result would reverse or alter the decision. “Another app has it” is insufficient; so are category-wide recommendations such as “simplify the interface” without saying which state, operation or choice changes.

Separate:

1. Category baseline the user reasonably needs to complete the task.
2. Differentiation that may make the product useful over that baseline.
3. Optional expansion that costs attention, implementation or operations.

A calm interface often comes from state hierarchy, not deleting useful functionality. A feature-rich competitor may serve another job or business model. Avoid turning the synthesis into a union of all visible controls.

## Report quality

Lead with the decision-relevant conclusion, then evidence. Keep observation, explanation and recommendation distinguishable. Link source IDs near important claims. Explicitly state the inspected material and major untested paths.

Preserve per-product depth in the final delivery: each identity gets its own complete HTML report; the multi-app index organizes and links those reports. Follow [html-delivery.md](html-delivery.md). A combined comparison page does not replace the individual reports, and Markdown/JSON are supporting inputs.

For each requested and supported dimension, give concrete visual rules, a task/state model or a technical data flow as appropriate. A list of app names plus marketing features does not satisfy a detailed teardown. Conversely, a huge token catalog without user-task implications is not a product analysis. Apply the change-app-name and cross-section checks: retain shared principles in synthesis, while individual reports explain their specific evidence, mechanism and consequence. Do not fill multiple chapters by paraphrasing the same recommendation.

End with a small ordered set of decisions and observations that could change them. Missing evidence should be actionable: “record the first export with library permission denied, then verify the file” is more useful than “more testing needed”. Do not automatically implement, clone, publish or release the proposed changes.
