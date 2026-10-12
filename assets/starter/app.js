import { localeInfo, fontStack } from "./locale.js";
import { textFields, defaultTextFields } from "./text.js";
const project = await (await fetch("project.json")).json();
const params = new URLSearchParams(location.search);
const isExport = params.has("export");
if (isExport) document.body.classList.add("export");
const selects = {};
for (const [key, list] of [
  ["locale", project.locales],
  ["device", project.devices],
  ["slide", project.slides],
]) {
  const select = document.getElementById(key);
  selects[key] = select;
  for (const item of list) {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = key === 'locale'
      ? `${new Intl.DisplayNames([item.id], {type:'language'}).of(item.id)} · ${item.id}`
      : item.id;
    select.append(option);
  }
  const requested = params.get(key);
  if (requested && !list.some((x) => x.id === requested))
    throw new Error(`Unknown ${key}: ${requested}`);
  select.value = requested || list[0].id;
  select.onchange = () => {
    const q = new URLSearchParams();
    for (const [k, v] of Object.entries(selects)) q.set(k, v.value);
    location.search = q;
  };
}
const locale = project.locales.find((x) => x.id === selects.locale.value);
const device = project.devices.find((x) => x.id === selects.device.value);
const slide = project.slides.find((x) => x.id === selects.slide.value);
const copy = slide.copy[locale.id];
if (!copy) throw new Error("Missing localized copy");
document.getElementById('project-status').textContent =
  `${project.locales.length} languages/regions` +
  (project.demo ? ' · Demo translations: draft' : '');
document.documentElement.lang = locale.id;
document.documentElement.dir = locale.direction;
const cover = document.getElementById("cover");
cover.className = device.kind;
const typography = localeInfo(locale.id);
cover.style.fontFamily = fontStack(
  locale.fontFamilies ?? typography.fontFamilies,
);
cover.style.setProperty("--headline-tracking", typography.tracking);
cover.style.setProperty("--headline-leading", typography.leading);
cover.style.setProperty(
  "--ui-title-leading",
  typography.leading === "1.2" ? "1.15" : typography.leading,
);
cover.style.setProperty(
  "--support-leading",
  String(Math.max(1.4, Number(typography.leading))),
);
cover.style.setProperty(
  "--body-leading",
  String(Math.max(1.55, Number(typography.leading))),
);
cover.style.setProperty(
  "--w",
  `${isExport ? device.width : Math.min(420, innerWidth - 48)}px`,
);
cover.style.setProperty(
  "--h",
  `${isExport ? device.height : (Math.min(420, innerWidth - 48) * device.height) / device.width}px`,
);
cover.dataset.locale = locale.id;
cover.dataset.device = device.id;
cover.dataset.slide = slide.id;
const fields = textFields(project);
for (const field of defaultTextFields) {
  if (fields.includes(field))
    document.querySelector(`#${field} [data-text]`).textContent = copy[field];
  else document.getElementById(field)?.remove();
}
if (slide.showBrand ?? project.showBrand ?? true)
  document.querySelector("#brand [data-text]").textContent = project.app;
else document.getElementById("brand")?.remove();
document.getElementById("art").src = slide.art[locale.id] ?? slide.art.shared;
if (slide.phases) {
  const strip = document.createElement("div");
  strip.className = "phases";
  strip.setAttribute("aria-label", "Illustrated motion phases");
  for (const [i, src] of slide.phases.entries()) {
    const img = document.createElement("img");
    img.src = src;
    img.alt = `Motion phase ${i + 1}`;
    strip.append(img);
  }
  cover.append(strip);
}
await document.fonts.ready;
await Promise.all([...document.images].map((img) => img.decode()));
for (const box of document.querySelectorAll("[data-text-box]")) {
  const text = box.querySelector("[data-text]");
  const base = parseFloat(getComputedStyle(text).fontSize);
  let scale = 1;
  const fits = () =>
    text.scrollWidth <= box.clientWidth + 1 &&
    text.scrollHeight <= box.clientHeight + 1;
  while (!fits() && scale > project.minTextScale) {
    scale = Math.max(
      project.minTextScale,
      Math.round((scale - 0.01) * 100) / 100,
    );
    text.style.fontSize = `${base * scale}px`;
  }
  box.dataset.textScale = String(scale);
  box.dataset.overflow = String(!fits());
}
window.coverReady = true;
