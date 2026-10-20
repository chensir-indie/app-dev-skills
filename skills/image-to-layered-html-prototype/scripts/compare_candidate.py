#!/usr/bin/env python3
"""A/B gate for a browser-rendered visual candidate before page contracts exist.

This is an iteration aid, never a visual-acceptance result.  All three inputs
must be native-size screenshots; a raw generated asset is not a candidate.
"""

import argparse
import json
from pathlib import Path

from runtime_support import ensure_pillow
ensure_pillow()
from PIL import Image, ImageChops, ImageStat

from visual_metrics import normalized_edge_disagreement


def metrics(reference: Image.Image, actual: Image.Image, box: tuple[int, int, int, int]) -> dict:
    ref = reference.crop(box)
    got = actual.crop(box)
    diff = ImageChops.difference(ref, got)
    return {
        "mae": round(sum(ImageStat.Stat(diff).mean) / 3, 4),
        "edgeDisagreement": round(normalized_edge_disagreement(reference, actual, box), 4),
        "rgbBias": [round(value, 3) for value in (
            ImageStat.Stat(got).mean[i] - ImageStat.Stat(ref).mean[i] for i in range(3)
        )],
    }


def compare(reference_path: Path, baseline_path: Path, candidate_path: Path,
            roi: tuple[int, int, int, int], min_improvement: float = 0.5) -> dict:
    images = [Image.open(path).convert("RGB") for path in
              (reference_path, baseline_path, candidate_path)]
    reference, baseline, candidate = images
    if not reference.size == baseline.size == candidate.size:
        raise ValueError("reference and both browser captures must have identical dimensions")
    left, top, right, bottom = roi
    if not (0 <= left < right <= reference.width and 0 <= top < bottom <= reference.height):
        raise ValueError("ROI must be within the native-size reference")
    full = (0, 0, *reference.size)
    before_full = metrics(reference, baseline, full)
    after_full = metrics(reference, candidate, full)
    before_roi = metrics(reference, baseline, roi)
    after_roi = metrics(reference, candidate, roi)
    full_gain = round(before_full["mae"] - after_full["mae"], 4)
    roi_gain = round(before_roi["mae"] - after_roi["mae"], 4)
    return {
        "reference": str(reference_path), "baseline": str(baseline_path),
        "candidate": str(candidate_path), "roi": list(roi),
        "full": {"before": before_full, "after": after_full, "maeImprovement": full_gain},
        "region": {"before": before_roi, "after": after_roi, "maeImprovement": roi_gain},
        "recommendation": "keep for further visual review"
        if full_gain > 0 and roi_gain >= min_improvement else "inspect or reject candidate",
        "visualAcceptance": "not evaluated; run frozen ROI and layer checks",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--roi", required=True, nargs=4, type=int,
                        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    parser.add_argument("--min-roi-improvement", type=float, default=0.5)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        report = compare(args.reference, args.baseline, args.candidate,
                         tuple(args.roi), args.min_roi_improvement)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if report["recommendation"].startswith("keep") else 1


if __name__ == "__main__":
    raise SystemExit(main())
