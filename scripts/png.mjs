import { PNG } from "pngjs";
import { createHash } from "node:crypto";
export const sha256 = (data) => createHash("sha256").update(data).digest("hex");
export function inspectPNG(data, width, height) {
  const png = PNG.sync.read(data, { checkCRC: true });
  if (png.width !== width || png.height !== height)
    throw new Error("PNG dimensions differ from expected matrix");
  let nonuniform = false;
  const first = [...png.data.subarray(0, 3)];
  for (let i = 0; i < png.data.length; i += 4) {
    if (png.data[i + 3] !== 255)
      throw new Error("PNG contains transparent pixels");
    if (!nonuniform && first.some((v, c) => png.data[i + c] !== v))
      nonuniform = true;
  }
  if (!nonuniform) throw new Error("PNG is uniform/blank");
  return { width: png.width, height: png.height, sha256: sha256(data) };
}
