# Core technology: explain the mechanism with bounded claims

Apply [analysis-depth.md](analysis-depth.md). The technical explanation must account for a product behavior through concrete data contracts and candidate mechanisms; naming familiar frameworks or repeating “implementation unknown” cannot substitute for it.

## Trace capabilities

For each mechanism that matters to the user task, map:

`input → trigger → preprocessing → local/remote work → output contract → state/cache/storage → UI or external consumer`

Identify where optional processing, permissions, entitlements, failures and retries enter this chain. Distinguish capability presence from the particular path that consumes it.

Useful questions:

- Does the input contain pixels, text, labels, identifiers, embeddings or only metadata?
- Is the result a retrieved record, generated image/text, geometric target, score or saved artifact?
- Who initiates work: explicit action, stable change, timer, background event, every frame?
- Is preparation reusable? What invalidates it? Are there stale/canceled results or races?
- Which data stays local, leaves the device, persists, or is discarded? Separate policy claims from observed/code-supported transfers.
- Does failure preserve the user's work? Can a success notification occur before durable completion?
- What is the minimum technology needed for the visible behavior? Is a simpler implementation also plausible?

For AI products, separate classification, retrieval/ranking, generation, segmentation, geometric matching and rendered overlays. “AI-powered” does not identify any of them. An attractive target image does not establish on-device generation, and a score does not establish aesthetic quality.

## Static inspection

Use only artifacts available under the task's authority. Inspect identity and hashes before linking a conclusion to a package. Locate the entry/caller, input, transform, output and consumer, not just a suggestive string. Track tool limitations, protected/missing code, decompiler uncertainty, dead/stub branches and version scope.

If the original binary is unavailable, cite its acquisition record, hash the inspected derivatives, and state who established the binary-to-derivative association. Do not claim to have reverified the original binary or its signer. Keep useful derivative findings within that provenance boundary.

For recovered low-level code, confirm encoding and units before reporting numeric specifications. Tagged integers, field offsets, unresolved enums and dynamic calls are not self-describing pixel sizes, state names or formulas.

Stop deep tracing when the decision-critical path reaches its consumer and its most consequential recovery branch is understood. List other paths as gaps unless they could change the decision; a detailed teardown need not become a whole-package audit.

A linked SDK/model establishes presence, not use in the main feature. A resource label may be obsolete. A method named “score” may not calculate a score. A client request establishes what the client sends; a server's algorithm, prompt or retention cannot be recovered solely from its endpoint name. Negative findings are bounded by the searched paths, patterns, versions and tool coverage.

Do not bundle competitor binaries, recovered code, credentials or private captures into the reusable skill. Link local evidence from private project reports; use original/synthetic minimal fixtures for portable validation.

## Hypothesis table

| Capability | Evidence-supported behavior | Candidate mechanism | Plausible alternative | Distinguishing test | Product consequence |
|---|---|---|---|---|---|

If several mechanisms produce the same UI, leave the implementation unresolved. Explain which constraint each architecture would impose on the user's task, and what evidence distinguishes them. For example, a displayed result may come from retrieving a stored item, composing existing elements or generating new content; these imply different update, consistency and availability questions. Do not assert any path from the result alone. Recommend a prospective implementation separately from reverse-engineered claims. A useful hypothesis can still guide engineering as long as its assumptions and falsification are visible.

Performance claims need a defined operation, start/end events, device/build/network/cache/thermal conditions, timing method and sample count. Source constants, animation durations or processing-frame counts are not observed latency. Distinguish cold/warm paths when the decision depends on them.

Offline availability needs the specific operation, prior cache/download state and failure behavior. A cached catalog does not prove all media/models are cached. Permission declarations do not prove data use, and “no network observed” in a short run does not prove universal offline privacy.
