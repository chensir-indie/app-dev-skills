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
