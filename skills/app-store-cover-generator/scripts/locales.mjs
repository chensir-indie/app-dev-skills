import "./runtime.mjs";
import { cp, mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { outsideSource, sourceSnapshot } from "./files.mjs";
import { catalog, addLocales, coverage } from "./localization.mjs";
import { localeInfo } from "../assets/starter/locale.js";
import { validateProject } from "./contract.mjs";
const [command, root, output, selection, ...extra] = process.argv.slice(2);
if (command === "list" && !root) {
  console.log(
    JSON.stringify(
      {
        ...catalog,
        locales: catalog.locales.map((id) => ({
          ...localeInfo(id),
          name: new Intl.DisplayNames(["en"], { type: "language" }).of(id),
        })),
      },
      null,
      2,
    ),
  );
} else if (command === "check" && root && !output) {
  const p = JSON.parse(await readFile(path.join(root, "project.json"), "utf8"));
  console.log(JSON.stringify(coverage(p), null, 2));
  validateProject(p); // Complete copy alone cannot hide a bad locale or direction.
} else if (command === "add" && root && output && selection && !extra.length) {
  const { source, target } = await outsideSource(root, output);
  await sourceSnapshot(source);
  const p = addLocales(
    JSON.parse(await readFile(path.join(source, "project.json"), "utf8")),
    selection,
  );
  await mkdir(target); // Refuse overwrite; keep the original project intact.
  await cp(source, target, { recursive: true, dereference: false });
  await writeFile(
    path.join(target, "project.json"),
    JSON.stringify(p, null, 2) + "\n",
  );
  console.log(JSON.stringify(coverage(p), null, 2));
} else {
  throw new Error(
    "Usage: locales.mjs list | check PROJECT | add PROJECT NEW_PROJECT app-store|ja,fr-FR,ar-SA",
  );
}
