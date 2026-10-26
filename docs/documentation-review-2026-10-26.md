# Collection documentation review — 2026-10-26

## Scope

This revision reorganizes the public documentation around skill selection, installation, first use, troubleshooting and contribution. It changes collection guides and adds a documentation index, getting-started guides, support/security policies and a pull-request template. It does not change skill execution contracts, helper implementations, dependencies or publication behavior.

The working tree already contained substantial uncommitted work. During this review, a concurrent change removed the two video preproduction packages. The final documentation follows the five remaining skill entrypoints and preserves that removal. This review does not claim ownership of unrelated skill or test changes.

## Editorial checks

- Both root catalogs link directly to every current `SKILL.md` and the corresponding localized standalone guide.
- Installation maintains one source checkout, preserves existing entries and explains how to avoid duplicate discovery.
- The source catalog command is distinguished from live Codex discovery. The existing collection symlink remains unchanged.
- English and Chinese guides cover the same five task types, installation, first-use steps, update/migration behavior and completion boundaries.
- Detailed contracts and dated evaluations are reachable through the documentation index rather than accumulated on the homepage.
- License wording follows the current package contents. No private reporting channel, support SLA, live store status or model/media runtime is promised.

## Routing desk review

These are document inspections, not live model or provider evaluations.

| Scenario | Expected route and endpoint | Documentation checked |
| --- | --- | --- |
| New user with approved screenshots | Reconstruction skill; editable output and real browser comparisons | Root catalog; getting-started example; standalone guide |
| User requests only a concept | Concept branch ends before HTML reconstruction | Getting-started first-task guidance; workflow endpoint table |
| Existing HTML needs a local repair | Preserve usable files and locked reference; verify the changed region | Getting-started first-task guidance; workflow repair row |
| Browser runtime is unavailable | Scoped doctor, named repair and pending dependent verification | Runtime guide; support report fields |
| User requests Duo adaptation | Layout analysis, minimal-change recommendations and complete HTML prototype; native acceptance remains separate | Root completion summary; adaptation workflow and linked contracts |
| User requests store covers only | Cover generation and review; no implied upload | Root catalog and completion summary; workflow cover row |
| User requests TestFlight upload | Project-owned local Fastlane workflow; stop at exact-artifact successful receipt | Getting-started upload example; publication workflow |
| User starts from a legacy copied install | Preserve edits, reconcile copies outside discovery directories, verify one source entry | Installation and migration guides |

## Automated checks

Validation used the current working tree on macOS, Python 3.9.6, Node.js 24.14.0 and installed Chrome 155.0.8059.86. These are observed local versions, not new minimum requirements.

| Check | Result |
| --- | --- |
| `npm run check:docs` | Passed: collection discovery/metadata, standalone local links, documentation paths/fragments and cover documentation checks. |
| Catalog and index inspection | Both root catalogs match all five current filesystem entrypoints; both documentation indexes include all 15 dated root-level records. |
| Shell examples | All 21 `sh` blocks across the root READMEs, getting-started/runtime guides and contribution guide passed `sh -n`. This is syntax validation, not execution of install/update commands. |
| `git diff --check` | Passed. |
| `PLAYWRIGHT_CHANNEL=chrome npm run test:browser --workspaces` | Passed separately: all 13 cover browser tests and the layered-prototype DOM/interaction suite. |
| Plain `npm run check`, before editing | Stopped at doctor: the Playwright-managed Chromium headless shell is missing on this host. |
| `PLAYWRIGHT_CHANNEL=chrome npm run check`, baseline and final | Runtime and documentation checks passed. All 230 root Python tests, 44 cover tests and 83 layered-prototype Python tests passed. The root browser suite passed 8/9 and reproduced the same pre-existing failure described below. |

The root browser failure is `index image windows preserve full portrait, landscape and square framing at each layout`, in `tests/competitor_html.browser.cjs`. At the 1000 px layout, the portrait fixture's bottom exceeds its screen-card content area; the assertion reports `-95.96875`. It occurred before and after the documentation changes. This revision does not alter that renderer or assertion, and the full check remains failed. The chained command stops before workspace browser suites; the separate run above completed those successfully. Local logs are retained under the ignored `.test-output/documentation-review-2026-10-26/` directory; the commands and failure description here are the portable reproduction record.

The source collection symlink resolves to this checkout's `skills/` directory and was not changed. No remote availability sweep was performed. Two setup references were checked on this date: the [official Codex skill guide](https://learn.chatgpt.com/docs/build-skills) documents user-scope skills and symlink discovery; the [Skills CLI package manifest](https://raw.githubusercontent.com/vercel-labs/skills/main/package.json) declares Node.js `>=22.20.0`. These checks support the installation guidance, not a live agent discovery or remote installation claim.

## Limits

Documentation validation does not prove aesthetic quality, translation acceptance, native-device behavior or any store operation. No skill was installed or rediscovered through a new Codex session during this documentation task. The existing source symlink and current filesystem catalog can be inspected locally, but that is not a fresh live discovery result. No commits, push or public release are part of this revision.
