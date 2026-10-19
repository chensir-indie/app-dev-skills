// Shared by the browser and Node validator; no network fonts or locale fallbacks.
const fonts = {
  Hans: ["Noto Sans SC", "PingFang SC", "Microsoft YaHei"],
  Hant: ["Noto Sans TC", "PingFang TC", "Microsoft JhengHei"],
  Jpan: ["Noto Sans JP", "Hiragino Sans", "Yu Gothic"],
  Kore: ["Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic"],
  Arab: ["Noto Sans Arabic", "Geeza Pro"],
  Hebr: ["Noto Sans Hebrew", "Arial Hebrew"],
  Deva: ["Noto Sans Devanagari", "Kohinoor Devanagari"],
  Beng: ["Noto Sans Bengali", "Kohinoor Bangla"],
  Gujr: ["Noto Sans Gujarati", "Gujarati Sangam MN"],
  Guru: ["Noto Sans Gurmukhi", "Gurmukhi MN"],
  Knda: ["Noto Sans Kannada", "Kannada Sangam MN"],
  Mlym: ["Noto Sans Malayalam", "Malayalam Sangam MN"],
  Orya: ["Noto Sans Oriya", "Oriya Sangam MN"],
  Taml: ["Noto Sans Tamil", "Tamil Sangam MN"],
  Telu: ["Noto Sans Telugu", "Telugu Sangam MN"],
  Thai: ["Noto Sans Thai", "Thonburi"],
  Khmr: ["Noto Sans Khmer", "Khmer Sangam MN"],
  Mymr: ["Noto Sans Myanmar", "Myanmar Sangam MN"],
};
export function localeInfo(id) {
  let locale;
  try {
    locale = new Intl.Locale(id);
  } catch {
    throw new Error(`${id}: invalid BCP 47 locale`);
  }
  if (locale.toString() !== id || locale.baseName !== id)
    throw new Error(
      `${id}: use a canonical BCP 47 base tag (${locale.baseName}); no extensions`,
    );
  const script = locale.maximize().script;
  const direction = (locale.getTextInfo?.() ?? locale.textInfo)?.direction;
  if (!direction)
    throw new Error(`${id}: runtime lacks Intl locale direction data`);
  return {
    id,
    direction,
    script,
    fontFamilies: [
      ...(fonts[script] ?? []),
      "Arial",
      "Noto Sans",
      "sans-serif",
    ],
    // Joining scripts and CJK should not inherit Latin negative tracking.
    tracking: ["Latn", "Cyrl", "Grek"].includes(script) ? "-0.045em" : "0em",
    leading: ["Latn", "Cyrl", "Grek"].includes(script)
      ? "1.2"
      : script === "Telu"
        ? "1.8"
        : "1.5",
  };
}
export function fontStack(families) {
  return families
    .map((name) => (name === "sans-serif" ? name : JSON.stringify(name)))
    .join(", ");
}
