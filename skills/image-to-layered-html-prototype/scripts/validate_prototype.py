#!/usr/bin/env python3
"""Fail-closed editable-prototype gate. Requires observed browser evidence."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from urllib.parse import unquote, urlparse
from PIL import Image, ImageChops, ImageColor, ImageStat
from validate_manifest import validate, number
from visual_metrics import normalized_edge_disagreement
from measure_ink_core import measure as measure_ink_core

FILES = ("index.html", "design-tokens.json", "layer-manifest.json", "render-config.json",
         "state-matrix.json", "asset-manifest.json", "geometry-table.md",
         "typography-table.md", "interaction-map.md")
ONE_TO_ONE_CEILINGS = {
    "maxMAE": 8, "maxChangedPixelRatio": .30,
    "channelThreshold": 12, "geometryPx": 2,
}
ROI_CEILINGS = {
    "maxMAE": 8, "maxChangedPixelRatio": .30,
    "maxEdgeDisagreementRatio": .15,
}
ROI_ROLES = {"background", "subject", "panel", "typography", "controls", "icon", "decoration"}
MANUAL_REVIEW_CHECKS = ("assetIdentity", "background", "typography", "contours",
                        "layerOrder", "controls")


def manual_review_errors(review, states, checks, default_reference):
    """Require an explicit visual review of the exact captured state, not a flag."""
    if not isinstance(review, dict) or review.get("status") != "passed":
        return ["manual review record missing or not passed"]
    entries = review.get("states")
    if not isinstance(entries, list) or not all(isinstance(entry, dict) for entry in entries):
        return ["manual review states missing"]
    ids = [entry.get("id") for entry in entries]
    errors = []
    if len(ids) != len(set(ids)) or set(ids) != {state["id"] for state in states}:
        errors.append("manual review state coverage mismatch")
    by_id = {entry.get("id"): entry for entry in entries}
    evidence_by_id = {item["id"]: item for item in checks}
    for state in states:
        state_id = state["id"]
        entry = by_id.get(state_id)
        evidence = evidence_by_id.get(state_id)
        if not entry or not evidence:
            continue
        if entry.get("reference") != state.get("reference", default_reference):
            errors.append("manual review reference mismatch: " + state_id)
        if entry.get("actual") != evidence.get("screenshot"):
            errors.append("manual review screenshot mismatch: " + state_id)
        visual_checks = entry.get("checks")
        if not isinstance(visual_checks, dict):
            visual_checks = {}
        for category in MANUAL_REVIEW_CHECKS:
            finding = visual_checks.get(category)
            if not isinstance(finding, dict):
                errors.append(f"manual review missing: {state_id}.{category}")
            elif finding.get("status") != "passed":
                errors.append(f"manual review not passed: {state_id}.{category}")
            elif not isinstance(finding.get("observation"), str) or len(finding["observation"].strip()) < 12:
                errors.append(f"manual review observation missing: {state_id}.{category}")
    return errors


def layer_roi_roles(layer):
    roles = []
    if layer["type"] == "text":
        roles.append("typography")
    elif layer["type"] in {"button", "control"}:
        roles.append("controls")
    elif layer["type"] == "raster" and layer.get("role") in {"subject", "photo"}:
        roles.append("subject")
    if layer.get("visualRole") in {"panel", "icon"}:
        roles.append(layer["visualRole"])
    return roles


def reference_geometry_errors(layer, observed, tolerance):
    """Compare critical DOM boxes with independently measured reference boxes.

    The implementation bounds above are still useful for detecting a stale DOM
    audit, but they cannot establish fidelity when copied from that same DOM.
    """
    if layer["type"] not in {"text", "button", "control"} and layer.get("visualRole") not in {"panel", "icon"}:
        return []
    box = layer.get("referenceBounds")
    if layer["type"] == "text":
        ink = layer.get("referenceInkBounds")
        if not isinstance(ink, dict) or any(not number(ink.get(key)) for key in ("x", "y", "width", "height")):
            return ["source glyph ink geometry missing: " + layer["id"]]
        if ink["width"] <= 0 or ink["height"] <= 0:
            return ["source glyph ink geometry invalid: " + layer["id"]]
    if not isinstance(box, dict) or any(not number(box.get(key)) for key in ("x", "y", "width", "height")):
        return ["reference geometry missing: " + layer["id"]]
    if box["width"] <= 0 or box["height"] <= 0:
        return ["reference geometry invalid: " + layer["id"]]
    actual = observed.get("bounds", {})
    if any(not number(actual.get(key)) for key in box):
        return ["observed geometry missing: " + layer["id"]]
    if any(abs(actual[key] - box[key]) > tolerance for key in ("x", "y", "width", "height")):
        return ["reference geometry differs: " + layer["id"]]
    return []


def source_ink_evidence_errors(root, layer, reference):
    """Bind a text ink box to a measurement of the locked source image."""
    if layer["type"] != "text":
        return []
    method = layer.get("referenceInkMethod")
    evidence_path = layer.get("referenceInkEvidence")
    if method not in {"apple-vision-ocr", "high-contrast-pixel-core"} or not evidence_path:
        return ["source ink evidence missing: " + layer["id"]]
    try:
        evidence = read_json(local(root, evidence_path))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return ["source ink evidence missing: " + layer["id"]]
    if method == "high-contrast-pixel-core":
        entry = next((item.get("source") for item in evidence.get("layers", [])
                      if item.get("id") == layer["id"]), None)
        if not isinstance(entry, dict):
            return ["source ink measurement missing: " + layer["id"]]
    else:
        entry = evidence
    if entry.get("sha256") != sha(reference):
        return ["source ink evidence hash differs: " + layer["id"]]
    with Image.open(reference) as source_image:
        if (entry.get("width"), entry.get("height")) != source_image.size:
            return ["source ink evidence dimensions differ: " + layer["id"]]
    ink = layer.get("referenceInkBounds", {})
    if not isinstance(ink, dict) or any(not number(ink.get(key))
                                         for key in ("x", "y", "width", "height")):
        return ["source glyph ink geometry missing: " + layer["id"]]
    if method == "apple-vision-ocr":
        candidates = [item.get("bounds", {}) for item in entry.get("observations", [])]
        if not any(all(number(candidate.get(key)) and abs(candidate[key] - ink[key]) <= .02
                       for key in ("x", "y", "width", "height")) for candidate in candidates):
            return ["source ink bounds not found in OCR evidence: " + layer["id"]]
    else:
        roi = entry.get("roi")
        thresholds = entry.get("thresholds", {})
        try:
            measured = measure_ink_core(reference, roi, entry["mode"],
                                        [thresholds[key] for key in ("red", "green", "blue")])
        except (ValueError, KeyError, TypeError):
            return ["source ink measurement invalid: " + layer["id"]]
        if measured["bounds"] != entry.get("bounds") or measured["bounds"] != ink:
            return ["source ink bounds not found in pixel evidence: " + layer["id"]]
    return []


def role_roi_coverage(layer, role, regions, size):
    bounds = layer["bounds"]
    x1 = max(0, math.floor(bounds["x"]))
    y1 = max(0, math.floor(bounds["y"]))
    x2 = min(size[0], math.ceil(bounds["x"] + bounds["width"]))
    y2 = min(size[1], math.ceil(bounds["y"] + bounds["height"]))
    if x2 <= x1 or y2 <= y1:
        return 0
    mask = Image.new("1", size, 0)
    for region in regions:
        if region.get("role") == role:
            mask.paste(1, tuple(region["box"]))
    return mask.crop((x1, y1, x2, y2)).histogram()[1] / ((x2-x1) * (y2-y1))

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def local(root, name):
    if not isinstance(name, str) or not name:
        raise ValueError("nonempty artifact path required")
    path = (root / name).resolve()
    allowed = path.is_relative_to(root.resolve())
    if not allowed and (root / "render-config.json").is_file():
        config = read_json(root / "render-config.json")
        for entry in config.get("sharedRuntimeDirs", []):
            shared = (root / entry).resolve()
            if (entry.startswith("../") and shared.parent == root.parent.resolve()
                    and shared.name not in {"reference", "evidence"}
                    and path.is_relative_to(shared)):
                allowed = True
                break
    if not allowed or not path.is_file():
        raise ValueError("missing or nonlocal artifact: " + name)
    return path

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def font_list(value):
    return [part.strip().strip('"\'').lower() for part in str(value).split(',')]

def region_coverage(size, regions):
    mask = Image.new("1", size, 0)
    for region in regions:
        mask.paste(1, tuple(region["box"]))
    return mask.getbbox(), sum(mask.histogram()[1:]) / (size[0] * size[1])

def critical_layers_uncovered(manifest, regions, size):
    area = size[0] * size[1]
    missing = []
    for layer in manifest["layers"]:
        bounds = layer["bounds"]
        large = bounds["width"] * bounds["height"] >= area * .01
        if layer["type"] not in {"text", "button", "control"} and not large:
            continue
        cx = bounds["x"] + bounds["width"] / 2
        cy = bounds["y"] + bounds["height"] / 2
        if not any(x1 <= cx < x2 and y1 <= cy < y2 for x1,y1,x2,y2 in (r["box"] for r in regions)):
            missing.append(layer["id"])
    return missing

def metrics(ref_path, actual_path, box=None, threshold=0):
    with Image.open(ref_path) as r, Image.open(actual_path) as a:
        if r.size != a.size:
            raise ValueError("screenshot dimensions differ")
        ref, actual = r.convert("RGB"), a.convert("RGB")
        if box is not None:
            if (not isinstance(box, list) or len(box)!=4 or
                any(type(v)!=int for v in box) or
                not (0<=box[0]<box[2]<=r.width and 0<=box[1]<box[3]<=r.height)):
                raise ValueError("ROI must be a nonempty in-bounds [left,top,right,bottom]")
            ref,actual = ref.crop(box),actual.crop(box)
    diff = ImageChops.difference(ref,actual)
    mask = Image.new("L",diff.size,0)
    for band in diff.split():
        mask = ImageChops.lighter(mask,band.point(lambda v:255 if v>threshold else 0))
    return sum(ImageStat.Stat(diff).mean)/3, mask.histogram()[255]/(diff.width*diff.height)

def edge_disagreement(ref_path, actual_path, box):
    with Image.open(ref_path) as r, Image.open(actual_path) as a:
        return normalized_edge_disagreement(r, a, box)

def check(root, structure_only=False):
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    try:
        for name in FILES:
            local(root,name)
        manifest=read_json(root/"layer-manifest.json")
        errors.extend(validate(manifest))
        if errors:
            return errors
        reference=local(root,manifest["reference"]["path"])
        with Image.open(reference) as img:
            require(img.size==(manifest["reference"]["width"],manifest["reference"]["height"]),
                    "reference dimensions disagree with manifest")
        require(manifest["reference"].get("sha256")==sha(reference),"reference hash mismatch")
        for name in ("design-tokens.json","render-config.json","state-matrix.json","asset-manifest.json"):
            read_json(root/name)
        for asset in read_json(root/"asset-manifest.json"):
            path=local(root,asset["source"])
            require(sha(path)==asset["sha256"],"asset hash mismatch: "+asset["source"])
            require(sha(path)!=sha(reference),"reference screenshot cannot be a runtime asset")
            require(asset.get("role") in {"subject","photo","decoration","logo","font"},"invalid asset role")
        if structure_only:
            return errors

        acceptance=read_json(local(root,"acceptance.json"))
        tokens=read_json(root/"design-tokens.json")
        require(tokens.get("fidelityProfile")=="one_to_one",
                "one-to-one fidelity profile required for visual acceptance")
        frozen_limits=tokens.get("validationLimits",{})
        frozen_regions=tokens.get("validationRegions",{})
        require(acceptance.get("status")=="passed","acceptance is not passed")
        require(acceptance.get("unresolved")==[],"unresolved visual/behavior differences remain")
        states=read_json(root/"state-matrix.json")
        require(isinstance(states,list) and bool(states),"state matrix must be nonempty")
        checks=acceptance.get("states",[])
        require(len({s["id"] for s in checks})==len(checks),"duplicate acceptance states")
        require({s["id"] for s in checks}=={s["id"] for s in states},"state evidence coverage mismatch")
        errors.extend(manual_review_errors(acceptance.get("manualReview"), states, checks,
                                           manifest["reference"]["path"]))
        for state in checks:
            prefix=state["id"]+": "
            state_manifest=manifest
            if state.get("layerManifest"):
                state_manifest=read_json(local(root,state["layerManifest"]))
                errors.extend(validate(state_manifest))
            # Recompute against images; do not trust a hand-written diff JSON.
            actual=local(root,state["screenshot"])
            state_ref=local(root,state.get("reference",manifest["reference"]["path"]))
            policy=state["limits"]
            require(policy==frozen_limits.get(state["id"]),prefix+"limits differ from frozen design tokens")
            for key in ("maxMAE","maxChangedPixelRatio","channelThreshold","geometryPx"):
                require(number(policy.get(key)),prefix+"numeric limit required: "+key)
            if any(not number(policy.get(k)) for k in ("maxMAE","maxChangedPixelRatio","channelThreshold","geometryPx")):
                continue
            require(0<=policy["maxMAE"]<=255 and 0<=policy["maxChangedPixelRatio"]<=1 and
                    0<=policy["channelThreshold"]<=255 and policy["geometryPx"]>=0,prefix+"invalid limit range")
            for key, ceiling in ONE_TO_ONE_CEILINGS.items():
                require(policy[key] <= ceiling,
                        prefix+f"one-to-one ceiling exceeded: {key}={policy[key]} > {ceiling}")
            mae,ratio=metrics(state_ref,actual,threshold=policy["channelThreshold"])
            require(mae<=policy["maxMAE"] and ratio<=policy["maxChangedPixelRatio"],
                    prefix+f"full-screen visual limits exceeded: MAE {mae:.2f}/{policy['maxMAE']}, changed {ratio:.2%}/{policy['maxChangedPixelRatio']:.2%}")
            regions=state.get("regions",[])
            require(regions==frozen_regions.get(state["id"]),prefix+"ROI limits differ from frozen design tokens")
            require(bool(regions),prefix+"critical ROI evidence required")
            with Image.open(state_ref) as source_image:
                ref_size = source_image.size
            if regions:
                _, covered = region_coverage(ref_size, regions)
                require(covered >= .75,prefix+f"ROI coverage below 75% ({covered:.1%})")
                for layer_id in critical_layers_uncovered(state_manifest, regions, ref_size):
                    errors.append(prefix+"critical layer not covered by ROI: "+layer_id)
                roles={region.get("role") for region in regions}
                required={role for layer in state_manifest["layers"] for role in layer_roi_roles(layer)}
                for role in required-roles:
                    errors.append(prefix+"required ROI role missing: "+role)
                for layer in state_manifest["layers"]:
                    for role in layer_roi_roles(layer):
                        if role in roles and role_roi_coverage(layer, role, regions, ref_size) < .8:
                            errors.append(prefix+"role ROI does not cover layer: "+layer["id"]+" ("+role+")")
            for region in regions:
                require(region.get("role") in ROI_ROLES,
                        prefix+"ROI role missing or invalid: "+str(region.get("id")))
                for key, ceiling in ROI_CEILINGS.items():
                    require(number(region.get(key)) and 0 <= region[key] <= ceiling,
                            prefix+f"one-to-one ceiling exceeded: {region.get('id')}.{key}")
                mae,ratio=metrics(state_ref,actual,region["box"],policy["channelThreshold"])
                require(mae<=region["maxMAE"] and ratio<=region["maxChangedPixelRatio"],
                        prefix+f"ROI failed: {region['id']} (MAE {mae:.2f}/{region['maxMAE']}, changed {ratio:.2%}/{region['maxChangedPixelRatio']:.2%})")
                edge_limit=region.get("maxEdgeDisagreementRatio")
                require(number(edge_limit) and 0<=edge_limit<=1,prefix+"edge limit required: "+region["id"])
                if number(edge_limit):
                    require(edge_disagreement(state_ref,actual,region["box"])<=edge_limit,
                            prefix+"ROI contour/edge failed: "+region["id"])
            audit=read_json(local(root,state["dom"]))
            url=urlparse(audit.get("url", ""))
            require(url.scheme=="file" and Path(unquote(url.path)).resolve()==(root/"index.html").resolve(),
                    prefix+"DOM audit URL is not this prototype's index.html")
            require(audit.get("viewport")=={"width":ref_size[0],"height":ref_size[1]} and
                    audit.get("dpr")==1,prefix+"capture viewport/DPR differs from native reference")
            require(audit.get("fontsReady") is True and audit.get("imagesReady") is True,prefix+"fonts/images not ready")
            require(isinstance(audit.get("unlistedText"),list) and
                    isinstance(audit.get("unlistedControls"),list),prefix+"DOM coverage audit missing")
            for item in audit.get("unlistedText",[]):
                errors.append(prefix+"unlisted visible text: "+str(item.get("text","")))
            for item in audit.get("unlistedControls",[]):
                errors.append(prefix+"unlisted visible control: "+str(item.get("text","")))
            capture=read_json(local(root,state.get("capture")))
            require(capture.get("schema")==1,prefix+"capture provenance schema missing")
            require(capture.get("screenshot")==state["screenshot"] and
                    capture.get("screenshotSha256")==sha(actual),prefix+"capture screenshot changed")
            require(capture.get("dom")==state["dom"] and
                    capture.get("domSha256")==sha(local(root,state["dom"])),prefix+"capture DOM audit changed")
            require(capture.get("url")==audit.get("url") and
                    capture.get("viewport")==audit.get("viewport") and
                    capture.get("dpr")==audit.get("dpr") and
                    bool(capture.get("browserVersion")),prefix+"capture environment mismatch")
            sources=capture.get("sources",{})
            require(isinstance(sources,dict) and "index.html" in sources and
                    "layer-manifest.json" in sources,prefix+"capture source hashes missing")
            if isinstance(sources,dict):
                for source,digest in sources.items():
                    require(sha(local(root,source))==digest,prefix+"capture source changed: "+source)
            observed={l["id"]:l for l in audit["layers"]}
            for layer in state_manifest["layers"]:
                item=observed.get(layer["id"],{})
                require(item.get("count")==1 and item.get("visible") is True,prefix+"missing/hidden/duplicate layer: "+layer["id"])
                bounds=item.get("bounds",{})
                require(all(number(bounds.get(k)) and abs(bounds[k]-v)<=policy["geometryPx"] for k,v in layer["bounds"].items()),
                        prefix+"geometry differs: "+layer["id"])
                errors.extend(prefix + error for error in
                              reference_geometry_errors(layer, item, policy["geometryPx"]))
                if layer["type"]=="text":
                    errors.extend(prefix + error for error in
                                  source_ink_evidence_errors(root, layer, state_ref))
                    require(item.get("text")==layer["text"] and item.get("tag") not in {"img","canvas","image"} and
                            bool(item.get("textRects")) and item.get("centerUncovered") is True,
                            prefix+"text is not visible editable DOM: "+layer["id"])
                    style=item.get("style",{})
                    target=layer["typography"]
                    for css,key in (("fontSize","fontSize"),("lineHeight","lineHeight"),
                                    ("letterSpacing","letterSpacing"),("fontWeight","weight")):
                        value=style.get(css,"")
                        if css == "letterSpacing" and value == "normal":
                            value = "0px"
                        try:
                            observed_value=float(str(value).removesuffix("px"))
                            require(abs(observed_value-target[key])<=.1,prefix+"text metric differs: "+layer["id"]+"."+css)
                        except (ValueError,TypeError):
                            errors.append(prefix+"missing explicit text metric: "+layer["id"]+"."+css)
                    require(font_list(style.get("fontFamily")) == font_list(target["fontFamily"]),
                            prefix+"font family differs: "+layer["id"])
                    try:
                        require(ImageColor.getrgb(style.get("color", "")) == ImageColor.getrgb(target["color"]),
                                prefix+"text color differs: "+layer["id"])
                    except ValueError:
                        errors.append(prefix+"invalid text color: "+layer["id"])
                    require(number(item.get("opacity")) and abs(item["opacity"]-target["opacity"])<=.02,
                            prefix+"text opacity differs: "+layer["id"])
                if layer["type"]=="button":
                    require(item.get("tag") in {"button","a"} and item.get("centerUncovered") is True,
                            prefix+"control not visible semantic DOM: "+layer["id"])
                if layer["type"] == "control":
                    target = layer["control"]
                    require(item.get("tag") == target["tag"] and item.get("tag") in {"input", "textarea", "select"} and
                            item.get("centerUncovered") is True and item.get("inputType") != "hidden",
                            prefix + "control not visible native semantic DOM: " + layer["id"])
                    require(item.get("value") == target["value"], prefix + "control value differs: " + layer["id"])
                    if "placeholder" in target:
                        require(item.get("placeholder") == target["placeholder"], prefix + "control placeholder differs: " + layer["id"])
                    if target["tag"] == "input":
                        require(item.get("inputType") == target["inputType"], prefix + "control input type differs: " + layer["id"])
                    for flag in ("disabled", "readOnly"):
                        require(type(item.get(flag)) is bool and item[flag] == target[flag],
                                prefix + "control state differs: " + layer["id"] + "." + flag)
            for media in audit.get("media",[]):
                require(media.get("tag")!="canvas",prefix+"canvas UI forbidden")
                require(media.get("role") in {"subject","photo","decoration","logo"},prefix+"undeclared image role")
                require(media.get("areaRatio",0)<.8 or media.get("role")=="decoration",
                        prefix+"large image requires manual no-UI decoration review")
            for bg in audit.get("backgrounds",[]):
                require(bg.get("role")=="decoration",prefix+"unclassified CSS image background")
            for key in ("withoutImages","textEdited","layerToggle","interaction","responsive"):
                proof=state.get("proofs",{}).get(key,{})
                before=local(root,proof.get("before"))
                after=local(root,proof.get("after"))
                require(sha(before)!=sha(after),prefix+"identical proof pair: "+key)
                require(proof.get("passed") is True and bool(proof.get("observation")),prefix+"unreviewed proof: "+key)
        for entry in acceptance.get("artifacts",[]):
            require(sha(local(root,entry["path"]))==entry["sha256"],"stale artifact: "+entry["path"])
        required={"index.html","layer-manifest.json","design-tokens.json","render-config.json",
                  "asset-manifest.json","state-matrix.json"}
        required.update(p.relative_to(root).as_posix() for p in root.rglob("*")
                        if p.is_file() and p.suffix in {".css",".js",".svg",".woff",".woff2"})
        for entry in read_json(root/"render-config.json").get("sharedRuntimeDirs", []):
            shared = (root / entry).resolve()
            # Verify the directory through the same explicit sibling boundary as local().
            if not (entry.startswith("../") and shared.parent == root.parent.resolve()
                    and shared.name not in {"reference", "evidence"} and shared.is_dir()):
                raise ValueError("invalid shared runtime directory: " + entry)
            required.update(Path(os.path.relpath(p, root)).as_posix() for p in shared.rglob("*")
                            if p.is_file() and p.suffix in {".css",".js",".woff",".woff2"})
        required.update(s[k] for s in checks for k in ("screenshot","dom","capture"))
        required.update(s["layerManifest"] for s in checks if s.get("layerManifest"))
        required.update(layer["referenceInkEvidence"] for layer in manifest["layers"]
                        if layer["type"] == "text" and layer.get("referenceInkEvidence"))
        required.update(proof[k] for s in checks for proof in s.get("proofs",{}).values() for k in ("before","after"))
        covered={e["path"] for e in acceptance.get("artifacts",[])}
        require(required<=covered,"artifact hash coverage incomplete: "+str(sorted(required-covered)))
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
        errors.append("incomplete/invalid contract: "+str(exc))
    return errors

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("root",type=Path)
    parser.add_argument("--structure-only",action="store_true")
    args=parser.parse_args()
    errors=check(args.root.resolve(),args.structure_only)
    if errors:
        print("\n".join("FAIL: "+e for e in errors))
        return 1
    print("STRUCTURE ONLY; visual acceptance pending" if args.structure_only else
          "Evidence gate passed; manual review remains part of the recorded acceptance.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
