import test from "node:test";
import assert from "node:assert/strict";
import {
  mkdtemp,
  cp,
  readFile,
  writeFile,
  symlink,
  rm,
} from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import { serve } from "../scripts/server.mjs";
import { auditCover } from "../scripts/audit.mjs";
import { verify } from "../scripts/verify.mjs";
const run = promisify(execFile),
  repo = fileURLToPath(new URL("../", import.meta.url));
test("browser detects clipping, occlusion, collision and missing images", async () => {
  const server = await serve(path.join(repo, "assets/starter"));
  let browser;
  try {
    browser = await chromium.launch({ channel: process.env.PLAYWRIGHT_CHANNEL || undefined });
    const page = await browser.newPage({
      viewport: { width: 1284, height: 2778 },
    });
    await page.goto(server.url + "/?export=1");
    await page.waitForFunction(() => window.coverReady);
    assert.deepEqual((await page.evaluate(auditCover, 0.8)).issues, []);
    await page.evaluate(
      () => (document.querySelector("#headline").style.height = "1px"),
    );
    assert.ok(
      (await page.evaluate(auditCover, 0.8)).issues.some(
        (x) => x.reason === "clipped-by-ancestor" || x.reason === "overflow",
      ),
    );
    await page.reload();
    await page.waitForFunction(() => window.coverReady);
    await page.evaluate(() => {
      const box = document.createElement("div");
      Object.assign(box.style, {
        position: "absolute",
        inset: "0",
        background: "white",
        zIndex: "999",
      });
      document.querySelector("#cover").append(box);
    });
    assert.ok(
      (await page.evaluate(auditCover, 0.8)).issues.some(
        (x) => x.reason === "possible-occlusion",
      ),
    );
    await page.reload();
    await page.waitForFunction(() => window.coverReady);
    await page.evaluate(() => {
      const a = document.querySelector("#headline");
      const b = a.cloneNode(true);
      b.id = "duplicate";
      Object.assign(b.style, { position: "absolute", inset: "0" });
      a.parentElement.append(b);
    });
    assert.ok(
      (await page.evaluate(auditCover, 0.8)).issues.some(
        (x) => x.reason === "possible-text-collision",
      ),
    );
    await page.evaluate(() => {
      const img = document.createElement("img");
      img.src = "missing.png";
      document.querySelector("#cover").append(img);
    });
    assert.ok(
      (await page.evaluate(auditCover, 0.8)).issues.some(
        (x) => x.reason === "missing-image",
      ),
    );
  } finally {
    await browser?.close();
    await server.close();
  }
});
test("local server denies traversal and external symlinks", async () => {
  const tmp = await mkdtemp(path.join(os.tmpdir(), "cover-server-"));
  const root = path.join(tmp, "project");
  await cp(path.join(repo, "assets/starter"), root, { recursive: true });
  await writeFile(path.join(tmp, "private.txt"), "should-not-be-served");
  await symlink(path.join(tmp, "private.txt"), path.join(root, "escape.txt"));
  const server = await serve(root);
  try {
    assert.equal((await fetch(server.url + "/escape.txt")).status, 404);
    assert.equal(
      (await fetch(server.url + "/%2e%2e%2fprivate.txt")).status,
      404,
    );
    assert.equal((await fetch(server.url + "/project.json")).status, 200);
  } finally {
    await server.close();
    await rm(tmp, { recursive: true, force: true });
  }
});
test("full multilingual matrix exports, refuses overwrite, detects tampering and stale cells", async () => {
  const tmp = await mkdtemp(path.join(os.tmpdir(), "cover-export-"));
  const root = path.join(tmp, "project"),
    out = path.join(tmp, "output");
  try {
    await run(process.execPath, ["scripts/init.mjs", root], { cwd: repo });
    await assert.rejects(
      run(process.execPath, ["scripts/init.mjs", root], { cwd: repo }),
    );
    const p = JSON.parse(
      await readFile(path.join(root, "project.json"), "utf8"),
    );
    p.devices = [
      { id: "phone", kind: "phone", width: 360, height: 780 },
      { id: "tablet", kind: "tablet", width: 600, height: 800 },
    ];
    await writeFile(path.join(root, "project.json"), JSON.stringify(p));
    await run(process.execPath, ["scripts/export.mjs", root, out], {
      cwd: repo,
    });
    assert.equal((await verify(out)).cells, 12);
    await assert.rejects(
      run(process.execPath, ["scripts/export.mjs", root, out], { cwd: repo }),
    );
    const manifestPath = path.join(out, "manifest.json"),
      original = await readFile(manifestPath, "utf8"),
      m = JSON.parse(original);
    m.results.pop();
    await writeFile(manifestPath, JSON.stringify(m));
    await assert.rejects(verify(out), /matrix count mismatch/);
    await writeFile(manifestPath, original);
    const image = path.join(out, "en-US/phone/01-capture.png");
    const bytes = await readFile(image);
    await writeFile(path.join(out, "extra.png"), bytes);
    await assert.rejects(verify(out), /unexpected PNG/);
    await rm(path.join(out, "extra.png"));
    await writeFile(image, Buffer.from("broken"));
    await assert.rejects(verify(out));
    await writeFile(image, bytes);
    m.results = JSON.parse(original).results;
    m.results[0].sha256 = "wrong";
    await writeFile(manifestPath, JSON.stringify(m));
    await assert.rejects(verify(out), /hash mismatch/);
    await writeFile(manifestPath, original);
    for (const [mutate, message] of [
      [(m) => (m.schemaVersion = 99), /manifest structure/],
      [(m) => (m.sources = []), /source hash/],
      [(m) => (m.visualReview = "approved"), /separate bound review/],
      [(m) => (m.results[0].texts = []), /text audit/],
      [
        (m) => (m.sourceIssues = [{ reason: "source-changed-during-export" }]),
        /source audit/,
      ],
    ]) {
      const malformed = JSON.parse(original);
      mutate(malformed);
      await writeFile(manifestPath, JSON.stringify(malformed));
      await assert.rejects(verify(out), message);
    }
    await writeFile(manifestPath, original);
    const reviewPath = path.join(tmp, "review.json");
    await run(
      process.execPath,
      ["scripts/review.mjs", "init", out, reviewPath],
      { cwd: repo },
    );
    await assert.rejects(
      run(process.execPath, ["scripts/review.mjs", "init", out, reviewPath], {
        cwd: repo,
      }),
      /EEXIST/,
    );
    await assert.rejects(
      run(process.execPath, ["scripts/review.mjs", "check", out, reviewPath], {
        cwd: repo,
      }),
      /unresolved review/,
    );
    const review = JSON.parse(await readFile(reviewPath, "utf8"));
    review.reviewer = "Test fixture";
    review.reviewedAt = new Date().toISOString();
    for (const cell of [review.referenceComparison, ...review.cells]) {
      cell.status = "pass";
      cell.notes = "Synthetic test record, not a real visual review";
    }
    await writeFile(reviewPath, JSON.stringify(review));
    await run(
      process.execPath,
      ["scripts/review.mjs", "check", out, reviewPath],
      { cwd: repo },
    );
    await writeFile(manifestPath, original + "\n");
    await assert.rejects(
      run(process.execPath, ["scripts/review.mjs", "check", out, reviewPath], {
        cwd: repo,
      }),
      /stale/,
    );
    // A route that silently renders English for Chinese must not pass a file-count audit.
    p.locales = p.locales.filter((x) => x.id === "zh-Hans");
    p.devices = p.devices.slice(0, 1);
    p.slides = p.slides.slice(0, 1);
    await writeFile(path.join(root, "project.json"), JSON.stringify(p));
    const appPath = path.join(root, "app.js");
    let app = await readFile(appPath, "utf8");
    app = app.replace(
      "const copy = slide.copy[locale.id]",
      'const copy = slide.copy["en-US"]',
    );
    app += '\ndocument.documentElement.dir = "rtl";\n';
    await writeFile(appPath, app);
    const badOut = path.join(tmp, "wrong-language");
    await assert.rejects(
      run(process.execPath, ["scripts/export.mjs", root, badOut], {
        cwd: repo,
      }),
    );
    const failed = JSON.parse(
      await readFile(path.join(badOut, "manifest.json"), "utf8"),
    );
    assert.ok(
      failed.results[0].issues.some((x) => x.reason === "wrong-rendered-copy"),
    );
    assert.ok(
      failed.results[0].issues.some(
        (x) => x.reason === "wrong-rendered-language-direction",
      ),
    );
  } finally {
    await rm(tmp, { recursive: true, force: true });
  }
});

test("every store locale renders both device layouts with its own lang, direction and script sample", async () => {
  const { selectLocales } = await import("../scripts/localization.mjs");
  const { localeInfo } = await import("../assets/starter/locale.js");
  const tmp = await mkdtemp(path.join(os.tmpdir(), "cover-world-"));
  const root = path.join(tmp, "project");
  await cp(path.join(repo, "assets/starter"), root, { recursive: true });
  const p = JSON.parse(await readFile(path.join(root, "project.json"), "utf8"));
  p.locales = selectLocales("app-store");
  p.slides = p.slides.slice(0, 1);
  p.devices = [
    { id: "phone", kind: "phone", width: 1284, height: 2778 },
    { id: "tablet", kind: "tablet", width: 2048, height: 2732 },
  ];
  const samples = {
    Arab: "فكرة جديدة",
    Hebr: "רעיון חדש",
    Hans: "记录灵感",
    Hant: "記錄靈感",
    Jpan: "新しいアイデア",
    Kore: "새로운 생각",
    Deva: "नया विचार",
    Beng: "নতুন ভাবনা",
    Gujr: "નવો વિચાર",
    Guru: "ਨਵਾਂ ਵਿਚਾਰ",
    Knda: "ಹೊಸ ಆಲೋಚನೆ",
    Mlym: "പുതിയ ആശയം",
    Orya: "ନୂଆ ଚିନ୍ତା",
    Taml: "புதிய சிந்தனை",
    Telu: "కొత్త ఆలోచన",
    Thai: "ความคิดใหม่",
    Cyrl: "Новая идея",
    Grek: "Νέα ιδέα",
    Latn: "Une idée nouvelle",
  };
  for (const locale of p.locales) {
    const sample = samples[localeInfo(locale.id).script];
    assert.ok(sample, locale.id);
    p.slides[0].copy[locale.id] = {
      headline: sample,
      support: sample,
      uiTitle: sample,
      uiBody: sample,
    };
  }
  await writeFile(path.join(root, "project.json"), JSON.stringify(p));
  const server = await serve(root);
  let browser;
  try {
    browser = await chromium.launch({ channel: process.env.PLAYWRIGHT_CHANNEL || undefined });
    const page = await browser.newPage();
    for (const locale of p.locales)
      for (const device of p.devices) {
        await page.setViewportSize({
          width: device.width,
          height: device.height,
        });
        await page.goto(
          `${server.url}/?locale=${locale.id}&device=${device.id}&export=1`,
        );
        await page.waitForFunction(() => window.coverReady);
        const rendered = await page.evaluate(() => ({
          lang: document.documentElement.lang,
          dir: document.documentElement.dir,
          font: getComputedStyle(document.querySelector("#cover")).fontFamily,
          copy: document.querySelector("#headline [data-text]").textContent,
        }));
        assert.equal(rendered.lang, locale.id);
        assert.equal(rendered.dir, locale.direction);
        assert.equal(rendered.copy, p.slides[0].copy[locale.id].headline);
        assert.ok(
          rendered.font.includes(localeInfo(locale.id).fontFamilies[0]),
        );
        assert.deepEqual(
          (await page.evaluate(auditCover, p.minTextScale)).issues,
          [],
          `${locale.id}/${device.id}`,
        );
      }
  } finally {
    await browser?.close();
    await server.close();
    await rm(tmp, { recursive: true, force: true });
  }
});
