// Invoked by doctor.sh, so even a missing runtime has actionable diagnostics.
import { readFile } from "node:fs/promises";
import path from "node:path";
import { skillRoot, loadDependency, installCommand, launchBrowser } from "./runtime.mjs";

const args = process.argv.slice(2);
const scope = !args.length ? "render" : args.length === 2 && args[0] === "--scope" ? args[1] : null;
if (!["render", "core"].includes(scope)) {
  console.error("Usage: sh scripts/doctor.sh [--scope core|render]");
  process.exitCode = 2;
} else {
  const manifest = JSON.parse(await readFile(path.join(skillRoot, "package.json"), "utf8"));
  const dependencies = {};
  let failures = 0;
  for (const [name, expected] of Object.entries(manifest.dependencies)) {
    try {
      const loaded = await loadDependency(name);
      if (name === "pngjs" && typeof loaded.PNG?.sync?.read !== "function")
        throw new Error(`Package pngjs is missing PNG.sync.read. Repair dependencies:\n  ${await installCommand()}`);
      if (name === "playwright" && (typeof loaded.chromium?.launch !== "function" || typeof loaded.chromium?.executablePath !== "function"))
        throw new Error(`Package playwright is missing Chromium APIs. Repair dependencies:\n  ${await installCommand()}`);
      dependencies[name] = loaded;
      console.log(`[PASS] package: ${name} (required ${expected}; import and API checks passed)`);
    } catch (error) {
      console.error(`[FAIL] package: ${name}\n${error.message}`);
      failures++;
    }
  }
  if (scope === "core") {
    console.log("[SKIP] browser: --scope core; export readiness has not been checked.");
  } else if (!dependencies.playwright) {
    console.error("[FAIL] browser: cannot launch until the Playwright package is available.");
    failures++;
  } else {
    let browser;
    try {
      browser = await launchBrowser(dependencies.playwright.chromium);
      const page = await browser.newPage();
      await page.setContent("<main>cover-doctor</main>");
      if (await page.locator("main").textContent() !== "cover-doctor")
        throw new Error("Browser page smoke check failed.");
      console.log(`[PASS] browser: ${process.env.PLAYWRIGHT_CHANNEL || "chromium"} ${browser.version()} launched and rendered a local page.`);
    } catch (error) {
      console.error(`[FAIL] browser: ${error.message}`);
      failures++;
    } finally {
      await browser?.close();
    }
  }
  console.log(`Dependency setup command: ${await installCommand()}`);
  console.log(failures ? `Environment check failed (${failures} check(s)). No packages or configuration were installed.` :
    `Environment check passed (${scope}). No packages or configuration were installed.`);
  process.exitCode = failures ? 1 : 0;
}
