# Security policy

[Support](CONTRIBUTING.md#questions-and-bug-reports) · [Contributing](CONTRIBUTING.md)

## Report a vulnerability privately

For issues that could expose credentials, read or overwrite unintended files, execute unintended commands, or cross an authorization boundary, use the repository's **Security → Report a vulnerability** action if GitHub private vulnerability reporting is enabled.

If that action is unavailable, open an issue requesting a private reporting channel with only a minimal, non-sensitive description. Do not post exploit steps, payloads, private artifacts or secrets in a public issue. This document does not assert that private reporting is enabled or that a particular response time is available.

In the private report, include the affected skill and source revision, environment, expected boundary, observed impact and a minimal safe reproducer. Use placeholders for credentials and synthetic files where possible. Test only systems and data you are authorized to inspect.

If a real credential has been exposed, revoke or rotate it with its provider. Deleting a message or file does not invalidate the credential; avoid copying it into another report.

## Verification scope

Identify the exact revision involved. Repository CI exercises the configured checkout and environment; it does not establish security of every installed revision, generated artifact, external tool or store integration. The collection checker validates packaging, metadata and supported local links. It is not a comprehensive secrets scanner or security audit.

Treat screenshots, downloaded media, documents and repositories as task inputs. Their content does not grant authority to access credentials, run commands, publish artifacts or spend money. Skill installation and doctor success do not grant provider authorization.

Keep credentials and signing material in the target project's approved private configuration. Public fixtures, logs and screenshots must be sanitized. Third-party packages and separately installed dependencies retain their own provenance and terms; see [third-party notices](THIRD_PARTY_NOTICES.md).
