import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { validateProject, cells } from "../scripts/contract.mjs";
import { inspectPNG } from "../scripts/png.mjs";
import { PNG } from "pngjs";
const fixture = JSON.parse(
  await readFile(
    new URL("../assets/starter/project.json", import.meta.url),
    "utf8",
  ),
);
test("matrix preserves locale/device/semantic story identity", () => {
  const p = validateProject(structuredClone(fixture));
  assert.equal(cells(p).length, 12);
  assert.equal(cells(p)[0].file, "en-US/iphone/01-capture.png");
  assert.equal(cells(p).at(-1).file, "ar-SA/ipad/02-motion.png");
});
for (const [name, mutate, pattern] of [
  [
    "missing locale",
    (p) => delete p.slides[0].copy["ar-SA"],
    /missing headline/,
  ],
  [
    "blank copy",
    (p) => (p.slides[0].copy["ar-SA"].headline = " "),
    /missing headline/,
  ],
  ["duplicate slide", (p) => (p.slides[1].id = "capture"), /duplicate ids/],
  ["path traversal", (p) => (p.locales[0].id = "../escape"), /invalid id/],
  [
    "remote art",
    (p) => (p.slides[0].art.shared = "https://example.com/a.png"),
    /local media path/,
  ],
  [
    "asset traversal",
    (p) => (p.slides[0].art.shared = "media/../secrets.png"),
    /local media path/,
  ],
  [
    "fractional dimensions",
    (p) => (p.devices[0].width = 1284.5),
    /invalid dimensions/,
  ],
  ["missing direction", (p) => delete p.locales[0].direction, /direction/],
  ["tiny type", (p) => (p.minTextScale = 0.4), /minTextScale/],
])
  test(`rejects ${name}`, () => {
    const p = structuredClone(fixture);
    mutate(p);
    assert.throws(() => validateProject(p), pattern);
  });
test("PNG checks dimensions, uniform content, alpha and corrupted bytes", () => {
  const p = new PNG({ width: 2, height: 2 });
  p.data.fill(255);
  assert.throws(() => inspectPNG(PNG.sync.write(p), 2, 2), /uniform/);
  p.data[0] = 0;
  const valid = PNG.sync.write(p);
  assert.equal(inspectPNG(valid, 2, 2).sha256.length, 64);
  assert.throws(() => inspectPNG(valid, 3, 2), /dimensions/);
  p.data[3] = 0;
  assert.throws(() => inspectPNG(PNG.sync.write(p), 2, 2), /transparent/);
  assert.throws(() => inspectPNG(Buffer.from("not a png"), 2, 2));
});

test("rejects case-colliding IDs and ambiguous contact-sheet names", () => {
  let p = structuredClone(fixture);
  p.devices.push({ ...p.devices[0], id: "IPHONE" });
  assert.throws(() => validateProject(p), /case-insensitive/);
  p = structuredClone(fixture);
  p.locales = [
    { id: "en", direction: "ltr" },
    { id: "en-US", direction: "ltr" },
  ];
  p.devices = [
    { ...p.devices[0], id: "US-phone" },
    { ...p.devices[0], id: "phone" },
  ];
  for (const slide of p.slides) slide.copy.en = slide.copy["en-US"];
  assert.throws(() => validateProject(p), /filename collision/);
});
test("motion phases require different paths and different file contents", async () => {
  const { checkAssets } = await import("../scripts/files.mjs");
  const p = structuredClone(fixture);
  p.slides[1].phases[1] = p.slides[1].phases[0];
  assert.throws(() => validateProject(p), /phases/);
  const sources = [
    "media/waves.svg",
    "media/waves-rise.svg",
    "media/waves-flow.svg",
  ].map((file) => ({ file, sha256: "same" }));
  assert.throws(() => checkAssets(fixture, sources), /identical/);
  assert.throws(() => checkAssets(fixture, []), /missing art/);
});

test("declared text fields control translation requirements without disabling headline checks", () => {
  const p = structuredClone(fixture);
  p.textFields = ["headline", "support"];
  p.showBrand = false;
  for (const slide of p.slides)
    for (const copy of Object.values(slide.copy)) {
      delete copy.uiTitle;
      delete copy.uiBody;
    }
  assert.equal(validateProject(p), p);
  p.textFields = [];
  assert.throws(() => validateProject(p), /textFields/);
  p.textFields = ["headline"];
  p.showBrand = "false";
  assert.throws(() => validateProject(p), /showBrand/);
});
