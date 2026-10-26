# Store metadata and screenshot artwork

Prepare copy and screenshots concurrently, review/upload them separately, and reuse the existing candidate. A TF-only upload does not require listing changes; listing changes do not require a new IPA.

## 1. Freeze remote state and the authorized write scope

Read current project artwork contracts, locale configuration and metadata/Deliverfile/Fastfile implementation. Obtain read-only evidence of actual storefront locales, app/platform/editable version, current text and device-asset slots. An old directory's locale count or README example is not the complete matrix.

Maintain two distinct inventories:

- **Completeness inventory:** Required delivery/review fields and files exist, meet length limits, are reachable and have been reviewed.
- **Write allowlist:** Locales, fields/files and new values/differences actually authorized for this task.

Including a privacy file in the first inventory or hashing it with a guard does not authorize writing it. Every transmitted value must trace to the allowlist. Inspect Deliverfile, defaults and environment variables rather than relying on the `metadata_path` name.

Creating a remote app record/version/locale or changing category/pricing/legal fields are writes too; do not hide them inside “initialization/downloading metadata.” If the remote version is locked or uneditable, report its exact state rather than switching to a public version or another draft to bypass the lock.

## 2. Copy and localization

Derive evidence from customer-visible changes between the exact public version and candidate before writing title/subtitle/description/keywords/promotional text/release notes and relevant review information. Exclude tests, dependencies, refactors, signing, logs and unimplemented features. Do not add unsupported claims such as “more stable,” “smoother” or “smarter.” Release notes must not describe unfinished test capabilities as delivered.

Localize naturally by meaning for every target locale, retaining canonical product names and technical terms. Copying the source language is not translation. Check current Apple character/byte limits, empty values and placeholders. Produce a previewable locale × field diff and record final hashes/content review. Inject reviewer login credentials through managed secrets rather than committed metadata or reports.

### Protected legal and subscription data

Apple requires an accessible Privacy Policy link in both ASC metadata and the app. Auto-renewable subscriptions also require working Terms of Use and Privacy Policy links in the app and store materials. Report missing compliance as its own blocker; a completeness check does not expand mutation authority.

Preserve these fields byte-for-byte by default: localized Privacy Policy URL, User Privacy Choices URL, App Privacy questionnaire, Terms URL/body legal footer, EULA text/standard-versus-custom mode/territories, and subscription product/group names, descriptions, durations, prices, trials and offers.

- Ordinary copy/artwork authority does not include those fields. Editing a description must preserve its protected legal footer verbatim, including during translation or whitespace cleanup.
- Before a protected-field change, require explicit authority naming that field, take a fresh remote snapshot for each affected locale and record current EULA mode. Apple standard EULA remains the default without a separately approved custom EULA.
- Transmit only authorized specific fields/files, then reread each and compare with the approved value and remaining protected snapshots.
- Missing, 404, stale or inconsistent Privacy/Terms links are independent blockers, not automatic repairs during ordinary upload. Website repair, source-link changes, store-field changes and repair of older clients are separate facts.

## 3. Metadata-only upload

Within existing authority, freeze the exact candidate, locale diff, material digest, protected-field snapshots and write allowlist. Pass the current project guard. The guard checks candidate/content identity; it neither grants field authority nor proves protected fields unchanged.

Inspect whether the project lane stages only allowed files in a restricted directory or sends approved values through explicit field arguments. Do not broadly sync a complete directory containing protected files such as `privacy_url.txt`. Supported restricted arguments, temporary staging, diffs and read-only rereads are routine work within authorized metadata upload and require no new confirmation. If safety requires changing publishing code covered by a project read-only rule, prepare the concrete reviewable change and use existing code-change authority. Ask only when that scope is actually missing; do not run an overbroad old lane.

A metadata-only action retains:

```ruby
skip_binary_upload: true
skip_screenshots: true
submit_for_review: false
automatic_release: false
```

Pin the app/version identity and inspect implicit app-version mutation, default files and environment injection. Afterward, reread authorized fields for every locale and confirm protected fields unchanged. If Apple normalizes a terminal newline, record the actual saved difference. Ordinary copy may be resealed with its real saved value/digest within scope; stop/report protected-field differences rather than hiding drift behind a new digest.

## 4. Produce the complete uploadable artwork matrix

Discover and read the actual available `app-store-cover-generator` or project artwork-tool contract before production. That specialist workflow owns editable artwork, export and visual checks; this skill owns candidate binding, complete matrices and store delivery. Without it, an existing editable HTML/CSS/SVG pipeline may satisfy equivalent checks. Prompts alone do not replace uploadable images.

Clarify “cover”: Apple listing display usually means screenshot sets; Google Play also has a Feature Graphic. App Preview posters and app icons are separate assets. One promotional poster is not a complete store screenshot matrix.

Freeze:

- App, platform, candidate version/build, source commit and terminal stage;
- Actual storefront locale → language family → final export-path mapping;
- Device slots, current official dimensions/orientation, slide IDs/count and canonical `01...N` order;
- Locale/device/orientation, exact candidate, clean-install/fixture state and source hash for every real app capture;
- Editable source, copy/layout tokens, final exports and SHA-256.

Use one semantic narrative and consistent cross-locale order. Every language family needs actual localized copy and app captures; another language, a placeholder or store inheritance is not complete local input. Different-build captures are preview-only unless the user explicitly accepts a recorded exception. Synthetic UI, design renders and AI images are not real app captures. AI may supply allowed decorative layers; retain editable sources for text, real captures and layout.

Projects using `store-creative-v1` require:

- A fixed caption box and consistent device start/end for the same layout/device across locales. Scale text inside the box from `1.00` to minimum `0.60`, then rewrite if it still does not fit; do not reposition devices per language.
- Shared portrait-phone caption-above defaults: x=8%, width=84%, top=5.5%, height=15%, gap about 1.8% of the short side, headline base about 8.4%, line-height 1.0. This is a workspace-template baseline; other layouts follow their explicit design contract.
- No overlap, clipping, excessive blank bands, wrong language, unreadably small text, transparent gutters, black frames or placeholders.
- Full-size and approximately 160px thumbnail/contact-sheet visual review for every language family × slide × device, plus per-cell automatic checks of dimensions, opacity, paths, nonempty files and filename order.

Visual records bind final copy/media hashes. A change to copy, source capture or export invalidates the corresponding review and requires rereview. A passing automatic layout check or creation of a `review init` file does not establish visual review.

## 5. Screenshot-only upload and remote acceptance

Prerequisites: upload authority, complete passing local matrix, matching final hashes/review, editable target version/locales/devices, saved prior remote state and retry evidence. Run verified project `apple:check`/staging tools where applicable; do not assume every app has the same commands.

A screenshot-only lane fixes app/version, transmits only the reviewed screenshot directory and retains:

```ruby
skip_binary_upload: true
skip_metadata: true
submit_for_review: false
automatic_release: false
```

`overwrite_screenshots:true` clears prior screenshots. Use it only when replacement of the entire corresponding set is actually authorized and backups/matrix are complete. On timeout, read completed remote work before scoped recovery rather than deleting everything on each retry. `force:true` only skips Deliver's HTML preview; it replaces neither checks nor user approval.

Reread **every enabled storefront locale** after upload: device sets, counts, visible `01...N` order, actual images/language, processing state and independent/inherited status. Also check Play Feature Graphic. A successful call, matching total, one correct locale, disabled Save button or selector timeout cannot establish completion of the batch.

A count checker proves counts only. Apple may transform images: record checksum algorithms/relationships when comparable remote checksums exist. Otherwise use verifiable remote IDs, order, dimensions and visual comparison with explicit limitations; do not invent SHA equality. Screenshot processing is separate from TF binary processing. An authorized screenshot upload may verify necessary terminal states within project timeouts; persistent anomalies remain pending rather than causing endless waiting/re-uploading.

Keep project evidence under `docs/qa/screenshots/store-assets/YYYY-MM-DD/`: frozen matrix, copy/capture/export hashes, contact sheets, per-cell review, per-store/locale rereads and remaining gates.

## Official sources

Checked 2026-10-26: [Deliver skip/overwrite semantics](https://docs.fastlane.tools/actions/upload_to_app_store/), [current Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/), [version fields/localization](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/), [App Review guidelines](https://developer.apple.com/app-store/review/guidelines/). Verify current official specifications and storefront capabilities during execution; historical counts/dimensions are not platform-wide rules.
