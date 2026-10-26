# Closing consequential evidence gaps

A gap is an unanswered decision question, not a final paragraph saying “data missing”. When public research is within scope, actively attempt appropriate acquisition before delivering an evidence-limited conclusion. If the user restricts browsing or provides a pinned historical corpus, honor that boundary and record it. Do not promise exhaustive knowledge of a closed-source product.

## Run the loop

1. **Inventory and diagnose.** Read the underlying supplied material, not only its summary. For each product, distinguish uncollected evidence, an uninspected artifact, a real source/access failure, conflicting revisions and private implementation that has never been disclosed. An empty report chapter proves none of those on its own.
2. **Ask a narrow question.** Record the missing answer, why it affects the user's decision, and what observation would close it. “Understand all technology” is not a closure criterion. “Does reference matching require sending preview pixels off-device?” is. Separate publisher promises, visible UI and verified execution into different questions.
3. **Prioritize.** P0 changes the main product decision or prevents understanding the core task; P1 explains an important branch, capability or condition; P2 adds optional depth. Keep requested products in the queue. In a landscape, rotate deep samples across distinct mechanisms; do not repeatedly choose the best-documented app. Do not manufacture generic gaps for capabilities irrelevant to that product.
4. **Acquire and inspect.** Choose a channel that can supply the required proof below. Read the relevant section, view the pixels or inspect the trace/call path. A search snippet, discovered link, successful fetch or downloaded file is not inspection. Preserve identity, source/capture date, platform, revision and useful region/timestamp/locator.
5. **Reconcile and apply.** Compare the new source with old findings. Keep conflicts and version boundaries visible. Update the claim, coverage, feature tree, relevant task/screen/data-flow nodes and report chapter. If only one assertion is supported, upgrade only that assertion. Split a partially answered question instead of broadening its answer.
6. **Re-evaluate.** Check the original closure criterion. Close it only when the required proof has been inspected and incorporated. Otherwise name the remaining question and execute the next useful route, or record the concrete boundary. Continue independent work while a device/access question is pending.

## Match the question to a channel

| Question / required proof | First useful channels | Alternative / escalation | What does not close it |
|---|---|---|---|
| Identity, platform, current declared capability | Canonical store ID, publisher site, help and dated release notes | Publisher-linked store or support material; pinned artifact metadata for its version | Similar name or another region/platform silently substituted |
| UI hierarchy, controls, styling (`pixels`) | Actually viewed official gallery, product walkthrough frames, supplied captures | Press kit or alternate publisher image host; authorized current app capture | Text descriptions, image URLs or generated mockups |
| Publisher's core flow (`stated_behavior`) | Official manual, walkthrough, named task documentation | Publisher demo with locatable steps | A static screenshot proving an unshown transition |
| Actual flow, persistence, recovery (`behavior`) | Authorized runtime/recording with start and resulting state | Compatible permitted environment or inspectable supplied runtime trace | Marketing, a success toast alone or a simulator asserting hardware performance |
| Implementation (`implementation`) | Authorized pinned artifact, reachable call/data path, relevant runtime trace | Official technical disclosure answers what is disclosed, not verified implementation | SDK names, model files, endpoint names or guessed backend vendors |
| Published mechanism (`disclosed_technology`) | Official technical article, architecture notes, documented API/data contract | Primary developer talk or release notes with explicit scope | Treating public claims as proof of private server internals |
| Entitlement, account/offline conditions (`commercial_terms`) | Region/tier/date-specific official terms and help | Authorized visible gate; trial boundary can be observed without purchase | Old price/review, invisible paywall or a plan name without its rights |

Consult other available sources when useful, but label secondary reporting accordingly. A review may locate a question or suggest a failure; it does not become current official/runtime proof. Never count search-result quantity as evidence coverage.

## Failure and stopping rules

- For a plausible transient error, make one focused retry, then change something material: source, host, channel or evidence route. Record the actual failed locator/error. Do not spend the session changing query wording or repeatedly hitting an inaccessible endpoint.
- A page failure need not block its publisher's image URL, help site or store page. Try a relevant alternative when available. Conversely, a text extraction fallback cannot resolve a pixel question. A failure on one CDN image does not prove every image on that host was attempted.
- Login, unavailable hardware, purchase or access restrictions require an explicit boundary. Use already authorized access. Do not buy, subscribe, bypass controls, upload private photos or ask for unnecessary approval. Ask for the smallest missing user input only when dependent work needs it; continue other questions meanwhile.
- `queued` means not attempted. `attempted` means acquisition was tried without enough evidence. `partial` means part of the question was answered. `blocked` requires an actual relevant failed/barrier attempt, a reason and a condition that would unblock it; mention useful untried alternatives instead of declaring the whole product blocked. `deferred` requires a reason and resumption condition. `out_of_scope` requires a recorded scope basis, never a convenient way to improve completion statistics.
- Stop a question when its criterion is satisfied. Stop a route when it cannot supply the required proof. Stop chasing undisclosed internals when further available research cannot distinguish the candidates; keep the implementation question open with alternatives and the evidence needed. Report why the decision can or cannot proceed despite it.
- For broad work, intermediate delivery is useful: say which products were actually researched, which gaps closed and which remain in the queue. HTML generation, attractive graphs, a successful audit or all files existing never means the research is complete. A work queue alone is not completion of authorized research.

## Acquisition record (schema version 1)

For a small task, a table with the following fields is enough. For a broad or recurring study use [acquisition.example.json](../assets/acquisition.example.json). It is a fictional fixture, not a real source record. Keep the actual ledger with project output; do not bundle private evidence with the skill.

Top level: `schema_version`, `scope`, `products`, `sources`, `gaps`.

- Products: `id`, stable `identity` (additional context allowed).
- Sources: `id`, `product_id`, `kind` from the evidence model, `locator`, `version` or `unknown`, boolean `inspected`, plus date/context and local hash/path where relevant. An inspected official web page remains `official`; add a separate `screenshot` source only after viewing its image.
- Gaps: `id`, `product_id`, `dimension` (`identity`, `ui`, `interaction`, `technology`, `business`), `priority`, `question`, `impact`, `proof` from the table, `target_version` or `unknown`, `closure_check`, `state`, `attempts`, `source_ids`, `resolution`, `remaining`, `next_action`, `report_updates`. Blocked/deferred/out-of-scope records also need `reason`; blocked/deferred need `resume_condition`.
- Each attempt: `date`, `channel`, exact `locator`, `outcome` (`success`, `partial`, `failed`, `unavailable`, `barrier`, `no_result`), useful `note`, and acquired `source_ids` (can be empty). Record failure as an attempt, not a fictitious evidence source. Successful text inspection and failed image viewing can coexist.
- `report_updates` names the actual updated report/diagram/claim. `resolution` answers only the recorded question. Do not mark it resolved while `remaining` still asks part of that question; split off a new gap instead.

```sh
python3 scripts/audit_acquisition.py path/to/acquisition.json
```

The standard-library checker validates joins, proof types, inspected-source declarations, pinned versions, actual-attempt records, report-update declarations and state requirements. It returns state counts and unresolved P0 count. `research_complete` requires at least one resolved question and all recorded in-scope questions resolved; excluding every question is not completed research. It does not certify that the question inventory is exhaustive. Exit 0 means structurally valid, even if research is incomplete. The checker cannot know whether a source was really viewed, an update really applied, a blocker exhausted alternatives, or an answer semantically sufficient. Review those against raw evidence and the rendered report.

## Reader-facing receipt

Each report's gaps section shows: consequential question → attempted channel/result → new finding/source → remaining boundary → next action. Link the acquisition ledger from the delivery where useful. Keep the receipt concise; move long failed fetch logs to the local record. On the index, distinguish products acquired this pass from untouched queued products. Update diagrams first where new evidence changes the product explanation; do not hide useful new findings in an appendix.
