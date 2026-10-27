# App Publish Skill

[简体中文](README.zh-CN.md) · [Agent instructions](SKILL.md)

Build mobile apps locally and complete a specified TestFlight or store-listing stage.

## Use it

```text
Use $app-publish-skill to build and upload this app to TestFlight
through its project-owned Fastlane workflow. Stop at the successful Apple
receipt and report the version/build, source commit and IPA hash.
```

**Provide:** App repository, platform/track and exact endpoint: local build, TestFlight upload, listing update or review. Keep signing credentials in approved local configuration.

**Receive:** The requested artifact or store result, exact version/build/source identity, hashes, receipts and remaining checks.

Supports native iOS/Android, Flutter and React Native/Expo through the project adapter. An upload receipt proves uploaded; processing, tester access and public release are separate states. Listing-only work reuses the existing candidate.

<details>
<summary>Installation (skip if the collection is installed)</summary>

No extra installation is needed with the collection. To install only this skill, clone the repository outside discovery directories and set the path below to that checkout.

```sh
APP_DEV_SKILLS_DIR="${HOME}/src/app-dev-skills"
# Clone here first if you have no checkout:
# git clone https://github.com/chensir-indie/app-dev-skills.git "$APP_DEV_SKILLS_DIR"
CODEX_SKILL_LINK="${HOME}/.agents/skills/app-publish-skill"
mkdir -p "$(dirname "$CODEX_SKILL_LINK")"
if [ -e "$CODEX_SKILL_LINK" ] || [ -L "$CODEX_SKILL_LINK" ]; then
  printf '%s\n' 'Existing entry: preserve edits and inspect before changing it.'
else
  ln -s "$APP_DEV_SKILLS_DIR/skills/app-publish-skill" "$CODEX_SKILL_LINK"
fi
```

Maintain the source; do not copy it into `~/.codex/skills`. Preserve edits and move duplicate copies outside discovery directories when migrating. Refresh Codex if needed and verify one entry. Other agents should retain the complete folder and load `SKILL.md`.

</details>

<details>
<summary>Manual tools and troubleshooting</summary>

## Read-only readiness and offline helpers

Run from this skill directory against a trusted project. Helpers need Python 3.9+; the app needs its own build/signing environment.

```sh
sh scripts/doctor.sh --project /path/to/app --platform ios
# For Android, use --platform android.
```

This checks the project tools without building or uploading. Missing Fastlane or gems: follow [setup and recovery](references/fastlane-setup.md). Stage details are in [build/TestFlight](references/fastlane-build-testflight.md), [listing](references/metadata-screenshots.md) and [review/Android](references/acceptance-review-android.md).

</details>

[MIT](LICENSE)
