# Contributing

Use Node 22 or newer and `npm ci`. Install Chromium, then run `npm run check` (documentation links/entry fields, unit tests and browser tests) before submitting executable changes. `npm test` and `npm run test:browser` remain available for focused iteration. Keep the lockfile current. Add a failing regression case for changed validation behavior rather than tests that match documentation wording.

Use original or redistribution-cleared fixtures. Never include credentials, real customer notes, private paths, screenshots containing personal data or private application source. Test only against local fixtures; do not publish to store/social accounts as part of tests.

Keep SKILL.md short and route detailed guidance to references. Document what automation cannot verify. A new check must describe both coverage and false-positive/false-negative limits. Preserve explicit user choices instead of turning one app's story, language count or release policy into a universal rule.

For a security concern, avoid public disclosure of secrets. Use GitHub private vulnerability reporting if available; otherwise report only a minimal non-sensitive description to the maintainer and request a private channel.

Freeze a baseline commit for each audit. Reproduce proposed validator fixes against a local broken fixture before implementation, then run the same test and the full check command. Keep browser fixtures isolated and close servers even if browser startup fails. A record validator must never fabricate reviewer judgments or convert automated-pass into visual approval.
