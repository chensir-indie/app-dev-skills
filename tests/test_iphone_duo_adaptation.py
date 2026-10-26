"""Workspace materialization must preserve rules, evidence and user-owned files."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/iphone-duo-adaptation"
DOCTOR = SKILL / "scripts/doctor.sh"
TOOL = SKILL / "scripts/workspace_rules.py"
spec = importlib.util.spec_from_file_location("duo_workspace_rules", TOOL)
rules = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rules)


def fixture_catalog():
    source = {"id": "apple-layout", "title": "Apple Layout", "url": "https://developer.apple.com/design/", "checked_at": "2026-10-23"}
    entries = []
    for rule_id, phase in (("layout-current", "layout_analysis"), ("html-complete", "html_prototype"),
                           ("native-config", "native_implementation")):
        entries.append({"id": rule_id, "title": "Rule " + rule_id, "kind": "apple_guidance",
                        "phases": [phase], "applies_when": "This phase is in scope.",
                        "statement": "Preserve hierarchy and state.", "workspace_action": "Record and implement a decision.",
                        "verification": "Inspect the actual artifact.", "source_ids": ["apple-layout"]})
    return {"schema_version": 1, "checked_at": "2026-10-23", "sources": [source], "rules": entries}


def fixture_project_convention(**changes):
    convention = {"id": "PROJECT-rich-message", "title": "Project rich-message layout",
                  "basis": "User project-rule review: preserve message semantics and reading anchors.",
                  "origin": "user_instruction", "applies_when": "The app renders rich messages.",
                  "phases": ["html_prototype"], "statement": "Define local rich-message wrapping and scrolling.",
                  "parent_rule_ids": ["html-complete"], "status": "pending", "reason": "",
                  "decision": "", "targets": [], "evidence": []}
    convention.update(changes)
    return convention


class DuoWorkspaceRulesTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.workspace = self.base / "workspace"
        self.workspace.mkdir()
        self.catalog = self.base / "catalog.json"
        self.catalog.write_text(json.dumps(fixture_catalog()), encoding="utf-8")
        self.directory = self.workspace / rules.DEFAULT_OUTPUT
        self.json_path = self.directory / "workspace-rules.json"
        self.md_path = self.directory / "workspace-rules.md"

    def run_tool(self, command, complete=False, output_dir=rules.DEFAULT_OUTPUT):
        return rules.run(command, self.workspace, output_dir, complete, self.catalog)

    def initialize(self):
        self.run_tool("init")
        return json.loads(self.json_path.read_text())

    def save(self, ledger):
        self.json_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def make_verified(self, binding):
        (self.workspace / "prototype.html").write_text("<button>Choose</button>", encoding="utf-8")
        (self.workspace / "browser-evidence.txt").write_text("Actual browser receipt fixture", encoding="utf-8")
        binding.update(status="verified", decision="Retain the selection across widths.",
                       targets=["prototype.html"], evidence=["browser-evidence.txt"])

    def test_init_copies_every_rule_source_and_creates_one_pending_binding_each(self):
        ledger = self.initialize()
        catalog, digest = rules.load_catalog(self.catalog)
        self.assertEqual(ledger["sources"], catalog["sources"])
        self.assertEqual(ledger["rules"], catalog["rules"])
        self.assertEqual(ledger["catalog_sha256"], digest)
        self.assertEqual({entry["rule_id"] for entry in ledger["bindings"]}, {entry["id"] for entry in catalog["rules"]})
        self.assertTrue(all(entry["status"] == "pending" for entry in ledger["bindings"]))
        self.assertEqual(ledger["project_conventions"], [])
        self.assertIn("pending=3", self.run_tool("check"))
        with self.assertRaises(rules.RuleError):
            self.run_tool("check", complete=True)

    def test_cli_is_self_contained_in_a_standalone_skill(self):
        standalone = self.base / "standalone"
        (standalone / "scripts").mkdir(parents=True)
        (standalone / "assets").mkdir()
        shutil.copy(TOOL, standalone / "scripts/workspace_rules.py")
        shutil.copy(self.catalog, standalone / "assets/official-rules.json")
        for command in ("init", "check"):
            result = subprocess.run([sys.executable, str(standalone / "scripts/workspace_rules.py"), command,
                                     "--workspace", str(self.workspace)], cwd=self.base,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_actual_bundled_catalog_loads_and_initializes_a_complete_pending_copy(self):
        catalog, digest = rules.load_catalog()
        rules.run("init", self.workspace)
        ledger = json.loads(self.json_path.read_text())
        self.assertEqual(ledger["catalog_sha256"], digest)
        self.assertEqual(ledger["rules"], catalog["rules"])
        self.assertEqual(ledger["sources"], catalog["sources"])
        self.assertEqual(len(ledger["bindings"]), len(catalog["rules"]))
        rules.run("check", self.workspace)

    def test_bundled_catalog_routes_mainstream_ios_frameworks(self):
        catalog, _ = rules.load_catalog()
        by_id = {rule["id"]: rule for rule in catalog["rules"]}
        for rule_id, field, marker in (
            ("FRAMEWORK-ROUTE-001", "statement", "SwiftUI"),
            ("FRAMEWORK-APPLE-001", "statement", "UIKit"),
            ("FRAMEWORK-RN-001", "statement", "React Native"),
            ("FRAMEWORK-WEB-001", "applies_when", "WKWebView"),
            ("FRAMEWORK-IMPL-001", "statement", "integration_test"),
        ):
            self.assertIn(marker, by_id[rule_id][field])
        self.assertEqual(by_id["FRAMEWORK-IMPL-001"]["phases"], ["native_implementation"])
        for rule in catalog["rules"]:
            if rule["kind"] == "flutter_contract":
                self.assertIn("Flutter", rule["applies_when"], rule["id"])

    def test_imx_example_can_be_adopted_explicitly_but_is_not_imported_by_init(self):
        rules.run("init", self.workspace)
        ledger = json.loads(self.json_path.read_text())
        self.assertEqual(ledger["project_conventions"], [])
        example = json.loads((SKILL / "assets/project-conventions.imx.example.json").read_text())
        ledger["project_conventions"] = example["project_conventions"]
        self.assertTrue(all(entry["status"] == "pending" for entry in ledger["project_conventions"]))
        self.save(ledger)
        rules.run("render", self.workspace)
        rules.run("check", self.workspace)
        self.assertIn("PROJECT-IMX-LAYOUT-SCOPE-001", self.md_path.read_text())

    def test_malformed_json_shapes_fail_cli_without_tracebacks_or_partial_output(self):
        standalone = self.base / "standalone"
        (standalone / "scripts").mkdir(parents=True)
        (standalone / "assets").mkdir()
        shutil.copy(TOOL, standalone / "scripts/workspace_rules.py")
        catalog_path = standalone / "assets/official-rules.json"
        for data in (None, [], {"schema_version": 1, "checked_at": "2026-10-23", "sources": [None]}):
            with self.subTest(catalog=data):
                catalog_path.write_text(json.dumps(data), encoding="utf-8")
                result = subprocess.run([sys.executable, str(standalone / "scripts/workspace_rules.py"), "init",
                                         "--workspace", str(self.workspace)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse(self.json_path.exists())
                self.assertFalse(self.md_path.exists())
        catalog_path.write_text(json.dumps(fixture_catalog()), encoding="utf-8")
        self.initialize()
        original_md = self.md_path.read_bytes()
        for data in (None, [], {"schema_version": True}):
            with self.subTest(ledger=data):
                self.json_path.write_text(json.dumps(data), encoding="utf-8")
                result = subprocess.run([sys.executable, str(standalone / "scripts/workspace_rules.py"), "render",
                                         "--workspace", str(self.workspace)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(original_md, self.md_path.read_bytes())

    def test_binding_omission_duplicate_and_unknown_are_rejected(self):
        original = self.initialize()
        mutations = [lambda data: data["bindings"].pop(),
                     lambda data: data["bindings"].append(copy.deepcopy(data["bindings"][0])),
                     lambda data: data["bindings"][0].update(rule_id="invented-rule")]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                ledger = copy.deepcopy(original)
                mutate(ledger)
                self.save(ledger)
                with self.assertRaises(rules.RuleError):
                    self.run_tool("check")

    def test_copied_rule_or_source_edits_cannot_weaken_the_catalog(self):
        original = self.initialize()
        for field in ("rules", "sources"):
            with self.subTest(field=field):
                ledger = copy.deepcopy(original)
                ledger[field][0]["title"] = "weakened local replacement"
                self.save(ledger)
                with self.assertRaises(rules.RuleError):
                    self.run_tool("render")

    def test_project_conventions_render_separately_with_attribution_and_counts(self):
        ledger = self.initialize()
        ledger["project_conventions"] = [fixture_project_convention()]
        ledger["reviewer_notes"] = {"draft": "Preserve independent user notes."}
        self.save(ledger)
        before = self.json_path.read_bytes()
        result = self.run_tool("render")
        self.assertEqual(before, self.json_path.read_bytes())
        rendered = self.md_path.read_text()
        self.assertIn("## General rules", rendered)
        self.assertIn("## Project conventions", rendered)
        self.assertLess(rendered.index("## General rules"), rendered.index("## Project conventions"))
        for value in ("PROJECT-rich-message", "Project rich-message layout", "user_instruction",
                      "User project-rule review", "html-complete"):
            self.assertIn(value, rendered)
        self.assertIn("general=3, project=1", result)
        self.assertIn("pending=4", self.run_tool("check"))

    def test_project_conventions_must_be_an_array_of_objects(self):
        original = self.initialize()
        for value in (None, {}, "ignored project", [None], ["ignored project"]):
            with self.subTest(project_conventions=value):
                ledger = copy.deepcopy(original)
                ledger["project_conventions"] = value
                self.save(ledger)
                with self.assertRaises(rules.RuleError):
                    self.run_tool("render")

    def test_project_ids_must_be_unique_prefixed_ascii_and_cannot_shadow_catalog(self):
        original = self.initialize()
        for value in ("rich-message", "PROJECT-", "PROJECT-\u4e2d\u6587", "PROJECT--rich", "PROJECT-rich message",
                      "layout-current", None):
            with self.subTest(project_id=value):
                ledger = copy.deepcopy(original)
                ledger["project_conventions"] = [fixture_project_convention(id=value)]
                self.save(ledger)
                with self.assertRaises(rules.RuleError):
                    self.run_tool("render")
        original["project_conventions"] = [fixture_project_convention(), fixture_project_convention()]
        self.save(original)
        with self.assertRaises(rules.RuleError):
            self.run_tool("render")

    def test_project_id_cannot_shadow_even_a_project_prefixed_canonical_id(self):
        catalog = fixture_catalog()
        catalog["rules"][0]["id"] = "PROJECT-canonical"
        self.catalog.write_text(json.dumps(catalog), encoding="utf-8")
        ledger = self.initialize()
        ledger["project_conventions"] = [fixture_project_convention(id="PROJECT-canonical")]
        self.save(ledger)
        with self.assertRaises(rules.RuleError):
            self.run_tool("render")

    def test_project_metadata_requires_local_basis_origin_and_canonical_parent_ids(self):
        original = self.initialize()
        cases = [{"basis": ""}, {"basis": None}, {"origin": "apple_guidance"},
                 {"origin": "official"}, {"title": ""}, {"applies_when": ""}, {"statement": ""},
                 {"phases": []}, {"phases": ["imaginary_phase"]},
                 {"parent_rule_ids": ["unknown-rule"]}, {"parent_rule_ids": ["PROJECT-rich-message"]},
                 {"parent_rule_ids": ["html-complete", "html-complete"]}]
        for changes in cases:
            with self.subTest(changes=changes):
                ledger = copy.deepcopy(original)
                ledger["project_conventions"] = [fixture_project_convention(**changes)]
                self.save(ledger)
                with self.assertRaises(rules.RuleError):
                    self.run_tool("render")
        for key in fixture_project_convention():
            with self.subTest(missing_field=key):
                ledger = copy.deepcopy(original)
                convention = fixture_project_convention()
                convention.pop(key)
                ledger["project_conventions"] = [convention]
                self.save(ledger)
                with self.assertRaises(rules.RuleError):
                    self.run_tool("render")

    def test_project_origins_and_all_canonical_parent_mappings_are_supported(self):
        original = self.initialize()
        for origin in ("user_instruction", "project_contract", "product_decision"):
            with self.subTest(origin=origin):
                ledger = copy.deepcopy(original)
                ledger["project_conventions"] = [fixture_project_convention(
                    origin=origin, parent_rule_ids=[rule["id"] for rule in ledger["rules"]])]
                self.save(ledger)
                self.run_tool("render")
                self.run_tool("check")
        ledger["project_conventions"][0]["parent_rule_ids"] = []
        self.save(ledger)
        self.run_tool("render")
        self.run_tool("check")

    def test_project_verified_requires_real_decision_targets_and_evidence(self):
        original = self.initialize()
        mutations = [lambda entry: entry.update(decision=""),
                     lambda entry: entry.update(targets=[]),
                     lambda entry: entry.update(targets=["absent.html"]),
                     lambda entry: entry.update(evidence=[]),
                     lambda entry: entry.update(evidence=["absent.txt"]),
                     lambda entry: entry.update(evidence=["docs"])]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                ledger = copy.deepcopy(original)
                convention = fixture_project_convention()
                self.make_verified(convention)
                mutate(convention)
                ledger["project_conventions"] = [convention]
                self.save(ledger)
                with self.assertRaises(rules.RuleError):
                    self.run_tool("render")

    def test_project_paths_stay_inside_workspace_in_every_status(self):
        original = self.initialize()
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "evidence.txt").write_text("outside", encoding="utf-8")
        (self.workspace / "escape").symlink_to(outside, target_is_directory=True)
        for status in ("pending", "implemented", "verified"):
            for key in ("targets", "evidence"):
                for path in ("../outside/evidence.txt", str(outside / "evidence.txt"),
                             "escape/evidence.txt", "C:\\outside\\file", "a/../prototype.html"):
                    with self.subTest(status=status, key=key, path=path):
                        ledger = copy.deepcopy(original)
                        convention = fixture_project_convention()
                        self.make_verified(convention)
                        convention.update(status=status, **{key: [path]})
                        ledger["project_conventions"] = [convention]
                        self.save(ledger)
                        with self.assertRaises(rules.RuleError):
                            self.run_tool("render")

    def test_project_noncompletion_statuses_require_a_reason(self):
        original = self.initialize()
        for status in ("not_applicable", "deferred", "blocked"):
            with self.subTest(status=status):
                ledger = copy.deepcopy(original)
                ledger["project_conventions"] = [fixture_project_convention(status=status)]
                self.save(ledger)
                with self.assertRaises(rules.RuleError):
                    self.run_tool("render")

    def test_complete_checks_projects_and_only_defers_native_only_projects(self):
        original = self.initialize()
        for binding in original["bindings"]:
            self.make_verified(binding)
        convention = fixture_project_convention()
        self.make_verified(convention)
        original["project_conventions"] = [convention]
        for changes in ({"status": "pending"}, {"status": "blocked", "reason": "Awaiting work."},
                        {"status": "implemented"}, {"status": "deferred", "reason": "Awaiting native work."}):
            with self.subTest(changes=changes):
                ledger = copy.deepcopy(original)
                ledger["project_conventions"][0].update(changes)
                self.save(ledger)
                self.run_tool("render")
                with self.assertRaises(rules.RuleError):
                    self.run_tool("check", complete=True)
        for changes in ({}, {"status": "not_applicable", "reason": "No rich messages in this product."},
                        {"status": "deferred", "reason": "Native work follows the HTML task.",
                         "phases": ["native_implementation"]}):
            with self.subTest(allowed_changes=changes):
                ledger = copy.deepcopy(original)
                ledger["project_conventions"][0].update(changes)
                self.save(ledger)
                self.run_tool("render")
                self.run_tool("check", complete=True)

    def test_old_ledger_without_project_conventions_remains_compatible_without_json_rewrite(self):
        ledger = self.initialize()
        ledger.pop("project_conventions", None)
        self.save(ledger)
        before = self.json_path.read_bytes()
        self.run_tool("render")
        self.assertEqual(before, self.json_path.read_bytes())
        self.assertIn("general=3, project=0", self.run_tool("check"))

    def test_catalog_byte_change_invalidates_old_ledger_without_overwriting_it(self):
        self.initialize()
        before = (self.json_path.read_bytes(), self.md_path.read_bytes())
        self.catalog.write_bytes(self.catalog.read_bytes() + b"\n")
        for command in ("render", "check"):
            with self.assertRaises(rules.RuleError):
                self.run_tool(command)
        self.assertEqual(before, (self.json_path.read_bytes(), self.md_path.read_bytes()))

    def test_json_edits_make_markdown_stale_and_render_preserves_all_json_data(self):
        ledger = self.initialize()
        ledger["bindings"][0]["decision"] = "Keep existing typography and route hierarchy."
        ledger["reviewer_notes"] = {"draft": "User-owned data remains untouched."}
        self.save(ledger)
        before = self.json_path.read_bytes()
        with self.assertRaises(rules.RuleError):
            self.run_tool("check")
        self.run_tool("render")
        self.assertEqual(before, self.json_path.read_bytes())
        self.run_tool("check")
        self.md_path.write_text(self.md_path.read_text() + "User edit\n", encoding="utf-8")
        with self.assertRaises(rules.RuleError):
            self.run_tool("check")

    def test_render_preserves_non_generated_markdown(self):
        self.initialize()
        self.md_path.write_text("# Personal notes\n", encoding="utf-8")
        with self.assertRaises(rules.RuleError):
            self.run_tool("render")
        self.assertEqual(self.md_path.read_text(), "# Personal notes\n")

    def test_init_never_clobbers_either_existing_output(self):
        self.directory.mkdir(parents=True)
        for existing, missing in ((self.json_path, self.md_path), (self.md_path, self.json_path)):
            with self.subTest(existing=existing.name):
                existing.write_text("user-owned", encoding="utf-8")
                with self.assertRaises(rules.RuleError):
                    self.run_tool("init")
                self.assertEqual(existing.read_text(), "user-owned")
                self.assertFalse(missing.exists())
                existing.unlink()

    def test_missing_ledger_never_changes_existing_markdown(self):
        self.directory.mkdir(parents=True)
        self.md_path.write_text("keep", encoding="utf-8")
        for command in ("render", "check"):
            with self.assertRaises(rules.RuleError):
                self.run_tool(command)
        self.assertEqual(self.md_path.read_text(), "keep")

    def test_interrupted_pair_creation_rolls_back_all_outputs_and_temporary_files(self):
        original_link = rules.os.link
        calls = []

        def fail_second(source, target):
            calls.append(target)
            if len(calls) == 2:
                raise OSError("Synthetic second publication failure")
            return original_link(source, target)

        with mock.patch.object(rules.os, "link", side_effect=fail_second):
            with self.assertRaises(OSError):
                self.run_tool("init")
        self.assertFalse(self.json_path.exists())
        self.assertFalse(self.md_path.exists())
        self.assertEqual(list(self.workspace.rglob(".workspace-rules-*")), [])

    def test_verified_needs_decision_target_and_real_evidence(self):
        original = self.initialize()
        mutations = [lambda binding: binding.update(decision=""),
                     lambda binding: binding.update(targets=[]),
                     lambda binding: binding.update(targets=["does-not-exist.html"]),
                     lambda binding: binding.update(evidence=[]),
                     lambda binding: binding.update(evidence=["does-not-exist.png"]),
                     lambda binding: binding.update(evidence=["docs"])]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                ledger = copy.deepcopy(original)
                self.make_verified(ledger["bindings"][0])
                mutate(ledger["bindings"][0])
                self.save(ledger)
                with self.assertRaises(rules.RuleError):
                    self.run_tool("render")

    def test_not_applicable_deferred_and_blocked_require_reason(self):
        original = self.initialize()
        for status in ("not_applicable", "deferred", "blocked"):
            with self.subTest(status=status):
                ledger = copy.deepcopy(original)
                ledger["bindings"][0]["status"] = status
                self.save(ledger)
                with self.assertRaises(rules.RuleError):
                    self.run_tool("check")

    def test_complete_allows_verified_reasoned_na_and_native_only_deferred(self):
        ledger = self.initialize()
        self.make_verified(ledger["bindings"][0])
        ledger["bindings"][1].update(status="not_applicable", reason="Explicit analysis-only user endpoint in this fixture.")
        ledger["bindings"][2].update(status="deferred", reason="Native implementation is outside the HTML design task.")
        self.save(ledger)
        self.run_tool("render")
        self.run_tool("check", complete=True)
        for index, status in ((0, "implemented"), (1, "blocked"), (1, "pending"), (1, "deferred")):
            with self.subTest(status=status):
                invalid = copy.deepcopy(ledger)
                invalid["bindings"][index].update(status=status, reason="Still awaiting this work.")
                self.save(invalid)
                self.run_tool("render")
                with self.assertRaises(rules.RuleError):
                    self.run_tool("check", complete=True)

    def test_all_binding_paths_must_stay_inside_workspace_even_while_pending(self):
        original = self.initialize()
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "evidence.txt").write_text("outside", encoding="utf-8")
        (self.workspace / "escape").symlink_to(outside, target_is_directory=True)
        for key in ("targets", "evidence"):
            for path in ("../outside/evidence.txt", str(outside / "evidence.txt"),
                         "escape/evidence.txt", "C:\\outside\\file", "a/../prototype.html"):
                with self.subTest(key=key, path=path):
                    ledger = copy.deepcopy(original)
                    ledger["bindings"][0][key] = [path]
                    self.save(ledger)
                    with self.assertRaises(rules.RuleError):
                        self.run_tool("render")

    def test_output_directory_cannot_escape_through_ancestors_or_symlinks(self):
        outside = self.base / "outside"
        outside.mkdir()
        (self.workspace / "docs").symlink_to(outside, target_is_directory=True)
        for command in ("init", "render", "check"):
            with self.subTest(command=command):
                with self.assertRaises(rules.RuleError):
                    self.run_tool(command)
        self.assertEqual(list(outside.iterdir()), [])
        for output_dir in ("../outside", str(outside), "C:/outside"):
            with self.assertRaises(rules.RuleError):
                self.run_tool("init", output_dir=output_dir)

    def test_output_file_symlink_does_not_touch_its_destination(self):
        self.directory.mkdir(parents=True)
        user_file = self.workspace / "user-file.md"
        user_file.write_text("preserve", encoding="utf-8")
        self.md_path.symlink_to(user_file)
        with self.assertRaises(rules.RuleError):
            self.run_tool("init")
        self.assertEqual(user_file.read_text(), "preserve")
        self.assertFalse(self.json_path.exists())

    def test_project_output_directory_override_works_across_all_commands(self):
        output_dir = ".scratch/duo"
        self.run_tool("init", output_dir=output_dir)
        self.run_tool("render", output_dir=output_dir)
        self.run_tool("check", output_dir=output_dir)
        self.assertTrue((self.workspace / output_dir / "workspace-rules.json").is_file())
        self.assertFalse(self.json_path.exists())

    def test_invalid_catalog_and_duplicate_json_keys_are_rejected(self):
        original = fixture_catalog()
        cases = []
        duplicate = copy.deepcopy(original)
        duplicate["rules"].append(copy.deepcopy(duplicate["rules"][0]))
        cases.append(duplicate)
        missing_source = copy.deepcopy(original)
        missing_source["rules"][0]["source_ids"] = ["unknown-source"]
        cases.append(missing_source)
        bad_phase = copy.deepcopy(original)
        bad_phase["rules"][0]["phases"] = ["invented-phase"]
        cases.append(bad_phase)
        for catalog in cases:
            self.catalog.write_text(json.dumps(catalog), encoding="utf-8")
            with self.assertRaises(rules.RuleError):
                self.run_tool("init")
        self.catalog.write_text('{"schema_version":1,"schema_version":1}', encoding="utf-8")
        with self.assertRaises(rules.RuleError):
            self.run_tool("init")
        self.assertFalse(self.json_path.exists())


class DuoPreflightTests(unittest.TestCase):
    def doctor(self, path, *arguments):
        return subprocess.run(["/bin/sh", str(DOCTOR), *arguments],
                              env={**os.environ, "PATH": path}, capture_output=True, text=True)

    def test_instructions_scope_needs_no_toolchain_or_collection(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "doctor.sh"
            shutil.copy(DOCTOR, target)
            result = subprocess.run(["/bin/sh", str(target), "--scope", "instructions"], cwd=directory,
                                    env={**os.environ, "PATH": ""}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_default_and_workspace_scope_fail_without_python(self):
        for arguments in ((), ("--scope", "workspace")):
            with self.subTest(arguments=arguments):
                result = self.doctor("", *arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("https://www.python.org/downloads/", result.stderr)

    def test_old_python_is_rejected_and_supported_fallback_is_used(self):
        with tempfile.TemporaryDirectory() as directory:
            old = Path(directory) / "python3"
            old.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
            old.chmod(0o755)
            self.assertNotEqual(self.doctor(directory).returncode, 0)
            supported = Path(directory) / "python"
            supported.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            supported.chmod(0o755)
            result = self.doctor(directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("available as python;", result.stdout)

    def test_unsupported_scope_or_arguments_fail(self):
        for arguments in (("--ios",), ("--scope", "unknown"), ("--scope", "instructions", "extra")):
            with self.subTest(arguments=arguments):
                self.assertNotEqual(self.doctor("", *arguments).returncode, 0)


if __name__ == "__main__":
    unittest.main()
