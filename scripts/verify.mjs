import { readFile, readdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { validateProject, cells } from "./contract.mjs";
import { inspectPNG } from "./png.mjs";
import { auditedFields } from "../assets/starter/text.js";
export async function verify(root) {
  const m = JSON.parse(
    await readFile(path.join(root, "manifest.json"), "utf8"),
  );
  if (
    m.schemaVersion !== 1 ||
    !Array.isArray(m.results) ||
    !Array.isArray(m.contactSheets)
  )
    throw new Error("Invalid export manifest structure");
  validateProject(m.project);
  if (
    !Array.isArray(m.sources) ||
    !m.sources.length ||
    m.sources.some(
      (x) =>
        typeof x?.file !== "string" ||
        !x.file ||
        x.file.startsWith("/") ||
        x.file.includes("\\") ||
        x.file.split("/").includes("..") ||
        !/^[a-f0-9]{64}$/.test(x.sha256),
    ) ||
    new Set(m.sources.map((x) => x.file)).size !== m.sources.length
  )
    throw new Error("Invalid source hash records");
  const expected = cells(m.project),
    errors = [];
  if (m.status !== "automated-pass")
    errors.push("export did not pass automated audit");
  if (m.results.length !== expected.length)
    errors.push("matrix count mismatch");
  if (
    m.sourceIssues !== undefined &&
    (!Array.isArray(m.sourceIssues) || m.sourceIssues.length)
  )
    errors.push("unresolved source audit issues");
  if (m.visualReview !== "pending")
    errors.push("visual review belongs in a separate bound review record");
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
    for (const id of auditedFields(
      m.project,
      m.project.slides.find((x) => x.id === e.slide),
    )) {
      const texts = r.texts?.filter((x) => x.id === id) ?? [];
      if (
        texts.length !== 1 ||
        !Number.isFinite(texts[0].scale) ||
        texts[0].scale < m.project.minTextScale ||
        !texts[0].rects?.length
      )
        errors.push(`${e.file}: missing or invalid text audit ${id}`);
    }
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
      if (
        inspectPNG(await readFile(path.join(root, file))).sha256 !==
        records[0].sha256
      )
        errors.push(`${file}: hash mismatch`);
    } catch {
      errors.push(`${file}: missing or invalid contact sheet`);
    }
  }
  async function visit(dir) {
    for (const e of await readdir(dir, { withFileTypes: true })) {
      const file = path.join(dir, e.name);
      if (e.isSymbolicLink()) errors.push(`output symlink: ${e.name}`);
      else if (e.isDirectory()) await visit(file);
      else if (
        e.name.toLowerCase().endsWith(".png") &&
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
