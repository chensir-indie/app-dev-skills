# Later acceptance, review and optional Android

## Apple: independently reconcile an existing candidate

Only when the user requests processing checks/test delivery, or metadata/review actually requires a processed candidate, perform one project-owned exact-build Fastlane/Spaceship read. Bind platform/bundle/version/build/source commit/IPA SHA/original receipt, adding the ASC build ID only after it exists.

If pending/not visible, report the observation and return without looping or re-uploading. Record exact `MISSING_EXPORT_COMPLIANCE` or invalid blockers without redefining a successful receipt as upload failure. Answer product-responsibility questions from facts; do not infer encryption exemption from the app name or invent declarations for the user.

After `VALID`, tester-group assignment, What to Test, Beta App Review and external distribution require the corresponding explicit authority. Confirm an active track/group, actual testers, a reachable installation link and installation of the exact version/build. Only successful core-flow verification establishes `TESTER_VERIFIED`. Review acceptance alone does not establish physical-device functional acceptance.

## Apple: submit App Review

Reuse the exact uploaded, accepted candidate: **no new archive, binary upload or build change**. Before submission, check:

- Exact public baseline/source ancestry, artifact identity, processing state and known test conclusions;
- All locales' copy/device assets, final material digest, screenshot order and terminal remote state;
- Privacy/Terms/EULA/App Privacy, export compliance and age/social declarations;
- Reviewer notes, valid access/contact information and registration/ICP/provider affiliation where applicable;
- Fixed app version/build selection, release mode and public consequences of approval.

Missing protected legal/subscription information is a blocker; submission authority does not authorize changing those fields. Inject review credentials through existing managed mechanisms, not Git/reports.

Pass project candidate/metadata-acceptance/verify-submit gates and act within existing submission authority. Default to `automatic_release:false`, with no `auto_release_date` or public-release lane. If the UI/current configuration means approval automatically exposes the app, present that specific consequence and obtain explicit authority. Do not switch public-release mode on the user's behalf without authority.

Fastlane submission must select the accepted version/build explicitly; do not omit build and let Deliver choose latest. Check whether the action retransmits metadata:

- For binding/submission only, with remotely verified review information, use the project's verified restricted adapter.
- If Deliver must apply `app_review_information`, `skip_metadata:true` may omit it. Reuse only the exact approved, immutable, guarded snapshot, sending required fields with `skip_metadata:false` while preserving the metadata allowlist and protected fields. Do not resync an entire old directory just to include reviewer information.

Save submission ID, exact state, time and observation precision. `WAITING_FOR_REVIEW` means submission succeeded, not `IN_REVIEW`, approved or public. Approval retained for manual release is `APPROVED_HELD`; the owner releases it manually in ASC. Do not poll review status without later authority.

## Android: enter only when that platform is requested

Android uses an independent local-signed-artifact/Chrome Play Console branch. Do not reuse Apple TF lanes, API build IDs or receipt endpoints.

Choose the actual framework adapter before building: Kotlin/Java uses the project Gradle wrapper; Flutter uses pinned SDK/flavor local Android builds; React Native/Expo uses a buildable native Android project, locked JavaScript/native dependencies and the project Gradle wrapper. If Expo lacks native files, confirm generation/maintenance policy and authority first. Do not overwrite with prebuild or substitute EAS cloud build for local signing. Other frameworks use only project-verified export/native build flows. Tests and production modes follow the corresponding framework contract.

1. Read Android release contracts, environment example, signing configuration and actual package ID. In authenticated Chrome, verify account/app, public/internal versions, highest versionCode across all builds, target track, testers and Managed publishing. Operate only the specified app; extract no browser credentials.
2. Apply the workspace's shared marketing-version decision and Android-wide build sequence, 30-minute baseline and clean/pushed exact-source gate. Stop for occupied candidate/track identity or incomplete query coverage. iOS/Android build sequences are independent; one marketing-version decision does not require identical build numbers.
3. Build/sign APK/AAB locally through that framework adapter; Fastlane may orchestrate managed Gradle/framework steps. Inspect final package/versionName/versionCode, upload certificate, embedded configuration, data/assets and SHA. Do not trigger GitHub Actions packaging or upload a wrongly signed package.
4. Upload to the explicit track through authenticated Chrome Play Console. Inspect processing/validation, release notes, countries/regions, Data safety, content rating, target API, policy declarations and test groups. Old screenshots do not establish current policy or track state; check current official sources and project contracts.
5. Save or submit within authority. Internal testing requires an active track, assigned testers and actual installation, beyond “available to internal testers.” Before production review, state current Managed publishing mode: when off, approval may automatically make the app public, requiring explicit authority for that consequence.
6. Report the actual endpoint: uploaded, processing, distributed, tester verified, submitted, in review, approved held or public. Without public-release authority, stop at the authorized boundary.

Fastlane supply does not replace the user's selected Chrome Play Console route for account authorization, upload and remote verification. Use another adapter only when the user explicitly changes that route for the release.
