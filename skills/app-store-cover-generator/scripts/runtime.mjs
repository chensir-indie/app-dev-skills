// Shared actionable failures for CLI entrypoints; built-ins only until requested.
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const skillRoot = fileURLToPath(new URL("../", import.meta.url));
if (Number(process.version.slice(1).split(".")[0]) < 22)
  throw new Error(`Node.js ${process.version} is unsupported; this toolkit requires Node.js 22+. Install or select it at https://nodejs.org/en/download, then reopen the terminal/agent and run sh scripts/doctor.sh from ${skillRoot}`);
const quote = (value) => `'${value.replaceAll("'", "'\\''")}'`;

export async function installCommand() {
  const repository = path.resolve(skillRoot, "../..");
  try {
    const manifest = JSON.parse(await readFile(path.join(repository, "package.json"), "utf8"));
    if (manifest.name === "app-dev-skills" && manifest.workspaces?.includes("skills/*"))
      return `cd ${quote(repository)} && npm ci`;
  } catch { /* An individually installed skill has no collection workspace. */ }
  return `cd ${quote(skillRoot)} && npm install`;
}

export async function loadDependency(name) {
  try {
    return await import(name);
  } catch (cause) {
    throw new Error(
      `Cannot load required package ${name}.\nRepair dependencies:\n  ${await installCommand()}\n` +
      `Then run:\n  sh ${quote(path.join(skillRoot, "scripts/doctor.sh"))}\n` +
      `Details: ${cause.message}`,
      { cause },
    );
  }
}

export function browserOptions() {
  const channel = process.env.PLAYWRIGHT_CHANNEL;
  if (!channel || channel === "chromium") return { timeout: 15000 };
  if (channel === "chrome") return { channel: "chrome", timeout: 15000 };
  throw new Error("Unsupported PLAYWRIGHT_CHANNEL. Use chromium (default) or chrome for installed Google Chrome.");
}

export function browserRepair(error, chromium) {
  const command = `cd ${quote(skillRoot)} && npx --no-install playwright install chromium`;
  const details = error.message;
  const channel = process.env.PLAYWRIGHT_CHANNEL;
  const lines = [
    `Browser launch failed (${channel || "chromium"}).`,
    `Browser installation: ${channel === "chrome" ? "installed Google Chrome (Playwright channel chrome)" : chromium.executablePath()} (headless launch path, if different, appears in Details)`,
  ];
  if (channel === "chrome")
    lines.push("Install Google Chrome: https://www.google.com/chrome/", "Or unset PLAYWRIGHT_CHANNEL and install bundled Chromium:");
  else lines.push("Install the browser matching the installed Playwright package:");
  lines.push(`  ${command}`);
  if (process.platform === "linux")
    lines.push(
      "If Chromium is installed but Linux libraries are missing, review Playwright's OS dependency requirements:",
      "  https://playwright.dev/docs/browsers#install-system-dependencies",
      `  cd ${quote(skillRoot)} && npx --no-install playwright install-deps chromium`,
      "The install-deps command changes OS packages and may require administrator access; run it intentionally.",
    );
  lines.push("An existing Chrome installation can be checked with:",
    `  PLAYWRIGHT_CHANNEL=chrome sh ${quote(path.join(skillRoot, "scripts/doctor.sh"))}`,
    `Details: ${details}`);
  return lines.join("\n");
}

export async function launchBrowser(chromium) {
  // Validate options separately so an unsupported channel keeps its exact fix.
  const options = browserOptions();
  try {
    return await chromium.launch(options);
  } catch (cause) {
    throw new Error(browserRepair(cause, chromium), { cause });
  }
}
