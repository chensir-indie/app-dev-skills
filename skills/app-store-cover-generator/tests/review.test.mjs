import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { createReview, validateReview } from "../scripts/review.mjs";
const project = JSON.parse(
  await readFile(
    new URL("../assets/starter/project.json", import.meta.url),
    "utf8",
  ),
);
const m = { project },
  digest = "f".repeat(64);
function complete() {
  const r = createReview(m, digest);
  r.reviewer = "Test reviewer";
  r.reviewedAt = "2026-10-12T00:00:00Z";
  for (const x of [r.referenceComparison, ...r.cells]) {
    x.status = "pass";
    x.notes = "Test evidence only";
  }
  return r;
}
test("review starts pending and binds every exact exported cell", () => {
  const r = createReview(m, digest);
  assert.equal(r.cells.length, 12);
  assert.throws(() => validateReview(r, m, digest), /unresolved review/);
  assert.equal(validateReview(complete(), m, digest).reviewRecord, "complete");
});
for (const [name, mutate, expected] of [
  ["stale export", (r) => (r.manifestSha256 = "old"), /stale/],
  ["missing cell", (r) => r.cells.pop(), /missing/],
  ["duplicate cell", (r) => (r.cells[0] = r.cells[1]), /duplicate/],
  [
    "extra cell",
    (r) => r.cells.push({ file: "extra.png", status: "pass", notes: "test" }),
    /matrix/,
  ],
  ["unresolved cell", (r) => (r.cells[0].status = "needs-fix"), /unresolved/],
  [
    "unsubstantiated exception",
    (r) => {
      r.cells[0].status = "accepted-exception";
      r.cells[0].notes = "";
    },
    /evidence/,
  ],
  [
    "unreviewed reference",
    (r) => (r.referenceComparison.status = "pending"),
    /reference comparison/,
  ],
  ["missing reviewer", (r) => (r.reviewer = ""), /reviewer/],
])
  test(`review rejects ${name}`, () => {
    const r = complete();
    mutate(r);
    assert.throws(() => validateReview(r, m, digest), expected);
  });
test("accepted exceptions stay distinct from an all-pass review", () => {
  const r = complete();
  r.cells[0].status = "accepted-exception";
  assert.equal(
    validateReview(r, m, digest).reviewRecord,
    "complete-with-exceptions",
  );
});
