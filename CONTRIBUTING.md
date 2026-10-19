# Contributing

Each folder under `skills/` is independently installable. Keep its SKILL.md, references, runtime assets, dependency manifests and LICENSE self-contained. Do not link from a skill to files outside its own directory. Repository-wide documentation and CI belong at the root.

Use Node 22+, Python 3.9+, and the root README setup commands, then run `npm run check`. It checks collection metadata and local links, the cover exporter tests, layered-prototype regression tests, and browser behavior. Add a failing case before changing executable validation behavior. Keep root and standalone npm lockfiles in sync when dependencies change.

For focused checks:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
npm test -w app-store-cover-generator
npm test -w image-to-layered-html-prototype
npm run test:browser --workspaces
```

Use local, original or redistribution-cleared fixtures. Never include credentials, private absolute paths, customer data, app source code or private screenshots. Keep caches, exports and installed dependencies out of Git. Tests must not publish to store or social accounts.

Keep each skill entry focused; move detailed schemas into references. Preserve the user's product, language and workflow choices. A validation tool must document its limitations and never fabricate reviewer judgments. The collection checker checks packaging and documentation paths; it is not a comprehensive secrets scanner.

Swift/Vision OCR is optional and macOS-only. Keep core Python and browser validation portable. Browser scripts use Playwright Chromium by default; `PLAYWRIGHT_CHANNEL=chrome` explicitly selects an installed Chrome. Never treat changed browser rasterization as visual approval.

For a security issue, avoid public disclosure of secrets. Use GitHub private vulnerability reporting if enabled; otherwise contact the maintainer with a minimal non-sensitive description to arrange a private channel.
