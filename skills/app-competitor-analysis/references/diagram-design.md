# Diagram meaning and composition

Read this when authoring the four maps or repairing weak visual explanation. A diagram should let the reader identify the task, its decisive choices and the limits of the evidence before inspecting individual nodes.

## Choose a grammar before laying out nodes

| Map | Primary expression | Secondary information |
| --- | --- | --- |
| Capabilities | An asymmetric landscape: task-critical capabilities, supporting conditions, independent/optional jobs | Preserve original module taxonomy, every atomic capability, useful role and evidence type |
| Task | A prominent, numbered spine following actual directed transitions | Optional entries, decisions and returns remain visible with their origin, condition, destination and evidence |
| Screens | Surface relationships, retaining containment and navigation wording from the evidence | Separate disconnected observations; a control shown on one screen does not establish a route to another |
| Technology | Responsibility symbols and a selected data path, paired with a concrete boundary statement | The full graph retains every data/control dependency, side input, retained state and unresolved endpoint |

The grammars communicate different questions. Capability tiers are analytical priority within an explicit task scope, not actual menus, usage frequency or business importance. A selected task path is one analyzed route, not proof that it is most common or already verified. Technical roles describe responsibilities; deployment location requires separate evidence.

Use a restrained system-font type scale, neutral surfaces, one restrained interaction accent and whitespace. Let the primary task carry more visual weight than metadata. Keep body, captions and evidence readable under the [Apple-guided web contract](apple-web-design.md). Analytical prominence and evidence certainty remain independent channels: a highlighted unknown transition is still dashed and labeled unknown.

## Author the meaning in report data

For new authored reports, include `features.priority`, `journey.focus` and `dataflow.contract`. The renderer keeps legacy maps readable, but does not assign priorities from array order, graph degree, keywords or familiar product categories. Review each competitor individually. A sparse product can have a necessary but unknown core capability; keep that gap rather than inventing its behavior. A broad product may have several independent core jobs; state which job the current comparison emphasizes.

`reading: {text, sources}` introduces the mechanism explained by each map. Node `caption` is a concise, qualified role explanation; full `detail`, status and sources remain in both the inspector and equivalent HTML index.

```json
{
  "priority": {
    "scope": "Write a note and recover it after interruption",
    "rationale": "Writing and recovery close this task; search serves a separate revisit task.",
    "core": ["write", "draft", "open"],
    "supporting": ["new", "storage"],
    "extension": ["search"],
    "sources": ["E1"]
  }
}
```

The three lists cover every feature ID exactly once, including historical and unknown capabilities. Keep their original evidence statuses and module labels. The rationale explains the scope of the analytical choice; it does not upgrade a source claim.

```json
{
  "focus": {
    "title": "Write, interrupt and recover",
    "rationale": "Follow the documented recovery path; retain the retry loop separately.",
    "path": ["start", "edit", "leave", "return"],
    "sources": ["E1"]
  }
}
```

Adjacent IDs must have an existing, unambiguous directed edge. The selected spine has no repeated nodes; show returns as explicit branch edges, with a link back to the earlier stage. Keep every nonselected node and edge visible. Group disconnected evidence as separate parallel paths, without a synthetic connecting arrow. On desktop, fit the main stages at readable size; a wrapped row names the next stage. On phones, reflow the spine vertically with its conditions and preserve the separate branches.

```json
{
  "contract": {
    "focus": ["input", "memory", "disk", "reopen"],
    "roles": {
      "input": "input", "memory": "state",
      "disk": "state", "reopen": "output"
    },
    "boundary": {
      "title": "Memory changes and durable recovery are separate",
      "detail": "Input reaches the buffer; the disk write and reopened text still need durable-storage evidence.",
      "sources": ["E1"]
    }
  }
}
```

Assign exactly one responsibility role to every technical node: `input`, `process`, `control`, `state`, `output` or `boundary`. Use an open input bracket, rounded transform, control marker, retained-state cylinder, output terminator and dashed unresolved boundary. These symbols describe the object/function, not whether it is on-device, remote, current or verified; retain the evidence badge independently. A short selected data path helps locate the important dependency within the complete graph.

The boundary statement names the consequence that changes interpretation: for example, a generated reference versus a real capture, local temporary data versus a system asset, a remote preview versus an original file, or accepting an edit versus saving it. Name specific known and unknown contracts. Keep competing mechanisms and version limits visible. A separate statement that says only “implementation unknown” does not explain a boundary.

Validation rejects incomplete/duplicate feature assignments, invalid roles, missing technical nodes, paths that invent transitions and unknown annotation sources. It checks references and structure, not the truth of authored priority or boundary reasoning. Keep competitor-specific annotations in the project bundle, not in reusable Skill fixtures.

## Place diagrams with the argument

In the `brief` reading layout, place the feature landscape after product positioning, screens with UI evidence, the task spine with interaction and technical responsibilities with the mechanism explanation. Keep each complete map outside research disclosures in its corresponding reader view; continuous reading and no-script output retain all views. Preserve the four-link map directory, map/node/source anchors, inspector and source/back return.

Maintain these grammars in `scripts/semantic_atlas.py`, general graph geometry in `scripts/visual_atlas.py`, shared atlas styling in `assets/atlas.css` and report/image composition in `assets/editorial.css`. Keep exact evidence, full node details and exhaustive research when changing prominence. Report-opening and catalog excerpts use the authored connected task path when available, otherwise the authored core list. Label the selection and retain evidence status, original transitions and excerpt length. Responsibility glyphs stay in technology views, where roles are authored; cover task glyphs carry no technical claim. Preserve original module containers within capability tiers, grouping by identity rather than display-label equality. A count bar shows recorded nodes, not measured product importance. Adapt short versus long technical chains as described in [report design](report-design.md).

## Preserve relationships and legibility

SVG labels use 16px titles and 13px caption/status text at the default drawing scale. Caption wrapping, card geometry and connector gutters form one layout contract. Check actual rendered text rather than enlarging text independently into an old box. Route arrows outside unrelated nodes, place condition labels in free space and reserve bounds for return lanes, labels, singleton groups and self-loops.

Wide full graphs retain readable scale in a labeled scrolling region; fit is an explicit control. Zoom/reset/fit apply equally to every component in that map. On phones, full spatial screen/technical graphs offer a reflowing adjacency view plus a clear diagram switch. Task spines, feature tiers and technical overview paths reflow directly; they do not require graph zoom. All complete maps and equivalent indexes remain available without scripts and in print.

## Review the whole requested collection

First inspect a dense capability landscape, a conditional/looping task, disconnected routes, a technical persistence boundary and sparse evidence. Then check every report for the authored scope, all feature assignments, exact node/edge inventory, evidence labels, source links and correct chapter association. Check SVG geometry separately from HTML reflow and actual text bounds.

Exercise desktop and phone layouts, wrapped-stage continuation, diagram controls, keyboard/node inspection, Escape focus return, source/back, enlarged text, no-script reading, print restoration and measured scrolling. Bind checks to the final HTML/asset hashes. Counts prove inventory coverage, not comprehension, visual quality or competitor runtime acceptance.
