# App Publish Skill validation — 2026-10-26

## Scope and sources

Created the independently installable [app-publish-skill](../skills/app-publish-skill/SKILL.md) in the canonical collection. Its revised platform-first flow routes native iOS, Flutter, React Native/Expo and native Android through their actual local build adapters, then coordinates receipt-bound TestFlight upload, localized metadata, screenshot covers, later exact-build acceptance and App Review; Android store operations use Chrome. It preserves current project contracts and existing authorization instead of creating another uploader or requiring repeated confirmations. The initial creation checks below precede the same-day framework/runtime revision recorded at the end.

Read-only source review covered AppOperations `AGENTS.md`, `docs/release-safety-playbook.md`, `docs/store-creative-contract.md` and shared checkers; the current release policies, contracts, wrappers and Fastfiles in NextNote, natureid, animalplant, yingjian and PoseGenius; and the installed Apple release/cover-generation skill contracts. Historical rollout evidence and NextNote `docs/releases/app-store/1.1.12-174.md` and `1.1.11-173.md` supplied dated examples, not current store baselines. The skill's [workspace reference](../skills/app-publish-skill/references/workspace-adapters.md) marks those examples and audited implementation limitations explicitly.

Checked official [pilot](https://docs.fastlane.tools/actions/upload_to_testflight/), [Deliver](https://docs.fastlane.tools/actions/upload_to_app_store/), [gym](https://docs.fastlane.tools/actions/build_app/), [API-key support](https://docs.fastlane.tools/app-store-connect-api/), [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) and [App Review guidance](https://developer.apple.com/app-store/review/guidelines/) on this date. These are documentation checks, not exercised live service behavior.

No product application, release script, signing material, account configuration or store was modified. No app was built, uploaded or submitted. Existing unrelated collection changes were retained; nothing was committed or pushed.

## Packaging and executable checks

| Check | Observed result |
| --- | --- |
| Skill Creator `quick_validate.py` | PASS |
| Collection metadata, links, standalone packaging | PASS |
| Default doctor | PASS on Python 3.9.6; standard library only |
| Project doctor against NextNote and natureid | PASS for shallow root/ios-layout and tool availability; no authentication or secret reads |
| New helper/doctor behavior tests | 13 PASS, also registered in root test discovery |
| Root Python suite | 215 PASS |
| Cover-generator Node suite | 44 PASS |
| Layered-prototype Python suite | 83 PASS |
| Actual Codex app-server `skills/list` | `forceReload:true`; seven enabled collection skills, one canonical entry each, no errors |
| Existing discovery link | Target/inode/mtime unchanged |
| `git diff --check` | PASS |

The helper rejects missing/stale/future/ambiguous baselines, inconsistent public/uploaded versions, invalid global builds and duplicate JSON keys. It preserves existing proposal output unless explicitly overwritten, and rejects changed artifact bytes. Doctor tests cover unavailable/old Python and an incomplete standalone package. A proposal is marked `PROPOSAL_ONLY`; a hash match is never described as artifact-content validation or provider acceptance.

Actual discovery used only a temporary local stdio app-server initialization and `skills/list`; it created no chat, changed no configuration and inspected no credentials. Machine-local evidence is retained under ignored `.test-output/app-publish-skill/`, including `discovery.json` and check logs.

## Independent forward-testing

Two independent agent runs read the actual completed package and used isolated synthetic artifacts. Their fixture outputs were retained under `.test-output/app-publish-skill/forward-test-testflight/` and `forward-test-metadata/`.

| Realistic request and supplied evidence | Observed behavior |
| --- | --- |
| Upload TF; public1.2.9, uploaded1.3.0, globalmax210; actual native lane parameters; old schema2 worktree still uses `altool --wait` | Helper proposed1.3.0(211), preserved native parameter routing, rejected historical uploader, and verified synthetic file SHA |
| Same TF request with exact successful receipt, but ASC list entry missing | Stopped at `UPLOADED`, no refresh/rebuild/increment/re-upload; ASC build ID may remain null |
| Same request with disconnected upload and no receipt | Kept attempt/artifact/hash/log, reported unknown reception and prohibited automatic retry based on list absence |
| Update/upload nine-language descriptions and covers, no review; historical captures explicitly authorized | Reused existing candidate, kept Terms footer/privacy bytes, staged description-only fields, and avoided new IPA |
| Old screenshot lane covers84 cells; requested matrix162 cells; old verifier counts only | Identified78 missing cells, rejected the old lane as a complete uploader, required full locale/device/order/visual verification |
| Missing review bound to this final copy/export hash | Kept screenshot upload pending while completing review autonomously; did not ask for a redundant per-post or per-locale approval |

The runs found two wording problems that were corrected: the clean/pushed source gate now clearly applies to a new binary candidate, while listing-only work freezes its own files; supported restricted parameters/staging can be used within existing upload authorization, while actual project-code changes still follow the owning repository's scope. A third clarification prevents treating a global worktree-checker failure as passed merely because the operator selects another checkout.

These runs exercised offline reasoning, fixture inventory and helper bytes, not real PNG visual acceptance, Fastlane execution, signing, Apple/Play writes, device installation or public delivery.

## Whole-collection limitation

Plain `npm run check` stopped because the configured Playwright headless Chromium executable was absent. Using the documented installed-browser route, `PLAYWRIGHT_CHANNEL=chrome npm run check`, passed runtime, docs and unit tests, then failed the existing `tests/competitor_html.browser.cjs:69` image-framing test: the portrait fixture bottom was outside the 1000px card, with measured offset `-95.96875`. Eight of nine root browser cases passed. The later workspace browser suites were not reached by that chained command.

That competitor renderer/test was outside this change and was already present in the working tree. It was not modified to make the publication-skill check appear green. The full collection check therefore remains failed; the new skill's focused checks, actual discovery and independent scenarios passed.

## Same-day revision: framework routing and real Fastlane setup

The user clarified that publication must not be limited to Flutter and asked for Fastlane installation checks and installation procedures. The scope/metadata, both standalone and collection READMEs, workflow/runtime docs and build adapters now identify native iOS Swift/SwiftUI/UIKit/Objective-C, Flutter, React Native/Expo and native Android Kotlin/Java/Gradle separately. Other frameworks require a verified project export/native adapter. Framework routing is an instruction contract, not a claim that every framework has been built on a device.

Added the self-contained [Fastlane setup reference](../skills/app-publish-skill/references/fastlane-setup.md): discover existing pins/runtime, distinguish global installation from a working project bundle, restore locked dependencies with Bundler, offer the Homebrew standalone branch, and verify again before independent signing/authentication gates. It avoids reinstalling an existing setup, broad dependency updates and automatically overwriting native projects. Pure documentation or skill edits do not trigger host installation.

The former `--project` doctor checked executable presence, which was insufficient. The revised implementation actually checks Ruby, the lockfile's exact installed Bundler, safe effective Bundler settings, frozen/dry-run dependency availability, and project `bundle exec fastlane --version`. It prevents implicit installs or lock resolution during diagnostics, rejects ambiguous adapter directories, supports explicit monorepo selection and `--platform ios|android`, and removes another project's Bundler context from standalone checks. It does not execute a lane. Flutter detection checks command presence without potentially bootstrapping the SDK; Android checks Java and wrapper presence without executing/downloading Gradle. SDK failures remain distinct from Fastlane installation failures and do not block independent copy preparation.

| Revised check | Observed result |
| --- | --- |
| Focused helper/doctor suite | 28 PASS; failure fixtures were run before implementation fixes |
| Root Python suite | 230 PASS |
| Existing cover Node/prototype Python suites | 44/83 PASS |
| Skill/collection validation, default doctor and whitespace | PASS |
| Actual Codex discovery | Seven enabled canonical entries; new framework/runtime description present; link unchanged |
| Whole collection with installed Chrome | Runtime/docs/unit stages passed; same existing image-framing assertion failed, eight of nine root browser tests passed |

New fixtures cover a runnable global Fastlane masking a broken project bundle, missing gems, exact Bundler mismatch, config overriding frozen/no-auto-install, missing lock, timeout, root/ios/android/explicit monorepo directories, unrelated package.json, native/RN without Flutter, Android without Xcode, nearest application manifests, and no SDK bootstrap. Logs are retained under ignored `.test-output/app-publish-skill/doctor-*.log` and `framework-runtime-full-check.log`.

An independent final run used temporary stub tools against the completed code: native Swift with missing project gems returned1 without falling back to global Fastlane; RN Android with an iOS directory but no Flutter/Xcode returned0; nested monorepo RN with missing Node returned1. Exact Bundler routing and safe-settings probes were exercised, lock hashes stayed unchanged, and no lane or Gradle/Flutter command ran. The retained evidence is `.test-output/app-publish-skill/setup-final-review/`.

Read-only host observations also found globally runnable Fastlane2.238.0. The revised NextNote check correctly returned nonzero in the current shell: selected Ruby2.6.10 could not activate the project's locked Bundler4.0.11. The existing project may select a different runtime through its wrapper; this diagnostic does not claim that runtime or the project is broken. The old shallow project-doctor PASS above is historical, and is not a current runtime acceptance claim. No host dependencies or App configuration were installed/changed to make this check pass.
