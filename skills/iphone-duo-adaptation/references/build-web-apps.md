# BUILD WEB APPS: preferred prototype workflow

Read after the layout baseline and adaptation recommendations are complete, when beginning the HTML stage. The sequence remains **whole-app layout analysis → adaptation recommendations → complete HTML prototype**. BUILD WEB APPS implements and checks the adaptation design; the Duo workflow owns the app's scope, HIG decisions, project contracts, and completion gate.

## Discover the actual contract

1. Look for the installed BUILD WEB APPS package and read its actual `frontend-app-builder` and `frontend-testing-debugging` entrypoints. Discover available plugin capabilities before claiming absence. Sites and similarly named frontend skills are separate workflows.
2. If no installed entry exists, a read-only checkout of its public official source can provide the real instruction Skills. Record repository revision, package version, entrypoint hashes, and that execution used upstream source rather than an installed plugin. Preserve the sole canonical Duo collection and existing discovery links; do not silently install or copy another maintained Skill.
3. If the actual builder cannot be read or a required capability cannot run, record the missing capability and use an equivalent available local construction/QA workflow for independent work. Label fallback checks and unfinished gates accurately.

The [official OpenAI use case](https://learn.chatgpt.com/use-cases/idea-to-proof-of-concept) links to [BUILD WEB APPS source](https://github.com/openai/plugins/tree/main/plugins/build-web-apps). On 2026-10-26, package `build-web-apps` v0.1.2 at commit `0722921d5542fc593105c27bd52630babd8b8c2a` exposed the two entrypoints above. This is provenance, not a permanent version or availability requirement. Read the selected actual contract each time it matters.

## Pass the adaptation design

Select the actual module by the work. For an existing app/design-preserving migration or scoped rendered correction, follow `frontend-testing-debugging`'s existing-design refinement workflow with the original UI as the reference. Use `frontend-app-builder` when an authorized new visual surface or concept is needed. A complete migration can involve substantial implementation while preserving its existing design; implementation size alone does not authorize a new style. Read the selected module's actual requirements and record the chosen route and reason. Do not claim that an unused module or its design-generation phase ran.

Give the selected workflow references to these existing artifacts, keeping their source identity and the populated [pre-implementation handoff](workspace-rules.md#pre-implementation-handoff-gate):

| Input | Required content |
| --- | --- |
| Baseline | App/framework identity; original screenshots, routes, tokens/components/copy, and their source identities; page/state/task coverage; known gaps |
| Recommendations | Current evidence, Apple/framework sources, general/project IDs, decisions and affected components |
| Design | Original UI authority, retain/adapt/change record and permitted deltas, exact required copy/content, tokens, shared components, narrow/wide/low-height behavior |
| Device presentation | Actual Device Hub/simulator or official reference identities; exterior/display calibration, source/capture/logical/CSS scale mapping and unknowns; Closed / PartiallyOpen / Open controls separate from rotation; required main views and active-preview/comparison-card behavior under the [device-presentation contract](device-presentation.md) |
| Behavior | Navigation/back, editing/saving, selection, rich content, overlays, focus and logical reading continuity |
| Acceptance | Named Duo environment matrix, independent task checks, expected visible results, same-page/state original/adapted comparisons, reference identities, stress states, native simulations and unknowns |
| Delivery | Output location, editable local source and HTML/static assets, how to open/build, explicit hosting scope |

Use references instead of duplicating the rule catalog into the build prompt. The workflow's generic website defaults must respect the existing product's information architecture and design. Keep the original single-page stack wherever it works; new columns, icons, toolbars, labels, or features are not mandatory migration outputs. Match the observed hardware wrapper without redesigning the app, deriving shell geometry and visible details from references rather than a generic phone preset. Lead with the active device and compact main-view comparisons; collapse coordinates, stress controls and evidence into a secondary inspector. Attribute optional improvements separately. Scope and user authorization remain authoritative.

## Execute the standard workflow honestly

When `frontend-app-builder` is selected, the inspected v0.1.2 contract requires Image Gen concepts before coding, except an explicit user opt-out or a genuinely small change in an existing design system. A full app adaptation is not automatically that exception. Follow actual conditions; do not invent an exception or add Image Gen to a refinement module that does not require it. Where required, generate enough relevant concepts using original-app references, tasks/content, permitted deltas, and HIG decisions in the brief; inspect them before implementation. Reuse original tokens/components, deriving only necessary new responsive behavior. Concepts remain supplementary and cannot supersede original product authority or authorize gratuitous redesign.

Use the selected builder's actual requirements if they change. In ordinary execution, evaluate and refine the design within the user's authorization; concept-review requests and explicit approval checkpoints retain their stated endpoints. Do not add a conversational approval gate that the current task does not require.

Follow existing project conventions and choose a stack appropriate to the deliverable. The inspected builder defaults complex new interfaces to React + Vite, with exceptions for an existing stack or an explicit static/single-file output. Local state is sufficient for simulated prototype tasks. Database, sign-in, payment, hosted services, and deployment are conditional product requirements, not prototype prerequisites.

Retain build and testing phases even for a buildless prototype: inspect actual files, serve/open the final entry, perform browser tasks, compare screenshots, and fix observed defects. Retain QA artifacts when the task requests validation evidence.

## Rendered and visual verification

Read and follow the available Browser skill/runtime when the selected builder routes to it. The inspected testing contract permits regular Playwright when its Browser plugin/skill is absent, recording `Browser plugin not available`; if a listed Browser path fails, record the actual failure and use only an authorized fallback. Record actual browser capabilities rather than substituting a different product under the same name.

For the inspected builder, functional checks and visual fidelity are distinct:

- Verify URL/title, meaningful content, absence of framework error overlays, console/resource health, screenshot evidence, and real task results.
- Inspect the original-app reference, authorized adaptation decisions, and latest browser screenshot with the available image-viewing tool. Record at least five concrete comparisons, an above-the-fold copy check, and a mismatch ledger; fix material discrepancies and capture again. Compare generated concepts additionally when that route used them, keeping their supplementary status explicit.
- Independently compare final shell/exterior crops to the identified actual device references and inspect the calibration/scale mapping under [device presentation](device-presentation.md). Record physical-posture and independent-rotation results, material mismatches and unknowns. Functional test counts cannot establish device fidelity or app visual quality.
- Check every in-scope layout family and key state across applicable named Duo environments and stress states under [migration review](migration-review.md). Verify physical posture and rotation controls change the actual presentation/app bounds as modeled, maintain one running app state, and keep comparison cards current. A single primary-screen match does not establish complete navigation, state continuity, rich content, accessibility, or all-page coverage.
- Apply [Duo validation](validation.md) independently, including the separated rule ledger. Browser resize and simulated regions do not prove iOS reserved-region, native-bar, keyboard, plugin, or hardware support.

Record builder identity/mode, accepted design and final source hashes, command/tool outcomes, final screenshots, fixes, intentional deviations, and remaining checks. A successful build or deploy alone does not meet these gates. Deliver local source and runnable HTML/static assets; publish only within the user's actual hosting request.
