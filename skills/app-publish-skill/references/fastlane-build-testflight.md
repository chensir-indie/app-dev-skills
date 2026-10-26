# Local builds and TestFlight

Use this reference for new candidates, local IPAs and TF uploads. Listing copy/screenshots or review of an existing build does not enter the new-build flow.

## 1. Environment and project preflight

On first use, missing/unrunnable Fastlane or incomplete locked dependencies, complete [Fastlane detection and installation](fastlane-setup.md). Distinguish command presence, complete project dependencies, runnable project Fastlane and passing release preflight. `bundle --version` does not replace `bundle check` and project `bundle exec fastlane --version`.

Inspect the actual wrapper, Fastfile and call chain first. Use `bundle exec fastlane lanes` or `bundle exec fastlane action <action>` only after checking that top-level/initialization logic has no external writes. Listing lanes must not accidentally authenticate, build or trigger network side effects.

Record current Ruby/Bundler/Fastlane, Xcode/SDK and framework-required Flutter, Node/package manager or JDK/Gradle versions. Check the project's Gemfile.lock, Podfile.lock, pubspec.lock, JavaScript lockfile or Gradle wrapper as applicable. Require only tools the selected adapter uses; non-Flutter projects do not need Flutter. Restore dependencies from project lockfiles and fix missing local-preflight dependencies locally. Intermediate runtime/proxy/checksum logs are not terminal failure evidence and must not trigger a second task.

The project should contain current `release/release-policy.yaml`, `docs/release-contract.md`, `.env.testflight.example`, and an Android release environment example when Android is supported. Shared checker names are:

```sh
ruby scripts/check_release_contract.rb
sh scripts/test_release_contract.sh
sh scripts/release_contract_preflight.sh
```

Read arguments and side effects before running. `check` validates the contract, `test` validates checker behavior, and `preflight` validates this candidate; they are not interchangeable. Reuse identical checks already run by the wrapper rather than repeating expensive tests for formality. Rerun affected checks when final source/inputs change.

## 2. Fresh baseline and candidate identity

Use the project's Fastlane/Spaceship for authenticated read-only evidence: correct Apple team/app/platform, public marketing version, latest uploaded marketing version, **highest uploaded build across every version train**, query time and raw evidence. `latest_testflight_build_number` for only the current marketing version does not establish the platform-wide maximum. Cover pagination and project API-visible pending uploads. Stop allocating a build if query coverage is incomplete, another upload for this bundle is pending/unknown, or the baseline conflicts with the local attempt ledger.

Apply this workspace's schema-2 decision:

| Condition | Next candidate marketing version | Next build |
| --- | --- | --- |
| Latest uploaded > public | Reuse latest uploaded `A.B.C` unchanged | Platform-wide maximum + 1 |
| Latest uploaded = public | Increment public patch by 1 | Same global increment |
| Latest uploaded < public, missing or ambiguous | Reject and obtain a complete baseline | Do not allocate |

This is a workspace policy, not an Apple-mandated version algorithm for every app. A first release without a public baseline must not invent `0.0.0`; use an explicit first-release policy supported by the project contract. The offline helper rejects empty baselines.

The store baseline must be no older than 30 minutes when deciding the candidate, changing version identity, starting the build and before uploading. If a long build exceeds that window, obtain one fresh **baseline read** before upload to confirm that the candidate remains the valid next build and is unoccupied. This is not a post-upload TF-list query, and expiry does not itself justify incrementing the build. Another upload or source change invalidates the candidate: stop and replan.

Freeze release intent/public baseline, bundle/platform/track, target branch, source commit, version/build, feature/data commits and endpoint. If the project requires a committed manifest version, complete the scoped version change, validation, commit/push and final-source proof first. Runtime inputs cannot override contradictory committed identity. For hotfixes, separately verify that the source base comes from the user-specified public version; version arithmetic does not decide hotfix ancestry.

## 3. Source, signing and runtime verification

- Fetch the relevant remote and prove exact equality between `HEAD` and the target remote ref, beyond a clean worktree. Verify required commits are ancestors. Record actual commit/ref rather than an old tag or remembered branch.
- Reuse a suitable checkout; create a worktree only when isolation is needed. Run the applicable shared worktree checker first. A historical-only worktree cannot be patched and reused for packaging: prepare a clean release checkout from a commit already containing current contracts.
- Validate ignored environment files, `.p8`, certificates/profiles/entitlements, extension bundles, team, export options and relative paths. Worktrees do not automatically include ignored files. Do not put secrets in Git to repair missing files.
- Do not automatically revoke/recreate certificates or change team, signing capabilities or subscription configuration. Use the authorized project signing method and existing managed API key without printing it. Treat new account/permission/key requirements as actual missing capabilities.
- Run framework-specific narrow tests, production-configuration/Release smoke tests and hardware gates; Flutter also covers Profile. Native/React Native test entrypoints, Release configurations and production-navigation checks follow their own contracts, not Flutter `integration_test`/`kDebugMode` rules. Without required physical-device evidence, do not claim the fix complete. If it is an upload prerequisite, keep upload blocked rather than “uploading to try.”
- For client configuration affected by domain migration, retain the legacy endpoint until DNS/TLS/provider control-plane states are terminal and health, authentication-boundary and non-sensitive real-canary checks pass.

If the build changes tracked project files, lockfiles or generated configuration, the frozen source identity is invalid. Stop upload, review/include necessary changes in a new pushed commit, then rerun preflight and build. Do not record the old commit while uploading a mixed-source artifact.

## 4. Build once and verify the exact artifact

Identify platform/framework before selecting the existing project build/beta wrapper. Fastlane orchestration/upload does not depend on Flutter; the corresponding adapter builds the binary:

| Actual stack | Local build adapter | Project facts to preserve |
| --- | --- | --- |
| Native iOS Swift/SwiftUI/UIKit/Objective-C | Project `build_app`/gym or managed Xcode archive/export | Workspace/project, shared scheme, Release configuration, targets/extensions, signing and export options |
| Flutter | Managed `flutter build ipa` or verified local wrapper | Pinned SDK, flavor/entrypoint, Dart defines, plugins and native iOS project |
| React Native bare / Expo with a native project | Restore locked JavaScript/native dependencies, then local Xcode workspace/scheme archive/export | Node/package manager, JS bundle/assets, native modules, Pods, Release configuration and environment |
| Expo without a buildable native project | Confirm support and authority to generate/maintain the native project before using a local Xcode adapter | No unapproved overwriting prebuild, no substituting EAS cloud build for local packaging; record missing adapters |
| Other frameworks or exported projects | Project-verified native/export adapter | Verify exports, native project, configuration and final artifacts; do not claim Unity, MAUI, KMP and others have all been exercised |

See the [Android branch](acceptance-review-android.md#android-enter-only-when-that-platform-is-requested) for Kotlin/Java, Flutter and React Native/Expo APK/AAB routing. One build produces one exact artifact. If Flutter or another adapter already produced a verified IPA, do not rebuild it again with gym. Preserve verified lanes rather than rewriting them to match a template.

If a Fastlane adapter is missing, implement/test project-owned lanes within authorized code scope before release. If project-code changes are unauthorized, deliver the missing capability and a reviewable implementation proposal. Do not replace the production contract with bare `pilot upload`, browser upload or a temporary script.

Before upload, unpack the final IPA and record:

- Main-app and extension bundle IDs, `CFBundleShortVersionString`, `CFBundleVersion` and minimum OS;
- Signing team/certificate, profiles, entitlements and required capabilities;
- Embedded domains, feature flags, required assets and database schema/version/tables/counts;
- Old-database migration/merge tests and ancestry of required feature/data commits;
- Source commit, absolute IPA path in project records, SHA-256, archive/dSYM locations.

Read values from the `.app`/final IPA. Source manifests, input Info.plists, pubspec, app config, logged build arguments and asset declarations are not substitutes. Report configuration conclusions without exposing keys, credentials in endpoints or customer data.

## 5. Fastlane's upload receipt boundary

The project upload lane explicitly selects the one verified IPA. This illustrates properties to audit, **not a complete implementation to paste over a project lane**:

```ruby
ENV.delete("PILOT_CHANGELOG")
upload_to_testflight(
  api_key: managed_api_key,
  app_identifier: candidate_bundle_id,
  ipa: verified_ipa_path,
  skip_waiting_for_build_processing: true,
  skip_submission: true,
  distribute_external: false,
  notify_external_testers: false
)
# No changelog / localized_build_info and no further TF/Build-list read.
# The project binds Apple's reception evidence to this candidate and IPA SHA.
```

Audit defaults/environment injection for executable `altool`, processing waits, implicit changelog values, subsequent list reads, beta review, distribution or App Review side effects. `skip_waiting_for_build_processing:true` with a changelog may still wait for the build to appear; clearing `PILOT_CHANGELOG` is part of the contract.

Once Fastlane/Transporter returns Apple's successful receipt for the exact IPA, save bundle, version/build, source commit, SHA, success time and available upload/delivery ID, then immediately report `UPLOADED`. ASC build ID may be null; do not query the list to fill it. Explicitly authorized multistage work treats later exact-build acceptance as a separate stage without changing this upload endpoint.

## 6. Efficiency and recovery

| Situation | Response |
| --- | --- |
| Repeated full cleans/repository updates are slow | Measure time; reuse lockfiles and project-verified caches/DerivedData/Pods. Clean only when justified, without deleting mandatory project checks |
| Missing backend/TS dev dependencies fail preflight | Restore local dependencies from their lockfile; do not skip checks or blame Apple |
| Ruby gem/ffi contamination | Use pinned project Ruby/Bundler and verified isolation; avoid ad hoc global gem upgrades affecting other apps |
| Upload process is still retrying/checksumming | Observe that process/logs; do not start another upload or treat intermediate output as terminal failure |
| Timeout/disconnect/killed process leaves reception unknown | Preserve attempt/log/IPA/SHA, stop automatic retries and reconcile through independent read-only evidence; list absence does not prove non-reception |
| Success receipt exists but list is delayed | Upload is complete: no rebuild, build increment or re-upload |
| Metadata/screenshots need retry | Reuse the same candidate, read remote state first and retry only confirmed incomplete authorized differences |

Resume the same unuploaded artifact under existing authority only with clear non-reception evidence, no active upload process and permission from the project deduplication ledger. Do not skip build numbers or create another candidate just to retry.

## Official sources

Checked 2026-10-26: [pilot upload options](https://docs.fastlane.tools/actions/upload_to_testflight/), [build_app/gym](https://docs.fastlane.tools/actions/build_app/), [API-key support](https://docs.fastlane.tools/app-store-connect-api/), [React Native native iOS publication](https://reactnative.dev/docs/publishing-to-app-store), [Expo local native projects/builds](https://docs.expo.dev/guides/local-app-development/). The last two explain framework native/Release artifacts; actual upload still follows this skill's project-owned Fastlane contract rather than copying browser/manual upload routes. Check the locked project's actual behavior; upstream capability does not prove correct project implementation.
