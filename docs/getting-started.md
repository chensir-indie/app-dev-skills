# Getting started

[简体中文](getting-started.zh-CN.md) · [Documentation](README.md) · [Choose a skill](../README.md#choose-a-skill)

Start with one task and the material you already have. You need an agent that can load `SKILL.md`; tool execution also needs that skill's dependencies. Installing every runtime is unnecessary for reading instructions or planning.

## Install and verify discovery

Follow the [homepage installation steps](../README.md#1-connect-codex-to-one-source-checkout) to link one source checkout. For a single skill, use its standalone README.

For other agents or a separate installation scope, [Skills CLI](https://github.com/vercel-labs/skills) supports `npx skills@latest add chensir-indie/app-dev-skills --list` and `--skill <name>` (Node.js 22.20+). Choose a scope that does not duplicate the Codex collection link; remote installation uses the published revision. Preserve local edits before updating.

### Verify the installation

From the source checkout, run `python3 scripts/list_skills.py` to see its packaged entries. This command checks the source catalog, **not the agent's live discovery state**. In Codex, inspect the available skills in a new session and confirm that each intended skill resolves to this checkout once. A missing entry and a missing Python/browser dependency are different problems.

| Symptom | Next step |
| --- | --- |
| Collection is missing | Check the symlink target is the checkout's `skills/` directory, then refresh discovery in a new session. |
| One skill appears twice | Compare collection and standalone installations in both discovery directories; preserve edits before moving redundant copies outside them. |
| Existing link points elsewhere | Inspect that checkout and its changes first. The installation command deliberately does not replace it. |
| Skill is visible but a command fails | Run its scoped doctor and follow [runtime troubleshooting](runtime.md). |

## Complete a first task

1. Select a skill from the [catalog](../README.md#choose-a-skill), then read its standalone guide and `SKILL.md`.
2. Supply your source files or project directory, the task scope, constraints, output language and requested endpoint. Use a separate product/output directory so generated artifacts do not modify the installed skill.
3. Run `sh scripts/doctor.sh` from that skill directory before executing its tools. Use the guide's narrower scope when appropriate. Install only required dependencies.
4. Invoke the skill using an example below. Preserve usable existing files and specify any locked references or decisions.
5. Inspect the resulting files and evidence against the selected workflow. Environment checks, artifact creation, visual review and provider states are different milestones; report remaining gaps.

For example, interface reconstruction should return editable source, separate assets and real browser comparisons. A concept-only request stops at the concept. Neither result establishes native app behavior.

## Example requests

Use the relevant skill token with your inputs, constraints, output language and endpoint. Full examples and output contracts are in the [standalone guides](../README.md#choose-a-skill).

| Task | Request outline |
| --- | --- |
| Competitor study | `$app-competitor-analysis`: analyze these captures for my product question; distinguish facts and hypotheses; deliver per-app reports and a comparison index. |
| Reconstruction | `$image-to-layered-html-prototype`: rebuild these approved screens as editable layers; preserve the design and show browser comparisons. |
| Store covers | `$app-store-cover-generator`: use these real captures and this reference; export and review the specified locale/device/slide matrix. |
| iOS adaptation | `$iphone-duo-adaptation`: analyze the existing app, recommend minimal changes and deliver a complete HTML prototype with browser evidence; keep native validation separate. |
| TestFlight upload | `$app-publish-skill`: follow the current release contract and project-owned local Fastlane workflow; stop at the exact-artifact successful upload receipt. |

## Update or migrate an installation

The source checkout is the maintained installation. Before updating it, inspect changes and preserve work:

```sh
cd "$APP_DEV_SKILLS_DIR"
git status --short
git remote -v
```

On a clean checkout tracking the intended upstream branch, use `git pull --ff-only`. If there are local edits, divergent commits or an unexpected remote, reconcile those explicitly before updating; do not reset or overwrite them. Rerun the relevant doctor and check agent discovery after the update. Dependency changes may also require the setup commands in [runtime support](runtime.md).

For clones of the former `app-store-cover-generator` repository, verify `origin` is the upstream you intend to follow. If it is the former upstream, update it with:

```sh
git remote set-url origin https://github.com/chensir-indie/app-dev-skills.git
```

Keep a fork's remote configuration if that is your workflow. Cover-tool commands now run from `skills/app-store-cover-generator`, or through the root npm workspace commands. Migrate old whole-repository or individual copied skill installations to one source link, preserving edits outside discovery directories. A compatibility path needed by existing scripts may remain a symlink to the same source after verifying there is only one discovered entry per skill.

To disconnect the collection from Codex, inspect `~/.agents/skills/app-dev-skills` and remove only that symlink. Retain the source checkout, project artifacts and any separately needed compatibility links. No account or provider configuration is changed by unlinking it.
