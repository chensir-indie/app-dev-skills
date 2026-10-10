# Contributing

Use Node 22 or newer and `npm ci`. Run `npm test`, install Chromium, then run `npm run test:browser` before submitting executable changes. Keep the lockfile current. Add a failing regression case for changed validation behavior rather than tests that match documentation wording.

Use original or redistribution-cleared fixtures. Never include credentials, real customer notes, private paths, screenshots containing personal data or private application source. Test only against local fixtures; do not publish to store/social accounts as part of tests.

Keep SKILL.md short and route detailed guidance to references. Document what automation cannot verify. A new check must describe both coverage and false-positive/false-negative limits. Preserve explicit user choices instead of turning one app's story, language count or release policy into a universal rule.

For a security concern, avoid public disclosure of secrets. Use GitHub private vulnerability reporting if available; otherwise report only a minimal non-sensitive description to the maintainer and request a private channel.
