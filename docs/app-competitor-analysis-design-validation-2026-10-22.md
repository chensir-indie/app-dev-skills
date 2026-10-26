# Report reader design validation · 2026-10-22

The report renderer now implements the Fieldnotes composition described in the skill's [report-design.md](../skills/app-competitor-analysis/references/report-design.md). Community Mintlify/Oura analyses inform document navigation and editorial hierarchy; Apple-guided rules remain the usability baseline. This is an authored adaptation, not an official brand implementation or certification.

Changes: shared reader tokens and type roles; desktop library/document/contents composition; responsive native menus; capability tiers with wide typographic grids; numbered journey spine; prominent technical responsibility boundary and data path. Consolidated the editorial stylesheet. Reports continue as independent offline files with shared hashed assets.

Actual generated collection verification used 44 existing products and all 176 maps. All desktop and phone product links were clicked, and all four map links in every product at both widths were checked (88 product switches, 352 map jumps). Sparse, image-based and dense reports and the index were visually reviewed. Medium width, enlarged text, source return, search/empty/clear, Escape, print CSS and reduced motion were exercised. Exact local artifact hashes and screenshots are saved with the report project; source truth and competitor runtime behavior were not revalidated by this visual pass.

A visual review found stale display derivatives for two crops of the same original. The crop-aware derivative generator already used a viewport-specific key, but the prior delivery referenced old derivatives. Regenerated reading images preserve exact originals. A new failing regression preceded the renderer's aspect-ratio rejection for a mismatched framed preview. This check catches the demonstrated geometry mismatch; it cannot prove pixel/content identity when two crops share an aspect ratio.

Manual instruction scenario review (not blind model evaluation):

| Scenario | Expected behavior | Governing instruction |
| --- | --- | --- |
| Existing collection rejected as ugly | Inspect current pixels, select concrete references, repair shared composition and re-render full requested set | report-design.md reference selection and review loop |
| Explicitly different user direction | Use that direction; retain evidence and native reader behavior | SKILL.md deliver and verify; report-design.md |
| Narrow technical-only research | Keep the requested scope and original technical evidence; do not add an unrelated visual rebuild | SKILL.md choose scope |
| No screenshots | Label capability extracts; acquire evidence where possible; preserve the specific gap | report-design.md opening; evidence-acquisition.md |
| Browser unavailable | Render and run available structural checks; leave visual/interaction checks pending | SKILL.md browser boundary |
| Python/Pillow unavailable | Run the read-only doctor; use existing images/manual paths; do not install or fabricate proof | SKILL.md preflight; prepare_previews.py error |

No change to research or external-publication authorization. No new dependency or remote resource. Unit checks passed; actual UI verification used CUA. The complete terminal browser suite was not run. Native Safari scrolling remains outside the observed browser scope.

## Reader generator refactor after the document-layout rejection

The later revision replaces the report document frame with a product library and seven addressable analysis views, plus continuous reading. `reader_shell.py` owns view composition, `reader.css` owns shell geometry, and `reader.js` owns visible-view state. Research rendering, semantic diagrams and anchor/history/inspector control retain their own owners. The new shell uses separate classes instead of cascading another theme over the old document layout. Legacy support pages keep their existing readable frame.

A new initially failing regression requires every chapter and all four maps to belong to a reachable view for both brief and legacy input; it passes after the frame replacement. Source links reveal the source view before scrolling; saved history restores the previous view before restoring scroll, node details and focus. Initial deep links select the right view. Without scripts all view content remains present; print reveals it all. Selecting the current product on phone also closes the product chooser.

The project-local `design-review.html` compares actual Runway, Oura and Linear Plan captures with the original and new reports across six surfaces. References influence visual composition only. Browser screenshots remain in the report project, not this Skill.

Additional instruction scenario review (manual desk review, not blind model execution):

| Scenario | Expected behavior |
| --- | --- |
| User says HTML needs reconstruction | Refactor shell, information structure, state and component ownership; preserve research instead of another palette patch |
| Direct link into a hidden map/source | Reveal its owning view before measuring and navigating |
| Source jump then browser back | Restore previous view, node inspector, scroll and focus together |
| Continuous reading / scripts unavailable | Retain every chapter, diagram and evidence item |
| Same-task cross-product comparison | Native product links retain a valid analysis anchor; identity and current state update |

Final counts, file hashes and actual browser scope are in the delivered verification receipt; earlier checks above belong to the earlier Fieldnotes iteration and do not certify this later refactor.
