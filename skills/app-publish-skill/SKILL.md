---
name: app-publish-skill
description: Coordinate local Fastlane builds, signing, TestFlight uploads, store metadata, screenshot artwork and review for iOS and Android apps. Route native, Flutter and React Native/Expo projects through their actual adapters and verify Fastlane readiness. Packaging authority does not imply upload or public-release authority; use the cover skill for artwork-only requests.
---

# App Publish Skill

Organize publication into stages that can be executed, verified and resumed independently. Reuse the project's verified Fastlane, signing and artwork tools. Historical versions, lane names and success records are discovery clues; current project contracts, actual authorization and live store state govern execution.

Distinguish the **target platform** from the **UI/application framework**. Swift/SwiftUI/UIKit/Objective-C, Flutter, React Native/Expo and Android Kotlin/Java each use the project's actual local build adapter. Versioning, source identity, final artifacts, metadata, screenshots and upload receipts share the stage contracts. See the [build adapter table](references/fastlane-build-testflight.md#4-build-once-and-verify-the-exact-artifact). Other frameworks require a verified native/export adapter; an ability to export an Xcode/Gradle project alone does not establish support or acceptance.

## Establish the requested endpoint

Identify the app, repository, platform, track and authorized endpoint from the current request and existing conversation; record the specific authorization. Read project facts before asking for information available there. Ask only for unresolved information that affects execution. A request only to summarize, plan or create a skill produces documentation/the skill without operating an app or store.

| Request | Completion boundary | Required reference |
| --- | --- | --- |
| Build/package a local IPA/APK/AAB | Verified locally signed artifact and `BUILT` evidence | iOS: [build and TestFlight](references/fastlane-build-testflight.md); Android: [its platform branch](references/acceptance-review-android.md#android-enter-only-when-that-platform-is-requested) |
| Upload to TF / TestFlight | Apple's successful receipt for the exact artifact, `UPLOADED`, then return | Same build reference |
| Check processing, distribute tests or accept a candidate | Independently reconcile the exact candidate and verify the requested state | [Acceptance, review and Android](references/acceptance-review-android.md) |
| Prepare/upload metadata | Reviewed copy; with upload authority, remote verification of explicit fields | [Metadata and screenshot artwork](references/metadata-screenshots.md) |
| Create/upload store screenshot artwork | Complete asset matrix and visual review; with upload authority, per-locale remote rereads | Same metadata reference |
| Submit App Review | Successful submission of the exact candidate/materials, retaining manual release | [Acceptance, review and Android](references/acceptance-review-android.md) |
| Deliver Android testing/store stages | Locally signed package, authenticated Chrome Play Console operations to the authorized track endpoint | Same acceptance reference |

If an ambiguous request to “publish” does not distinguish TF, review or public availability, complete reversible preparation and identify the unresolved endpoint. Existing explicit authorization remains valid: add no repeated per-step, per-locale or pre-upload confirmation. For an unauthorized new stage or protected field, first prepare a concrete reviewable result, then request only the missing authority.

## Workflow

1. **Discover the stack and environment.** Determine the platform, framework, local native project and toolchain from current project files, dependencies and documentation. Read `AGENTS.md`, `docs/release-contract.md`, `release/release-policy.yaml`, `Gemfile.lock`, the actual Fastfile/wrappers, artwork contracts and receipts. On first use, a missing/unrunnable Fastlane or incomplete dependencies, read [Fastlane detection and installation](references/fastlane-setup.md). Resolve the actual Gemfile/Fastfile working directories, bundle ID, target/scheme, signing and lane parameters. Label commands as local, Apple read-only, TF upload, metadata, screenshots or review. Inspect and prefer an existing wrapper; do not impose one argument signature on every app.
2. **Create the release record.** Use the project's format or the [evidence contract](references/evidence-contract.md) to freeze intent, public baseline, latest uploaded version, platform-wide highest build, exact source, track and endpoint. Metadata/screenshot-only work binds an existing candidate without creating a binary candidate.
3. **Prepare independent work concurrently.** Environment/dependency diagnosis, copy drafts and design templates can run in parallel. Final candidate captures depend on frozen identity; signing, building, upload and submission follow dependency order. Multiple agents/processes must not compete for one bundle/platform build sequence or upload.
4. **Execute the current stage.** Use the build reference for builds/TF, the metadata reference for copy/assets, and the acceptance reference for later acceptance/review. Inspect lane implementation: a lane's presence or a passing guard is neither authorization nor proof that it meets the contract.
5. **Record the result and stop at the endpoint.** Report the completed state, exact identity, evidence paths, unverified states and blockers. The TF receipt ends the upload task. Continue to a later independent stage only when the task explicitly includes it.

## Shared constraints

- **Separate authority:** Judge TF, tester distribution, metadata, screenshots, legal/subscription fields, review and public release separately. One request may explicitly authorize multiple stages; do not ask again. TF must be named; code completion or packaging alone does not authorize a TF upload.
- **Local builds:** Build/sign Apple archives/IPAs and Android APKs/AABs locally. Do not trigger or recreate GitHub Actions packaging, signing, TF or store-upload workflows unless the user explicitly overrides this rule for that release.
- **Project-owned Fastlane:** Use the project's Fastlane/Spaceship for Apple TF baseline reads, signing, upload and later exact-build reconciliation. Do not upload, approve or confirm TF through App Store Connect/Chrome, including as a fallback after preflight fails.
- **Source gate:** A new binary candidate requires a clean, pushed release worktree whose `HEAD` exactly equals the target remote branch; required feature/fix/data commits must be ancestors. Ahead/behind/diverged states block. For listing-only work, verify the existing candidate's source and freeze current materials with allowlists/digests/review; do not invent a rebuild or a requirement to commit working materials. Stricter existing project contracts still apply. Do not “commit everything” to conceal uncertain scope.
- **Current contracts:** In workspaces adopting this collection's historical policy, the target worktree itself must contain schema 2, `reuse_testing_else_patch_public` and the current receipt-boundary uploader. Read [workspace adapters and historical lessons](references/workspace-adapters.md), then run applicable shared checkers and project preflight. Historical worktrees lacking the contract are evidence only; do not patch them in place to bypass the gate and build.
- **Artifact gate:** Inspect the final package actually being uploaded. A manifest or source declaration does not establish inclusion of assets/databases. Version/build, signing, configuration, assets, schema/counts and migration checks are independent.
- **Runtime gate:** Run the framework's narrow regressions and production-configuration/Release smoke test. iOS rendering, sharing, plugins, signing, lifecycle and hardware-sensitive fixes require exact-build physical-device verification. Flutter additionally checks Profile/Release; new pages require `integration_test` through production navigation. Native/React Native projects use their own production-navigation and test contracts, not Flutter commands. Packaging existing code alone does not create a new-page test requirement.
- **Debug APIs:** Verify debug/assert/test-only production-path APIs against the actual framework contract. For Flutter, distinguish Debug/Profile/Release; guard relevant render diagnostics with `kDebugMode && ...` or return before evaluation, rather than only using `kReleaseMode`. Other frameworks use their corresponding compile/runtime conditions.
- **Credentials:** Reuse ignored configuration, Keychain or managed secrets. Check referenced paths, permissions and readability without printing contents. Keep raw credentials out of commands, tool arguments, reports and Git; do not extract Chrome passwords, cookies or tokens. Environment files do not store version/build identity or cached store baselines.
- **Recovery:** Identify the failed stage; invalidate only affected gates. Metadata/screenshot failures do not rebuild the IPA. Unknown reception preserves the attempt, IPA, hash and logs; stop automatic retries and reconcile independently. List delay does not justify another upload.

## Bundled tools

Set `SKILL_DIR` to the actual loaded skill directory and `PROJECT_ROOT` to the target repository. Do not confuse them.

```sh
sh "$SKILL_DIR/scripts/doctor.sh"
sh "$SKILL_DIR/scripts/doctor.sh" --project "$PROJECT_ROOT" --platform ios
# Explicitly select a project-local entry for a monorepo or multiple adapters:
sh "$SKILL_DIR/scripts/doctor.sh" --project "$PROJECT_ROOT" --fastlane-dir "$FASTLANE_DIR"
python3 "$SKILL_DIR/scripts/release_evidence.py" plan --baseline "$BASELINE_JSON" --output "$PROPOSAL_JSON"
python3 "$SKILL_DIR/scripts/release_evidence.py" verify-artifact --artifact "$IPA_PATH" --expected-sha256 "$IPA_SHA256"
```

Default doctor checks only the package and Python. `--project` actually checks Ruby/Bundler versions, `bundle check` and project `bundle exec fastlane --version`, or an existing no-Gemfile standalone setup; it does more than inspect PATH. It neither installs, authenticates, builds nor uploads, and does not replace release preflight. Follow [installation and recovery](references/fastlane-setup.md), then rerun the same check. `plan` is an offline proposal from a supplied normalized baseline: it does not query a store, reserve a build, validate Git or confer authority. The result still requires project preflight. Hash verification checks file bytes, not IPA contents. See the [evidence contract](references/evidence-contract.md) for inputs, freshness and evidence.

## Reporting

Report exact observed states, times and evidence:

`BUILT` → `UPLOADED` → `PROCESSING` → `VALID` → `DISTRIBUTED_INTERNAL` → `TESTER_VERIFIED`; track review separately as `SUBMITTED_FOR_REVIEW`, `IN_REVIEW`, `APPROVED_HELD`, `PUBLIC`.

This is not an automatic execution chain. Each transition needs its own scope, authority and new evidence. Record copy/assets separately as `prepared`, `reviewed`, `uploaded/saved`, `remote_verified`. `VALID` does not prove distribution; grouping does not prove installability; submission does not prove public availability. Apple public release defaults to owner-manual, and this skill provides no automatic public-release lane.

Delivery includes the completed endpoint; app/platform/bundle/version/build/source commit; artifact/material SHA-256; Apple receipt or store operation ID; actual checks and limitations; and remaining gates. Mark unsupported states unverified rather than assuming success.
