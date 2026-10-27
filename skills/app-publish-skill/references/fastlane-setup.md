# Fastlane detection, installation and project setup

Read this reference on first project use, missing runtimes or doctor failure. Establish that **Fastlane runs in the selected project environment**, then independently check signing, accounts and release preflight. A global `fastlane` executable does not establish availability of the project's Gemfile.lock dependencies.

## 1. Discover the existing environment

Read project release documentation/wrappers to identify the actual framework, target platform, Ruby selection method and Gemfile/Gemfile.lock/Fastfile directories. Inspect `.ruby-version`, `.tool-versions`, mise configuration or wrapper-declared Ruby, preserving existing version/dependency conventions. Some projects use managed standalone Fastlane; do not force a migration for consistency alone.

Report three separate levels:

| Level | Evidence required | Does not establish |
| --- | --- | --- |
| Executable available | Ruby/Bundler/Fastlane actually start and return versions | Complete project dependencies |
| Project runnable | Dependency check and locked Fastlane version command succeed in the correct Gemfile context | Signing, Apple-account access or upload eligibility |
| Release ready | Project preflight, authenticated read-only baseline, signing, source/artifact and tests pass | Authority for an unapproved later stage |

From the actual skill directory:

```sh
sh scripts/doctor.sh
sh scripts/doctor.sh --project "$PROJECT_ROOT" --platform ios
```

Bundled helpers require Python 3.9+ with no pip packages; app builds need the project toolchain. Default doctor checks only the package and Python. `--project` performs actual Ruby/Bundler/Fastlane checks. Use it only against a trusted project because Bundler evaluates its Gemfile/configuration. For multiple adapters or a monorepo, explicitly select the **directory containing Fastfile**:

```sh
sh scripts/doctor.sh --project "$PROJECT_ROOT" --platform ios \
  --fastlane-dir "$PROJECT_ROOT/apps/mobile/ios/fastlane"
```

Use `--platform android` to avoid imposing the same repository's iOS/Xcode requirements on an Android task. Doctor detects relevant native, Flutter and React Native/Expo tools from actual project markers. Other framework export tools require their own project adapter/preflight; generic doctor success does not validate every framework build.

Distinguish Fastlane failures from SDK failures. Missing Xcode/Flutter/JDK blocks a binary build that depends on it, not independent copy/artwork preparation. Metadata-only API work verifies its actual Fastlane/authentication needs without requiring unrelated build SDKs. Doctor checks the project toolchain; an overall nonzero result does not always mean Fastlane is absent.

For a Gemfile project, the conceptual check order is:

```text
ruby --version
bundle --version
bundle check
bundle exec fastlane --version
```

Actual commands select the installed locked Bundler, correct working directory and `BUNDLE_GEMFILE`. Diagnostic mode freezes the lock, disables implicit dependency installation and Fastlane update checks, and runs no lane. Existing no-Gemfile standalone projects use `fastlane --version` and receive a warning about missing Gemfile pinning evidence.

Doctor does not run `bundle install`, `fastlane init`, lanes, signing or store login. Existing executables that fail version checks, miss gems, have incompatible versions or time out produce a nonzero result. Report safe summaries and repairs rather than complete Bundler errors, `.bundle/config`, `.env` or other potentially credential-bearing diagnostics.

## 2. Existing Gemfile: restore locked dependencies

Dependency installation writes locally and downloads files; keep it separate from read-only doctor and within the requested environment-preparation/publication scope. A skill-editing-only task does not install host tools or modify an app. Activate the existing project Ruby first; check Gemfile Ruby constraints, lockfile `RUBY VERSION`/`BUNDLED WITH` and Fastlane version rather than forcing another gem environment through system Ruby.

Reuse existing rbenv/mise/asdf rather than installing another manager or overwriting global shell configuration. Once the required Bundler is confirmed missing, install its locked version under the selected non-system Ruby:

```sh
gem install bundler --version "$BUNDLER_VERSION" --no-document
```

Obtain `BUNDLER_VERSION` from the reviewed Gemfile.lock/project contract, not “latest.” Prepare the chosen Ruby manager through its official installation route. Identify specific administrator/system-configuration needs rather than bypassing failures with `sudo gem install`, global `gem update --system` or disabled certificate verification.

Restore dependencies from the **Gemfile directory**, then return to this skill directory and rerun the same doctor for locked-Bundler, correct-cwd, dry-run and no-auto-install checks:

```sh
bundle install
# After returning to this skill directory:
sh scripts/doctor.sh --project "$PROJECT_ROOT" --platform ios
```

For an existing lock, prefer `bundle install` to restore its dependency set, rather than `bundle update` to re-resolve the tree. If the release candidate requires an unchanged lock, apply the project's frozen configuration to installation too; stop and investigate a mismatch. Review Git differences before/after installation and include only authorized necessary dependency/configuration changes. Restore the clean/pushed release-source gate after dependency preparation.

Do not print `.bundle/config` or the full environment to diagnose paths: private gem-source credentials may be present. Report only pass/failure, versions and safe paths.

## 3. First project setup or missing Fastlane

Distinguish an existing project missing installed dependencies from one without Fastlane configuration. Gemfile projects use the preceding recovery flow rather than adding a global installation because the global command is absent. Existing managed standalone projects first reuse their specified runtime/version.

For a new project or an explicit release-automation setup request, prefer managed Ruby + Bundler; official guidance also provides macOS Homebrew. Ruby support changes by Fastlane version: check current official setup and target-gem requirements without imposing the newest upstream requirement on an existing historical lock. [Official Fastlane setup](https://docs.fastlane.tools/getting-started/ios/setup/)

Within authorized project-configuration scope, create a minimal Gemfile with the reviewed Fastlane version constraint, run `bundle install`, then review and track Gemfile/Gemfile.lock. Modify only necessary dependencies in an existing Gemfile. Preserve existing Fastfile/Appfile and add only missing adapters rather than reinitializing over them. Missing configuration may be created manually as managed lanes. If choosing `bundle exec fastlane init`, inspect its interactive options first to avoid extra remote-app creation, downloads or metadata synchronization.

For an existing macOS Homebrew standalone approach:

```sh
brew install fastlane
FASTLANE_SKIP_UPDATE_CHECK=1 FASTLANE_OPT_OUT_USAGE=1 fastlane --version
```

This is a standalone installation branch, not a fallback execution path for a broken Gemfile project. Use Bundler when exact project versions are required. Check existing installation before installing; do not default to `brew upgrade`, reinstalls, global gem upgrades or changing project pins.

## 4. Platform and framework setup

- **Apple:** Local archive/export requires full Xcode, required SDKs and the selected developer directory; Command Line Tools alone do not establish iOS archive capability. With existing Xcode, check `xcodebuild -version` against project needs before installation/selection. Flutter, React Native and Expo additionally restore their locked SDK/Node/Pods dependencies. Native Swift/UIKit does not need Flutter.
- **Android:** Use the project's JDK, Android SDK and Gradle wrapper. Check Java and wrapper files first. `gradlew` may download Gradle, so do not run it inside read-only doctor; dependency preparation/building follows the locked toolchain separately. Fastlane may orchestrate local Gradle but does not replace this workspace's Chrome Play Console authorization/upload route.
- **Other frameworks:** Locate the project's local export/native adapter, establish consistent framework-export and native-package identity, then reuse shared Fastlane/material stages. Fastfile presence alone does not validate that framework's build/export.

## 5. Verify authority and signing after installation

`fastlane --version` establishes startup only. Under the actual project lane contract, subsequently verify app/team/bundle, managed API key or Apple ID session, signing certificates/profiles/entitlements, current store baseline and roles. Reuse managed authentication first and verify actual action support for API keys. API keys and app-specific passwords have different capabilities: ability to upload a binary does not establish metadata or tester-distribution access. [Apple authentication methods](https://docs.fastlane.tools/getting-started/ios/authentication/)

Inspect top-level/Fastfile initialization even for a read-only baseline lane. Do not run an upload lane to “test installation.” Respect real login/2FA/security boundaries and extract no browser authentication material.

## Failure branches

| Observation | Next action |
| --- | --- |
| Ruby missing/incompatible | Activate or install the required Ruby through existing project management, then recheck; leave system Ruby intact |
| Bundler command or locked Bundler missing | Install the matching Bundler under selected Ruby, rather than another global Fastlane first |
| `bundle check` reports missing gems | Run locked `bundle install` from the Gemfile directory, then recheck |
| Global Fastlane works, project `bundle exec` fails | Project remains unready; repair dependencies/cwd/Ruby rather than uploading through the global version |
| Multiple root/ios/android/monorepo adapters | Select by target platform and actual lane through `--fastlane-dir`; do not guess |
| Correct paths/versions but native gem/ffi cannot load | Restore project Ruby architecture and gem isolation without broad global changes affecting other apps |
| CLI works but authentication/signing fails | Record a separate later-gate failure; reinstalling Fastlane does not repair account/certificate problems |

## Official basis

Checked 2026-10-26: [iOS setup](https://docs.fastlane.tools/getting-started/ios/setup/), [Android setup](https://docs.fastlane.tools/getting-started/android/setup/), [Bundler project dependencies](https://guides.rubygems.org/using_bundler_in_applications/), [bundle check behavior](https://guides.rubygems.org/command-reference/bundle-check/), [Bundler configuration](https://guides.rubygems.org/command-reference/bundle-config/). Verify option support against current project pins and tool versions during execution.
