# Workspace adapters and historical lessons

Applicability: the target project adopts MyBusiness cross-workspace release contracts, or its AGENTS explicitly references equivalent rules. These are read-only audit clues from 2026-10-26, not an executable command checklist. Reread the owning source before execution. Discover project locations from the active session/workspace rather than hardcoding a user's directory.

## Shared check entrypoints

Discover/read these in AppOperations:

- `AGENTS.md` and `docs/release-safety-playbook.md`;
- `scripts/check_release_worktree_contracts.sh`: run before selecting a release worktree; currently registers NextNote, animalplant, natureid and yingjian;
- `scripts/check_testflight_upload_boundary.rb`: actual non-waiting Fastlane receipt-boundary implementation contract;
- `docs/store-creative-contract.md` and `scripts/check_store_creative_contracts.sh`: three-app `store-creative-v1` contracts and entrypoint links.

Run current release preflight in the mobile project. Schema 2 is necessary but insufficient: inspect the active uploader. Executable `altool`, processing waits, upload changelogs or a missing receipt boundary make that worktree historical-only. New apps absent from the shared registry are not implicitly covered; directly check their contract and applicable current boundary-checker invocation.

A shared checker may exit nonzero because other historical worktrees remain registered. Record each blocked path and the target checkout's individual result; switching checkouts does not establish a globally passing checker. Do not modify/delete historical registrations to manufacture success or disregard project requirements. If the applicable gate requires a global pass and still fails, keep build/upload blocked and report exact paths.

Run relevant shared checkers after changing shared contracts or mobile entrypoints. Creating this skill without changing those entrypoints does not require building/signing every app. During a real release, record newly discovered recurring problems in the project/shared playbook and turn prevention into preflight, an artifact assertion, a test or a specific authority gate. A narrative retrospective alone is insufficient.

## iOS build/TF entrypoint differences

| Project | Current owning-source clues | Misuse to avoid |
| --- | --- | --- |
| NextNote | Root `scripts/release_ios_testflight.sh`, `fastlane/Fastfile`, `fastlane/lib/nextnote_release.rb` | Wrapper uses short-lived runtime VERSION/BUILD_NUMBER; beta also checks committed pubspec identity. Complete version commit/push and source synchronization rather than overriding only through environment inputs |
| natureid | Root `scripts/release_ios_testflight.sh`, `ios/fastlane/Fastfile` | Wrapper rejects preset VERSION/BUILD_NUMBER/RELEASE_*, reads `read_testflight_baseline` and feeds beta itself; Fastlane working directory is ios |
| animalplant | Root `scripts/release_ios_testflight.sh`, `fastlane/Fastfile` | Wrapper consumes runtime VERSION/BUILD_NUMBER; preserve project-verified cache/Pods conventions |
| yingjian | `docs/release-contract.md`, root `fastlane/Fastfile` | Beta uses `version:/build:/source_commit:`, exclusive candidate directory and attempt/receipt ledger, not older Flutter wrapper arguments |
| PoseGenius | `docs/release-contract.md`, root `fastlane/Fastfile` | `release_baseline` and the same exact parameters; at audit time it shared a store bundle/global sequence/machine ledger with yingjian. Different names do not permit concurrent number allocation |

For shared bundle IDs, account for occupied builds by store identity rather than repository name. Revalidate that relationship each time; historical sharing is not permanent evidence.

If `apple-store-release` or a project-specific release skill is available, read its actual contract and reuse relevant guards. An old `required_files` entry containing privacy values is a completeness requirement, not authority overriding the current protected-field allowlist. Never claim an unavailable project helper ran. This package includes stage contracts; missing specialist tools are handled against current project implementation.

## Store-material lane audit findings

| Project clue | Limitation and required check |
| --- | --- |
| NextNote `upload_store_metadata` | A sealed snapshot/verify-submit does not grant legal-field authority; inspect the actual snapshot and allowlist |
| NextNote `upload_store_screenshots` / `verify_store_screenshots` | Old implementation hardcodes 84 images, six locales, two devices and seven slides/set; verification mainly counts, not complete enabled-locale/order/image acceptance |
| natureid `upload_store_listing` | Writes metadata and screenshots together; copy-only or screenshot-only authority does not permit the combined lane |
| natureid `upload_store_metadata` / legal mutation lane | Ordinary and legal changes are separate; legal mutation is not automatic recovery for ordinary listing failure |
| animalplant `upload_store_metadata` | Audit found the entire `fastlane/metadata/ios` directory passed to Deliver; privacy files create broad-sync risk. Use a safe restricted implementation before execution rather than trusting the lane name |

These are **code-audit observations from 2026-10-26, without live-mutation validation**. Later fixes may change them. Current source and real remote rereads remain authoritative.

## Historical cases converted to decisions

| Historical case | Reusable decision |
| --- | --- |
| NextNote 2026-10-19: public/latest both 1.1.11, global maximum 173, selected 1.1.12(174), successful IPA receipt | Demonstrates patch+1 on equality and global build+1; these numbers are not a current baseline |
| Same release: Flutter archive normalized iOS project/lockfiles; preflight lacked TS dev dependencies | Review/commit/push/refreeze/rebuild after automatic tracked changes; local dependency failure does not waive gates |
| NatureID 2026-10-13: 1.1.6(68), stopped at receipt without processing polling | `UPLOADED` ends upload; processing, distribution and physical-device acceptance are recorded separately |
| NextNote 2026-10-12: reused 1.1.11(173), completed nine-locale materials and authorized reuse of 162 historical screenshots; `WAITING_FOR_REVIEW`, manual release | Materials/review do not rebuild; retain historical-capture exceptions; old matrices are not universal templates and submission is not public availability |
| Same submission: Apple normalized a promotional-text terminal newline; public-version legal URLs were state-locked | Reseal ordinary values against actual saved remote content; protected values do not change automatically; do not bypass locks by targeting a wrong version |
| Shared playbook: missing shipped data, Profile debug API failures and inactive internal tracks | Unpacked data/migration checks, runtime/device acceptance and real tester installation are independent gates |

Locate historical evidence as needed in project `docs/releases/`, QA records, ignored receipts/logs and the AppOperations playbook. Historical receipts, old manifests and recollections cannot establish this release's authenticated baseline, source identity or public state.
