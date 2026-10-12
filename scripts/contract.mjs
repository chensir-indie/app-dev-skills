import { localeInfo } from "../assets/starter/locale.js";
const slug = /^[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*$/;
export function cells(project) {
  return project.locales.flatMap((locale) =>
    project.devices.flatMap((device) =>
      project.slides.map((slide, index) => ({
        locale: locale.id,
        device: device.id,
        slide: slide.id,
        width: device.width,
        height: device.height,
        file: `${locale.id}/${device.id}/${String(index + 1).padStart(2, "0")}-${slide.id}.png`,
      })),
    ),
  );
}
export function validateProject(p) {
  const errors = [];
  const assert = (ok, msg) => {
    if (!ok) errors.push(msg);
  };
  assert(p.schemaVersion === 1, "schemaVersion must equal 1");
  assert(typeof p.app === "string" && p.app.trim(), "app is required");
  for (const key of ["locales", "devices", "slides"]) {
    assert(
      Array.isArray(p[key]) && p[key].length > 0,
      `${key} must be nonempty`,
    );
    if (!Array.isArray(p[key])) continue;
    const ids = p[key].map((x) => x?.id);
    assert(
      ids.every((id) => typeof id === "string" && slug.test(id)),
      `${key}: invalid id`,
    );
    assert(new Set(ids).size === ids.length, `${key}: duplicate ids`);
  }
  if (errors.length) throw new Error(errors.join("\n"));
  assert(
    Number.isFinite(p.minTextScale) &&
      p.minTextScale >= 0.6 &&
      p.minTextScale <= 1,
    "minTextScale must be within 0.60..1",
  );
  for (const l of p.locales) {
    try {
      const info = localeInfo(l.id);
      assert(
        l.direction === info.direction,
        `${l.id}: direction must be ${info.direction}`,
      );
    } catch (error) {
      errors.push(error.message);
    }
    if (l.fontFamilies !== undefined)
      assert(
        Array.isArray(l.fontFamilies) &&
          l.fontFamilies.length > 0 &&
          l.fontFamilies.every(
            (x) => typeof x === "string" && x.trim() && !/[;{}\\\n\r]/.test(x),
          ),
        `${l.id}: invalid fontFamilies`,
      );
  }
  for (const d of p.devices) {
    assert(
      ["phone", "tablet"].includes(d.kind),
      `${d.id}: kind must be phone or tablet`,
    );
    assert(
      [d.width, d.height].every(
        (n) => Number.isInteger(n) && n >= 320 && n <= 5000,
      ),
      `${d.id}: invalid dimensions`,
    );
  }
  for (const s of p.slides)
    if (s.phases !== undefined)
      assert(
        Array.isArray(s.phases) &&
          s.phases.length >= 2 &&
          s.phases.length <= 4 &&
          s.phases.every(
            (x) =>
              typeof x === "string" &&
              /^media\/[a-zA-Z0-9_./-]+$/.test(x) &&
              !x.split("/").includes(".."),
          ),
        `${s.id}: phases must contain 2-4 local media paths`,
      );
  for (const s of p.slides)
    for (const l of p.locales) {
      const c = s.copy?.[l.id];
      for (const field of ["headline", "support", "uiTitle", "uiBody"])
        assert(
          typeof c?.[field] === "string" && c[field].trim(),
          `${s.id}/${l.id}: missing ${field}`,
        );
      const art = s.art?.[l.id] ?? s.art?.shared;
      assert(
        typeof art === "string" &&
          /^media\/[a-zA-Z0-9_./-]+$/.test(art) &&
          !art.split("/").includes(".."),
        `${s.id}/${l.id}: art must be a local media path`,
      );
      assert(
        typeof s.provenance === "string" && s.provenance.trim(),
        `${s.id}: provenance required`,
      );
    }
  if (errors.length) throw new Error(errors.join("\n"));
  return p;
}
