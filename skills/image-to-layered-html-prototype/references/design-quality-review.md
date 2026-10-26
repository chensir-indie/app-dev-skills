# Design quality review and improvement

Use for design exploration, requested improvements and review of actual reconstructed pages. Record the intent in the existing project record first: faithful reconstruction, active refinement or review only. These are workflow branches, not new manifest enum values. Read the applicable sections without producing a full design report for a local repair.

## 1. Establish the design basis

Read existing project standards, pages, components and chosen references, then add a short design brief to existing files rather than creating a conflicting DESIGN.md:

- Who completes which task in what context; the page's single primary action and success feedback.
- Content, brand features, navigation and data to preserve; areas open to change.
- Visual subject, reading order, density, whitespace strategy and observable style features.
- Primary design system, target platform, font/icon provenance, shared tokens and necessary page variants.
- Pages, states, languages and viewports to verify; current reference and source identity.

Translate “premium” into inspectable decisions, such as “the heading is noticed before decoration, primary and secondary actions have different emphasis, and body text avoids busy texture.” Preserve product character. Uniform glass, gradients, large radii, giant headings or stacked cards do not replace design judgment; reproduce these accurately when the reference actually uses them rather than applying a reverse blacklist of styles.

Choose the primary standard using [sources and applicability](design-sources.md). Existing project standards come first. When starting from scratch, consider HIG for Apple, Material for Android, and Carbon or Ant Design for complex Web business interfaces. Flutter is an implementation technology, not an automatic visual-style choice. Share brand and semantic tokens across platforms and record component differences; do not randomly combine several component skins.

In faithful reconstruction, approved images determine visible geometry and styling. Guidelines identify issues and fill unknown states; they do not override frozen backplates, font sizes, layout or selected states. If the reference conflicts with accessibility, record fidelity results and proposed product revisions separately rather than claiming both pass. When improvement is authorized, edit and review within that scope without additional item-by-item approval. Preserve the original and explain conflicts with explicitly retained design requirements.

## 2. Diagnose first, then repair by impact

Inspect the actual artifact: generated images during generation; open pages, trigger primary states and capture them during HTML work. Reading CSS or describing an image cannot replace viewing the page. List the 3–5 issues with the greatest task/visual impact, ordered by blocked actions, broken hierarchy/fidelity and local detail. Use the actual number if fewer than three local issues exist. For review only, deliver issues, evidence and recommendations, then stop without editing.

Each issue includes page/state, screenshot or ROI, relevant selector/source location when available, concrete observation, user impact, proposed change and verification method. Distinguish measurable errors from aesthetic judgment; avoid unsupported overall scores.

| Pass | Inspect | Change and verify |
| --- | --- | --- |
| Hierarchy and task | First impression, reading order, primary/secondary actions and information groups | Address competing focal points, duplication and unclear actions first. Use thumbnails for structure, native size for content and an actual primary-flow walkthrough |
| Layout and proportion | Alignment anchors, within/between-group spacing, main-image visible area, whitespace, scrolling and safe areas | Change shared grids/spacing or specific components rather than accumulating page patches. Measure the source for reconstruction instead of forcing values to an arbitrary spacing scale |
| Typography and color | Glyphs, CJK fallback, weight, line height, wrapping, heading/body hierarchy and composited backgrounds | Verify fonts really load before changing size. Compare baselines and visible glyphs, not only CSS values; inspect actual content and contrast |
| Icons, shapes and materials | Icon family, stroke, optical size, individual corners, lighting, shadows and occlusion | Restore SVG paths and alpha boundaries, calibrate subject/backplate as separate layers, and hide layers to detect duplicated baked-in effects |
| States and adaptation | selected/pressed/focus/disabled, long copy, empty/error/loading, narrow layouts and keyboard | Trigger applicable cases below, check all consumers after shared-component repairs, and label designed/inferred states without references |
| Final polish | Numeric alignment, truncation, borders, icon baselines, scroll edges and feedback timing | Save same-environment before/after captures and check improvements/regressions. Stabilize layout before decorative motion |

Change one issue category per iteration. Reconstruction continues using [visual-convergence](visual-convergence.md)'s frozen limits. Active refinement uses the design brief and before/after evidence; similarity to the old draft is not the measure of new-design quality. Reconsider font, asset or structure causes after two iterations without improvement rather than adding more effects.

## 3. Completeness and Web quality

Select scope from actual page functionality: do not invent form tests when there is no form or add a dark mode outside product scope. Record reasons for not-applicable checks; untested items remain untested, not passed.

- Content: actual headings, mixed Chinese/Latin text, long names, empty content and varying counts; test RTL when supported. Wrapping, truncation or expansion must keep important information available; do not hide overflow by shrinking the global font.
- States: loading, empty, error/retry, success and disabled. Check selected and pressed separately. Restore reasonable focus/scroll after closing dialogs and support back navigation.
- Input: native semantic buttons, links and labels; accessible names on icon buttons. Complete the main flow with a keyboard, with visible focus unobscured by fixed bottom bars. Do not duplicate keyboard click handling on native buttons.
- Readability: compare text against its actual composited background. Under Web WCAG 1.4.3, normal text generally needs 4.5:1 and large text 3:1; read definitions/exceptions in the source. Test the worst region of gradients/images rather than one sampled pixel. Inspect thin text visually even after numeric checks pass.
- Adaptation: pass the baseline viewport first, then narrow/wide widths, text enlargement and scrolling. For Web, check 200% text scaling and applicable 320 CSS px reflow. A fixed-pixel reference does not establish responsive-product acceptance.
- Targets: separate visible graphics from hit areas. Web WCAG 2.5.8 uses 24 × 24 CSS px or its specified exceptions, not a universal 44 px across platforms. Native targets follow current platform guidance; do not mix pt, dp and CSS px. Expanded hit areas must not overlap adjacent actions.
- Motion and resources: respect reduced motion and allow interruption of feedback. Add motion only when it explains state. Reserve image space; capture after fonts/images load and observe actual layout shifts. Do not turn one performance choice into a prescription for every page.

These focused checks are not a complete WCAG compliance audit. Vercel guidance may aid Web review, but choose style and technical recommendations in project context. Do not introduce unrelated frameworks or change locked copy merely to follow guidance.

## 4. Evidence and completion

Reuse existing `evidence/` and acceptance records; add a short `design-review.md` if needed instead of a second machine schema. Record:

```text
Scope and intent: page/state; reconstruction / refinement / review only
Basis: project standard, primary design system, reference path/SHA, allowed changes
Issue: id; priority; observation; task impact; screenshot/ROI; selector or file:line
Change: modification/reason; related token/component; affected other pages
Verification: source/asset identity; before/after images; browser/viewport/DPR; interactions; observed results
Decision: retain or revert; unfinished checks; next action
```

Inspect before/after images at the same viewport/state: native size for glyphs and controls, thumbnails for hierarchy, and enlarged crops for edges/occlusion. Thumbnails aid hierarchy only, not readability or target testing. Every improvement claim points to an observation; refreshed captures require corresponding source/asset hashes.

Report design quality, reference fidelity and interaction/adaptation scope separately. Review-only does not claim fixes; refinement without an approved reference does not claim one-to-one acceptance. Full reconstruction still passes [acceptance](acceptance.md)'s scripts and manual review. List reconstruction-time design suggestions separately rather than changing the baseline automatically. Improving existing HTML does not require imagegen. When a new design followed by full reconstruction is requested, preserve the old reference, save and freeze the chosen new draft and its rationale separately, then measure and close the loop; do not overwrite old acceptance failures with a new draft.
