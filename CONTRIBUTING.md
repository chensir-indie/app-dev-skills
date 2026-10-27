# Contributing

## Questions and bug reports

For setup problems, start with the reference linked from the selected `SKILL.md` or the [runtime support guide](docs/runtime.md). When opening an [issue](https://github.com/chensir-indie/app-dev-skills/issues), include the skill and revision, the command or request, what you expected, what happened, and doctor output with sensitive information removed. For visual problems, also include the reference image, browser and viewport.

Report vulnerabilities through GitHub private reporting when available. Otherwise, ask for a private channel before sharing secrets or exploit details.

## Package and source rules

- Use the flat `skills/<name>/SKILL.md` layout. Keep each package's references, assets, scripts, dependencies and license together. Local runtime links must stay within the package.
- Maintain one source checkout and expose it through the Codex collection symlink. Preserve local edits. Compatibility paths may link to the same source, but discovery must return only one entry per skill.
- Add a skill when a recurring task has distinct inputs, actions and an observable result. Explain how it overlaps with existing skills, which tools it needs and how to install it independently. Keep product credentials, account mappings and release history in the relevant product workspace.
- Give each skill a read-only `scripts/doctor.sh` that explains how to repair failures and exits with a nonzero status when required tools are missing. Keep the root and standalone lockfiles consistent. Use fixtures to test missing or older runtimes; leave the host's installations in place.

## Instructions and documentation

Use the English and Chinese root READMEs to help readers choose a skill, copy a request and install it. Keep setup instructions in each skill's existing references; do not add per-skill READMEs. Put execution order and completion requirements in `SKILL.md`, with detailed conditions for each workflow in its local references.

Keep useful output previews visible on both homepages. Preserve source and rights notices, and label examples so readers can distinguish them from real app evidence. Avoid duplicate walkthroughs, documentation indexes and dated cleanup reports.

Write instructions, references and metadata in English, and keep bilingual guides consistent. Preserve the user's requested output language, evidence in its original language and legal notices. Retain required evidence and license files. When removing obsolete explanations, update anything that links to or relies on them.

When adding, renaming or removing a skill, or changing its scope, update the folder and frontmatter, `agents/openai.yaml`, both root catalogs, references, doctor, and affected tests and configuration. Check metadata types and preserve the exact `$skill-name` token in default prompts. Search for old names and broken links.

## Verification

| Change | Checks |
| --- | --- |
| Documentation/instructions | `npm run check:docs`, language parity and affected route review |
| Validation code | Failure fixture for the original problem, focused tests, then `npm run check` |
| Other tool/package changes | Relevant focused tests, then `npm run check` |

See [runtime support](docs/runtime.md#focused-verification) for setup. When changing instructions, review requests that name the wrong skill, repairs to existing projects, requests that stop at an earlier stage, and cases where tools are unavailable. Describe the expected behavior and limits in the task or PR. Label a review of written scenarios as such; it does not establish how a live agent behaves.

Use local synthetic fixtures for tests and do not publish from them. Isolate browser fixtures and close servers even if browser startup fails. Automated checks still need the relevant visual or provider evidence. Validators must not invent reviewer judgments or report an automated pass as visual approval.

## Submit the change

Explain the problem, what the change does, which checks you ran and what remains unverified. Preserve unrelated edits. Keep credentials, private paths, customer data and unlicensed fixtures out of the change, and retain applicable licenses. Routine documentation cleanup does not need a separate historical report.
