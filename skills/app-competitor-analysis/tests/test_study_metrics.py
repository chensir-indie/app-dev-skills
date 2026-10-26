"""Synthetic observations test arithmetic and exclusions, never competitor outcomes."""
import copy
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/study_metrics.py'


def fixture():
    return {
        'schema_version': 1, 'mode': 'synthetic', 'status': 'completed',
        'products': ['A', 'B'], 'participants': ['u1', 'u2', 'u3'],
        'protocol': {'population': 'Fictional note users', 'conditions': 'Same device and data scale',
                     'order_assignment': 'AB, BA, AB; exploratory only',
                     'analysis_unit': 'first_valid_attempt_per_participant_product_task'},
        'tasks': [{'id': 'find', 'start': 'Home', 'end': 'Correct note open', 'timeout_s': 90,
                   'moderator_help': 'After explicit request only', 'error_rule': 'Wrong note opened',
                   'exclusion_rule': 'Recording failure with reason; retain invalid row',
                   'timing': 'Silent task, start instruction end to correct note/stop/timeout'}],
        'attempts': [dict(participant_id=u, product_id=p, task_id='find', trial=1,
                          result='independent_success' if u != 'u3' else 'failure',
                          elapsed_s=t, errors=0, help_events=0, evidence=f'synthetic:{p}/{u}')
                     for p in ['A', 'B'] for u, t in [('u1', 20), ('u2', 40), ('u3', 90)]]
    }


class StudyMetricsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('study_metrics', SCRIPT)
        cls.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.m)

    def setUp(self):
        self.d = fixture()

    def fails(self, text):
        with self.assertRaisesRegex(ValueError, text):
            self.m.summarize(self.d)

    def test_success_median_and_all_attempt_median_differ(self):
        s = self.m.summarize(self.d)['summaries'][0]
        self.assertEqual(s['independent_success'], {'n': 2, 'N': 3})
        self.assertEqual(s['independent_success_time_s'], {'n': 2, 'median': 30})
        self.assertEqual(s['all_selected_time_s'], {'n': 3, 'median': 40})
        self.assertEqual(s['failure'], 1)

    def test_repeated_trial_is_not_another_participant(self):
        row = dict(self.d['attempts'][0], trial=2, elapsed_s=1)
        self.d['attempts'].insert(0, row)
        s = self.m.summarize(self.d)['summaries'][0]
        self.assertEqual(s['participants'], 3)
        self.assertEqual(s['additional_valid_trials'], 1)
        self.assertEqual(s['independent_success_time_s']['median'], 30)

    def test_invalid_does_not_erase_later_first_valid(self):
        row = dict(self.d['attempts'][0], trial=0, result='invalid', exclusion_reason='recording lost')
        self.d['attempts'].append(row)
        s = self.m.summarize(self.d)['summaries'][0]
        self.assertEqual(s['invalid_trials'], 1)
        self.assertEqual(s['selected_attempts'], 3)

    def test_technical_invalidation_can_retain_unknown_measurements(self):
        row = dict(self.d['attempts'][0], trial=0, result='invalid',
                   elapsed_s=None, errors=None, help_events=None,
                   exclusion_reason='Recording and timer failed before observation')
        self.d['attempts'].append(row)
        s = self.m.summarize(self.d)['summaries'][0]
        self.assertEqual(s['invalid_trials'], 1)
        self.assertEqual(s['independent_success'], {'n': 2, 'N': 3})
        self.assertEqual(s['all_selected_time_s']['median'], 40)

    def test_helped_success_stays_out_of_independent_rate(self):
        self.d['attempts'][0].update(result='helped_success', help_events=2, errors=3)
        s = self.m.summarize(self.d)['summaries'][0]
        self.assertEqual(s['independent_success'], {'n': 1, 'N': 3})
        self.assertEqual(s['helped_success'], 1)
        self.assertEqual(s['help'], {'events': 2, 'affected_participants': 1})
        self.assertEqual(s['errors'], {'events': 3, 'affected_participants': 1})

    def test_matched_participants_are_reported(self):
        self.d['attempts'].pop()
        out = self.m.summarize(self.d)
        self.assertEqual(out['matched_participants_by_task']['find'], ['u1', 'u2'])
        self.assertEqual(out['recorded_participants'], 3)
        self.assertEqual(out['recorded_trials'], 5)

    def test_planned_is_null_not_zero_percent(self):
        self.d.update(status='planned', participants=[], attempts=[])
        out = self.m.summarize(self.d)
        self.assertIsNone(out['summaries'])
        self.assertIsNone(out['matched_participants_by_task'])

    def test_no_success_has_null_median(self):
        for row in self.d['attempts']: row['result'] = 'failure'
        self.assertEqual(self.m.summarize(self.d)['summaries'][0]['independent_success_time_s'],
                         {'n': 0, 'median': None})

    def test_invalid_only_product_is_unmeasured(self):
        for row in self.d['attempts']:
            if row['product_id'] == 'A': row.update(result='invalid', exclusion_reason='device crash')
        s = self.m.summarize(self.d)['summaries'][0]
        self.assertEqual(s['independent_success'], {'n': 0, 'N': 0})
        self.assertEqual(s['invalid_trials'], 3)
        self.assertEqual(s['measurement_status'], 'no_valid_attempts')

    def test_planned_with_results_rejected(self):
        self.d['status'] = 'planned'; self.fails('planned')

    def test_completed_without_attempts_rejected(self):
        self.d['attempts'] = []; self.fails('completed')

    def test_unsupported_analysis_unit_rejected(self):
        self.d['protocol']['analysis_unit'] = 'treat_trials_as_people'; self.fails('analysis_unit')

    def test_duplicate_trial_rejected(self):
        self.d['attempts'].append(copy.deepcopy(self.d['attempts'][0])); self.fails('duplicate trial')

    def test_unknown_participant_rejected(self):
        self.d['attempts'][0]['participant_id'] = 'ghost'; self.fails('participant_id')

    def test_duplicate_product_rejected(self):
        self.d['products'].append('A'); self.fails('products')

    def test_false_independent_success_rejected(self):
        self.d['attempts'][0]['help_events'] = 1; self.fails('independent_success')

    def test_helped_without_help_rejected(self):
        self.d['attempts'][0]['result'] = 'helped_success'; self.fails('helped_success')

    def test_invalid_exclusion_requires_reason(self):
        self.d['attempts'][0]['result'] = 'invalid'; self.fails('exclusion_reason')

    def test_elapsed_over_timeout_rejected(self):
        self.d['attempts'][0]['elapsed_s'] = 91; self.fails('elapsed_s')

    def test_nan_duration_rejected(self):
        self.d['attempts'][0]['elapsed_s'] = float('nan'); self.fails('elapsed_s')

    def test_boolean_event_count_rejected(self):
        self.d['attempts'][0]['errors'] = True; self.fails('errors')

    def test_missing_evidence_rejected(self):
        self.d['attempts'][0]['evidence'] = ''; self.fails('evidence')

    def test_invalid_shapes_return_actionable_errors(self):
        for data in [None, [], {}, dict(self.d, tasks=[None]), dict(self.d, attempts=[None])]:
            with self.subTest(data=data), self.assertRaises(ValueError): self.m.summarize(data)


if __name__ == '__main__': unittest.main()
