# Workflows and handoffs

[简体中文](workflows.zh-CN.md) · [Documentation](README.md) · [Choose a skill](../README.md#choose-a-skill)

Choose from the user's starting material and requested endpoint. Read the selected `SKILL.md` before recommending, executing or ruling out a branch; names and summaries are only navigation. Preserve existing authorization and usable project files.

## Choose the endpoint

| Request | Entry and first action | Completion signal |
| --- | --- | --- |
| Explain competitors or identify product gaps | [App Competitor Analysis](../skills/app-competitor-analysis/SKILL.md): inventory evidence and attempt acquisition of missing material | Per-app HTML reports and required maps/index, source-linked conclusions, explicit unknowns, audit results and product implications |
| Explore a direction or write image prompts | [Image to Layered HTML Prototype](../skills/image-to-layered-html-prototype/SKILL.md): select the concept/prompt branch | Requested directions or prompts, constraints and selection criteria. Generate images only when that is the requested output; HTML is a separate endpoint |
| Reconstruct approved images | [Image to Layered HTML Prototype](../skills/image-to-layered-html-prototype/SKILL.md): freeze reference identity and establish the page/state contract | Editable pages/assets, manifest, browser captures, required comparisons and honest remaining gaps |
| Repair an existing layered page | Same skill: inventory the current HTML and assets, then scope the repair | Changed region/state verified against the preserved reference and existing contracts; unaffected structure retained |
| Adapt an existing iOS app for resizability | [iPhone Duo Adaptation](../skills/iphone-duo-adaptation/SKILL.md): identify the UI framework, then analyze the whole app's layout before proposing changes | Whole-app findings → Apple HIG-linked recommendations → complete interactive HTML prototype with actual browser evidence; stop earlier only for an explicit audit/recommendation request |
| Create or adjust store covers | [App Store Cover Generator](../skills/app-store-cover-generator/SKILL.md): distinguish a new project from an existing matrix; inventory source/configuration first | Requested cells exported from editable sources, layout/localization checks and final visual review recorded against hashes |
| Build, upload TestFlight or deliver store listing changes | [App Publish Skill](../skills/app-publish-skill/SKILL.md): discover the app's release contract and freeze the requested terminal stage | Evidence for that stage only: signed local artifact, exact upload receipt, allowlisted listing delivery or separately authorized later acceptance/review/public state |

Partial evidence can support a scoped report or concept. It cannot satisfy a missing capture, measurement or review. Report the completed branch and its limitations explicitly.

## App publication

Use App Publish Skill to coordinate an existing app's release by target platform and actual framework: native iOS, Flutter, React Native/Expo with a supported local native project, or native Android. Shared source/baseline/artifact/listing stages stay separate from the framework's local build adapter. First follow its Fastlane setup guide for first-use or missing-runtime cases, then verify Ruby/Bundler, installed project gems and the actual Fastlane version. Discover the project's actual lanes, wrappers, contracts and authorization before choosing commands; lane names and version inputs vary across repositories. A build-only request stops at a verified local artifact. An explicitly authorized TestFlight upload uses local build/signing and project-owned Fastlane/Spaceship, then stops at Apple's successful receipt for the exact IPA/version/build. Keep source commit, artifact hash and provider receipt together. Processing, validity, tester assignment and exact-build installation remain later states; a delayed list does not justify another upload.

Listing work can proceed independently of binary upload when authorized. Freeze text-field and screenshot-file allowlists, preserve protected legal/subscription values, inspect the complete enabled-locale × device × slide matrix, and reread the affected remote state after delivery. Reuse accepted source and artifact evidence instead of rebuilding for a listing-only change. A cover-only request belongs to App Store Cover Generator; pass its exact exports, hashes and review record into the publication stage when upload is requested.

Later exact-build acceptance, review submission and manual public release require their own requested scope and evidence. Check release mode and its public consequence before submitting; do not treat review approval as public availability. Optional Android delivery builds/signs locally and uses the authenticated Chrome Play Console for its authorized track operations. It has its own version, artifact and track checks rather than inheriting TestFlight commands or receipt semantics. Installing the skill, running its doctor or creating an offline candidate proposal performs no app/store operation and grants no publication authority.

## iOS framework resizability adaptation

After the layout inventory, materialize every official-basis rule into the target workspace JSON/Markdown ledger, with applicability, decisions, landing paths and evidence. Keep IDs consistent across design rules, recommendations, HTML and validation; add a conditional Agent-instruction pointer. Native-only rules remain recorded when deferred. Mark another framework's rules not applicable with the identified framework as the reason. Follow the Skill workspace-rule contract and pass its completion check before claiming the default deliverable complete.

Keep general guidance and collection workflow rules separate from app-specific `project_conventions`; record project provenance and corresponding general IDs. The completion gate covers both. IMX examples are conditional project inputs, not defaults for other apps.

The Duo workflow aims to help adapt and optimize the existing application for iPhone Duo. Its analysis, recommendations and complete HTML prototype make the necessary improvements concrete and reviewable. The default workflow identifies whether the UI is SwiftUI, UIKit, Flutter, React Native, or a WKWebView shell, then analyzes that app's overall layout and inventories pages, shared components, navigation, overlays and significant states. It gives recommendations mapped to current Apple iPhone HIG and Duo guidance, then delivers a complete, high-quality, runnable interactive HTML prototype covering that inventory. Keep current-layout evidence, official guidance, the active framework contract and product choices attributable. Only an explicit audit-only or recommendation-only request ends before the prototype. The skill entry and its references define the detailed coverage and quality gates.

At the HTML stage, follow the [BUILD WEB APPS handoff](../skills/iphone-duo-adaptation/references/build-web-apps.md) as the preferred construction workflow. Discover/read the actual contract and record its identity and installed/upstream-source mode, or explain the available fallback. Supply the completed baseline, recommendations, design, coverage, and general/project rules; retain local editable source and runnable output. Apply design fidelity, functional, and visual checks within the requested hosting scope. The Duo Skill and generated rule prose use English.

Follow the [device-presentation contract](../skills/iphone-duo-adaptation/references/device-presentation.md) for source-calibrated device exteriors and display geometry. Keep Closed / PartiallyOpen / Open separate from rotation, use a device-focused opening view and collapsed diagnostics, and review shell fidelity independently from the original app and functional checks.

Use the original app as design authority and choose its smallest necessary migration changes. Freeze populated applicability/decision/planned-target records and adopted project conventions before the first implementation, while verification can remain pending. Follow [migration review](../skills/iphone-duo-adaptation/references/migration-review.md) for retain/adapt/change rationale, named Duo contexts, one persistent app state and same-state before/after evidence; route existing-design refinement through the matching builder contract.

Inspect the HTML in an actual available browser at the relevant widths and interaction states, including navigation, resizing and continuity. Record screenshots and results; without browser checks, HTML acceptance remains pending. Layout analysis and HTML authoring can proceed without Xcode, a simulator, a device, or that framework's toolchain. Prototype evidence does not establish native Duo behavior.

Product implementation and device validation are later stages requested separately; they do not replace the HTML deliverable. For such a request, work in the product repository and use the identified framework's runner, recording actual commands, target/build mode and evidence for affected flows. New Flutter pages require integration coverage through production navigation; SwiftUI, UIKit, React Native, and WebView shells use their own contracts instead of that Flutter gate. Device-sensitive production changes require the framework's production-mode smoke test and physical-device validation where iOS hardware behavior differs. Keep missing native checks pending; an audit, prototype or doctor result does not prove native adaptation acceptance.

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
| Analysis → design direction | Report, evidence links, product constraints, prioritized opportunities and unknowns | Choose the design problem within the user's scope; competitor hypotheses remain hypotheses |
| Direction → reconstruction | Selected design reference and hashes, pages/states, dimensions, assets/fonts and acceptance criteria | A prompt-only request ends before reconstruction. For full reconstruction, missing references or assets remain visible constraints |
| Prototype → app implementation | Editable source, design contract, comparisons and known gaps | Implementation and device verification occur in the product repository; prototype success does not prove them |
| Adaptation prototype → product implementation | Whole-app layout inventory, official-source recommendations, complete HTML source, browser evidence, layout/state decisions and native validation matrix | Requires the user's separate implementation request; run relevant product checks and identify pending device evidence |
| Implemented app → store covers | Actual app captures, app/build identity where available, supported claims, locale/device/slide plan | Label demo/concept material; use actual product evidence for claims and screenshot-based deliverables |
| Cover export → store workflow | Exact PNGs, matrix, hashes, contact sheet and review record | Upload/submission requires its own authorized task and provider checks; an export remains an export |
| Verified local artifact → TestFlight upload | Frozen intent, fresh store baseline, synchronized source commit, artifact identity/hash and passing project checks | Explicit TestFlight scope and project-owned Fastlane; successful exact-artifact receipt ends the upload task |
| Upload receipt → later store stage | Exact bundle/version/build, source commit, artifact hash, receipt and separately reviewed listing assets | Authorize the required acceptance, metadata/screenshots, review or public-release stage; verify its own state without repeating the upload |

Existing projects enter at their current stage. Do not restart them from a template to satisfy the sequence.

## When a capability is missing

Immediately before running a dependent script, use the skill's scoped `doctor.sh`. A concept or reading task does not require the full rendering environment. Follow [runtime support](runtime.md) for installation and repair.

Continue independent work while keeping the dependent step pending. State the missing runtime/package/browser, its repair command and the check to rerun. Use an alternative only when it produces the evidence required by the selected contract; never replace a missing check with an assumed pass.
