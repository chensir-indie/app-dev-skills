# Acceptance quick check

Use this checklist for reconstruction. Review-only or active refinement follows [design quality review](design-quality-review.md); do not fabricate pixel acceptance for pages without references.

- The intent, primary design standard and allowed changes are explicit; aesthetic suggestions have not silently redesigned a faithful reconstruction.
- Inspect the actual page's reading order, primary/secondary actions, layout rhythm, typography and icon consistency; issues have region/component references and review evidence.
- Exercise applicable keyboard, focus, long-copy, loading/empty/error, text-resizing and reduced-motion behavior. Record not applicable separately from untested.

- Full references are comparison-only; page text, controls and backplates remain independently editable.
- Every important element has a selector, measurements and actual DOM geometry. Hidden/occluded text does not masquerade as editable UI.
- Compare fonts, colors, spacing, individual corner radii, backplate contours, icons and navigation arrangement.
- Image semantics match plant names; inspect subject transparency against light and dark backgrounds.
- Subject/backplate occlusion is correct, and the UI remains complete when images are hidden.
- Browser captures come from current source after fonts/images load, with consistent dimensions and DPR mapping.
- Keep full-screen and important ROI diffs, including threshold-0 raw error.
- Both `one_to_one` fixed ceilings and frozen page limits pass. Matching-role ROIs cover each text/button/subject/important panel or icon; do not attach role names to unrelated areas.
- Compare at native size: background light/texture; leaf contours, holes and pot proportions; irregular backplate paths and occlusion; glyphs, weight and baselines; icon shape/stroke; bottom navigation and selection. Any obvious visible mismatch stays `pending`, even below average-error ceilings.
- Repair each worst ROI/local block from `diagnose_visual.py` and recapture. Listing failed regions as remaining issues does not complete a request to finish reconstruction.
- Interactions have visible outcomes and return paths; size/long-copy adaptation has actual evidence.
- Report file completeness, script results and visual acceptance separately. Critical failed differences prevent a completion claim.
