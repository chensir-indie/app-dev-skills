# Workflows and handoffs

[简体中文](workflows.zh-CN.md) · [Choose a skill](../README.md#choose-a-skill)

Choose from the user's starting material and requested endpoint. Read the selected `SKILL.md` before recommending, executing or ruling out a branch; names and summaries are only navigation. Preserve existing authorization and usable project files.

## Choose the endpoint

| Request | Entry and first action | Completion signal |
| --- | --- | --- |
| Explore a direction or write image prompts | [Image to Layered HTML Prototype](../skills/image-to-layered-html-prototype/SKILL.md): select the concept/prompt branch | Requested directions or prompts, constraints and selection criteria. Generate images only when that is the requested output; HTML is a separate endpoint |
| Reconstruct approved images | [Image to Layered HTML Prototype](../skills/image-to-layered-html-prototype/SKILL.md): freeze reference identity and establish the page/state contract | Editable pages/assets, manifest, browser captures, required comparisons and honest remaining gaps |
| Repair an existing layered page | Same skill: inventory the current HTML and assets, then scope the repair | Changed region/state verified against the preserved reference and existing contracts; unaffected structure retained |
| Create or adjust store covers | [App Store Cover Generator](../skills/app-store-cover-generator/SKILL.md): distinguish a new project from an existing matrix; inventory source/configuration first | Requested cells exported from editable sources, layout/localization checks and final visual review recorded against hashes |

Research supplied from an earlier task can inform a design concept; it is an input to these two skills. Partial evidence cannot satisfy a missing capture, measurement or review. Report the completed branch and its limitations explicitly.

## Pass artifacts between stages

Use a compact note in the existing report/project. Link the files rather than copying all their contents:

```text
Requested next outcome:
Artifact paths + identities/hashes (when files are frozen):
Source, version/date, viewport and interaction state (where relevant):
Observed facts / declared claims / inferences / unknowns:
Completed checks + evidence files:
Remaining gaps + next concrete action:
```

Keep existing schema/status fields authoritative. The handoff is navigation to evidence, not a new approval step or replacement manifest.

| Transition | Carry forward | Next-stage condition |
| --- | --- | --- |
| External research → design direction | Report, evidence links, product constraints, prioritized opportunities and unknowns | Choose the design problem within the user's scope; research hypotheses remain hypotheses |
| Direction → reconstruction | Selected design reference and hashes, pages/states, dimensions, assets/fonts and acceptance criteria | A prompt-only request ends before reconstruction. For full reconstruction, missing references or assets remain visible constraints |
| Prototype → app implementation | Editable source, design contract, comparisons and known gaps | Implementation and device verification occur in the product repository; prototype success does not prove them |
| Implemented app → store covers | Actual app captures, app/build identity where available, supported claims, locale/device/slide plan | Label demo/concept material; use actual product evidence for claims and screenshot-based deliverables |
| Cover export → store workflow | Exact PNGs, matrix, hashes, contact sheet and review record | Upload/submission requires its own authorized task and provider checks; an export remains an export |

Existing projects enter at their current stage. Do not restart them from a template to satisfy the sequence.

## When a capability is missing

Immediately before running a dependent script, use the skill's scoped `doctor.sh`. A concept or reading task does not require the full rendering environment. Follow [runtime support](runtime.md) for installation and repair.

Continue independent work while keeping the dependent step pending. State the missing runtime/package/browser, its repair command and the check to rerun. Use an alternative only when it produces the evidence required by the selected contract; never replace a missing check with an assumed pass.
