# Release records and helper tools

Reuse the project's manifest/receipt format. Do not maintain two drifting authoritative records for one candidate. Add missing evidence in the existing release/QA directory; keep sensitive logs and artifacts in approved ignored locations.

| Record | Minimum evidence |
| --- | --- |
| Intent | App, repository, bundle/platform/track, user authorization, terminal stage, public/source base and hotfix intent when applicable |
| Baseline | Original authenticated read-only source, `observed_at` and precision, public/latest uploaded/global maximum build, query coverage and raw snapshot hash |
| Candidate | Version/build, source commit, remote ref, remote equality/ancestry and contract/preflight/test results |
| Artifact | Actual package path, SHA-256, unpacked identity/configuration/signing/data assertions, archive/dSYM and build toolchain |
| Upload attempt | Unique candidate identity, start/end, existing process, terminal or unknown status and logs; an attempt is not a successful receipt |
| Apple success receipt | Bundle, version/build, source commit, IPA SHA, provider success evidence, observation time and available upload/delivery ID; ASC build ID is null until it exists |
| Copy | Locale × field diff, approved write allowlist, protected-field before/after snapshots, sealed digest, preview/review and remote values |
| Screenshots | Capture identity, locale-family/device/slide matrix, editable sources/export hashes, full-size/thumbnail review and per-locale remote order/state |
| Later states | Exact ASC build ID when available, validity/distribution/actual installation; submission ID/state/release mode; exact public evidence if separately authorized |

Record observed states, not planned values. Changes invalidate only affected gates: source/configuration changes invalidate the binary candidate; copy changes invalidate its acceptance/digest; exports invalidate corresponding visual review; any identity drift invalidates acceptance/submission binding.

## `plan`: offline candidate proposal

The helper uses Python 3.9+ standard library without accessing stores, credentials, Git or the network. It checks whether supplied JSON follows the two-branch version algorithm. It neither establishes authenticated provenance, reserves a build nor replaces project preflight.

Normalize actual project Fastlane/Spaceship/Play read-only results into these fields, retaining the original snapshot and mapping. This example is a **historical algorithm illustration; its time and versions are not a current release baseline**:

```json
{
  "bundle_id": "com.example.app",
  "platform": "ios",
  "observed_at": "2026-10-19T06:00:00+00:00",
  "public_version": "1.1.11",
  "latest_uploaded_version": "1.1.11",
  "highest_uploaded_build": 173
}
```

```sh
python3 "$SKILL_DIR/scripts/release_evidence.py" plan \
  --baseline "$BASELINE_JSON" --output "$PROPOSAL_JSON"
```

- `observed_at` must include a timezone, be at most 30 minutes old and no more than 60 seconds in the future. The fixed historical example is rejected during real execution.
- `platform` is `ios` or `android`; versions must be exact `A.B.C`. The global highest build is a positive integer, not the maximum from only the current version train.
- If latest > public, reuse latest; only equality permits patch+1. Build = highest+1. Reject latest < public, missing values, a new app without a public baseline, prerelease strings and ambiguous formats.
- Output includes `PROPOSAL_ONLY`, candidate version/build, decision and SHA of the original input. It confers no execution authority; actual store/source/contract verification remains required.
- Existing output is preserved by default. Use `--overwrite` only for an intentional proposal replacement. An old proposal is not a reusable store baseline.

## `verify-artifact`: file-byte identity

```sh
python3 "$SKILL_DIR/scripts/release_evidence.py" verify-artifact \
  --artifact "$IPA_PATH" --expected-sha256 "$IPA_SHA256"
```

Read actual file bytes and compare them with an existing expected SHA. This does **not** inspect IPA contents, signing, source commit or Apple reception. Matching hashes do not replace unpacked-package assertions or a success receipt. Use it for transfer consistency of IPA/AAB/screenshots and other files.

## Doctor and its limits

```sh
sh "$SKILL_DIR/scripts/doctor.sh"
sh "$SKILL_DIR/scripts/doctor.sh" --project "$PROJECT_ROOT" --platform ios
```

The default checks readable package resources and Python. `--project` discovers actual Fastfile/Gemfile layout and runs Ruby, Bundler, locked-dependency and Fastlane version checks; executable presence alone is insufficient. Existing no-Gemfile projects use a managed standalone version check with a lock-evidence warning. Select the directory containing Fastfile using `--fastlane-dir` when adapters are ambiguous, and the target with `--platform ios|android`. Neither mode authenticates, downloads dependencies, builds, uploads or reads secret contents. Run Bundler checks only against trusted projects; [setup and recovery](fastlane-setup.md) explains project-code execution and frozen/no-auto-install limits. Passing does not establish signing, a store baseline, device acceptance or release eligibility.

Maintenance check:

```sh
python3 -m unittest discover -s "$SKILL_DIR/tests" -p 'test_*.py'
```

Tests use temporary files and offline fixtures. Success proves helper version/freshness/overwrite/hash and doctor failure behavior, not live Fastlane/Apple/Play delivery.
