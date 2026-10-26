# From imagegen to a reconstructable design

## Choose the entry point

Determine the requested endpoint first. For directions or prompts only, deliver them and stop. For a reference image only, actually generate, inspect and deliver the image, then stop. Continue to reference measurement, asset preservation, HTML comparison and complete page workflows only when a full HTML prototype is requested.

If an approved design already exists for full reconstruction, preserve its original image, dimensions and SHA and measure it directly. Edit assets only when a subject is missing or the background contains UI. When a new image is needed, establish page, primary task, visual subject, main action, density and language from the user goal before generation. Do not reconfirm an already chosen direction.

Read the actual available imagegen tool's skill before invoking it. Inspect local images before editing and use its supported reference mechanism. Request transparent backgrounds for transparent assets. Writing workflow documentation or a skill does not require spending an image-generation call.

For new design or refinement, establish the primary standard, reading order and action hierarchy using [design quality review](design-quality-review.md). Faithful reconstruction of an approved image does not reselect the style. Existing-HTML refinement edits source and verifies in a browser directly; imagegen is not a prerequisite.

## Design-image prompt template

Replace bracketed placeholders with actual content; do not send template text to the generation tool.

```text
Design [product]'s [page and state] as a front-facing UI reference for HTML implementation.
Canvas ratio [W:H], content language [language], exact copy [text list].
Primary task [task], primary action [action], focal subject [object].
Inherit the attached chosen reference's [color field/typography/material/component relationships].
Primary design standard [project standard or chosen system], core tokens [font/color/spacing roles].
Visual hierarchy [first focus, second focus, supporting information]; primary/secondary emphasis [specific difference].
Content order [order]; layout priorities [anchors, size relationships, whitespace].
Explicit layers: background, decoration, backplate, subject, text, controls, navigation.
Place the subject in front of [layers]; backplate contour [actual shape description].
Navigation includes [items, selected item, icon/text arrangement].
Output one complete front-facing interface, without a hand holding a phone, perspective bezel or presentation board.
Keep text regions legible and button states clear; background texture must not impede reading.
```

After generating a new design, check subject, reading order, action hierarchy, rhythm and readability against the brief. Repair the most consequential issues first. A gradient or glass effect alone does not establish quality. Full-page regeneration cannot erase reconstruction errors against a locked draft.

Actually inspect glyphs, truncation, buttons and occlusion after generation. Generated Chinese text may contain invalid glyphs and is not authoritative copy. For HTML, preserve the pixel reference and record intended correct text in the copy table. If they conflict, label the region as a copy correction rather than claiming pixel identity. Requested dimensions may differ from output dimensions; read actual width/height when saving.

## Subject extraction prompt template

```text
Reconstruct and output only [subject] from the reference, on a transparent background.
Preserve the visible contour, count, pose, viewpoint, proportions, material, colors and lighting direction.
Remove all text, icons, buttons, backplates and background; carry none of their UI pixels into the asset.
Complete only occluded parts that are actually needed; do not redesign the visible subject.
Keep the subject whole with clean edges, no white fringe and no clipping.
```

This is generative reconstruction, not lossless matting. Check leaves, product parts, pot, viewpoint and shadows. Drift remains pending repair; a successful tool response does not prove asset identity.

## Background cleanup prompt template

```text
Use the reference to retain/restore only the underlying background.
Remove the subject and all UI text, icons, buttons, navigation and information backplates.
Preserve the original color field, lighting direction, texture scale and decoration positions.
Fill removed regions naturally, adding no new subjects, text or decorations.
```

Background texture may use an independent bitmap. Prefer CSS/SVG for geometry expressible as gradients or vectors. If a glass backplate is blurred again in the browser, its asset must not already bake in that same backplate, shadow or blur, which would duplicate the effect. Likewise, assign each shadow explicitly to either an asset or CSS/SVG.

## Asset checks and traceability

The following traceability and HTML comparisons apply to full reconstruction. Directions, prompts and standalone reference images end at their endpoints above.

For every generation, record purpose, reference SHA, actual prompt, the model/settings actually returned by the tool (`unknown` if absent), output path/SHA, intrinsic dimensions, alpha channel, visible alpha bounds, version and reason for adoption. Do not invent seeds or internal settings. Save files in the prototype's assets directory rather than depending on temporary conversation attachments.

Check transparency against white, dark and target backgrounds before placing the asset in actual HTML; compare subject/background ROIs. Change one variable per iteration and preserve prior assets/captures. Full-page regeneration changes layout and is not a shortcut for HTML calibration.

## Complete page sets

For a complete multi-page prototype, freeze an approved representative page as the style source, extract shared standards, then use actual page content/states to generate the other pages. Do not ask a single generation to produce many pages too small to measure. Collages aid browsing only; retain a separate original for each page. Track generation, HTML implementation and visual acceptance separately. Generating all images does not mean implementing all pages.
