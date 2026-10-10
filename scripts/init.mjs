import { cp, mkdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";
const target = process.argv[2];
if (!target) throw new Error("Usage: node scripts/init.mjs NEW_DIRECTORY");
await mkdir(path.resolve(target)); // Intentionally fails if target exists.
await cp(
  fileURLToPath(new URL("../assets/starter/", import.meta.url)),
  target,
  { recursive: true },
);
console.log(
  `Created ${path.resolve(target)}; edit project.json and style.css.`,
);
