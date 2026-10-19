// Browser-side geometry checks. These are conservative heuristics, not OCR or pixel fidelity.
export function auditCover(config) {
  const minScale = typeof config === "number" ? config : config.minScale;
  const fields =
    typeof config === "number"
      ? ["headline", "support", "uiTitle", "uiBody"]
      : config.fields;
  const issues = [];
  const cover = document.querySelector("#cover");
  if (!cover) return { issues: [{ reason: "missing-cover" }], texts: [] };
  for (const id of fields) {
    const boxes = cover.querySelectorAll(`#${id}[data-text-box]`);
    if (
      boxes.length !== 1 ||
      boxes[0].querySelectorAll("[data-text]").length !== 1
    )
      issues.push({ id, reason: "missing-required-text-box" });
  }
  const invisible = (el) => {
    const css = getComputedStyle(el);
    // Chromium returns computed rgb/rgba for ordinary text fill. Complex paints still need visual review.
    const fill = css.webkitTextFillColor || css.color;
    if (fill === "transparent" || /^rgba\(.*,[\s]*0(?:\.0+)?\)$/.test(fill))
      return true;
    for (let node = el; node; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (
        Number(style.opacity) === 0 ||
        style.visibility === "hidden" ||
        style.display === "none"
      )
        return true;
    }
    return false;
  };
  const rect = (r) => ({
    left: r.left,
    top: r.top,
    right: r.right,
    bottom: r.bottom,
  });
  const outside = (a, b) =>
    a.left < b.left - 2 ||
    a.top < b.top - 2 ||
    a.right > b.right + 2 ||
    a.bottom > b.bottom + 2;
  const texts = [];
  for (const box of cover.querySelectorAll("[data-text-box]")) {
    const el = box.querySelector("[data-text]");
    const id = box.id;
    const scale = Number(box.dataset.textScale);
    const add = (reason) => issues.push({ id, reason });
    if (!el || !el.textContent.trim()) {
      add("missing-text");
      continue;
    }
    if (!Number.isFinite(scale) || scale < minScale) add("scale-floor");
    if (
      box.dataset.overflow === "true" ||
      el.scrollWidth > box.clientWidth + 2 ||
      el.scrollHeight > box.clientHeight + 2
    )
      add("overflow");
    const range = document.createRange();
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()].filter(
      (r) => r.width > 0 && r.height > 0,
    );
    if (!rects.length || invisible(el)) add("invisible-text");
    for (const r of rects) {
      if (outside(r, cover.getBoundingClientRect())) add("outside-canvas");
      for (
        let ancestor = el.parentElement;
        ancestor && ancestor !== document.body;
        ancestor = ancestor.parentElement
      ) {
        const css = getComputedStyle(ancestor);
        const a = ancestor.getBoundingClientRect();
        const clipsX = ["hidden", "clip", "scroll", "auto"].includes(
            css.overflowX,
          ),
          clipsY = ["hidden", "clip", "scroll", "auto"].includes(css.overflowY);
        if (
          (clipsX && (r.left < a.left - 2 || r.right > a.right + 2)) ||
          (clipsY && (r.top < a.top - 2 || r.bottom > a.bottom + 2))
        )
          add("clipped-by-ancestor");
      }
      // Sample inline rectangle centers; complex masks, transforms and pointer-events:none need visual review.
      const hit = document.elementFromPoint(
        (r.left + r.right) / 2,
        (r.top + r.bottom) / 2,
      );
      if (hit && !el.contains(hit) && !hit.contains(el))
        add("possible-occlusion");
    }
    texts.push({
      id,
      scale,
      font: getComputedStyle(el).fontFamily,
      fontSize: getComputedStyle(el).fontSize,
      rects: rects.map(rect),
    });
  }
  for (let i = 0; i < texts.length; i++)
    for (let j = i + 1; j < texts.length; j++) {
      if (
        texts[i].rects.some((a) =>
          texts[j].rects.some(
            (b) =>
              Math.min(a.right, b.right) - Math.max(a.left, b.left) > 2 &&
              Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 2,
          ),
        )
      )
        issues.push({
          id: texts[i].id,
          other: texts[j].id,
          reason: "possible-text-collision",
        });
    }
  for (const img of cover.querySelectorAll("img"))
    if (!img.complete || !img.naturalWidth)
      issues.push({ id: img.id, reason: "missing-image" });
  if ([...document.fonts].some((font) => font.status === "error"))
    issues.push({ reason: "font-load-error" });
  if (document.fonts.status !== "loaded")
    issues.push({ reason: "fonts-not-ready" });
  if (!texts.length) issues.push({ reason: "no-audited-text" });
  return {
    issues: [...new Map(issues.map((x) => [JSON.stringify(x), x])).values()],
    texts,
  };
}
