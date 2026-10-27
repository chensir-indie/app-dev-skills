# Screen and state matrix

Treat each supplied screen as a stateful contract, not as an isolated poster.

```json
{
  "id": "home-ready",
  "route": "/home",
  "trigger": "app launch with fixture data loaded",
  "reference": "reference/home-ready.png",
  "viewport": {"width": 591, "height": 1280, "dpr": 1},
  "landmarks": ["hero-title", "open-detail", "bottom-nav-home"],
  "primaryInteraction": "open-detail",
  "expectedOutcome": "opens the selected item detail"
}
```

Record selected and unselected controls, loading and error states, empty states, scroll position, modal overlays, keyboard/focus states, and system chrome when they are part of the reference set. Each state gets its own screenshot and diff report.

Do not merge two references because their copy or subject image looks similar. A state mismatch invalidates the comparison.

The example uses the native-reference DPR=1 coordinate strategy. Record logical-size/DPR conversions explicitly for other strategies; never multiply the reference size by DPR again. `capture_native.cjs` labels output with the state id but does not execute this trigger. Verify the target state is actually visible before collecting evidence; use an explicit browser interaction flow for non-entry states.
