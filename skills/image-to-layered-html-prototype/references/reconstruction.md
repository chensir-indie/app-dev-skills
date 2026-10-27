# Asset extraction and contour reconstruction

A screenshot is not a layered source file, but its visible shapes can be measured and fitted. Infer unknown occluded regions only where needed; inference is not permission to change visible contours arbitrarily.

1. Look for separate assets from the same generation task. Compare visible parts, shape, viewpoint and shadows; similar filenames do not establish identity. An unrelated substitute is for layout debugging only. If it remains in the final capture, that asset and its ROI stay visually `pending`.
2. If only a flattened image exists, locate source coordinates and edges for the photo/subject. Extract a transparent subject under the actual imagegen tool's constraints, preserving visible parts, viewpoint and proportions while removing all text, backplates, buttons and background. Independent background assets must also be UI-free. Do not treat the whole image as the extracted result.
3. Inspect white/green fringes, holes and translucent pixels against white, dark and target backgrounds. Record alpha bounds and sourceCrop. Scale to visible boundaries, not merely PNG dimensions.
4. Mark occluded boundaries `inferred`. If generation changes visible subject shapes, record the mismatch and continue repairing it. Do not describe failed extraction as “the source file is missing, so HTML cannot be made.”
5. Mark backplate anchors along visible contours: curvature changes, sloped-edge endpoints, steps and corner tangencies. Use one SVG viewBox, record Bézier control points and close the path. Draw fill, stroke and shadow separately. Plants are usually in front of the backplate and text above both; follow actual occlusion.
6. Redraw icons as independent vectors, checking stroke-width, linecap, linejoin and optical size. A heart cannot become a leaf, and an emoji cannot replace a camera icon.
7. Sample unobstructed background color areas and fit the gradient before adding separate texture and subject shadows. Derive angle, stops and opacity through comparison iterations instead of substituting an unrelated gradient.

For each asset record provenance, original hash, processing, source crop, intrinsic dimensions, alpha bounds, target rectangle, object-position and contour differences. Measurements observe the visible screenshot; original font parameters and generation internals may remain unknown.
