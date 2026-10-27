# iPhone Duo Adaptation

[简体中文](README.zh-CN.md) · [Agent instructions](SKILL.md)

Adapt an existing iOS app for iPhone Duo while preserving its design.

## Use it

```text
Use $iphone-duo-adaptation to analyze this app and recommend minimal changes.
Deliver a complete interactive HTML prototype with Duo review contexts
and original/adapted browser comparisons.
```

**Provide:** App repository or runnable UI, current screenshots/recordings, and any page or design constraints.

**Receive:** Whole-app layout analysis → adaptation recommendations → complete HTML prototype, with browser evidence and a rule ledger.

Supports SwiftUI, UIKit, Flutter, React Native/Expo and WKWebView shells. Ask explicitly for advice only to stop before HTML. Native implementation/device validation are separate tasks. This is a community skill.

<details>
<summary>Installation (skip if the collection is installed)</summary>

No extra installation is needed with the collection. To install only this skill, clone the repository outside discovery directories and set the path below to that checkout.

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
# Clone here first if you have no checkout:
# git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
CODEX_SKILL_LINK="${HOME}/.agents/skills/iphone-duo-adaptation"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing entry: preserve edits and inspect before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/iphone-duo-adaptation" "$CODEX_SKILL_LINK"
fi
```

Maintain the source; do not copy it into `~/.codex/skills`. Preserve edits and move duplicate copies outside discovery directories when migrating. Refresh Codex if needed and verify one entry. Other agents should retain the complete folder and load `SKILL.md`.

</details>

<details>
<summary>Manual tools and troubleshooting</summary>

## Runtime and evidence

Layout analysis and HTML work do not require Xcode or a device. The rule helper needs Python 3.9+ with no pip packages. Run from this skill directory:

```sh
sh scripts/doctor.sh
```

The agent uses an available builder/browser for the prototype. If unavailable, browser acceptance stays pending. For manual ledger commands, read [workspace rules](references/workspace-rules.md); the agent handles these during normal use.

</details>

[MIT](LICENSE)
