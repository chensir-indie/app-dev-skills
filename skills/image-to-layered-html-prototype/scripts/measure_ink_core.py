#!/usr/bin/env python3
"""Read-only source-image ink measurement inside a deliberately tight ROI.

This measures high-contrast pixel cores, not antialiased glyph edges or a CSS
layout box. Inspect the ROI and result before using it as reference evidence.
"""

import argparse
import hashlib
import json
from pathlib import Path

from runtime_support import ensure_pillow
ensure_pillow()
from PIL import Image


DEFAULTS = {"light": (200, 220, 200), "dark": (100, 155, 135)}


def measure(path, box, mode, thresholds=None):
    path = Path(path)
    if mode not in DEFAULTS:
        raise ValueError("mode must be light or dark")
    with Image.open(path) as opened:
        image = opened.convert("RGB")
    x1, y1, x2, y2 = box
    if not (0 <= x1 < x2 <= image.width and 0 <= y1 < y2 <= image.height):
        raise ValueError("ROI must fit the native image")
    red, green, blue = thresholds or DEFAULTS[mode]
    matched = []
    for y in range(y1, y2):
        for x in range(x1, x2):
            r, g, b = image.getpixel((x, y))
            if (r > red and g > green and b > blue) if mode == "light" else (
                r < red and g < green and b < blue
            ):
                matched.append((x, y))
    if not matched:
        raise ValueError("no matching ink pixels in ROI")
    left = min(x for x, _ in matched)
    top = min(y for _, y in matched)
    right = max(x for x, _ in matched) + 1
    bottom = max(y for _, y in matched) + 1
    return {
        "schema": 1,
        "method": "high-contrast pixel core in manually selected native-pixel ROI",
        "image": str(path.resolve()),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "width": image.width,
        "height": image.height,
        "roi": list(box),
        "mode": mode,
        "thresholds": {"red": red, "green": green, "blue": blue},
        "bounds": {"x": left, "y": top, "width": right - left, "height": bottom - top},
        "pixelCount": len(matched),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--box", nargs=4, type=int, required=True, metavar=("X1", "Y1", "X2", "Y2"))
    parser.add_argument("--mode", choices=tuple(DEFAULTS), required=True)
    parser.add_argument("--thresholds", nargs=3, type=int, metavar=("R", "G", "B"))
    args = parser.parse_args()
    print(json.dumps(measure(args.image, args.box, args.mode, args.thresholds), indent=2))


if __name__ == "__main__":
    main()
