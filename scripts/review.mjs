import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { verify } from "./verify.mjs";
import { sha256 } from "./png.mjs";
import { cells } from "./contract.mjs";
const nonempty = (value) =>
  typeof value === "string" && value.trim().length > 0;
export function createReview(manifest, digest) {
  return {
    schemaVersion: 1,
    manifestSha256: digest,
    reviewer: "",
    reviewedAt: "",
    referenceComparison: { status: "pending", notes: "" },
    cells: cells(manifest.project).map((cell) => ({
      file: cell.file,
      status: "pending",
      notes: "",
    })),
  };
}
export function validateReview(review, manifest, digest) {
  const errors = [],
    expected = cells(manifest.project).map((x) => x.file);
  if (review?.schemaVersion !== 1)
    errors.push("review schemaVersion must equal 1");
  if (review?.manifestSha256 !== digest)
    errors.push("review is stale: manifest hash mismatch");
  if (!nonempty(review?.reviewer)) errors.push("reviewer is required");
  if (
    !nonempty(review?.reviewedAt) ||
    !/^\d{4}-\d\d-\d\dT/.test(review.reviewedAt) ||
    !Number.isFinite(Date.parse(review.reviewedAt))
  )
    errors.push("reviewedAt must be an ISO timestamp");
  const check = (record, label) => {
    if (!["pass", "accepted-exception"].includes(record?.status))
      errors.push(`${label}: unresolved review`);
    if (!nonempty(record?.notes))
      errors.push(`${label}: evidence notes are required`);
  };
  check(review?.referenceComparison, "reference comparison");
  const records = Array.isArray(review?.cells) ? review.cells : [];
  if (
    records.length !== expected.length ||
    records.some((x) => !expected.includes(x?.file))
  )
    errors.push("review matrix mismatch");
  for (const file of expected) {
    const matches = records.filter((x) => x?.file === file);
    if (matches.length !== 1)
      errors.push(`${file}: missing or duplicate review`);
    else check(matches[0], file);
  }
  if (errors.length) throw new Error(errors.join("\n"));
  const exceptions = [review.referenceComparison, ...records].filter(
    (x) => x.status === "accepted-exception",
  ).length;
  return {
    cells: expected.length,
    reviewRecord: exceptions ? "complete-with-exceptions" : "complete",
    exceptions,
    limitation:
      "Validates the record and export binding, not the reviewer judgments.",
  };
}
export async function checkReview(output, file) {
  await verify(output);
  const bytes = await readFile(path.join(output, "manifest.json"));
  return validateReview(
    JSON.parse(await readFile(file, "utf8")),
    JSON.parse(bytes),
    sha256(bytes),
  );
}
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const [command, output, file, ...extra] = process.argv.slice(2);
  if (!output || !file || extra.length || !["init", "check"].includes(command))
    throw new Error(
      "Usage: review.mjs init OUTPUT NEW_REVIEW.json | check OUTPUT REVIEW.json",
    );
  if (command === "check") console.log(await checkReview(output, file));
  else {
    await verify(output);
    const bytes = await readFile(path.join(output, "manifest.json"));
    await writeFile(
      file,
      JSON.stringify(createReview(JSON.parse(bytes), sha256(bytes)), null, 2) +
        "\n",
      { flag: "wx" },
    );
    console.log(
      "Created pending review. Inspect the images and reference before recording judgments.",
    );
  }
}
