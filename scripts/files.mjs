import { readFile, readdir, realpath } from "node:fs/promises";
import path from "node:path";
import { createHash } from "node:crypto";
const sha256 = (data) => createHash("sha256").update(data).digest("hex");
export async function outsideSource(root, output) {
  const source = await realpath(root),
    resolved = path.resolve(output);
  const target = path.join(
    await realpath(path.dirname(resolved)),
    path.basename(resolved),
  );
  if (target === source || target.startsWith(source + path.sep))
    throw new Error("Output must be outside the source project");
  return { source, target };
}
export async function sourceSnapshot(root) {
  const files = [];
  async function visit(dir) {
    for (const entry of await readdir(dir, { withFileTypes: true })) {
      const file = path.join(dir, entry.name);
      if (entry.isSymbolicLink())
        throw new Error("Source symlinks are unsupported");
      if (entry.isDirectory()) await visit(file);
      else if (entry.isFile())
        files.push({
          file: path.relative(root, file).split(path.sep).join("/"),
          sha256: sha256(await readFile(file)),
        });
      else throw new Error("Only regular project files are supported");
    }
  }
  await visit(root);
  return files.sort((a, b) => a.file.localeCompare(b.file));
}
export function checkAssets(project, sources) {
  const hashes = new Map(sources.map((x) => [x.file, x.sha256]));
  for (const slide of project.slides) {
    for (const locale of project.locales) {
      const file = slide.art[locale.id] ?? slide.art.shared;
      if (!hashes.has(file))
        throw new Error(`${slide.id}/${locale.id}: missing art ${file}`);
    }
    if (slide.phases) {
      const values = slide.phases.map((file) => {
        if (!hashes.has(file))
          throw new Error(`${slide.id}: missing phase ${file}`);
        return hashes.get(file);
      });
      if (new Set(values).size !== values.length)
        throw new Error(`${slide.id}: motion phases contain identical files`);
    }
  }
}
