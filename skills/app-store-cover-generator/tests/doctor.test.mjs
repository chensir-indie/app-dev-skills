import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, cp, writeFile, chmod, symlink, rm, access } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const run = promisify(execFile);
const source = fileURLToPath(new URL("../", import.meta.url));

async function fixture(t, { node = true, npm = true, repository = false } = {}) {
  const base = await mkdtemp(path.join(tmpdir(), "cover doctor 'fixture-"));
  t.after(() => rm(base, { recursive: true, force: true }));
  const root = path.join(base, "skills", "app-store-cover-generator");
  await cp(source, root, { recursive: true, filter: (file) => path.basename(file) !== "node_modules" });
  const bin = path.join(base, "bin");
  await mkdir(bin);
  if (node) await symlink(process.execPath, path.join(bin, "node"));
  if (npm) {
    await writeFile(path.join(bin, "npm"), "#!/bin/sh\nprintf '11.0.0\\n'\n");
    await chmod(path.join(bin, "npm"), 0o755);
  }
  if (repository) await writeFile(path.join(base, "package.json"), JSON.stringify({ name: "app-dev-skills", workspaces: ["skills/*"] }));
  const env = { ...process.env, PATH: bin };
  delete env.PLAYWRIGHT_CHANNEL;
  return { root, bin, base, env };
}
async function doctor(f, args = [], extraEnv = {}) {
  try {
    const result = await run("/bin/sh", [path.join(f.root, "scripts/doctor.sh"), ...args], {
      cwd: f.base, env: { ...f.env, ...extraEnv },
    });
    return { code: 0, output: result.stdout + result.stderr };
  } catch (error) {
    return { code: error.code, output: error.stdout + error.stderr };
  }
}
async function packageStub(f, name, body) {
  const root = path.join(f.root, "node_modules", name);
  await mkdir(root, { recursive: true });
  await writeFile(path.join(root, "package.json"), JSON.stringify({ name, type: "module", exports: "./index.mjs" }));
  await writeFile(path.join(root, "index.mjs"), body);
}
async function packages(f, launch = "throw new Error('Executable does not exist at /missing/cache/chromium');") {
  await packageStub(f, "pngjs", "export const PNG = {sync:{read: () => ({})}};");
  await packageStub(f, "playwright", `export const chromium = {
    executablePath: () => '/missing/cache/chromium',
    launch: async (options) => { ${launch} }
  };`);
}

test("shell doctor diagnoses missing Node without using Node", async (t) => {
  const f = await fixture(t, { node: false });
  const result = await doctor(f);
  assert.equal(result.code, 1);
  assert.match(result.output, /Node.js: executable not found/);
  assert.match(result.output, /https:\/\/nodejs.org\/en\/download/);
  assert.doesNotMatch(result.output, /ERR_MODULE_NOT_FOUND/);
  const retry = result.output.match(/After fixing the runtime, run:\n  (.+)\n/)?.[1];
  assert.ok(retry);
  await symlink("/bin/sh", path.join(f.bin, "sh"));
  const help = await run("/bin/sh", ["-c", `${retry} --help`], { env: f.env });
  assert.match(help.stdout, /Usage: sh scripts\/doctor.sh/);
});

test("shell doctor rejects unsupported Node before npm or package execution", async (t) => {
  const f = await fixture(t, { node: false });
  await writeFile(path.join(f.bin, "node"), "#!/bin/sh\nprintf 'v20.19.0\\n'\n");
  await chmod(path.join(f.bin, "node"), 0o755);
  const result = await doctor(f);
  assert.equal(result.code, 1);
  assert.match(result.output, /v20.19.0; requires >=22/);
});

test("shell doctor diagnoses missing and broken npm", async (t) => {
  const f = await fixture(t, { npm: false });
  let result = await doctor(f);
  assert.equal(result.code, 1);
  assert.match(result.output, /npm: executable not found/);
  await writeFile(path.join(f.bin, "npm"), "#!/bin/sh\nexit 9\n");
  await chmod(path.join(f.bin, "npm"), 0o755);
  result = await doctor(f);
  assert.equal(result.code, 1);
  assert.match(result.output, /npm: executable exists but cannot run/);
});

test("missing packages get install commands for independent and collection installs", async (t) => {
  for (const repository of [false, true]) {
    const f = await fixture(t, { repository });
    const result = await doctor(f, ["--scope", "core"]);
    assert.equal(result.code, 1);
    assert.match(result.output, /package: playwright/);
    assert.match(result.output, /package: pngjs/);
    assert.match(result.output, repository ? /&& npm ci/ : /&& npm install/);
    assert.match(result.output, /'\\''fixture/); // Printed commands escape a literal apostrophe in the installation path.
    assert.match(result.output, /\[SKIP\] browser/);
  }
});

test("default doctor checks browser launch; core skips only that check", async (t) => {
  const f = await fixture(t);
  await packages(f);
  const result = await doctor(f);
  assert.equal(result.code, 1);
  assert.match(result.output, /Browser installation: \/missing\/cache\/chromium/);
  assert.match(result.output, /npx --no-install playwright install chromium/);
  assert.match(result.output, /PLAYWRIGHT_CHANNEL=chrome/);
  const core = await doctor(f, ["--scope", "core"]);
  assert.equal(core.code, 0);
  assert.match(core.output, /export readiness has not been checked/);
});

test("doctor uses the selected Chrome channel and renders a smoke page", async (t) => {
  const f = await fixture(t);
  await packages(f, `
    if(options.channel !== 'chrome') throw new Error('Wrong browser channel');
    return { version: () => '123.test', close: async () => {}, newPage: async () => ({
      setContent: async (html) => { if(!html.includes('cover-doctor')) throw new Error('Missing smoke content'); },
      locator: () => ({ textContent: async () => 'cover-doctor' })
    }) };
  `);
  const result = await doctor(f, [], { PLAYWRIGHT_CHANNEL: "chrome" });
  assert.equal(result.code, 0);
  assert.match(result.output, /chrome 123.test launched and rendered/);
  const invalid = await doctor(f, [], { PLAYWRIGHT_CHANNEL: "firefox" });
  assert.equal(invalid.code, 1);
  assert.match(invalid.output, /Unsupported PLAYWRIGHT_CHANNEL/);
});

test("invalid doctor arguments fail instead of silently skipping checks", async (t) => {
  const f = await fixture(t);
  assert.equal((await doctor(f, ["--scope", "unknown"])).code, 2);
  assert.equal((await doctor(f, ["--core"])).code, 2);
});

test("direct export and verify explain missing dependencies", async (t) => {
  const f = await fixture(t);
  for (const command of ["export.mjs", "verify.mjs"]) {
    await assert.rejects(run(process.execPath, [path.join(f.root, "scripts", command), "missing-project", "unused-output"], { cwd: f.base }), (error) => {
      assert.notEqual(error.code, 0);
      assert.match(error.stderr, /Cannot load required package/);
      assert.match(error.stderr, /&& npm install/);
      return true;
    });
  }
});

test("browser failure happens before export creates an output directory", async (t) => {
  const f = await fixture(t);
  await packages(f);
  const project = path.join(f.base, "project");
  await cp(path.join(f.root, "assets/starter"), project, { recursive: true });
  const output = path.join(f.base, "output");
  await assert.rejects(run(process.execPath, [path.join(f.root, "scripts/export.mjs"), project, output], { cwd: f.base, env: f.env }), (error) => {
    assert.match(error.stderr, /Browser launch failed/);
    assert.match(error.stderr, /playwright install chromium/);
    return true;
  });
  await assert.rejects(access(output), { code: "ENOENT" });
});


test("Linux launch failures include explicit OS-library repair without running it", async (t) => {
  const f = await fixture(t);
  const runtimeURL = new URL(`file://${path.join(f.root, "scripts/runtime.mjs")}`).href;
  const script = `Object.defineProperty(process, 'platform', {value:'linux'}); const {browserRepair}=await import(${JSON.stringify(runtimeURL)}); console.log(browserRepair(new Error('libnss3.so missing'), {executablePath:()=>'/cache/chromium'}));`;
  const result = await run(process.execPath, ["--input-type=module", "-e", script]);
  assert.match(result.stdout, /libnss3.so missing/);
  assert.match(result.stdout, /npx --no-install playwright install-deps chromium/);
  assert.match(result.stdout, /may require administrator access/);
});


test("direct CLI imports reject an unsupported runtime with an installation guide", async (t) => {
  const f = await fixture(t);
  const entryURL = new URL(`file://${path.join(f.root, "scripts/init.mjs")}`).href;
  const script = `Object.defineProperty(process, 'version', {value:'v20.19.0'}); await import(${JSON.stringify(entryURL)});`;
  await assert.rejects(run(process.execPath, ["--input-type=module", "-e", script]), (error) => {
    assert.match(error.stderr, /Node.js v20.19.0 is unsupported/);
    assert.match(error.stderr, /https:\/\/nodejs.org\/en\/download/);
    assert.match(error.stderr, /doctor.sh/);
    return true;
  });
});


test("core doctor rejects an imported package with unusable exports", async (t) => {
  const f = await fixture(t);
  await packages(f);
  await packageStub(f, "pngjs", "export const PNG = {};\n");
  const result = await doctor(f, ["--scope", "core"]);
  assert.equal(result.code, 1);
  assert.match(result.output, /missing PNG.sync.read/);
  assert.match(result.output, /&& npm install/);
});
