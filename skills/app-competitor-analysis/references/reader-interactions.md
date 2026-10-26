# Reading workspace interaction contract

Use when implementing or repairing the generated report's interaction. The user's accepted composition and research remain the baseline. Write down the reader's jobs before adding controls: find a competitor, compare the same dimension, inspect a claim, understand a diagram, read the design specification, then return to the original argument.

## Navigation and state

One controller owns report loading, view selection, deep links, history and reading position. Keep native report links and complete static HTML as the offline/no-script fallback. For an HTTP reading workspace, enhance competitor links with on-demand loading of just the chosen report. Keep the library and its search stable, cancel superseded requests and bound the in-memory report cache. Never preload the whole collection. A failed load leaves the current report usable and offers retry and a native document link.

Switching competitors keeps the current analysis dimension. Switching dimensions restores that dimension's position; explicit deep links reveal and align the actual target. Browser back/forward restores product, dimension, position and any active inspection. Update title, current-product state, accessible focus and mobile controls together. Loading, error, no-results and current state must be visible; do not present an old report under a new name.

On phones, product switching and the full chapter choice remain reachable from the sticky reading controls. Do not make the reader scroll back to the top or discover an offscreen horizontal tab to navigate. Native links still work with modifier keys and opening in another tab.

## Inspect without losing the argument

Use one accessible inspection surface for node meaning and provenance, with a clear close action, Escape and focus restoration. Following a node's source preserves the node as its return destination. Browser back should perform the same return. Keep original source anchors for copied URLs and no-script reading.

Original images open in a separate viewer with descriptive context and native original-file access; support previous/next when there is real additional evidence. Do not decode every full-resolution image at page load. Expand a map into an inspectable workspace, retaining its complete nodes/edges, readable scale, zoom/fit and equivalent text view. Node inspection must work there too. Closing returns to the same map and location.

Open Design.md as formatted reading content inside the workspace, with a section outline and an explicit Markdown-file link. Generate this view from the same specification as the exported artifact. Preserve all elements, state matrices, counterexplanations, protocols and sources. Do not make a raw-text browser tab the only normal reading path.

## Shared implementation and acceptance

Use native dialogs/links/buttons/selects and delegated events where they simplify lifecycle management. Replacing a report disposes its observers, stale requests, selection and transient content. Keep overlay focus inside the active dialog; return focus to a connected trigger or a meaningful fallback. Refrain from extra toolbars whose actions duplicate the current view.

Apply shared changes to every requested report. Verify real journeys, not only control counts: find → switch → inspect node → inspect source → back → close → change dimension → browser back; inspect full image; read Design.md and follow an internal source; expand map and inspect a node; cancel a slow report switch with a newer selection; recover a failed load. Include keyboard, phone, text enlargement, print and no-script cases. Bind results to final artifact hashes. Measure actual report switches and scrolling when responsiveness is in scope; disclose browser/device limits separately.
