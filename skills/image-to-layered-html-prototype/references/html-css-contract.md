# Editable implementation

## Structure
Use CSS or independent UI-free decorative assets for backgrounds, CSS/SVG for backplates, images only for photos/subjects, DOM for text, and button/a elements for visible actions. Full-screen raster/Canvas, large UI slices and hidden text over screenshots are not valid substitutes.

Every delivered layer has a stable id / data-layer-id. Map text and controls to manifest selectors; images carry data-asset-role="subject|photo|decoration|logo". Do not hide a full reference image in a data URI or SVG image element. Full references belong only in a separate review.html, never in requests from index.html.

## Typography and stacking
After freezing baseline coordinates, use absolute positioning, grid or flex as appropriate to reproduce measured values. Do not use unmeasured space-between distribution.
Express stacking explicitly: background < decor < backplate < subject < content < navigation < dialog; this is not a requirement for fixed numeric z values.
overflow, transform, filter and opacity affect stacking. Verify by hiding layers and inspecting intersections, rather than relying only on z-index values.
Record regular corner radii individually. Measure turning points and curves for irregular SVG backplates instead of replacing them with large rounded rectangles.
Specify actual font family/fallback, weight, size, pixel line height, tracking, color, alignment and wrapping; reset browser defaults on buttons and similar elements.
Record each navigation item's own shape, icon/text direction and selected/unselected states. Do not assume equal widths or horizontal arrangement.

## Interactions
Visible controls produce actual feedback: navigation changes visible content and aria-current, an add action updates a list/button state, and details can open and close.
data-clicked attributes, console output or hidden aria-live text alone are insufficient. Label unavailable production behavior as a demo and do not write real user data.

## Proof of editability
Change a heading in the browser and capture it; hide subject and backplate separately and capture each. With all photo/subject assets hidden, headings, backplates, navigation and buttons must remain. These are verification actions, not required toggles in the final UI.
