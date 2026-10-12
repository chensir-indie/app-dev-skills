import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { localeInfo } from "../assets/starter/locale.js";
import {
  catalog,
  selectLocales,
  addLocales,
  coverage,
} from "../scripts/localization.mjs";
import { cells, validateProject } from "../scripts/contract.mjs";
const fixture = JSON.parse(
  await readFile(
    new URL("../assets/starter/project.json", import.meta.url),
    "utf8",
  ),
);
test("all 50 store locales have canonical IDs and script-aware direction", () => {
  const list = selectLocales("app-store");
  assert.equal(list.length, 50);
  assert.equal(new Set(list.map((x) => x.id)).size, 50);
  assert.deepEqual(
    list.filter((x) => x.direction === "rtl").map((x) => x.id),
    ["ar-SA", "he", "ur-PK"],
  );
  for (const id of [
    "bn-BD",
    "ta-IN",
    "zh-Hant",
    "en-AU",
    "fr-CA",
    "es-MX",
    "pt-BR",
  ])
    assert.ok(catalog.locales.includes(id));
});
test("custom locales respect explicit scripts and reject malformed or ambiguous keys", () => {
  assert.equal(localeInfo("fa-IR").direction, "rtl");
  assert.equal(localeInfo("ar-Latn").direction, "ltr");
  assert.equal(localeInfo("pa-Arab").direction, "rtl");
  assert.equal(localeInfo("pa-IN").script, "Guru");
  assert.notDeepEqual(
    localeInfo("zh-Hans").fontFamilies,
    localeInfo("zh-Hant").fontFamilies,
  );
  for (const id of ["en_US", "en-us", "iw", "en-US-u-ca-gregory", "../en"])
    assert.throws(() => localeInfo(id));
  assert.throws(() => selectLocales("ja,ja"), /unique/);
});
test("expansion preserves copy and regional variants, leaves new translations empty", () => {
  const original = structuredClone(fixture);
  const p = addLocales(fixture, "app-store");
  assert.deepEqual(fixture, original);
  assert.equal(p.locales.length, 50);
  assert.equal(cells(p).length, 200);
  assert.deepEqual(p.slides[0].copy["en-US"], fixture.slides[0].copy["en-US"]);
  assert.equal(p.slides[0].copy["en-GB"].headline, "");
  assert.equal(coverage(p).missing.length, 47 * 2 * 4);
  assert.throws(() => validateProject(p), /missing headline/);
  p.slides[0].copy["en-GB"].headline = "Your regional wording";
  assert.equal(
    addLocales(p, "en-GB").slides[0].copy["en-GB"].headline,
    "Your regional wording",
  );
});
test("complete translations cannot conceal wrong direction or invalid font config", () => {
  const p = structuredClone(fixture);
  assert.equal(coverage(p).status, "complete");
  p.locales[2].direction = "ltr";
  assert.throws(() => validateProject(p), /direction must be rtl/);
  p.locales[2].direction = "rtl";
  p.locales[2].fontFamilies = [""];
  assert.throws(() => validateProject(p), /fontFamilies/);
});

test("locale CLI copies safely, reports missing fields, and rejects overwrite and symlinks", async () => {
  const { mkdtemp, cp, rm, symlink, writeFile } = await import(
    "node:fs/promises"
  );
  const { tmpdir } = await import("node:os");
  const { join } = await import("node:path");
  const { fileURLToPath } = await import("node:url");
  const { execFile } = await import("node:child_process");
  const { promisify } = await import("node:util");
  const run = promisify(execFile);
  const repo = fileURLToPath(new URL("../", import.meta.url));
  const tmp = await mkdtemp(join(tmpdir(), "cover-locales-"));
  const source = join(tmp, "source"),
    output = join(tmp, "expanded");
  try {
    await cp(join(repo, "assets/starter"), source, { recursive: true });
    const original = await readFile(join(source, "project.json"), "utf8");
    const args = ["scripts/locales.mjs", "add", source, output, "app-store"];
    await run(process.execPath, args, { cwd: repo });
    const p = JSON.parse(await readFile(join(output, "project.json"), "utf8"));
    assert.equal(p.locales.length, 50);
    assert.equal(
      await readFile(join(source, "project.json"), "utf8"),
      original,
    );
    assert.ok(await readFile(join(output, "locale.js"), "utf8"));
    await assert.rejects(
      run(process.execPath, ["scripts/locales.mjs", "check", output], {
        cwd: repo,
      }),
      (e) => e.stdout.includes("ja/capture/headline"),
    );
    await assert.rejects(run(process.execPath, args, { cwd: repo }), /EEXIST/);
    await symlink(source, join(tmp, "alias"));
    await assert.rejects(
      run(
        process.execPath,
        ["scripts/locales.mjs", "add", source, join(tmp, "alias/nested"), "ja"],
        { cwd: repo },
      ),
      /outside source/,
    );
    await writeFile(join(tmp, "private.txt"), "untouched");
    await symlink(join(tmp, "private.txt"), join(source, "unsafe.txt"));
    await assert.rejects(
      run(
        process.execPath,
        [
          "scripts/locales.mjs",
          "add",
          source,
          join(tmp, "unsafe-output"),
          "ja",
        ],
        { cwd: repo },
      ),
      /symlinks/,
    );
    assert.equal(await readFile(join(tmp, "private.txt"), "utf8"), "untouched");
  } finally {
    await rm(tmp, { recursive: true, force: true });
  }
});
