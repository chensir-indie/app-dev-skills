import { readFile } from "node:fs/promises";
import { localeInfo } from "../assets/starter/locale.js";
export const catalog = JSON.parse(
  await readFile(
    new URL("../assets/locales/app-store.json", import.meta.url),
    "utf8",
  ),
);
export const copyFields = ["headline", "support", "uiTitle", "uiBody"];
export function selectLocales(selection) {
  const ids =
    selection === "app-store"
      ? catalog.locales
      : selection.split(",").map((x) => x.trim());
  if (!ids.length || new Set(ids).size !== ids.length)
    throw new Error("Locale selection must be nonempty and unique");
  return ids.map((id) => {
    const { direction } = localeInfo(id);
    return { id, direction };
  });
}
export function addLocales(project, selection) {
  const p = structuredClone(project);
  for (const locale of selectLocales(selection)) {
    if (!p.locales.some((x) => x.id === locale.id)) p.locales.push(locale);
    for (const slide of p.slides) {
      slide.copy ??= {};
      slide.copy[locale.id] ??= Object.fromEntries(
        copyFields.map((key) => [key, ""]),
      );
    }
  }
  return p;
}
export function coverage(project) {
  const missing = [];
  for (const locale of project.locales)
    for (const slide of project.slides)
      for (const field of copyFields)
        if (
          typeof slide.copy?.[locale.id]?.[field] !== "string" ||
          !slide.copy[locale.id][field].trim()
        )
          missing.push(`${locale.id}/${slide.id}/${field}`);
  return {
    locales: project.locales.length,
    slides: project.slides.length,
    missing,
    status: missing.length ? "incomplete" : "complete",
  };
}
