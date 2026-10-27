# Runtime setup and support

[简体中文](runtime.zh-CN.md) · [Collection overview](../README.md)

Install instructions and runtime dependencies separately. Reading references, planning a teardown or writing a concept does not require all the rendering tools. Run a preflight for the task you are actually about to execute.

## Choose the check

From a repository checkout:

```sh
python3 scripts/list_skills.py                            # actual skill entrypoints; optional --json
sh scripts/doctor.sh                                      # all collection and skill runtimes
sh scripts/doctor.sh --scope collection                   # metadata/check prerequisites
sh scripts/doctor.sh --skill app-competitor-analysis      # Python standard-library tools
sh scripts/doctor.sh --skill app-publish-skill            # Python 3.9+ offline release helpers
sh scripts/doctor.sh --skill iphone-duo-adaptation        # Python standard-library workspace-rule tools
sh scripts/doctor.sh --skill image-to-layered-html-prototype
sh scripts/doctor.sh --skill app-store-cover-generator
```

From an independently installed skill, run `sh scripts/doctor.sh` inside that skill. Its README documents narrower scopes. The shell entry can explain a missing runtime before trying to run Python or Node. `npm run doctor` is a convenience only when Node/npm already work.

The catalog and full doctor discover `skills/*/SKILL.md` in the current checkout. A targeted `--skill` check dispatches directly to that skill's shell bootstrap, so a Node-only skill can be checked without installing collection Python first. Collection validation separately rejects incomplete skill folders and missing documentation entries.

### Adaptation tools and browser evidence

iPhone Duo Adaptation's workspace-rule helpers require Python 3.9+ and only the standard library. Its default doctor checks that runtime; `--scope instructions` remains available for reading without Python. It bundles no renderer; collection metadata is checked separately. The HTML stage prefers [BUILD WEB APPS](../skills/iphone-duo-adaptation/references/build-web-apps.md) through its discovered actual contract, recording installed/upstream-source use or an honest fallback. Its builder/browser capabilities are checked at execution time rather than added as mandatory Python-preflight dependencies. Keep local editable output and design/functional/visual evidence; hosting is separate. HTML acceptance uses the agent's available browser or the target environment and requires actual rendered and interaction checks; doctor success cannot substitute for them. Layout analysis and HTML authoring can proceed without Xcode, a simulator, a device, or the UI framework's toolchain. That framework's toolchain and device checks apply to separately requested product implementation; without them, native Duo behavior remains unverified.

### Publication tools and project runtimes

App Publish Skill's candidate-proposal and file-hash helpers require Python 3.9+ and only the standard library. Its default doctor checks the installed package and Python. From that skill directory, `sh scripts/doctor.sh --project /path/to/app` also runs Ruby/Bundler version checks, `bundle check`, and the project's `bundle exec fastlane --version`, or checks an existing standalone Fastlane setup with an unpinned-runtime warning. Use `--fastlane-dir /path/to/app/ios/fastlane` when multiple or monorepo entries require an explicit project-local choice. These checks do not install, authenticate, build or upload; use the [setup and recovery guide](../skills/app-publish-skill/references/fastlane-setup.md) for missing dependencies. A passing doctor does not validate store baselines, credentials, signing identities, artifact contents or publication authority. Native iOS needs the project's macOS/Xcode and signing; Flutter adds its pinned SDK, React Native/Expo adds its pinned JavaScript/native setup, and native Android uses its Gradle/JDK setup. Check only tools required by the selected adapter; native iOS does not require Flutter. Android delivery uses authenticated Chrome Play Console. Preserve project-owned version pins and wrappers; the skill bundles no Fastlane or mobile toolchain.

### What the doctor establishes

Checks are local and read-only: no downloads, package installs, privileged commands or credential access. Browser checks launch and close a blank headless browser. A nonzero status means a required check failed; follow the repair and rerun the same check. A successful preflight proves environment readiness, not visual quality, evidence accuracy or completion of your task.

## Set up the repository

Use a POSIX shell on macOS, Linux or Windows through WSL. Full collection checks require **Node.js 22+, npm, Python 3.9+ available as `python3`, Pillow, PyYAML and Playwright Chromium**. Individual skills can need less. Optional Swift/Vision OCR is macOS-only and does not gate the portable pipeline. Mobile packaging has the selected project's separate platform requirements.

From the repository root:

```sh
npm ci
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r skills/image-to-layered-html-prototype/requirements.txt
npx playwright install chromium
npm run check
```

Use `npm ci` in a repository checkout with its lockfile. Use the selected skill README's standalone setup when installing only one skill. The optional [Skills CLI installer](https://github.com/vercel-labs/skills) requires Node.js 22.20+; the bundled toolkit runtime remains Node.js 22+. Python imports are checked in the active interpreter: installing into another Python environment will not repair the current one. Activate the same virtual environment in each new terminal.

## Repair a failed check

| Failure | Action |
| --- | --- |
| Python missing or too old | Install a supported Python from [python.org](https://www.python.org/downloads/), reopen the terminal, then create/activate `.venv`. The full npm suite uses `python3`. |
| `venv` or `ensurepip` missing | Install your distribution's Python venv/pip package (for example `python3-venv` on Debian/Ubuntu), then recreate `.venv`. |
| Node/npm missing or Node below 22 | Install Node.js 22+ with npm using the [official download options](https://nodejs.org/en/download); reopen the terminal. Without Node, use manual skill installation to read/use instructions first. |
| Pillow/PyYAML cannot import | Activate `.venv`; run `python -m pip install -r skills/image-to-layered-html-prototype/requirements.txt`. Avoid system-wide pip installation. |
| Playwright/pngjs missing | From the repository root run `npm ci`; for a standalone copy use its README's `npm install` instructions. |
| Chromium executable missing | After npm dependencies are installed, run `npx playwright install chromium` from the package/repository that owns them. |
| Browser OS libraries missing on Linux | Run `npx playwright install --with-deps chromium` where authorized; this may require system-administrator access. If unavailable, use a supported host for capture and keep browser verification pending. |
| Existing Chrome should be used | Set `PLAYWRIGHT_CHANNEL=chrome` for both the doctor and capture/export command, for example `PLAYWRIGHT_CHANNEL=chrome sh scripts/doctor.sh`. Chrome must already be installed; preserve the actual browser version in evidence. |
| Downloads fail or the host is managed | Keep the diagnostic output, check your network/package-registry policy, and ask the environment owner to provide the named runtime/package. Do not repeatedly rerun a failing workflow or change security settings. |

Native PowerShell does not execute the POSIX bootstrap. Use WSL for the documented shell/npm checks; a custom Windows workflow may run the `.py`/`.mjs` helpers directly, but is not covered by the collection's shell test path.

## Continue when one capability is unavailable

Continue research, source inspection or concept work that does not need the failed tool. Keep the dependent capture/render/check step pending and report the missing capability. An alternative browser or inspection tool is useful only if it can produce the same required evidence. A missing runtime does not justify fabricated screenshots or an unverified acceptance result.

When requesting support, include the command, working directory, operating system, active interpreter/version, doctor output and failed scope. Remove private paths and sensitive project content before sharing publicly. Never include tokens, cookies, signing files or account credentials.

## Focused verification

```sh
npm run check:docs
python3 -m unittest discover -s tests -p 'test_*.py'
npm test -w image-to-layered-html-prototype
npm test -w app-store-cover-generator
npm run test:browser
npm run demo
```

Run only the relevant scopes during iteration; run `npm run check` before delivering collection/tooling changes. The demo uses synthetic UI. CI checks this repository and does not package or upload mobile apps.
