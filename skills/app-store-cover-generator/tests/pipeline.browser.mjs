import test from "node:test";
import assert from "node:assert/strict";
import {
  mkdtemp,
  cp,
  readFile,
  writeFile,
  rm,
  symlink,
  access,
} from "node:fs/promises";
import { writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFile, spawn } from "node:child_process";
import { promisify } from "node:util";
import { chromium } from "playwright";
import { serve } from "../scripts/server.mjs";
import { auditCover } from "../scripts/audit.mjs";
const run = promisify(execFile),
  repo = fileURLToPath(new URL("../", import.meta.url));
async function fixture(work) {
  const tmp = await mkdtemp(path.join(tmpdir(), "cover-pipeline-"));
  const root = path.join(tmp, "project");
  try {
    await cp(path.join(repo, "assets/starter"), root, { recursive: true });
    const p = JSON.parse(
      await readFile(path.join(root, "project.json"), "utf8"),
    );
    p.locales = p.locales.slice(0, 1);
    p.devices = [{ id: "phone", kind: "phone", width: 360, height: 780 }];
    await writeFile(path.join(root, "project.json"), JSON.stringify(p));
    await work({ root, tmp, p });
  } finally {
    await rm(tmp, { recursive: true, force: true });
  }
}
for (const [name, mutate, reason] of [
  [
    "missing audit marker",
    () => document.querySelector("#headline").removeAttribute("data-text-box"),
    "missing-required-text-box",
  ],
  [
    "transparent ancestor",
    () => (document.querySelector("header").style.opacity = "0"),
    "invisible-text",
  ],
  [
    "transparent fill",
    () =>
      (document.querySelector(
        "#headline [data-text]",
      ).style.webkitTextFillColor = "transparent"),
    "invisible-text",
  ],
])
  test(`audit rejects ${name}`, async () => {
    const server = await serve(path.join(repo, "assets/starter"));
    let browser;
    try {
      browser = await chromium.launch({ channel: process.env.PLAYWRIGHT_CHANNEL || undefined });
      const page = await browser.newPage({
        viewport: { width: 1284, height: 2778 },
      });
      await page.goto(server.url + "/?export=1");
      await page.waitForFunction(() => window.coverReady);
      await page.evaluate(mutate);
      assert.ok(
        (await page.evaluate(auditCover, 0.8)).issues.some(
          (x) => x.reason === reason,
        ),
      );
    } finally {
      await browser?.close();
      await server.close();
    }
  });
for (const [name, url, reason] of [
  [
    "external font fallback",
    "https://fonts.example.invalid/font.woff2",
    "external-request",
  ],
  ["missing local font fallback", "media/missing.woff2", "http-error"],
])
  test(`export fails on ${name}`, () =>
    fixture(async ({ root, tmp }) => {
      const css = path.join(root, "style.css");
      await writeFile(
        css,
        (await readFile(css, "utf8")) +
          `\n@font-face { font-family: TestFont; src: url("${url}"); } #headline { font-family: TestFont, Arial; }`,
      );
      const out = path.join(tmp, "out");
      await assert.rejects(
        run(process.execPath, ["scripts/export.mjs", root, out], { cwd: repo }),
      );
      const m = JSON.parse(
        await readFile(path.join(out, "manifest.json"), "utf8"),
      );
      assert.ok(
        m.results.some((r) => r.issues.some((x) => x.reason === reason)),
      );
    }));
test("export detects source changed between cells", () =>
  fixture(async ({ root, tmp }) => {
    const css = path.join(root, "style.css");
    const initial = await readFile(css, "utf8");
    const out = path.join(tmp, "out");
    let changed = false;
    const child = spawn(process.execPath, ["scripts/export.mjs", root, out], {
      cwd: repo,
    });
    child.stdout.on("data", (data) => {
      if (!changed && data.toString().includes("01-capture.png:")) {
        changed = true;
        writeFileSync(css, initial + "\n#cover { background: #eee; }");
      }
    });
    const code = await new Promise((resolve, reject) => {
      child.on("error", reject);
      child.on("close", resolve);
    });
    assert.ok(changed);
    assert.notEqual(code, 0);
    const m = JSON.parse(
      await readFile(path.join(out, "manifest.json"), "utf8"),
    );
    assert.equal(m.status, "automated-fail");
    assert.ok(
      m.sourceIssues.some((x) => x.reason === "source-changed-during-export"),
    );
  }));
test("export refuses source-nested output reached through a directory symlink", () =>
  fixture(async ({ root, tmp }) => {
    await symlink(root, path.join(tmp, "alias"));
    const out = path.join(tmp, "alias/out");
    await assert.rejects(
      run(process.execPath, ["scripts/export.mjs", root, out], { cwd: repo }),
      /outside the source/,
    );
    await assert.rejects(access(out));
  }));

test("capture-based layouts can omit synthetic UI copy and repeated branding", () =>
  fixture(async ({ root, tmp, p }) => {
    p.textFields = ["headline", "support"];
    p.showBrand = false;
    for (const slide of p.slides)
      for (const copy of Object.values(slide.copy)) {
        delete copy.uiTitle;
        delete copy.uiBody;
      }
    await writeFile(path.join(root, "project.json"), JSON.stringify(p));
    const out = path.join(tmp, "out");
    await run(process.execPath, ["scripts/export.mjs", root, out], {
      cwd: repo,
    });
    const { verify } = await import("../scripts/verify.mjs");
    assert.equal((await verify(out)).status, "automated-pass");
    const m = JSON.parse(
      await readFile(path.join(out, "manifest.json"), "utf8"),
    );
    assert.deepEqual(
      m.results[0].texts.map((x) => x.id),
      ["headline", "support"],
    );
    const app = path.join(root, "app.js");
    await writeFile(
      app,
      (await readFile(app, "utf8")) +
        '\ndocument.querySelector("#headline").removeAttribute("data-text-box");',
    );
    await assert.rejects(
      run(
        process.execPath,
        ["scripts/export.mjs", root, path.join(tmp, "bad")],
        { cwd: repo },
      ),
    );
  }));
