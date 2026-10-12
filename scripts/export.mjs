import { readFile, writeFile, mkdir, readdir } from "node:fs/promises";
import path from "node:path";
import { chromium } from "playwright";
import { serve } from "./server.mjs";
import { validateProject, cells } from "./contract.mjs";
import { auditCover } from "./audit.mjs";
import { inspectPNG, sha256 } from "./png.mjs";
const [rootArg, outArg] = process.argv.slice(2);
if (!rootArg || !outArg)
  throw new Error(
    "Usage: node scripts/export.mjs PROJECT NEW_OUTPUT_DIRECTORY",
  );
const root = path.resolve(rootArg),
  out = path.resolve(outArg);
const p = validateProject(
  JSON.parse(await readFile(path.join(root, "project.json"), "utf8")),
);
const sources = [];
async function sourceTree(dir) {
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const file = path.join(dir, e.name);
    if (e.isSymbolicLink()) throw new Error("Source symlinks are unsupported");
    if (e.isDirectory()) await sourceTree(file);
    else
      sources.push({
        file: path.relative(root, file).split(path.sep).join("/"),
        sha256: sha256(await readFile(file)),
      });
  }
}
if (out === root || out.startsWith(root + path.sep))
  throw new Error("Output must be outside the source project");
await sourceTree(root);
sources.sort((a, b) => a.file.localeCompare(b.file));
await mkdir(out); // Preserve previous runs; no overwrite flag.
const server = await serve(root);
let browser;
const report = {
  schemaVersion: 1,
  generatedAt: new Date().toISOString(),
  status: "incomplete",
  visualReview: "pending",
  project: p,
  sources,
  results: [],
  contactSheets: [],
  limitations: [
    "Range rectangles are not exact glyph outlines.",
    "Occlusion sampling is heuristic; masks, transparency and pointer-events:none require visual review.",
    "CSS font names do not prove glyph coverage or actual fallback face.",
    "No OCR, translation, reference fidelity, rights or store acceptance check.",
  ],
};
try {
  browser = await chromium.launch();
  report.environment = {
    node: process.version,
    platform: process.platform,
    architecture: process.arch,
    browser: browser.version(),
  };
  const context = await browser.newContext({
    deviceScaleFactor: 1,
    locale: "en-US",
    timezoneId: "UTC",
    colorScheme: "light",
    reducedMotion: "reduce",
  });
  const page = await context.newPage();
  let runtimeErrors = [];
  page.on("pageerror", (error) => runtimeErrors.push(error.message));
  await page.route("**/*", (route) => {
    const url = new URL(route.request().url());
    return url.origin === server.url ||
      ["data:", "blob:"].includes(url.protocol)
      ? route.continue()
      : route.abort();
  });
  for (const cell of cells(p)) {
    runtimeErrors = [];
    const result = { ...cell, issues: [] };
    report.results.push(result);
    try {
      await page.setViewportSize({ width: cell.width, height: cell.height });
      await page.goto(
        `${server.url}/?${new URLSearchParams({ ...cell, export: "1" })}`,
        { waitUntil: "networkidle" },
      );
      await page.waitForFunction(
        () => window.coverReady === true,
        {},
        { timeout: 10000 },
      );
      const audit = await page.evaluate(auditCover, p.minTextScale);
      Object.assign(result, audit);
      const rendered = await page.evaluate(() => ({
        identity: { ...document.querySelector("#cover").dataset },
        lang: document.documentElement.lang,
        direction: document.documentElement.dir,
        copy: Object.fromEntries(
          ["headline", "support", "uiTitle", "uiBody"].map((key) => [
            key,
            document.querySelector(`#${key} [data-text]`)?.textContent,
          ]),
        ),
      }));
      for (const key of ["locale", "device", "slide"])
        if (rendered.identity[key] !== cell[key])
          result.issues.push({ reason: "wrong-rendered-identity", key });
      const expectedLocale = p.locales.find((x) => x.id === cell.locale);
      if (
        rendered.lang !== cell.locale ||
        rendered.direction !== expectedLocale.direction
      )
        result.issues.push({ reason: "wrong-rendered-language-direction" });
      const expectedCopy = p.slides.find((x) => x.id === cell.slide).copy[
        cell.locale
      ];
      for (const key of Object.keys(rendered.copy))
        if (rendered.copy[key] !== expectedCopy[key])
          result.issues.push({ reason: "wrong-rendered-copy", key });
      result.issues.push(
        ...runtimeErrors.map((message) => ({
          reason: "runtime-error",
          message,
        })),
      );
      const file = path.join(out, cell.file);
      await mkdir(path.dirname(file), { recursive: true });
      const data = await page.locator("#cover").screenshot({
        path: file,
        animations: "disabled",
        omitBackground: false,
      });
      Object.assign(result, inspectPNG(data, cell.width, cell.height));
    } catch (error) {
      result.issues.push({ reason: "render-failed", message: error.message });
    }
    console.log(`${cell.file}: ${result.issues.length ? "FAIL" : "PASS"}`);
  }
  // Independent sheet page uses rendered PNGs, so it cannot substitute for native export checks.
  const sheet = await context.newPage();
  for (const l of p.locales)
    for (const d of p.devices) {
      const subset = report.results.filter(
        (x) => x.locale === l.id && x.device === d.id && x.sha256,
      );
      if (subset.length !== p.slides.length) continue;
      const images = await Promise.all(
        subset.map(
          async (x) =>
            `<figure><img src="data:image/png;base64,${(await readFile(path.join(out, x.file))).toString("base64")}"><figcaption>${x.slide}</figcaption></figure>`,
        ),
      );
      await sheet.setViewportSize({
        width: Math.min(4, subset.length) * 220,
        height:
          Math.ceil(subset.length / 4) *
            (Math.ceil((196 * d.height) / d.width) + 50) +
          70,
      });
      await sheet.setContent(
        `<html><style>body{margin:0;padding:12px;font:14px Arial;background:#eaf0f4}section{display:grid;grid-template-columns:repeat(${Math.min(4, subset.length)},196px);gap:24px}figure{margin:0}img{width:196px}h1{font-size:16px}</style><h1>${l.id} / ${d.id}</h1><section>${images.join("")}</section></html>`,
      );
      await sheet.evaluate(() =>
        Promise.all([...document.images].map((x) => x.decode())),
      );
      const file = `contact-${l.id}-${d.id}.png`;
      await sheet.screenshot({ path: path.join(out, file), fullPage: true });
      report.contactSheets.push({
        file,
        sha256: sha256(await readFile(path.join(out, file))),
      });
    }
  report.status = report.results.every((x) => x.issues.length === 0)
    ? "automated-pass"
    : "automated-fail";
} catch (error) {
  report.error = error.message;
  process.exitCode = 1;
} finally {
  await browser?.close();
  await server.close();
  await writeFile(
    path.join(out, "manifest.json"),
    JSON.stringify(report, null, 2) + "\n",
  );
  if (report.status !== "automated-pass") process.exitCode = 1;
  console.log(
    `Report: ${path.join(out, "manifest.json")} (${report.status}; visual review pending)`,
  );
}
