// Narrow repository checks; not a general Markdown/YAML parser.
import { readFile, readdir, access } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
const root = fileURLToPath(new URL("../", import.meta.url));
const files = ["SKILL.md", "README.md", "README.zh-CN.md", "CONTRIBUTING.md"];
for (const dir of ["references", "docs"]) {
  for (const entry of await readdir(path.join(root, dir)))
    if (entry.endsWith(".md")) files.push(`${dir}/${entry}`);
}
const errors = [];
const skill = await readFile(path.join(root, "SKILL.md"), "utf8");
const header = skill.match(/^---\r?\n([\s\S]*?)\r?\n---/m)?.[1];
if (
  !header ||
  !/^name: app-store-cover-generator$/m.test(header) ||
  !/^description: .+$/m.test(header)
)
  errors.push("Missing skill name or single-line description");
for (const file of files) {
  const text = await readFile(path.join(root, file), "utf8");
  for (const match of text.matchAll(/\]\(([^)]+)\)/g)) {
    const link = match[1];
    if (/^[a-z][a-z0-9+.-]*:/i.test(link) || link.startsWith("#")) continue;
    try {
      await access(path.resolve(root, path.dirname(file), link.split("#")[0]));
    } catch {
      errors.push(`${file}: broken local link ${link}`);
    }
  }
}
if (errors.length) throw new Error(errors.join("\n"));
console.log(
  `Skill entry fields and local links: PASS (${files.length} documents; external URLs and anchors not checked)`,
);
