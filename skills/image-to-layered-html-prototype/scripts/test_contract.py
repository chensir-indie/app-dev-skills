#!/usr/bin/env python3
"""Regression tests for the layered prototype validation failures."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from validate_manifest import validate
from validate_prototype import check, sha, metrics, edge_disagreement, FILES, local
from diagnose_visual import diagnose
from compare_iteration import compare
from validate_batch import next_step, validate_batch
from triage_batch import triage_batch

SCRIPT = Path(__file__).parent

def manifest():
    return {"schema":2,"mode":"layered_rebuild",
      "reference":{"path":"reference.png","width":10,"height":10},
      "layers":[{"id":"label","selector":"#label","type":"text","z":1,
        "bounds":{"x":0,"y":0,"width":10,"height":10},"text":"Care",
        "referenceBounds":{"x":0,"y":0,"width":10,"height":10},
        "referenceInkBounds":{"x":1,"y":1,"width":8,"height":8},
        "referenceInkMethod":"apple-vision-ocr",
        "referenceInkEvidence":"ink.json",
        "typography":{"fontFamily":"sans-serif","fallback":["sans-serif"],
          "weight":400,"fontSize":8,"lineHeight":10,"letterSpacing":0,
          "baseline":8,"opacity":1,"color":"#000000","align":"left",
          "wrap":"nowrap","locale":"en","confidence":"measured"}}]}

def fixture(root):
    # Synthetic contract fixture only; not represented as a real browser render.
    for name in FILES:
        (root/name).write_text("[]" if name.endswith(".json") else "fixture")
    (root/"render-config.json").write_text("{}")
    (root/"index.html").write_text('<main data-artboard><span id="label">Care</span></main>')
    Image.new("RGB",(10,10),"white").save(root/"reference.png")
    Image.new("RGB",(10,10),"white").save(root/"native.png")
    Image.new("RGB",(10,10),"black").save(root/"changed.png")
    data=manifest()
    data["reference"]["sha256"]=sha(root/"reference.png")
    (root/"ink.json").write_text(json.dumps({"schema":1,"sha256":data["reference"]["sha256"],
      "width":10,"height":10,"observations":[{"text":"Care",
      "bounds":{"x":1,"y":1,"width":8,"height":8}}]}))
    (root/"layer-manifest.json").write_text(json.dumps(data))
    (root/"state-matrix.json").write_text('[{"id":"home"}]')
    policy={"maxMAE":0,"maxChangedPixelRatio":0,"channelThreshold":0,"geometryPx":0}
    regions=[{"id":"label","role":"typography","box":[0,0,10,10],"maxMAE":0,
              "maxChangedPixelRatio":0,"maxEdgeDisagreementRatio":0}]
    (root/"design-tokens.json").write_text(json.dumps({"fidelityProfile":"one_to_one","validationLimits":{"home":policy},"validationRegions":{"home":regions}}))
    audit={"fontsReady":True,"imagesReady":True,"layers":[{
      "id":"label","count":1,"visible":True,"tag":"span","text":"Care",
      "bounds":data["layers"][0]["bounds"],"textRects":[{"width":10}],
      "centerUncovered":True,"opacity":1,"style":{"fontFamily":"sans-serif","color":"rgb(0, 0, 0)","fontSize":"8px","lineHeight":"10px","letterSpacing":"0px","fontWeight":"400"}}],"media":[],"backgrounds":[]}
    audit.update({"url":(root/"index.html").as_uri(),"viewport":{"width":10,"height":10},
                  "dpr":1,"unlistedText":[],"unlistedControls":[]})
    (root/"dom.json").write_text(json.dumps(audit))
    proof={"before":"native.png","after":"changed.png","passed":True,"observation":"synthetic test fixture"}
    capture={"schema":1,"browserVersion":"synthetic-fixture","url":audit["url"],
             "viewport":audit["viewport"],"dpr":1,"screenshot":"native.png",
             "screenshotSha256":sha(root/"native.png"),"dom":"dom.json",
             "domSha256":sha(root/"dom.json"),
             "sources":{"index.html":sha(root/"index.html"),"layer-manifest.json":sha(root/"layer-manifest.json")}}
    (root/"capture.json").write_text(json.dumps(capture))
    state={"id":"home","screenshot":"native.png","dom":"dom.json","capture":"capture.json","limits":policy,
      "regions":regions,
      "proofs":{k:proof.copy() for k in ("withoutImages","textEdited","layerToggle","interaction","responsive")}}
    accepted={"status":"passed","manualReview":{"status":"passed","states":[{
      "id":"home","reference":"reference.png","actual":"native.png",
      "checks":{name:{"status":"passed","observation":"Synthetic fixture visually matches the white reference"}
                for name in ("assetIdentity","background","typography","contours",
                             "layerOrder","controls")}}]},"unresolved":[],
      "states":[state],"artifacts":[{"path":n,"sha256":sha(root/n)} for n in
      ("index.html","layer-manifest.json","design-tokens.json","render-config.json",
       "asset-manifest.json","state-matrix.json","native.png","changed.png","dom.json","capture.json","ink.json")]}
    (root/"acceptance.json").write_text(json.dumps(accepted))
    return data,audit,accepted

class ContractTests(unittest.TestCase):
    def test_batch_cannot_pass_when_expected_page_is_missing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / '01-page'
            page.mkdir()
            fixture(page)
            report = validate_batch(root, expected_pages=['01-page', '02-page'])
            self.assertEqual(report['pageCount'], 2)
            self.assertEqual(report['status'], 'pending')
            missing = next(item for item in report['pages'] if item['id'] == '02-page')
            self.assertEqual(missing['stage'], 'missing')
            self.assertIn('index.html', missing['errors'][0])

    def test_batch_cannot_hide_reference_page_by_omitting_it_from_list(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / '01-page').mkdir()
            (root / '01-page' / 'index.html').write_text('<main></main>')
            (root / '02-page' / 'reference').mkdir(parents=True)
            Image.new('RGB', (4, 4), 'white').save(root / '02-page/reference/source.png')
            report = validate_batch(root, expected_pages=['01-page'])
            self.assertEqual(report['status'], 'pending')
            self.assertEqual(report['unlistedReferencePages'], ['02-page'])

    def test_triage_reports_all_missing_contracts_and_visual_gap(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / '01-page'
            (page / 'reference').mkdir(parents=True)
            (page / 'evidence').mkdir()
            (page / 'index.html').write_text('<main>Hello</main>')
            Image.new('RGB', (16, 16), 'white').save(page / 'reference/source.png')
            Image.new('RGB', (16, 16), 'black').save(page / 'evidence/native.png')
            report = triage_batch(root, expected_pages=['01-page', '02-page'])
            first = report['pages'][0]
            self.assertEqual(first['id'], '01-page')
            self.assertEqual(first['visual']['mae'], 255)
            self.assertIn('design-tokens.json', first['missingArtifacts'])
            self.assertIn('layer-manifest.json', first['missingArtifacts'])
            self.assertEqual(report['pages'][1]['stage'], 'missing')
            self.assertEqual(report['strictPassedCount'], 0)
            self.assertEqual(report['nextAcceptanceCandidate']['id'], '01-page')

    def test_triage_finishes_partially_contractual_page_before_more_drafts(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name, missing in [('01-many-gaps', True), ('02-contract-started', False)]:
                page = root / name
                (page / 'reference').mkdir(parents=True)
                (page / 'evidence').mkdir()
                (page / 'index.html').write_text('<main>draft</main>')
                Image.new('RGB', (16, 16), 'white').save(page / 'reference/source.png')
                Image.new('RGB', (16, 16), 'black').save(page / 'evidence/native.png')
                if not missing:
                    for artifact in FILES:
                        (page / artifact).write_text('{}' if artifact.endswith('.json') else 'draft')
            report = triage_batch(root, expected_pages=['01-many-gaps', '02-contract-started'])
            self.assertEqual(report['nextAcceptanceCandidate']['id'], '02-contract-started')
            self.assertLess(len(report['nextAcceptanceCandidate']['missingArtifacts']),
                            len(report['pages'][0]['missingArtifacts']))

    def test_declared_sibling_shared_runtime_is_local_and_other_pages_are_not(self):
        with tempfile.TemporaryDirectory() as folder:
            suite = Path(folder)
            page = suite / "01-page"
            shared = suite / "shared"
            other = suite / "02-page"
            for directory in (page, shared, other):
                directory.mkdir()
            (page / "render-config.json").write_text('{"sharedRuntimeDirs":["../shared"]}')
            (shared / "styles.css").write_text("body{}")
            (other / "private.css").write_text("body{}")
            self.assertEqual(local(page, "../shared/styles.css"), (shared / "styles.css").resolve())
            with self.assertRaisesRegex(ValueError, "nonlocal"):
                local(page, "../02-page/private.css")

    def test_structure_gate_accepts_hashed_shared_asset(self):
        with tempfile.TemporaryDirectory() as folder:
            suite = Path(folder)
            page = suite / "01-page"
            shared = suite / "shared"
            page.mkdir()
            shared.mkdir()
            fixture(page)
            (page / "render-config.json").write_text('{"sharedRuntimeDirs":["../shared"]}')
            Image.new("RGB", (6, 6), "green").save(shared / "plant.png")
            (page / "asset-manifest.json").write_text(json.dumps([{
                "source": "../shared/plant.png", "sha256": sha(shared / "plant.png"),
                "role": "photo"
            }]))
            self.assertEqual(check(page, structure_only=True), [])

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.data,self.audit,self.accepted=fixture(self.root)
    def tearDown(self):
        self.temp.cleanup()
    def write(self,name,data):
        (self.root/name).write_text(json.dumps(data))
    def native_control_fixture(self, tag='input', value='Monstera'):
        control={"id":"name","selector":"#name","type":"control","z":2,
          "bounds":{"x":0,"y":0,"width":10,"height":10},
          "referenceBounds":{"x":0,"y":0,"width":10,"height":10},
          "interaction":{"event":"input","label":"Plant name","visibleOutcome":"Visible field value changes"},
          "control":{"tag":tag,"value":value,"disabled":False,"readOnly":False}}
        if tag=='input': control['control']['inputType']='text'
        self.data['layers'].append(control)
        self.audit['layers'].append({"id":"name","count":1,"visible":True,"tag":tag,
          "bounds":control['bounds'],"centerUncovered":True,"value":value,"inputType":"text",
          "disabled":False,"readOnly":False})
        region={"id":"name-control","role":"controls","box":[0,0,10,10],
          "maxMAE":0,"maxChangedPixelRatio":0,"maxEdgeDisagreementRatio":0}
        self.accepted['states'][0]['regions'].append(region)
        tokens=json.loads((self.root/'design-tokens.json').read_text())
        tokens['validationRegions']['home']=self.accepted['states'][0]['regions']
        self.write('design-tokens.json',tokens)
        self.write('layer-manifest.json',self.data)
        self.write('dom.json',self.audit)
        capture=json.loads((self.root/'capture.json').read_text())
        capture['sources']['layer-manifest.json']=sha(self.root/'layer-manifest.json')
        capture['domSha256']=sha(self.root/'dom.json')
        self.write('capture.json',capture)
        for artifact in self.accepted['artifacts']:
            artifact['sha256']=sha(self.root/artifact['path'])
        self.write('acceptance.json',self.accepted)
        return control
    def test_native_input_textarea_select_contract_passes(self):
        for tag in ['input','textarea','select']:
            with self.subTest(tag=tag):
                self.data,self.audit,self.accepted=fixture(self.root)
                self.native_control_fixture(tag)
                self.assertEqual(check(self.root),[])
    def test_native_control_wrong_value_rejected(self):
        self.native_control_fixture()
        self.audit['layers'][-1]['value']='Different visible name'
        self.write('dom.json',self.audit)
        self.assertTrue(any('control value differs' in e for e in check(self.root)))
    def test_native_control_fake_div_hidden_and_readonly_rejected(self):
        for field,value,expected in [('tag','div','native semantic'),('inputType','hidden','native semantic'),('readOnly',True,'control state differs'),('centerUncovered',False,'native semantic')]:
            with self.subTest(field=field):
                self.data,self.audit,self.accepted=fixture(self.root)
                self.native_control_fixture()
                self.audit['layers'][-1][field]=value
                self.write('dom.json',self.audit)
                self.assertTrue(any(expected in e for e in check(self.root)))
    def test_native_control_needs_reference_geometry(self):
        control=self.native_control_fixture()
        control.pop('referenceBounds')
        self.write('layer-manifest.json',self.data)
        self.assertTrue(any('reference geometry missing' in e for e in check(self.root)))
    def test_complete_synthetic_contract_passes(self):
        self.assertEqual(check(self.root),[])
    def test_bare_manual_review_claim_rejected(self):
        self.accepted["manualReview"]="passed"
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("manual review record" in e for e in check(self.root)))
    def test_manual_review_must_cover_every_visual_category(self):
        self.accepted["manualReview"]["states"][0]["checks"].pop("layerOrder")
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("manual review missing: home.layerOrder" in e for e in check(self.root)))
    def test_manual_review_must_match_browser_evidence(self):
        self.accepted["manualReview"]["states"][0]["actual"]="changed.png"
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("manual review screenshot mismatch: home" in e for e in check(self.root)))
    def test_manual_review_cannot_pass_with_pending_contour(self):
        self.accepted["manualReview"]["states"][0]["checks"]["contours"]["status"]="pending"
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("manual review not passed: home.contours" in e for e in check(self.root)))
    def test_flat_image_mode_rejected(self):
        self.data["mode"]="pixel_locked"
        self.assertTrue(validate(self.data))
    def test_mislabeled_flattened_layer_rejected(self):
        self.data["layers"][0]["type"]="flattened-asset"
        self.assertTrue(validate(self.data))
    def test_unknown_visual_role_rejected(self):
        self.data["layers"][0]["visualRole"]="approximate-panel"
        self.assertTrue(any("visualRole" in e for e in validate(self.data)))
    def test_hidden_text_rejected(self):
        self.audit["layers"][0]["visible"]=False
        self.write("dom.json",self.audit)
        self.assertTrue(any("hidden" in e for e in check(self.root)))
    def test_wrong_geometry_rejected(self):
        self.audit["layers"][0]["bounds"]["x"]=7
        self.write("dom.json",self.audit)
        self.assertTrue(any("geometry" in e for e in check(self.root)))
    def test_reference_geometry_required_for_text(self):
        self.data["layers"][0].pop("referenceBounds")
        self.write("layer-manifest.json",self.data)
        self.assertTrue(any("reference geometry missing" in e for e in check(self.root)))
    def test_source_glyph_ink_is_separate_from_dom_line_box(self):
        self.data["layers"][0].pop("referenceInkBounds")
        self.write("layer-manifest.json",self.data)
        self.assertTrue(any("source glyph ink geometry missing" in e for e in check(self.root)))
    def test_source_ink_requires_independent_evidence(self):
        self.data["layers"][0].pop("referenceInkEvidence")
        self.write("layer-manifest.json",self.data)
        self.assertTrue(any("source ink evidence missing" in e for e in check(self.root)))
    def test_source_ink_rejects_wrong_source_hash(self):
        evidence=json.loads((self.root/"ink.json").read_text())
        evidence["sha256"]="0"*64
        self.write("ink.json",evidence)
        self.assertTrue(any("source ink evidence hash differs" in e for e in check(self.root)))
    def test_source_ink_rejects_unmeasured_box(self):
        self.data["layers"][0]["referenceInkBounds"]["x"]=4
        self.write("layer-manifest.json",self.data)
        self.assertTrue(any("source ink bounds not found" in e for e in check(self.root)))
    def test_self_consistent_dom_bounds_do_not_hide_reference_drift(self):
        self.data["layers"][0]["bounds"]["x"]=5
        self.audit["layers"][0]["bounds"]["x"]=5
        self.write("layer-manifest.json",self.data)
        self.write("dom.json",self.audit)
        self.assertTrue(any("reference geometry differs" in e for e in check(self.root)))
        self.assertEqual(next_step(['home: reference geometry differs: label'])[0], 'layers')
    def test_manifest_array_bounds_no_crash(self):
        self.data["layers"][0]["bounds"]=[0,0,10,10]
        self.assertTrue(validate(self.data))
    def test_files_without_acceptance_are_not_pass(self):
        (self.root/"acceptance.json").unlink()
        self.assertTrue(check(self.root))
        self.assertEqual(check(self.root,structure_only=True),[])
    def test_visible_difference_recomputed_not_trusted(self):
        Image.new("RGB",(10,10),"black").save(self.root/"native.png")
        self.assertTrue(any("visual limits" in e for e in check(self.root)))
    def test_roi_catches_local_defect(self):
        im=Image.new("RGB",(10,10),"white")
        im.putpixel((0,0),(0,0,0))
        im.save(self.root/"native.png")
        self.assertEqual(metrics(self.root/"reference.png",self.root/"native.png",[0,0,1,1]),(255,1))
    def test_roi_edge_limit_catches_contour_mismatch(self):
        regions=self.accepted["states"][0]["regions"]
        regions[0]["maxMAE"]=255
        regions[0]["maxChangedPixelRatio"]=1
        tokens=json.loads((self.root/"design-tokens.json").read_text())
        tokens["validationRegions"]["home"]=regions
        self.write("design-tokens.json",tokens)
        self.write("acceptance.json",self.accepted)
        im=Image.new("RGB",(10,10),"white")
        for y in range(3,7):
            for x in range(3,7):
                im.putpixel((x,y),(0,0,0))
        im.save(self.root/"native.png")
        self.assertTrue(any("ROI contour/edge failed" in e for e in check(self.root)))
    def test_contour_metric_is_normalized_by_edges_not_roi_area(self):
        reference=Image.new("RGB",(100,100),"white")
        actual=Image.new("RGB",(100,100),"white")
        for y in range(25,75):
            for x in range(25,75):
                reference.putpixel((x,y),(0,0,0))
                actual.putpixel((x+10,y),(0,0,0))
        reference.save(self.root/"edge-reference.png")
        actual.save(self.root/"edge-actual.png")
        self.assertGreater(edge_disagreement(self.root/"edge-reference.png",self.root/"edge-actual.png",[0,0,100,100]),.15)
    def test_fake_identical_proof_rejected(self):
        self.accepted["states"][0]["proofs"]["interaction"]["after"]="native.png"
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("identical proof" in e for e in check(self.root)))
    def test_stale_source_rejected(self):
        (self.root/"index.html").write_text("changed UI")
        self.assertTrue(any("stale artifact" in e for e in check(self.root)))
    def test_browser_normal_letter_spacing_means_zero(self):
        self.audit['layers'][0]['style']['letterSpacing']='normal'
        self.write('dom.json',self.audit)
        capture=json.loads((self.root/'capture.json').read_text())
        capture['domSha256']=sha(self.root/'dom.json')
        self.write('capture.json',capture)
        for artifact in self.accepted['artifacts']:
            artifact['sha256']=sha(self.root/artifact['path'])
        self.write('acceptance.json',self.accepted)
        self.assertEqual(check(self.root),[])
    def test_native_control_placeholder_mismatch_rejected(self):
        control=self.native_control_fixture()
        control['control']['placeholder']='Plant name'
        self.write('layer-manifest.json',self.data)
        self.audit['layers'][-1]['placeholder']='Wrong placeholder'
        self.write('dom.json',self.audit)
        self.assertTrue(any('control placeholder differs' in e for e in check(self.root)))
    def test_wrong_text_size_rejected(self):
        self.audit["layers"][0]["style"]["fontSize"]="20px"
        self.write("dom.json",self.audit)
        self.assertTrue(any("text metric differs" in e for e in check(self.root)))
    def test_wrong_text_color_rejected(self):
        self.audit["layers"][0]["style"]["color"]="rgb(255, 0, 0)"
        self.write("dom.json",self.audit)
        self.assertTrue(any("text color differs" in e for e in check(self.root)))
    def test_wrong_font_family_rejected(self):
        self.audit["layers"][0]["style"]["fontFamily"]="serif"
        self.write("dom.json",self.audit)
        self.assertTrue(any("font family differs" in e for e in check(self.root)))
    def test_unlisted_visible_text_rejected(self):
        self.audit["unlistedText"]=[{"text":"Forgotten label","x":2,"y":2}]
        self.write("dom.json",self.audit)
        self.assertTrue(any("unlisted visible text" in e for e in check(self.root)))
    def test_unlisted_visible_control_rejected(self):
        self.audit["unlistedControls"]=[{"tag":"button","text":"Skip"}]
        self.write("dom.json",self.audit)
        self.assertTrue(any("unlisted visible control" in e for e in check(self.root)))
    def test_absent_coverage_audit_rejected(self):
        self.audit.pop("unlistedText")
        self.write("dom.json",self.audit)
        self.assertTrue(any("DOM coverage audit missing" in e for e in check(self.root)))
    def test_wrong_source_url_rejected(self):
        self.audit["url"]=(self.root/"reference.png").as_uri()
        self.write("dom.json",self.audit)
        self.assertTrue(any("DOM audit URL" in e for e in check(self.root)))
    def test_wrong_capture_viewport_rejected(self):
        self.audit["viewport"]["width"]=20
        self.write("dom.json",self.audit)
        self.assertTrue(any("capture viewport" in e for e in check(self.root)))
    def test_stale_capture_source_rejected(self):
        capture=json.loads((self.root/"capture.json").read_text())
        capture["sources"]["index.html"]="0"*64
        self.write("capture.json",capture)
        self.assertTrue(any("capture source changed" in e for e in check(self.root)))
    def test_easy_blank_roi_cannot_replace_landmark_coverage(self):
        regions=[{"id":"blank","box":[0,0,2,10],"maxMAE":0,"maxChangedPixelRatio":0}]
        tokens=json.loads((self.root/"design-tokens.json").read_text())
        tokens["validationRegions"]["home"]=regions
        self.accepted["states"][0]["regions"]=regions
        self.write("design-tokens.json",tokens)
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("critical layer not covered" in e for e in check(self.root)))
    def test_insufficient_roi_coverage_rejected(self):
        regions=[{"id":"label","box":[4,4,6,6],"maxMAE":0,"maxChangedPixelRatio":0}]
        tokens=json.loads((self.root/"design-tokens.json").read_text())
        tokens["validationRegions"]["home"]=regions
        self.accepted["states"][0]["regions"]=regions
        self.write("design-tokens.json",tokens)
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("ROI coverage" in e for e in check(self.root)))
    def test_reference_renamed_as_asset_rejected(self):
        (self.root/"decoration.png").write_bytes((self.root/"reference.png").read_bytes())
        self.write("asset-manifest.json",[{"source":"decoration.png","sha256":sha(self.root/"decoration.png"),"role":"decoration"}])
        self.assertTrue(any("reference screenshot" in e for e in check(self.root)))
    def test_widening_limits_rejected(self):
        self.accepted["states"][0]["limits"]["maxMAE"]=100
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("frozen" in e for e in check(self.root)))
    def test_matching_lax_limits_still_fail_one_to_one_standard(self):
        tokens=json.loads((self.root/"design-tokens.json").read_text())
        tokens["validationLimits"]["home"].update({"maxMAE":255,"maxChangedPixelRatio":1,"channelThreshold":255,"geometryPx":50})
        self.accepted["states"][0]["limits"]=tokens["validationLimits"]["home"]
        self.write("design-tokens.json",tokens)
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("one-to-one ceiling" in e for e in check(self.root)))
    def test_moderately_wide_visual_limits_are_not_one_to_one(self):
        tokens=json.loads((self.root/"design-tokens.json").read_text())
        tokens["validationLimits"]["home"].update({"maxMAE":9,"maxChangedPixelRatio":.35})
        tokens["validationRegions"]["home"][0].update({"maxMAE":9,"maxChangedPixelRatio":.35})
        self.accepted["states"][0]["limits"]=tokens["validationLimits"]["home"]
        self.accepted["states"][0]["regions"]=tokens["validationRegions"]["home"]
        self.write("design-tokens.json",tokens)
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("one-to-one ceiling" in e for e in check(self.root)))
    def test_missing_fidelity_profile_fails_closed(self):
        tokens=json.loads((self.root/"design-tokens.json").read_text())
        tokens.pop("fidelityProfile")
        self.write("design-tokens.json",tokens)
        self.assertTrue(any("fidelity profile" in e for e in check(self.root)))
    def test_matching_lax_roi_limits_still_fail_one_to_one_standard(self):
        tokens=json.loads((self.root/"design-tokens.json").read_text())
        tokens["validationRegions"]["home"][0].update({
            "maxMAE":255,"maxChangedPixelRatio":1,"maxEdgeDisagreementRatio":1,
        })
        self.accepted["states"][0]["regions"]=tokens["validationRegions"]["home"]
        self.write("design-tokens.json",tokens)
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("one-to-one ceiling" in e for e in check(self.root)))
    def test_unclassified_roi_fails(self):
        tokens=json.loads((self.root/"design-tokens.json").read_text())
        tokens["validationRegions"]["home"][0].pop("role")
        self.accepted["states"][0]["regions"]=tokens["validationRegions"]["home"]
        self.write("design-tokens.json",tokens)
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("ROI role" in e for e in check(self.root)))
    def test_text_roi_cannot_be_replaced_by_background_roi(self):
        tokens=json.loads((self.root/"design-tokens.json").read_text())
        tokens["validationRegions"]["home"][0]["role"]="background"
        self.accepted["states"][0]["regions"]=tokens["validationRegions"]["home"]
        self.write("design-tokens.json",tokens)
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("required ROI role missing: typography" in e for e in check(self.root)))
    def test_typography_roi_must_cover_the_text_layer(self):
        tokens=json.loads((self.root/"design-tokens.json").read_text())
        tokens["validationRegions"]["home"]=[
            {"id":"background","role":"background","box":[0,0,10,10],"maxMAE":0,"maxChangedPixelRatio":0,"maxEdgeDisagreementRatio":0},
            {"id":"wrong-place","role":"typography","box":[0,0,1,1],"maxMAE":0,"maxChangedPixelRatio":0,"maxEdgeDisagreementRatio":0},
        ]
        self.accepted["states"][0]["regions"]=tokens["validationRegions"]["home"]
        self.write("design-tokens.json",tokens)
        self.write("acceptance.json",self.accepted)
        self.assertTrue(any("role ROI does not cover layer: label" in e for e in check(self.root)))
    def test_channel_ratio_is_not_pixel_ratio(self):
        im=Image.new("RGB",(10,10),"white")
        im.putpixel((0,0),(254,255,255))
        im.save(self.root/"native.png")
        result=subprocess.run([sys.executable,str(SCRIPT/"compare_screenshots.py"),
          str(self.root/"reference.png"),str(self.root/"native.png")],capture_output=True,text=True)
        report=json.loads(result.stdout)
        self.assertEqual(report["different_pixels"],1)
        self.assertEqual(report["different_pixel_ratio"],.01)
        self.assertAlmostEqual(report["different_channel_ratio"],.003333)
    def test_dimension_error_writes_report(self):
        Image.new("RGB",(2,2)).save(self.root/"native.png")
        result=subprocess.run([sys.executable,str(SCRIPT/"compare_screenshots.py"),
          str(self.root/"reference.png"),str(self.root/"native.png"),
          "--json-out",str(self.root/"diff.json")],capture_output=True,text=True)
        self.assertEqual(result.returncode,1)
        self.assertEqual(json.loads((self.root/"diff.json").read_text())["status"],"dimension_mismatch")
    def test_visual_diagnosis_ranks_failed_region_without_changing_limits(self):
        image=Image.new("RGB",(10,10),"white")
        for y in range(10):
            for x in range(5):
                image.putpixel((x,y),(0,0,0))
        image.save(self.root/"native.png")
        tokens=json.loads((self.root/"design-tokens.json").read_text())
        tokens["validationRegions"]["home"]=[
            {"id":"right","box":[5,0,10,10],"maxMAE":0,"maxChangedPixelRatio":0},
            {"id":"left","box":[0,0,5,10],"maxMAE":0,"maxChangedPixelRatio":0}]
        self.write("design-tokens.json",tokens)
        report,_,_=diagnose(self.root,tile_size=16)
        self.assertFalse(report["allRegionsPass"])
        self.assertEqual(report["regionsWorstFirst"][0]["id"],"left")
        self.assertEqual(report["regionsWorstFirst"][0]["mae"],255)
        self.assertEqual(report["regionsWorstFirst"][1]["mae"],0)
        self.assertEqual(tokens,json.loads((self.root/"design-tokens.json").read_text()))
    def test_visual_diagnosis_prioritizes_error_area(self):
        image=Image.new("RGB",(10,10),"white")
        for y in range(10):
            for x in range(5):
                image.putpixel((x,y),(155,155,155))
        image.putpixel((9,9),(0,0,0))
        image.save(self.root/"native.png")
        tokens=json.loads((self.root/"design-tokens.json").read_text())
        tokens["validationRegions"]["home"]= [
            {"id":"small","box":[9,9,10,10],"maxMAE":0,"maxChangedPixelRatio":0},
            {"id":"large","box":[0,0,5,10],"maxMAE":0,"maxChangedPixelRatio":0}]
        self.write("design-tokens.json",tokens)
        report,_,_=diagnose(self.root,tile_size=16)
        self.assertEqual(report["regionsWorstFirst"][0]["id"],"large")
        self.assertGreater(report["regionsWorstFirst"][0]["excessErrorMass"],
                           report["regionsWorstFirst"][1]["excessErrorMass"])
    def test_iteration_report_rewards_improvement_without_roi_regression(self):
        report=compare(self.root,"home","changed.png","native.png")
        self.assertTrue(report["fullImageImproved"])
        self.assertEqual(report["regressedRegions"],[])
        self.assertEqual(report["review"],"keep candidate")
        reverse=compare(self.root,"home","native.png","changed.png")
        self.assertEqual(reverse["review"],"inspect tradeoff or revert")
    def test_batch_gate_never_passes_when_any_page_is_pending(self):
        batch = self.root / 'batch'
        passed = batch / '01-passed'
        pending = batch / '02-pending'
        passed.mkdir(parents=True)
        pending.mkdir(parents=True)
        fixture(passed)
        fixture(pending)
        (pending / 'acceptance.json').unlink()
        report = validate_batch(batch)
        self.assertEqual(report['status'], 'pending')
        self.assertEqual((report['pageCount'], report['passedCount'], report['pendingCount']), (2, 1, 1))
        self.assertEqual(report['pages'][1]['status'], 'pending')
    def test_batch_gate_empty_directory_is_pending(self):
        batch = self.root / 'empty'
        batch.mkdir()
        report = validate_batch(batch)
        self.assertEqual(report['status'], 'pending')
        self.assertEqual(report['pageCount'], 0)
    def test_batch_reports_actionable_visual_stage(self):
        stage, action=next_step(['home: ROI contour/edge failed: hero-backplate'])
        self.assertEqual(stage,'visual')
        self.assertIn('ROI',action)

if __name__=="__main__":
    unittest.main()
