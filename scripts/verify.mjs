import { readFile, readdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { validateProject, cells } from "./contract.mjs";
import { inspectPNG, sha256 } from "./png.mjs";
export async function verify(root) {
  const m = JSON.parse(
    await readFile(path.join(root, "manifest.json"), "utf8"),
  );
  validateProject(m.project);
  const expected = cells(m.project),
    errors = [];
  if (m.status !== "automated-pass")
    errors.push("export did not pass automated audit");
  if (m.results.length !== expected.length)
    errors.push("matrix count mismatch");
  const seen = new Set();
  for (const e of expected) {
    const matches = m.results.filter((r) => r.file === e.file);
    if (matches.length !== 1) {
      errors.push(`${e.file}: missing or duplicate record`);
      continue;
    }
    const r = matches[0];
    seen.add(r.file);
    if (
      ["locale", "device", "slide", "width", "height"].some(
        (k) => r[k] !== e[k],
      )
    )
      errors.push(`${e.file}: wrong cell identity`);
    if (!Array.isArray(r.issues) || r.issues.length)
      errors.push(`${e.file}: unresolved audit issues`);
    try {
      const info = inspectPNG(
        await readFile(path.join(root, e.file)),
        e.width,
        e.height,
      );
      if (info.sha256 !== r.sha256) errors.push(`${e.file}: hash mismatch`);
    } catch (error) {
      errors.push(`${e.file}: ${error.message}`);
    }
  }
  const sheets = m.project.locales.flatMap((l) =>
    m.project.devices.map((d) => `contact-${l.id}-${d.id}.png`),
  );
  if (m.contactSheets?.length !== sheets.length)
    errors.push("contact sheet count mismatch");
  for (const file of sheets) {
    const records = m.contactSheets?.filter((x) => x.file === file) || [];
    if (records.length !== 1) {
      errors.push(`${file}: missing/duplicate contact sheet`);
      continue;
    }
    seen.add(file);
    try {
      if (sha256(await readFile(path.join(root, file))) !== records[0].sha256)
        errors.push(`${file}: hash mismatch`);
    } catch {
      errors.push(`${file}: missing file`);
    }
  }
  async function visit(dir) {
    for (const e of await readdir(dir, { withFileTypes: true })) {
      const file = path.join(dir, e.name);
      if (e.isDirectory()) await visit(file);
      else if (
        e.name.endsWith(".png") &&
        !seen.has(path.relative(root, file).split(path.sep).join("/"))
      )
        errors.push(`unexpected PNG: ${e.name}`);
    }
  }
  await visit(root);
  if (errors.length) throw new Error(errors.join("\n"));
  return {
    cells: expected.length,
    status: "automated-pass",
    visualReview: m.visualReview,
  };
}
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  if (!process.argv[2])
    throw new Error("Usage: node scripts/verify.mjs OUTPUT_DIRECTORY");
  console.log(await verify(path.resolve(process.argv[2])));
}
