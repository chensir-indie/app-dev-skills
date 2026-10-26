# Official basis and workspace rules

The previous overall check of general guidance was **2026-10-23**; mainstream UI-framework sources were added on **2026-10-26**. Each source retains its own catalog check date. This reference does not maintain a second prose copy of the rules. Stable IDs, kinds, phases, applicability, workspace actions, verification methods, and sources live in [official-rules.json](../assets/official-rules.json).

## Materialize the complete catalog

After whole-app layout analysis, read the [workspace-rule contract](workspace-rules.md) and materialize the **complete catalog** in the target app workspace as a JSON ledger and generated Markdown. Record actual applicability, design/implementation decisions, landing files, and evidence. Add a conditional short pointer to the project's Agent entrypoint. Analysis, recommendations, Design.md, HTML, and acceptance share rule IDs; HIG links alone do not establish application of the rules.

Apply layout/design rules first to the recommendations and complete HTML. Native-only implementation rules may be deferred with reasons while remaining in the ledger. Generated records do not establish implementation or verification. Preserve the distinction between product choices and Apple requirements. Structural and completion checks are defined in the workspace contract.

## Sources and verification

The catalog's `sources` is the single maintained source registry: general iPhone HIG, Duo HIG, Prepare, the native-bar talk, SwiftUI/UIKit region documentation, React Native/WebView layout documentation, and Flutter API/adaptive guidance. `SKILL-*` sources identify this collection's contracts; their relative paths resolve from the catalog's `assets/` directory. HTML sequencing, framework routing, preferred construction workflow, and evidence gates are collection policy. App-specific business semantics belong to [project conventions](project-conventions.md). Each rule references source IDs and check dates. Recheck decision-relevant material online during adaptation; record changes and update the catalog rather than presenting an old check as current guidance.

This is an original multi-framework iOS workflow, not Apple's official Skill. It does not redistribute or relicense Apple's text. Framework identification and contracts are in [framework identification](frameworks.md). The official export was successfully exercised with Xcode **27.1 (27A9275)** on 2026-10-23. When native guidance is needed, retrieve it again using the local help:

```sh
xcodebuild -version
xcrun agent skills export --help
xcrun agent skills export --output-dir /tmp/apple-skills
```

Read the actual exported `app-resizability/SKILL.md` and relevant references. Export, Xcode, and devices are not prerequisites for layout analysis or HTML; their applicability and evidence boundaries remain in the catalog.
