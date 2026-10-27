# Runtime setup and support

[简体中文](runtime.zh-CN.md) · [Collection overview](../README.md)

Installing a skill gives you its instructions; its scripts may need additional tools. You can read references, plan a competitor analysis or develop a concept before installing the rendering tools. Check the environment for the task you are about to run.

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

If you installed a skill independently, run `sh scripts/doctor.sh` from its directory. See its `SKILL.md` and linked setup reference for more specific checks. The shell script checks for missing runtimes before trying to run Python or Node. You can also use `npm run doctor` if Node/npm already work.

The catalog command and full doctor find skills through `skills/*/SKILL.md` in the current checkout. With `--skill`, doctor runs that skill's shell script directly. A skill that only needs Node can therefore be checked without installing Python for the collection. Collection validation also checks for incomplete skill folders and missing documentation entries.

### Skill-specific setup

| Task | Required environment and setup |
| --- | --- |
| Competitor report helpers | Python 3.9+ standard library; [renderer setup](../skills/app-competitor-analysis/references/html-delivery.md#reusable-renderer) |
| Editable HTML captures | Python, Node and a browser; [capture setup](../skills/image-to-layered-html-prototype/references/render-contract.md#environment-check-and-setup) |
| Store cover exports | Node and a browser; [export setup](../skills/app-store-cover-generator/references/template-contract.md#environment-check-and-setup) |
| iPhone Duo workspace rules | Python 3.9+ standard library; [rule helper](../skills/iphone-duo-adaptation/references/workspace-rules.md). Layout/HTML work needs no Xcode; browser acceptance requires a browser. |
| App publication | Python 3.9+ for offline helpers; [project toolchain setup](../skills/app-publish-skill/references/fastlane-setup.md) for builds/uploads. From the skill directory, add `--project /path/to/app --platform ios` or `android` to doctor. |

Doctor checks your environment without installing tools, signing in, building or uploading. Its browser check launches a blank headless browser. Follow any repair instructions and rerun the same command. A pass means the required tools are available; artifact quality and task acceptance need their own checks.

## Set up the repository

Use a POSIX shell on macOS or Linux, or WSL on Windows. To run all collection checks, you need Node.js 22+, npm, Python 3.9+ available as `python3`, Pillow, PyYAML and Playwright Chromium. Individual skills may need fewer tools. Optional Swift/Vision OCR runs only on macOS; the portable workflow works without it. Mobile packaging also needs the selected project's platform tools.

From the repository root:

```sh
npm ci
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r skills/image-to-layered-html-prototype/requirements.txt
npx playwright install chromium
npm run check
```

Use `npm ci` with the repository's lockfile. If you are installing only one skill, follow the setup reference linked from its `SKILL.md`. Install Python packages into the environment that runs the checks, and activate that same virtual environment in each new terminal. Packages installed into another environment will not fix an import error here.

## Repair a failed check

| Failure | Action |
| --- | --- |
| Python missing or too old | Install a supported Python from [python.org](https://www.python.org/downloads/), reopen the terminal, then create/activate `.venv`. The full npm suite uses `python3`. |
| `venv` or `ensurepip` missing | Install your distribution's Python venv/pip package (for example `python3-venv` on Debian/Ubuntu), then recreate `.venv`. |
| Node/npm missing or Node below 22 | Install Node.js 22+ with npm using the [official download options](https://nodejs.org/en/download); reopen the terminal. Without Node, use manual skill installation to read/use instructions first. |
| Pillow/PyYAML cannot import | Activate `.venv`; run `python -m pip install -r skills/image-to-layered-html-prototype/requirements.txt`. Avoid system-wide pip installation. |
| Playwright/pngjs missing | From the repository root run `npm ci`; for an independently installed skill with `package.json`, run `npm install` in its directory. |
| Chromium executable missing | After npm dependencies are installed, run `npx playwright install chromium` from the package/repository that owns them. |
| Browser OS libraries missing on Linux | Run `npx playwright install --with-deps chromium` where authorized; this may require system-administrator access. If unavailable, use a supported host for capture and keep browser verification pending. |
| Existing Chrome should be used | Set `PLAYWRIGHT_CHANNEL=chrome` for both the doctor and capture/export command, for example `PLAYWRIGHT_CHANNEL=chrome sh scripts/doctor.sh`. Chrome must already be installed; preserve the actual browser version in evidence. |
| Downloads fail or the host is managed | Keep the diagnostic output, check your network/package-registry policy, and ask the environment owner to provide the named runtime/package. Do not repeatedly rerun a failing workflow or change security settings. |

On Windows, use WSL for the documented shell/npm checks; native PowerShell cannot run the POSIX startup script. You may adapt a Windows workflow to run the `.py`/`.mjs` helpers directly, but the collection's shell tests do not cover that setup.

## Continue when one capability is unavailable

Continue research, source inspection or concept work that does not need the unavailable tool. Report what is missing and leave any dependent capture, render or check step pending. You can use another browser or inspection tool if it produces the required evidence. Never fill the gap with fabricated screenshots or claim that an unverified result passed.

When asking for help, include the command, working directory, operating system, active interpreter and version, doctor output, and the check that failed. Remove private paths and sensitive project content before sharing publicly. Do not include tokens, cookies, signing files or account credentials.

## Focused verification

```sh
npm run check:docs
python3 -m unittest discover -s tests -p 'test_*.py'
npm test -w image-to-layered-html-prototype
npm test -w app-store-cover-generator
npm run test:browser
npm run demo
```

While working, run the checks relevant to your change. Run `npm run check` before delivering changes to the collection or its tools. The demo uses synthetic UI, and CI checks only this repository; it does not package or upload mobile apps.
