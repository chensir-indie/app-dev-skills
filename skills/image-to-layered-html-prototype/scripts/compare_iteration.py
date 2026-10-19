#!/usr/bin/env python3
"""Compare two real browser captures against one frozen visual plan."""
import argparse
import json
from pathlib import Path

from PIL import Image

from diagnose_visual import inside, read_json, score


def compare(root, state_id, before_name, after_name):
    root = root.resolve()
    manifest = read_json(root / "layer-manifest.json")
    states = read_json(root / "state-matrix.json")
    state = next((item for item in states if item["id"] == state_id), None)
    if state is None:
        raise ValueError(f"unknown state: {state_id}")
    tokens = read_json(root / "design-tokens.json")
    reference = Image.open(inside(root, state.get("reference", manifest["reference"]["path"]))).convert("RGB")
    before = Image.open(inside(root, before_name)).convert("RGB")
    after = Image.open(inside(root, after_name)).convert("RGB")
    if reference.size != before.size or reference.size != after.size:
        raise ValueError("reference, before and after dimensions differ")
    threshold = tokens["validationLimits"][state_id]["channelThreshold"]
    regions = [{"id": "full", "box": [0, 0, *reference.size]}] + tokens["validationRegions"][state_id]
    results = []
    for region in regions:
        box = tuple(region["box"])
        old = score(reference, before, box, threshold)
        new = score(reference, after, box, threshold)
        results.append({"id": region["id"], "before": old, "after": new,
                        "deltaMAE": round(new["mae"] - old["mae"], 4),
                        "deltaChangedPixelRatio": round(new["changedPixelRatio"] - old["changedPixelRatio"], 6)})
    regressions = [item["id"] for item in results[1:]
                   if item["deltaMAE"] > .5 or item["deltaChangedPixelRatio"] > .01]
    return {"state": state_id, "before": before_name, "after": after_name,
            "fullImageImproved": results[0]["deltaMAE"] < 0,
            "regressedRegions": regressions, "regions": results,
            "review": "keep candidate" if results[0]["deltaMAE"] < 0 and not regressions
                      else "inspect tradeoff or revert"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prototype", type=Path)
    parser.add_argument("--state", required=True)
    parser.add_argument("--before", required=True, help="path relative to prototype")
    parser.add_argument("--after", required=True, help="path relative to prototype")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        report = compare(args.prototype, args.state, args.before, args.after)
    except (KeyError, OSError, ValueError) as exc:
        parser.error(str(exc))
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if report["review"] == "keep candidate" else 1


if __name__ == "__main__":
    raise SystemExit(main())
