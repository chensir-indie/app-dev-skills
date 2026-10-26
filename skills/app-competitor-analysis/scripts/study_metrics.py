#!/usr/bin/env python3
"""Summarize first valid task attempts. Arithmetic checks are not research validation."""
import argparse
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(obj, key):
    require(isinstance(obj, dict) and isinstance(obj.get(key), str) and obj[key].strip(),
            f'{key}: nonempty text required')


def ids(data, key):
    values = data.get(key)
    require(isinstance(values, list) and all(isinstance(v, str) and v.strip() for v in values)
            and len(values) == len(set(values)), f'{key}: distinct text IDs required')
    return values


def duration(value):
    return type(value) in (float, int) and math.isfinite(value) and value >= 0


def times(rows):
    values = [r['elapsed_s'] for r in rows]
    return {'n': len(values), 'median': statistics.median(values) if values else None}


def summarize(data):
    require(isinstance(data, dict) and data.get('schema_version') == 1, 'schema_version: expected object v1')
    require(data.get('mode') in ('synthetic', 'user_study'), 'mode: synthetic or user_study required')
    require(data.get('status') in ('planned', 'completed'), 'status: planned or completed required')
    products, participants = ids(data, 'products'), ids(data, 'participants')
    require(products, 'products: at least one required')
    protocol = data.get('protocol')
    for key in ('population', 'conditions', 'order_assignment', 'analysis_unit'):
        nonempty(protocol, key)
    require(protocol['analysis_unit'] == 'first_valid_attempt_per_participant_product_task',
            'analysis_unit: helper supports first_valid_attempt_per_participant_product_task only')
    tasks = data.get('tasks')
    require(isinstance(tasks, list) and tasks, 'tasks: nonempty list required')
    task_map = {}
    for task in tasks:
        for key in ('id', 'start', 'end', 'moderator_help', 'error_rule', 'exclusion_rule', 'timing'):
            nonempty(task, key)
        require(task['id'] not in task_map, 'tasks: duplicate id')
        require(duration(task.get('timeout_s')) and task['timeout_s'] > 0, 'timeout_s: positive duration required')
        task_map[task['id']] = task
    rows = data.get('attempts')
    require(isinstance(rows, list), 'attempts: list required')
    out = {'schema_version': 1, 'mode': data['mode'], 'status': data['status'],
           'analysis_unit': protocol['analysis_unit'], 'recorded_trials': len(rows),
           'boundary': 'Arithmetic and record consistency only; does not verify recruitment, recordings, comparability or causal validity.'}
    if data['status'] == 'planned':
        require(not rows, 'planned: results must be absent')
        return dict(out, recorded_participants=0, summaries=None, matched_participants_by_task=None)
    require(rows, 'completed: attempts required')
    seen, selected, invalid = set(), {}, []
    for row in rows:
        require(isinstance(row, dict), 'attempt: object required')
        for key, choices in [('participant_id', participants), ('product_id', products), ('task_id', task_map)]:
            require(isinstance(row.get(key), str) and row[key] in choices, f'{key}: unknown ID')
        require(type(row.get('trial')) is int and row['trial'] >= 0, 'trial: nonnegative integer required')
        key = (row['participant_id'], row['product_id'], row['task_id'])
        trial_key = key + (row['trial'],)
        require(trial_key not in seen, 'duplicate trial for participant/product/task')
        seen.add(trial_key)
        require(row.get('result') in ('independent_success', 'helped_success', 'failure', 'invalid'), 'result: unsupported value')
        # An invalid recording may have no trustworthy measurements. Preserve
        # those nulls rather than requiring invented zeroes to record exclusion.
        if row['result'] != 'invalid' or row.get('elapsed_s') is not None:
            require(duration(row.get('elapsed_s')) and row['elapsed_s'] <= task_map[row['task_id']]['timeout_s'],
                    'elapsed_s: finite duration within task timeout required')
        for field in ('errors', 'help_events'):
            if row['result'] != 'invalid' or row.get(field) is not None:
                require(type(row.get(field)) is int and row[field] >= 0, f'{field}: nonnegative integer required')
        nonempty(row, 'evidence')
        if row['result'] == 'independent_success':
            require(row['help_events'] == 0, 'independent_success: help_events must be zero')
        if row['result'] == 'helped_success':
            require(row['help_events'] > 0, 'helped_success: positive help_events required')
        if row['result'] == 'invalid':
            nonempty(row, 'exclusion_reason')
            invalid.append(row)
        elif key not in selected or row['trial'] < selected[key]['trial']:
            selected[key] = row
    summaries, matched = [], {}
    for task in tasks:
        sets = []
        for product in products:
            actual = [r for r in selected.values() if r['product_id'] == product and r['task_id'] == task['id']]
            valid_trials = [r for r in rows if r['product_id'] == product and r['task_id'] == task['id'] and r['result'] != 'invalid']
            independent = [r for r in actual if r['result'] == 'independent_success']
            helped = [r for r in actual if r['result'] == 'helped_success']
            sets.append({r['participant_id'] for r in actual})
            summaries.append({
                'product_id': product, 'task_id': task['id'],
                'measurement_status': 'measured' if actual else 'no_valid_attempts',
                'participants': len(actual), 'selected_attempts': len(actual),
                'independent_success': {'n': len(independent), 'N': len(actual)},
                'helped_success': len(helped), 'failure': len(actual) - len(independent) - len(helped),
                'invalid_trials': sum(r['product_id'] == product and r['task_id'] == task['id'] for r in invalid),
                'additional_valid_trials': len(valid_trials) - len(actual),
                'independent_success_time_s': times(independent), 'helped_success_time_s': times(helped),
                'all_selected_time_s': times(actual),
                'errors': {'events': sum(r['errors'] for r in actual),
                           'affected_participants': sum(r['errors'] > 0 for r in actual)},
                'help': {'events': sum(r['help_events'] for r in actual),
                         'affected_participants': sum(r['help_events'] > 0 for r in actual)}})
        matched[task['id']] = sorted(set.intersection(*sets))
    return dict(out, recorded_participants=len({r['participant_id'] for r in rows}),
                summaries=summaries, matched_participants_by_task=matched)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        raw = args.input.read_bytes()
        result = summarize(json.loads(raw))
        result['input_sha256'] = hashlib.sha256(raw).hexdigest()
        rendered = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
        if args.output:
            args.output.write_text(rendered, encoding='utf-8')
        else:
            print(rendered, end='')
    except (OSError, ValueError, TypeError) as exc:
        print(f'study_metrics: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
