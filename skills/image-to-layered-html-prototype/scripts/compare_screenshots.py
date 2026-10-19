#!/usr/bin/env python3
"""Compare two same-size screenshots and emit a compact JSON report."""
import argparse, json, sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageStat
except ImportError:
    print("compare_screenshots.py requires Pillow; install it in the active workspace runtime", file=sys.stderr)
    raise SystemExit(2)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=Path)
    parser.add_argument("actual", type=Path)
    parser.add_argument("--threshold", type=int, default=0)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--diff-out", type=Path, help="write a transparent red diff mask")
    args = parser.parse_args()
    if not 0 <= args.threshold <= 255:
        parser.error("--threshold must be between 0 and 255")
    reference = Image.open(args.reference).convert("RGB")
    actual = Image.open(args.actual).convert("RGB")
    if reference.size != actual.size:
        report = {"status":"dimension_mismatch", "reference":reference.size, "actual":actual.size}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if args.json_out:
            args.json_out.write_text(json.dumps(report, indent=2) + "\n")
        return 1
    diff = ImageChops.difference(reference, actual)
    mask = Image.new("L", reference.size, 0)
    for channel in diff.split():
        channel_mask = channel.point(lambda value: 255 if value > args.threshold else 0)
        mask = ImageChops.lighter(mask, channel_mask)
    diff_bbox = mask.getbbox()
    stats = ImageStat.Stat(diff)
    histogram = diff.histogram()
    differing = 0
    pixels = reference.width * reference.height
    for value in range(args.threshold + 1, 256):
        differing += sum(histogram[value + channel * 256] for channel in range(3))
    mean_abs_error = sum(stats.mean) / 3
    report = {
        "status": "ok" if differing == 0 else "different",
        "width": reference.width,
        "height": reference.height,
        "mean_absolute_error": round(mean_abs_error, 4),
        "different_channel_values": differing,
        "different_channel_ratio": round(differing / (pixels * 3), 6),
        "different_pixels": mask.histogram()[255],
        "different_pixel_ratio": round(mask.histogram()[255] / pixels, 6),
        "threshold": args.threshold,
        "different_bbox": list(diff_bbox) if diff_bbox else None,
    }
    if args.diff_out:
        visual_diff = Image.new("RGBA", reference.size, (255, 0, 0, 0))
        visual_diff.putalpha(mask)
        visual_diff.save(args.diff_out)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.json_out:
        args.json_out.write_text(output + "\n")
    return 0 if differing == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
