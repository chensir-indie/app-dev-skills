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
