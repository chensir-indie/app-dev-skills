#!/usr/bin/env python3
"""Rank visual gaps against a frozen prototype contract without changing it."""

import argparse
import json
from pathlib import Path

from runtime_support import ensure_pillow
ensure_pillow()
from PIL import Image, ImageChops, ImageEnhance, ImageStat
from visual_metrics import normalized_edge_disagreement


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def inside(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f"missing or nonlocal file: {name}")
    return path


def score(reference, actual, box, threshold):
    ref_crop, actual_crop = reference.crop(box), actual.crop(box)
    difference = ImageChops.difference(ref_crop, actual_crop)
    mask = Image.new("L", difference.size, 0)
    for channel in difference.split():
        mask = ImageChops.lighter(
            mask, channel.point(lambda value: 255 if value > threshold else 0)
        )
    count = difference.width * difference.height
    ref_mean = ImageStat.Stat(ref_crop).mean
    actual_mean = ImageStat.Stat(actual_crop).mean
    return {
        "mae": round(sum(ImageStat.Stat(difference).mean) / 3, 4),
        "changedPixelRatio": round(mask.histogram()[255] / count, 6),
        "edgeDisagreementRatio": round(normalized_edge_disagreement(reference, actual, box), 6),
        "meanActualMinusReferenceRGB": [
            round(a - r, 2) for r, a in zip(ref_mean, actual_mean)
        ],
    }


def diagnose(root, state_id=None, tile_size=128):
    root = root.resolve()
    manifest = read_json(root / "layer-manifest.json")
    tokens = read_json(root / "design-tokens.json")
    states = read_json(root / "state-matrix.json")
    state = next((s for s in states if s["id"] == state_id), None) if state_id else states[0]
    if state is None:
        raise ValueError(f"unknown state: {state_id}")
    state_id = state["id"]
    acceptance_path = root / "acceptance.json"
    accepted = read_json(acceptance_path) if acceptance_path.is_file() else {}
    evidence = next((s for s in accepted.get("states", []) if s["id"] == state_id), {})
    screenshot = evidence.get("screenshot", f"evidence/{state_id}.png")
    reference_path = inside(root, state.get("reference", manifest["reference"]["path"]))
    actual_path = inside(root, screenshot)
    reference = Image.open(reference_path).convert("RGB")
    actual = Image.open(actual_path).convert("RGB")
    if reference.size != actual.size:
        raise ValueError(f"dimension mismatch: reference={reference.size}, actual={actual.size}")
    policy = tokens["validationLimits"][state_id]
    regions = tokens["validationRegions"][state_id]
    threshold = policy["channelThreshold"]
    full = score(reference, actual, (0, 0, reference.width, reference.height), threshold)
    full["passes"] = full["mae"] <= policy["maxMAE"] and full["changedPixelRatio"] <= policy["maxChangedPixelRatio"]
    ranked_regions = []
    for region in regions:
        result = score(reference, actual, tuple(region["box"]), threshold)
        result.update({"id": region["id"], "box": region["box"],
                       "limits": {"maxMAE": region["maxMAE"],
                                  "maxChangedPixelRatio": region["maxChangedPixelRatio"],
                                  "maxEdgeDisagreementRatio": region.get("maxEdgeDisagreementRatio")}})
        result["passes"] = (result["mae"] <= region["maxMAE"] and
                            result["changedPixelRatio"] <= region["maxChangedPixelRatio"] and
                            (region.get("maxEdgeDisagreementRatio") is None or
                             result["edgeDisagreementRatio"] <= region["maxEdgeDisagreementRatio"]))
        result["excessMAE"] = round(max(0, result["mae"] - region["maxMAE"]), 4)
        result["excessErrorMass"] = round(result["excessMAE"] * (region["box"][2] - region["box"][0]) * (region["box"][3] - region["box"][1]), 2)
        ranked_regions.append(result)
    ranked_regions.sort(key=lambda r: (r["excessErrorMass"], r["changedPixelRatio"]), reverse=True)
    tiles = []
    for y in range(0, reference.height, tile_size):
        for x in range(0, reference.width, tile_size):
            box = [x, y, min(x + tile_size, reference.width), min(y + tile_size, reference.height)]
            result = score(reference, actual, tuple(box), threshold)
            tiles.append({"box": box, **result})
    tiles.sort(key=lambda t: t["mae"] * (t["box"][2]-t["box"][0]) * (t["box"][3]-t["box"][1]), reverse=True)
    return {
        "state": state_id, "reference": str(reference_path), "actual": str(actual_path),
        "size": list(reference.size), "channelThreshold": threshold,
        "ranking": "excess MAE multiplied by ROI area; overlapping ROIs are not additive",
        "full": full, "regionsWorstFirst": ranked_regions,
        "worstTiles": tiles[:12],
        "allRegionsPass": full["passes"] and all(r["passes"] for r in ranked_regions),
    }, reference, actual


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prototype", type=Path)
    parser.add_argument("--state")
    parser.add_argument("--tile-size", type=int, default=128)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--overlay-out", type=Path)
    parser.add_argument("--heatmap-out", type=Path)
    args = parser.parse_args()
    if args.tile_size < 16:
        parser.error("--tile-size must be at least 16")
    root = args.prototype.resolve()
    try:
        report, reference, actual = diagnose(root, args.state, args.tile_size)
    except (KeyError, IndexError, OSError, ValueError) as exc:
        parser.error(str(exc))
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    if args.overlay_out:
        args.overlay_out.parent.mkdir(parents=True, exist_ok=True)
        Image.blend(reference, actual, 0.5).save(args.overlay_out)
    if args.heatmap_out:
        args.heatmap_out.parent.mkdir(parents=True, exist_ok=True)
        diff = ImageChops.difference(reference, actual)
        ImageEnhance.Contrast(diff).enhance(3).save(args.heatmap_out)
    print(output, end="")
    return 0 if report["allRegionsPass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
