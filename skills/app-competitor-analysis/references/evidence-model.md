# Evidence model

## Identity and provenance

Identify each product with platform and store ID, bundle/package ID or canonical website. Preserve a sample's version/build, acquisition source and SHA-256. A mirror package's consistent signature does not establish an official-store signer match. A shared display name does not establish that two apps are the same product.

For an observation record source date, inspected date, platform/version when known, device/viewport, locale, account/tier and relevant permission/network state. Use “unknown” for unavailable values. Record a video timestamp, screenshot region, document section or file/function/line range. A URL alone is insufficient when the finding cannot be located on that page.

`observed_at` is the date of the source observation/capture, or the date a live source was consulted. Use `unknown` for an undated supplied artifact and explain it in `context`. Optional `inspected_at` records when you read/viewed a previously supplied artifact; `source_date` can preserve its publication/revision date separately. Never replace an unknown capture/publication date with today's reading date. Date values use `YYYY-MM-DD` or `unknown`.

Separate inspecting an artifact from verifying who published it. A supplied image can support an `observed` pixel claim even when “official screenshot” is only the user's source description. Record attribution as supplied, independently checked, or unknown; do not imply a webpage revisit. The optional source field `provenance_basis` can be `supplier_metadata`, `publisher_verified` or `unknown`, with the details in `context`.

## Evidence types and permitted conclusions

| Source kind | Supports | Does not establish by itself |
|---|---|---|
| `runtime` | Behavior observed under the recorded conditions | Other devices, tiers or versions; hidden backend implementation |
| `screenshot` | Visible structure, copy, geometry and style in the actual image | Unshown interactions, real latency, font files, responsive behavior |
| `official` | What the publisher documents or promises, at a dated source | Actual availability, performance, correctness or implementation |
| `static` | Resources, call paths and state/data handling in a pinned artifact | Successful runtime reachability, current release, backend internals |
| `research_note` | What an earlier analysis reports | Fresh verification of its primary sources |
| `concept` | A proposed design or synthetic test example | Competitor appearance, functionality or performance |

Claims use `observed`, `declared`, `static`, `reported`, `inferred` or `unknown`. These are provenance labels, not a universal confidence ranking. A static caller and an official screenshot answer different questions. Give important claims a precise scope instead of a generic “high confidence” badge.

For a supplied natural-language observer log without a recording/raw trace, use `research_note / reported` and retain its timestamps and conditions. An inspectable recording or raw runtime trace can support observation of what it actually shows, with attribution marked as supplied; reviewing it is not a new execution by the analyst.

- `observed` UI needs actual screenshot/runtime inspection. Observed interactions need runtime evidence. An official screenshot remains a screenshot **published by the vendor**, not an installed-app walkthrough.
- `declared` needs an official source. A secondhand quote in old research is `reported` until the official source is checked.
- `static` needs the pinned artifact and locator; describe supported code behavior in that version. “No match found” is limited to the searched files/methods, query and tool coverage.
- `inferred` states the inference and, for technology claims, at least one plausible alternative plus a way to distinguish them.
- `unknown` states the gap and the observation needed; it need not cite a nonexistent source. For consequential gaps, execute [the acquisition loop](evidence-acquisition.md) and record attempts; an unknown label is not a substitute for available research.

If versions conflict, keep both claims, dates and scopes. Do not combine an old package implementation with today's marketing into one verified product. Record that an action was attempted separately from its successful result. Do not interpret a success toast as proof of persistence, delivery or installability.

## Optional JSON ledger (schema version 1)

Use this when the report is broad enough to benefit from joins and automated checks. Markdown source IDs in the report should correspond to the ledger.

```json
{
  "schema_version": 1,
  "products": [{"id":"app-a", "name":"Example", "platform":"ios", "identity":"store:example", "kind":"app"}],
  "sources": [{"id":"E01", "product_id":"app-a", "kind":"official", "locator":"https://example.org/help#saving", "observed_at":"2026-10-20", "version":"unknown", "context":"Publisher help; not runtime"}],
  "claims": [{"id":"C01", "product_id":"app-a", "dimension":"interaction", "status":"declared", "text":"Publisher documents export after editing.", "source_ids":["E01"], "version":"unknown", "scope":"Published saving instructions"}],
  "coverage": [
    {"product_id":"app-a", "dimension":"ui", "status":"missing", "source_ids":[], "reason":"No image inspected"},
    {"product_id":"app-a", "dimension":"interaction", "status":"partial", "source_ids":["E01"], "reason":"Official happy path only"},
    {"product_id":"app-a", "dimension":"technology", "status":"missing", "source_ids":[], "reason":"No implementation evidence"},
    {"product_id":"app-a", "dimension":"business", "status":"out_of_scope", "source_ids":[], "reason":"Not requested"}
  ],
  "recommendations": [{"id":"R01", "text":"Make export state explicit", "basis_claim_ids":["C01"], "fit":"Users need portable results", "tradeoff":"Adds visible state", "validation":"Observe whether users locate the saved result"}]
}
```

Product kind is `app`, `system_feature` or `web`. Every product has one coverage row for each dimension: `ui`, `interaction`, `technology`, `business`. Coverage is `supported` within the stated scope, `partial`, `missing`, or `out_of_scope`; it is not an overall quality score. Supported/partial rows link sources. Unknown dimensions remain in the matrix rather than disappearing from the comparison.

Static sources additionally need `artifact_sha256` (64 hex characters). Local source locators may be relative to the ledger directory; add `sha256` and `local_path` when checking file integrity matters. Remote locators are never fetched by the checker. Record raw artifact hashes separately from derived text hashes.

Technology inferences require `alternatives` (a nonempty array) and `verification` (the distinguishing test). A measured claim additionally uses `measurement` with `unit`, `n`, `conditions` and `method`, and must have runtime evidence. A source's known version must match an observed/static claim's version. Split claims spanning revisions instead of hiding the mismatch with “latest”.

Before running `audit_evidence.py`, run `sh scripts/doctor.sh` from the skill directory and use the Python command it reports. The audit uses only the Python 3.9+ standard library. If no compatible interpreter is available, follow [setup guidance](html-delivery.md#reusable-renderer); a readable ledger and source inspection can continue while the automated audit remains pending.

`audit_evidence.py` checks these structural conditions, IDs, cross-product joins and declared coverage. It cannot determine whether a screenshot was viewed, whether a function is reachable, whether text supports a claim, or whether a recommendation is good. Review those manually with the evaluation rubric.
