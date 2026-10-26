"""Original synthetic fixtures; no competitor assets or private project paths."""
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/audit_evidence.py'
spec = importlib.util.spec_from_file_location('audit_evidence', SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def study():
    return {
        'schema_version': 1,
        'products': [{'id': 'notes', 'name': 'Example Notes', 'platform': 'ios',
                      'identity': 'store:example-notes', 'kind': 'app'}],
        'sources': [{'id': 'E1', 'product_id': 'notes', 'kind': 'runtime',
                     'locator': 'recording.mov#t=12', 'observed_at': '2026-10-20',
                     'version': '2.0', 'context': 'simulator, guest, offline; synthetic fixture'}],
        'claims': [{'id': 'C1', 'product_id': 'notes', 'dimension': 'interaction',
                    'status': 'observed', 'text': 'The draft remains after returning to the list.',
                    'source_ids': ['E1'], 'scope': 'One offline editing task', 'version': '2.0'}],
        'coverage': [{'product_id': 'notes', 'dimension': d,
                      'status': 'partial' if d == 'interaction' else 'missing',
                      'source_ids': ['E1'] if d == 'interaction' else [],
                      'reason': 'One observed task' if d == 'interaction' else 'Not inspected'}
                     for d in ['ui', 'interaction', 'technology', 'business']],
        'recommendations': [{'id': 'R1', 'text': 'Preserve interrupted drafts', 'basis_claim_ids': ['C1'],
                             'fit': 'Users switch tasks', 'tradeoff': 'Recovery state needs ownership',
                             'validation': 'Reopen an interrupted draft and compare text'}],
    }


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data = study()

    def fails(self, code):
        findings = audit.validate(self.data)
        self.assertTrue(any(code in e for e in findings), findings)

    def test_original_non_camera_case_passes(self):
        self.assertEqual(audit.validate(self.data), [])

    def test_duplicate_identity_fails_even_if_display_name_changes(self):
        p = dict(self.data['products'][0], id='renamed', name='New label')
        self.data['products'].append(p)
        self.fails('duplicate_identity')

    def test_same_name_different_identity_is_not_merged(self):
        p = dict(self.data['products'][0], id='other', identity='store:other')
        self.data['products'].append(p)
        self.data['coverage'] += [dict(c, product_id='other', status='missing', source_ids=[])
                                  for c in self.data['coverage'].copy()]
        self.assertEqual(audit.validate(self.data), [])

    def test_cross_product_source_cannot_support_claim(self):
        self.data['sources'][0]['product_id'] = 'other'
        self.fails('source_product')

    def test_marketing_is_not_runtime(self):
        self.data['sources'][0]['kind'] = 'official'
        self.fails('evidence_kind')

    def test_screenshot_supports_ui_but_not_interaction(self):
        self.data['sources'][0]['kind'] = 'screenshot'
        self.fails('evidence_kind')
        self.data['claims'][0]['dimension'] = 'ui'
        self.assertEqual(audit.validate(self.data), [])

    def test_concept_is_not_competitor_observation(self):
        self.data['sources'][0]['kind'] = 'concept'
        self.fails('evidence_kind')

    def test_package_static_claim_requires_hash_and_version(self):
        self.data['sources'][0]['kind'] = 'static'
        self.data['claims'][0]['status'] = 'static'
        self.fails('artifact_hash')
        self.data['sources'][0]['artifact_sha256'] = 'a' * 64
        self.assertEqual(audit.validate(self.data), [])
        self.data['claims'][0]['version'] = '3.0'
        self.fails('version_mismatch')

    def test_unknown_claim_version_cannot_hide_known_sample(self):
        self.data['claims'][0]['version'] = 'unknown'
        self.fails('version_mismatch')

    def test_secondary_note_is_reported_not_observed(self):
        self.data['sources'][0]['kind'] = 'research_note'
        self.fails('evidence_kind')
        self.data['claims'][0]['status'] = 'reported'
        self.assertEqual(audit.validate(self.data), [])

    def test_technical_inference_needs_alternative_and_test(self):
        c = self.data['claims'][0]
        c.update(status='inferred', dimension='technology')
        self.fails('inference_test')
        c.update(alternatives=['The service could store the draft remotely'],
                 verification='Compare offline edits and reconnection with consent')
        self.assertEqual(audit.validate(self.data), [])

    def test_unknown_can_have_no_source_but_still_has_scope(self):
        self.data['claims'][0].update(status='unknown', source_ids=[])
        self.assertEqual(audit.validate(self.data), [])

    def test_unknown_source_date_is_not_replaced_by_inspection_date(self):
        self.data['sources'][0].update(observed_at='unknown', inspected_at='2026-10-20',
                                      context='Undated supplied observer note, read on the inspection date')
        self.data['sources'][0]['kind'] = 'research_note'
        self.data['claims'][0]['status'] = 'reported'
        self.assertEqual(audit.validate(self.data), [])

    def test_malformed_date_is_still_rejected(self):
        self.data['sources'][0]['observed_at'] = '2026-99-99'
        self.fails('date')

    def test_missing_source_reference(self):
        self.data['claims'][0]['source_ids'] = ['absent']
        self.fails('unknown_source')

    def test_missing_dimension_is_visible(self):
        self.data['coverage'].pop()
        self.fails('coverage_missing')

    def test_fake_supported_coverage_has_no_source(self):
        self.data['coverage'][0]['status'] = 'supported'
        self.fails('coverage_sources')

    def test_missing_coverage_reason(self):
        self.data['coverage'][0]['reason'] = ''
        self.fails('required_text')

    def test_measurement_requires_runtime_and_method(self):
        self.data['claims'][0]['measurement'] = {'unit': 'ms', 'n': 1}
        self.fails('measurement')
        self.data['claims'][0]['measurement'].update(conditions='offline simulator', method='video timestamps')
        self.assertEqual(audit.validate(self.data), [])
        self.data['claims'][0]['status'] = 'declared'
        self.data['sources'][0]['kind'] = 'official'
        self.fails('measurement')

    def test_recommendation_requires_traceable_basis(self):
        self.data['recommendations'][0]['basis_claim_ids'] = ['missing']
        self.fails('recommendation_basis')

    def test_local_integrity_and_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'sample.txt'
            p.write_text('original fixture')
            self.data['sources'][0].update(local_path='sample.txt', sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            self.assertEqual(audit.validate(self.data, Path(d)), [])
            p.write_text('changed fixture')
            self.assertTrue(any('hash_mismatch' in e for e in audit.validate(self.data, Path(d))))
            p.unlink()
            self.assertTrue(any('local_file' in e for e in audit.validate(self.data, Path(d))))

    def test_invalid_shape_returns_diagnostics(self):
        for data in [None, [], {'schema_version': 1, 'products': 'wrong'},
                     dict(study(), claims=[None]), dict(study(), sources=[{'id': []}])]:
            with self.subTest(data=data):
                self.assertTrue(audit.validate(data))

    def test_cli_fails_for_invalid_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'broken.json'
            p.write_text('{')
            r = subprocess.run([sys.executable, str(SCRIPT), str(p)], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertNotIn('Traceback', r.stderr)

    def test_cli_valid_case(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'evidence.json'
            p.write_text(json.dumps(self.data))
            r = subprocess.run([sys.executable, str(SCRIPT), str(p)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn('not semantic verification', r.stdout)


if __name__ == '__main__':
    unittest.main()
