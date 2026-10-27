# Shared workspace contracts

Read this only when the target project's instructions adopt a shared release policy. Discover the current owning repository and checkers from those instructions; app names, old release numbers and historical lane signatures are not portable configuration.

## Verify the target checkout

Where provided by the shared policy, run `scripts/check_release_worktree_contracts.sh` before selecting a release worktree and `scripts/check_testflight_upload_boundary.rb` for the active uploader. Then run the target project's current release preflight. Schema 2 with `reuse_testing_else_patch_public` is necessary but insufficient: executable `altool`, processing waits, upload changelogs or a missing receipt boundary make the worktree historical-only.

Record the target's result and any other failing registered paths separately. A switch to another checkout does not make a shared check pass; preserve registrations and follow the policy's actual global/target gate. A new app absent from the registry still needs its own applicable checks. Run shared checks after changing their contracts or entrypoints.

## Inspect the actual adapter

- Resolve working directory, lane parameters and who reads the live baseline from current wrappers/Fastfiles. Do not copy another app's `VERSION`, `BUILD_NUMBER` or lane arguments.
- For shared bundle IDs, serialize build allocation and uploads by store identity, not repository name. Revalidate any shared identity each time.
- If building changes tracked files, review/commit/push/refreeze before rebuilding; missing dependencies do not waive source gates.
- Inspect listing lanes for combined writes, broad directory sync and hardcoded locale/device counts. Match actual fields/files to authority and verify complete remote content, order and images.
- Legal/subscription changes remain protected. A missing-file check or locked store field does not authorize a write or targeting another version. Bind ordinary values to the actual saved remote content.

Use project receipts and QA records when they answer a current question. Historical uploads cannot supply a fresh baseline or prove this candidate's artifact contents, runtime behavior or tester access. Keep product-specific release history in that product's workspace.
