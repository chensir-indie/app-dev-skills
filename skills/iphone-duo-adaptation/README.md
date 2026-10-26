# iPhone Duo Adaptation

[Agent workflow](SKILL.md) · [Compatibility documentation entry](README.zh-CN.md)

The goal is to **help adapt and optimize an existing application for iPhone Duo**. Identify its UI framework, then follow **whole-app layout analysis → adaptation recommendations → complete HTML prototype** to make the necessary improvements concrete and reviewable while preserving the original design.

Supported UI frameworks are SwiftUI, UIKit in Swift or Objective-C, Flutter, React Native including Expo, and WKWebView shells such as Capacitor, Cordova, Ionic, uni-app, and Taro. Compose Multiplatform, .NET MAUI, and Unity are identified and keep the shared HIG and HTML path; their engine APIs are not invented here.

This is a community workflow, not Apple's exported Skill. It distinguishes official guidance, framework contracts, engineering inferences, product choices and actual test results. A split layout or navigation rail is a choice to evaluate against your task.

The original app is the primary design reference. Default to the smallest changes needed to migrate all existing pages and tasks: preserve working hierarchy, styling, tokens, components, copy and behavior. Record retain/adapt/change decisions and compare the same original/adapted page and state. Extra space alone does not require a split view, new toolbar, new icons, restyling or business features. See the [minimal migration and pose-review contract](references/migration-review.md).

## Provide the current app

Supply the project, current screenshots/recordings or a runnable UI, and any scope constraints. The default covers all known pages, navigation, shared components and relevant states. Layout analysis comes before redesign: retain what works and explain each adaptation from current evidence through HIG guidance to its prototype behavior.

```text
Use $iphone-duo-adaptation with this existing iOS app.
Identify whether its UI is SwiftUI, UIKit, Flutter, React Native, or a WebView
shell. Analyze the overall layout across all pages, then recommend adaptations
based on Apple's iPhone HIG. Deliver a complete interactive HTML prototype
covering the app's pages and tasks, with real browser checks and visual review.
```

Unless you explicitly ask only for analysis or advice, the final HTML is required. It should behave like the adapted app, with working navigation, primary tasks and state-preserving narrow/wide transitions; a report website or a few polished screens do not satisfy the default. Product-source implementation, SDK upgrades and native/device validation are later tasks when requested.

## Preferred HTML construction with BUILD WEB APPS

After the baseline and Apple-linked adaptation decisions, follow the [BUILD WEB APPS handoff](references/build-web-apps.md). Read its actual `frontend-app-builder` and `frontend-testing-debugging` Skills and use them for design, implementation, rendered testing and screenshot comparison. Record the selected package/revision and entrypoint identities. This package keeps its own instructions, references, catalog and helper self-contained; it does not vendor or install the external builder.

Select the actual existing-design refinement/testing route for design-preserving migration; use the creation route when a new visual surface is authorized. The inspected creation contract includes Image Gen requirements and documented exceptions, while ordinary rendered refinement uses the original UI as its reference. Pass page/state coverage, `Design.md`, populated rule decisions and exact content into construction, freezing that handoff before implementation. Generated concepts cannot silently replace original design authority. Deliver editable local source and runnable HTML/static assets; hosting is separately scoped. Record unavailable-builder fallback accurately and retain the same quality gates.

Follow the [device-presentation contract](references/device-presentation.md) when collecting the actual Device Hub/simulator reference, calibrating display geometry and reproducing the exterior. Physical Closed / PartiallyOpen / Open states remain separate from rotation. Lead with a large active device and current-state comparison cards; keep diagnostics and stress controls in a collapsed inspector. Verify the shell, original-app design and interaction independently.

The complete prototype exposes applicable outer-display orientations, inner portrait/landscape, app-left/app-right multitasking and partial-fold contexts through review controls outside the app. Keyboard/text/overlay states are separate stress controls. Keep one running app instance and task state across mode changes, measure actual container reflow, and label assumed geometry/native limits. Include original-versus-adapted evidence for the same page/state; a generic narrow/wide demo or decorative device frame alone is insufficient.

## Materialize every rule in the app workspace

After the whole-app layout analysis, follow the [workspace-rule contract](references/workspace-rules.md). Every rule from the canonical catalog is copied into a project ledger with applicability, decisions, landing files and evidence; its Markdown is generated from the same JSON. Native-only items can be deferred with reasons. Add a conditional pointer to the project's Agent instructions and apply design rules to its existing Design.md and HTML.

Keep reusable guidance in the catalog and app-specific scope or business behavior in the ledger's `project_conventions`, with attributable project sources and parent rule IDs. See [project conventions](references/project-conventions.md); the six-point IMX example is optional and is not imported into other apps. Both sections participate in the completion check. The contracts cover the full layout baseline, HTML delivery, rich content, region data, accessible tasks and exact evidence identity.

```sh
python3 scripts/workspace_rules.py init --workspace /path/to/app
# Update the project bindings in workspace-rules.json, then:
python3 scripts/workspace_rules.py render --workspace /path/to/app
python3 scripts/workspace_rules.py check --workspace /path/to/app --complete
```

Default files live in `docs/iphone-duo-adaptation/`. Use `--output-dir` for the project's existing relative output location. Existing records are preserved; pending records do not count as implemented or verified. If Python is missing, install a supported version from [python.org](https://www.python.org/downloads/), reopen the terminal and rerun the preflight. No pip packages are required.

## Install from one source

For Codex, prefer the [collection link](https://github.com/chensir-indie/app-dev-skills#1-connect-codex-to-one-source-checkout). An existing collection link discovers this skill automatically; no second installation is needed.

To expose only this skill, clone the repository outside discovery directories, set its absolute path and preserve any existing entry:

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
CODEX_SKILL_LINK="${HOME}/.agents/skills/iphone-duo-adaptation"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing entry: compare and preserve edits before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/iphone-duo-adaptation" "$CODEX_SKILL_LINK"
fi
```

Use the source checkout for edits. Compare earlier collection or individual entries in both `~/.agents/skills` and `~/.codex/skills`, preserve edits, and move superseded copies outside discovery directories. Refresh Codex discovery or open a new session and verify one entry resolving to the source `SKILL.md`. Examples use macOS/Linux or WSL.

## Runtime and evidence

From the skill directory:

```sh
sh scripts/doctor.sh
```

The read-only default preflight checks Python 3.9+ for the standard-library workspace-rule tool and installs nothing. Use `sh scripts/doctor.sh --scope instructions` for reading without Python. It does **not** test browsers, HTML quality, a UI-framework toolchain, Xcode or a device. This package bundles no rendering runtime. Build and review the HTML with the agent's available browser tools or the project's existing tooling; browser and visual checks remain pending if unavailable. Xcode and a Duo device are not prerequisites for layout analysis or HTML creation.

Skill instructions, invocation metadata, references, catalog/example prose and generated rule Markdown are maintained in English. Product UI copy and localization still follow the target app and the user's requested language. The legacy `README.zh-CN.md` entry is retained for packaging/link compatibility and points to this English documentation.

The [official basis](references/official-basis.md) records sources, SDK distinctions and how to optionally export Apple's Skill. SwiftUI and UIKit read reserved regions from the current view. Flutter's documented `displayFeatures` support must be checked for iOS before claiming the same data. React Native and page CSS do not receive that region unless the project has a verified bridge. Simulated sizes and Android foldable data do not establish Duo platform support.

Read [framework identification](references/frameworks.md) and [whole-app layout analysis](references/layout-analysis.md), then the [HTML prototype contract](references/html-prototype.md) and [validation](references/validation.md). The default delivery includes the identified framework, current-layout coverage, a complete workspace-rule ledger, attributable HIG recommendations, an editable `index.html` with relative assets, and actual browser/visual evidence. Read the matching framework contract for feasibility questions or later authorized app changes: [SwiftUI and UIKit](references/apple-frameworks.md), [Flutter](references/flutter-adaptation.md), [React Native](references/react-native.md), or [WebView shells](references/webview-shells.md). Product validation uses that framework's toolchain; HTML results do not establish native support.

Original workflow files use [MIT](LICENSE). Referenced Apple, Flutter, React Native, Expo and MDN materials retain their own terms and are not redistributed here.
