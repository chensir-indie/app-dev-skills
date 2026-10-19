#!/usr/bin/env python3
"""Validate the editable layer contract. Validation is not visual acceptance."""
import json
import math
import sys
from pathlib import Path


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["manifest must be an object"]
    if data.get("schema") != 2:
        errors.append("schema must be 2; legacy contracts need editable selectors and evidence")
    if data.get("mode") != "layered_rebuild":
        errors.append("only layered_rebuild satisfies editable HTML delivery")
    ref = data.get("reference", {})
    if not isinstance(ref, dict):
        ref = {}
    if not ref.get("path"):
        errors.append("reference.path required")
    for key in ("width", "height"):
        if type(ref.get(key)) != int or ref[key] <= 0:
            errors.append("reference." + key + " must be a positive integer")
    layers = data.get("layers")
    if not isinstance(layers, list) or not layers:
        return errors + ["layers must be a nonempty list"]
    seen, selectors = set(), set()
    for layer in layers:
        if not isinstance(layer, dict):
            errors.append("layer must be an object")
            continue
        name = layer.get("id")
        if not isinstance(name, str) or not name or name in seen:
            errors.append("layer id must be a unique nonempty string")
        else:
            seen.add(name)
        selector = layer.get("selector")
        if not isinstance(selector, str) or not selector or selector in selectors:
            errors.append(str(name) + ": unique selector required")
        else:
            selectors.add(selector)
        if type(layer.get("z")) != int:
            errors.append(str(name) + ": integer z required")
        bounds = layer.get("bounds", {})
        if not isinstance(bounds, dict) or any(not number(bounds.get(k)) for k in ("x", "y", "width", "height")):
            errors.append(str(name) + ": numeric bounds required")
        elif bounds["width"] <= 0 or bounds["height"] <= 0:
            errors.append(str(name) + ": bounds must have positive size")
        if layer.get("type") not in {"text", "button", "control", "svg", "svg-path", "css-shape", "raster", "group"}:
            errors.append(str(name) + ": unsupported type (flattened UI/hotspots are not accepted)")
        if "visualRole" in layer and layer["visualRole"] not in {"panel", "icon"}:
            errors.append(str(name) + ": visualRole must be panel or icon")
        if layer.get("type") == "raster" and layer.get("role") not in {"subject", "photo", "decoration", "logo"}:
            errors.append(str(name) + ": raster role must be subject/photo/decoration/logo")
        if "flattenedAsset" in layer:
            errors.append(str(name) + ": flattened UI is forbidden")
        if layer.get("type") == "text":
            if not isinstance(layer.get("text"), str) or not layer["text"].strip():
                errors.append(str(name) + ": visible text required")
            typo = layer.get("typography", {})
            if not isinstance(typo, dict):
                typo = {}
            for key in ("fontFamily", "fallback", "color", "align", "wrap", "locale", "confidence"):
                if key not in typo:
                    errors.append(str(name) + ": typography." + key + " required")
            for key in ("weight", "fontSize", "lineHeight", "letterSpacing", "baseline", "opacity"):
                if not number(typo.get(key)):
                    errors.append(str(name) + ": numeric typography." + key + " required")
        if layer.get("type") in {"button", "control"}:
            action = layer.get("interaction", {})
            if not isinstance(action, dict) or not all(action.get(k) for k in ("event", "label", "visibleOutcome")):
                errors.append(str(name) + ": event, label and visibleOutcome required")
        if layer.get("type") == "control":
            control = layer.get("control", {})
            if not isinstance(control, dict) or control.get("tag") not in {"input", "textarea", "select"}:
                errors.append(str(name) + ": native control tag required")
            elif not isinstance(control.get("value"), str) or any(type(control.get(key)) is not bool for key in ("disabled", "readOnly")):
                errors.append(str(name) + ": control value and boolean disabled/readOnly required")
            elif control["tag"] == "input" and (not control.get("inputType") or control["inputType"] == "hidden"):
                errors.append(str(name) + ": visible inputType required")
    return errors


def main():
    try:
        errors = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    except (IndexError, OSError, ValueError) as exc:
        print("manifest invalid: " + str(exc), file=sys.stderr)
        return 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Layer structure valid; visual acceptance is a separate gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
