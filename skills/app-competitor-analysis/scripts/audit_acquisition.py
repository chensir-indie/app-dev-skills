#!/usr/bin/env python3
"""Validate acquisition records. No network access or automatic truth assessment."""
import sys

if sys.version_info < (3, 9):
    sys.exit('Python 3.9+ is required. Run sh scripts/doctor.sh for setup guidance.')

import argparse
from collections import Counter
import json
from pathlib import Path

PROOFS = {
    'identity': {'official', 'static', 'runtime'},
    'pixels': {'screenshot', 'runtime'},
    'stated_behavior': {'official'},
    'behavior': {'runtime'},
    'implementation': {'static', 'runtime'},
    'disclosed_technology': {'official'},
    'commercial_terms': {'official', 'runtime'},
}
STATES = {'queued', 'attempted', 'partial', 'resolved', 'blocked', 'deferred', 'out_of_scope'}
OUTCOMES = {'success', 'partial', 'failed', 'unavailable', 'barrier', 'no_result'}


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ['document: expected object']
    def error(where, rule):
        errors.append(f'{where}: {rule}')
    def text(value):
        return isinstance(value, str) and bool(value.strip())
    def choice(value, options):
        return isinstance(value, str) and value in options
    def references(value, where, label):
        if not isinstance(value, list):
            error(where, f'{label} must be array of nonempty strings')
            return []
        if any(not text(ref) for ref in value):
            error(where, f'{label} must be array of nonempty strings')
        return [ref for ref in value if text(ref)]
    if type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        error('document', 'schema_version must be 1')
    if not text(data.get('scope')):
        error('document', 'scope required')
    indexes = {}
    for key in ('products', 'sources', 'gaps'):
        rows = data.get(key)
        if not isinstance(rows, list):
            error(key, 'expected array')
            rows = []
        index = {}
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id']:
                error(key, 'object with nonempty id required')
                continue
            if row['id'] in index:
                error(row['id'], 'duplicate id')
            index[row['id']] = row
        indexes[key] = index
    products, sources, gaps = (indexes[k] for k in ('products', 'sources', 'gaps'))
    if not products or not gaps:
        error('document', 'products and gaps must be nonempty')
    for pid, product in products.items():
        if not text(product.get('identity')):
            error(pid, 'identity required')
    for sid, source in sources.items():
        if not choice(source.get('product_id'), products):
            error(sid, 'unknown source_product')
        for field in ('kind', 'locator', 'version'):
            if not text(source.get(field)):
                error(sid, f'{field} required')
        if type(source.get('inspected')) is not bool:
            error(sid, 'inspected must be boolean')
    for gid, gap in gaps.items():
        pid = gap.get('product_id')
        if not choice(pid, products):
            error(gid, 'unknown product_id')
        for field in ('question', 'impact', 'closure_check', 'target_version'):
            if not text(gap.get(field)):
                error(gid, f'{field} required')
        if not choice(gap.get('dimension'), {'identity', 'ui', 'interaction', 'technology', 'business'}):
            error(gid, 'invalid dimension')
        if not choice(gap.get('priority'), {'P0', 'P1', 'P2'}):
            error(gid, 'invalid priority')
        proof, state = gap.get('proof'), gap.get('state')
        if not choice(proof, PROOFS):
            error(gid, 'invalid proof')
            proof = ''
        if not choice(state, STATES):
            error(gid, 'invalid state')
            state = ''
        refs = references(gap.get('source_ids'), gid, 'source_ids')
        attempts = gap.get('attempts')
        if not isinstance(attempts, list):
            error(gid, 'attempts must be array')
            attempts = []
        attempt_refs = []
        for attempt in attempts:
            if not isinstance(attempt, dict):
                error(gid, 'attempt must be object')
                continue
            for field in ('date', 'channel', 'locator', 'note'):
                if not text(attempt.get(field)):
                    error(gid, f'attempt {field} required')
            if not choice(attempt.get('outcome'), OUTCOMES):
                error(gid, 'invalid attempt outcome')
            attempt_refs.extend(references(attempt.get('source_ids'), gid, 'attempt source_ids'))
        for sid in refs + attempt_refs:
            source = sources.get(sid)
            if not source:
                error(gid, f'unknown source {sid}')
            elif source.get('product_id') != pid:
                error(gid, f'source_product mismatch {sid}')
        if state in {'attempted', 'partial', 'resolved', 'blocked'} and not attempts:
            error(gid, 'actual attempts required')
        if state == 'resolved':
            if not refs:
                error(gid, 'resolution_sources required')
            for sid in refs:
                source = sources.get(sid, {})
                if not choice(source.get('kind'), PROOFS.get(proof, set())):
                    error(gid, f'proof_kind mismatch {sid}')
                if source.get('inspected') is not True:
                    error(gid, f'resolution source not inspected {sid}')
                version = gap.get('target_version')
                if version != 'unknown' and source.get('version') != version:
                    error(gid, f'version mismatch {sid}')
                if not any(isinstance(a, dict) and a.get('outcome') == 'success'
                           and isinstance(a.get('source_ids'), list) and sid in a['source_ids'] for a in attempts):
                    error(gid, f'no successful acquisition for {sid}')
            if not gap.get('resolution'):
                error(gid, 'resolution required')
            if gap.get('remaining'):
                error(gid, 'remaining question prevents resolution')
            updates = gap.get('report_updates')
            if not isinstance(updates, list) or not updates or not all(isinstance(u, str) and u.strip() for u in updates):
                error(gid, 'report_updates required')
        elif state != 'out_of_scope' and not gap.get('next_action'):
            error(gid, 'next_action required for open question')
        if state in {'blocked', 'deferred', 'out_of_scope'} and not gap.get('reason'):
            error(gid, f'{state} requires recorded basis')
        if state in {'blocked', 'deferred'} and not gap.get('resume_condition'):
            error(gid, f'{state} requires resume_condition')
        if state == 'blocked' and not any(isinstance(a, dict) and choice(a.get('outcome'), {'failed', 'unavailable', 'barrier'}) for a in attempts):
            error(gid, 'blocked requires a concrete unsuccessful attempt')
    return errors


def summary(data):
    gaps = data.get('gaps', [])
    counts = Counter(g.get('state', 'invalid') for g in gaps)
    open_gaps = [g for g in gaps if g.get('state') not in {'resolved', 'out_of_scope'}]
    return {
        'products': len(data.get('products', [])), 'gaps': len(gaps),
        'states': dict(sorted(counts.items())), 'resolved': counts['resolved'],
        'unresolved_core': sum(g.get('priority') == 'P0' for g in open_gaps),
        'research_complete': counts['resolved'] > 0 and not open_gaps and not validate(data),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.ledger.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        parser.exit(2, f'{exc}\n')
    errors = validate(data)
    print(json.dumps({'errors': errors, 'summary': summary(data) if not errors else None}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
