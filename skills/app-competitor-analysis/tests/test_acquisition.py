"""Acquisition must close the requested evidence gap, not merely fetch a page."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit_acquisition', ROOT / 'scripts/audit_acquisition.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def sample():
    return json.loads((ROOT / 'assets/acquisition.example.json').read_text())


class AcquisitionTests(unittest.TestCase):
    def test_malformed_shapes_return_specific_errors_without_cli_traceback(self):
        mutations = (
            ('document', lambda data: []),
            ('gaps', lambda data: {**data, 'gaps': None}),
            ('gaps', lambda data: {**data, 'gaps': [None]}),
            ('products', lambda data: {**data, 'products': [None]}),
            ('sources', lambda data: {**data, 'sources': [None]}),
            ('unknown source_product', lambda data: self.changed(data, 'sources', 'product_id', [])),
            ('kind', lambda data: self.changed(data, 'sources', 'kind', {})),
            ('unknown product_id', lambda data: self.changed(data, 'gaps', 'product_id', {})),
            ('invalid dimension', lambda data: self.changed(data, 'gaps', 'dimension', [])),
            ('invalid priority', lambda data: self.changed(data, 'gaps', 'priority', {})),
            ('invalid proof', lambda data: self.changed(data, 'gaps', 'proof', [])),
            ('invalid state', lambda data: self.changed(data, 'gaps', 'state', {})),
            ('source_ids', lambda data: self.changed(data, 'gaps', 'source_ids', [{}])),
            ('attempt source_ids', lambda data: self.changed_attempt(data, 'source_ids', None)),
            ('attempt source_ids', lambda data: self.changed_attempt(data, 'source_ids', [[]])),
            ('invalid attempt outcome', lambda data: self.changed_attempt(data, 'outcome', {})),
        )
        for expected, mutate in mutations:
            with self.subTest(expected=expected, mutate=mutate):
                data = mutate(sample())
                errors = audit.validate(data)
                self.assertTrue(any(expected in error for error in errors), errors)
                with tempfile.TemporaryDirectory() as folder:
                    ledger = Path(folder) / 'malformed.json'
                    ledger.write_text(json.dumps(data))
                    result = subprocess.run(
                        [sys.executable, str(ROOT / 'scripts/audit_acquisition.py'), str(ledger)],
                        capture_output=True, text=True, check=False,
                    )
                self.assertEqual(result.returncode, 1)
                self.assertNotIn('Traceback', result.stderr)
                output = json.loads(result.stdout)
                self.assertTrue(any(expected in error for error in output['errors']))
                self.assertIsNone(output['summary'])

    @staticmethod
    def changed(data, collection, field, value):
        data[collection][0][field] = value
        return data

    @staticmethod
    def changed_attempt(data, field, value):
        data['gaps'][0]['attempts'][0][field] = value
        return data

    def test_valid_partial_study_is_not_research_complete(self):
        data = sample()
        self.assertEqual(audit.validate(data), [])
        self.assertFalse(audit.summary(data)['research_complete'])

    def test_text_page_cannot_close_pixel_or_runtime_gap(self):
        for proof in ('pixels', 'behavior', 'implementation'):
            data = sample()
            data['gaps'][0]['proof'] = proof
            self.assertTrue(any('proof_kind' in e for e in audit.validate(data)))

    def test_resolution_needs_inspection_and_report_updates(self):
        for field in ('inspected', 'report_updates'):
            data = sample()
            if field == 'inspected':
                data['sources'][0]['inspected'] = False
            else:
                data['gaps'][0]['report_updates'] = []
            self.assertTrue(audit.validate(data))

    def test_found_link_without_source_cannot_resolve(self):
        data = sample()
        data['gaps'][0]['source_ids'] = []
        self.assertTrue(any('resolution_sources' in e for e in audit.validate(data)))

    def test_cross_product_evidence_is_rejected(self):
        data = sample()
        data['products'].append({'id':'other', 'identity':'example.other'})
        data['sources'][0]['product_id'] = 'other'
        self.assertTrue(any('source_product' in e for e in audit.validate(data)))

    def test_exact_version_is_required_when_gap_is_pinned(self):
        data = sample()
        data['gaps'][0]['target_version'] = '2.0'
        self.assertTrue(any('version' in e for e in audit.validate(data)))

    def test_blocked_requires_actual_attempt_and_resume_condition(self):
        for field in ('attempts', 'resume_condition'):
            data = sample()
            data['gaps'][1].update(state='blocked', reason='Device absent', resume_condition='A compatible device is available')
            data['gaps'][1]['attempts'] = [{'date':'2026-10-20','channel':'environment','locator':'Supplied device inventory','outcome':'unavailable','note':'No compatible hardware','source_ids':[]}]
            data['gaps'][1][field] = [] if field == 'attempts' else ''
            self.assertTrue(audit.validate(data))

    def test_open_core_gap_prevents_completion_even_if_optional_gap_is_closed(self):
        data = sample()
        self.assertEqual(audit.summary(data)['unresolved_core'], 1)
        self.assertEqual(audit.summary(data)['resolved'], 1)

    def test_out_of_scope_and_deferral_require_a_recorded_basis(self):
        for state in ('out_of_scope', 'deferred'):
            data = sample()
            data['gaps'][1].update(state=state, reason='', resume_condition='')
            self.assertTrue(audit.validate(data))

    def test_remaining_question_cannot_be_silently_marked_resolved(self):
        data = sample()
        data['gaps'][0]['remaining'] = 'Still cannot locate the saved result'
        self.assertTrue(any('remaining' in e for e in audit.validate(data)))

    def test_excluding_every_question_does_not_claim_completed_research(self):
        data = sample()
        for gap in data['gaps']:
            gap.update(state='out_of_scope', reason='User narrowed this task to another product')
        self.assertEqual(audit.validate(data), [])
        self.assertFalse(audit.summary(data)['research_complete'])

    def test_fully_answered_recorded_scope_can_complete(self):
        data = sample()
        source = copy.deepcopy(data['sources'][0])
        source.update(id='trace', kind='runtime', locator='original-fixture-export-record')
        data['sources'].append(source)
        gap = data['gaps'][1]
        gap.update(state='resolved', remaining='', resolution='The fictional trace preserves the complete test note.',
                   source_ids=['trace'], report_updates=['notes.html#interaction; export recovery'],
                   attempts=[{'date':'2026-10-20', 'channel':'runtime', 'locator':'original-fixture-export-record',
                              'outcome':'success', 'note':'Synthetic trace inspection', 'source_ids':['trace']}])
        self.assertEqual(audit.validate(data), [])
        self.assertTrue(audit.summary(data)['research_complete'])


if __name__ == '__main__':
    unittest.main()
