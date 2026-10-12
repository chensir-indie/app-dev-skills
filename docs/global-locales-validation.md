# Global locale support validation — 2026-10-12

Scope: locale catalog/tooling, script-aware typography, skill description, and English/Chinese installation documentation. This supplements the historical initial-release evidence; it does not replace that snapshot.

- `npm test`: 16 passing tests, including preservation of regional copy, missing translations, custom script direction, malformed tags, and safe project-copy behavior.
- `npm run test:browser`: 4 passing tests. The global test exercises 50 locales × 2 native device canvases (1284×2778 and 2048×2732), checking DOM copy, lang/dir, selected font stack and layout geometry. It uses short **script samples**, not 50 product translations.
- Additional native PNG export and verification: 12 demo cells (English, simplified Chinese, Arabic; two slides and two devices) plus 8 script-sample cells (Telugu, Hebrew, Bangla, Japanese; one slide and two devices).
- Visual spot checks of Chinese, Arabic, Hebrew and Telugu contact sheets. These are geometry/appearance checks, not native-speaker translation approval or proof that every character uses a specific font.
- Skills CLI 1.7.2 successfully discovered and installed the local repository into a fresh temporary Codex project. The installed localization check ran successfully. Public-repository installation depends on the published revision and network availability.
- Skill frontmatter validation and `git diff --check` passed.

| Local evidence directory under `.test-output/` | PNG cells | Automated status | Manifest SHA-256 |
| --- | --- | --- | --- |
| final-native-demo-20261012 | 12 | automated-pass | `502328bfa18f8bcf7b5f6424880988c037d8bb05ef4969eca58918801f410430` |
| final-script-native-export | 8 | automated-pass | `3f237844b07f0ca0fbabcf95eeabbd3a3280bc84ee3d9d54333ba784d1ff95b6` |

Export artifacts remain Git-ignored. Each manifest records source hashes and browser/OS metadata; `visualReview` remains `pending`. System-font availability differs across machines. All production translations, raster UI language, fonts and approved-reference fidelity still need review for the actual app.

## Complete translated demo follow-up — 2026-10-12

The runnable demo now includes explicit draft copy for all 50 catalog locales, across two stories and phone/tablet canvases. The original three-locale starter remains available for small projects; `npm run demo` and `init.mjs --locales app-store` use the full set. Product locale expansion still leaves missing translations blank.

- `npm run check`: 32 unit tests and 13 browser tests passed. The new browser matrix checks all 200 cells at native dimensions, exact copy, language/direction, and layout constraints.
- Native export and `verify.mjs`: all 200 PNG cells passed dimensions, opacity, nonblank content, hashes, and layout checks.
- The first full-copy run exposed two Telugu tablet headline overflows. Increasing the tablet header box from 20% to 21% resolved both while preserving the 0.80 text scale floor.
- Inspected all 100 locale/device contact sheets as ten overview mosaics, plus larger Arabic, Gujarati, Kannada, Japanese, Telugu and Urdu tablet exports. This is layout review, not native-speaker approval.
- Browser platform-font inspection found nonempty font records for all 50 demo headlines and no LastResort font on this macOS machine. This does not guarantee font availability on other systems.
- The export manifest intentionally retains `visualReview: pending`: demo inspection does not approve production translations or fidelity against a real product reference.

| Local evidence under `.test-output/` | Purpose |
| --- | --- |
| all-locales-final-check.log | Passing unit and browser checks |
| all-locales-export-v2/ | 200 native exports and 100 contact sheets |
| all-locales-review/ | Ten inspected overview mosaics |
| global-demo-fonts.json | Browser-reported headline font records |

Manifest SHA-256: `52793814468dd5dcc03d17ec85fac58b6cf66cb8ce8dc4f349fd7cef6ddb9fe4`. Export artifacts remain Git-ignored. Bundled translations are drafts; production copy requires review.
