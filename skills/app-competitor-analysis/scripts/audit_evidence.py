#!/usr/bin/env python3
"""Check ledger provenance structure, not semantic truth. Python 3.9+, stdlib only."""
import sys

if sys.version_info < (3, 9):
    sys.exit('Python 3.9+ is required. Run sh scripts/doctor.sh for setup guidance.')

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re

DIMENSIONS = {'ui', 'interaction', 'technology', 'business'}
KINDS = {'runtime', 'screenshot', 'official', 'static', 'research_note', 'concept'}
STATUSES = {'observed', 'declared', 'static', 'reported', 'inferred', 'unknown'}


def validate(data, base_dir=None):
    errors = []

    def fail(code, where, detail):
        errors.append(f'{code}: {where}: {detail}')

    def required(obj, field, where):
        value = obj.get(field)
        if not isinstance(value, str) or not value.strip():
            fail('required_text', where, field)
            return ''
        return value.strip()

    def rows(key):
        value = data.get(key)
        if not isinstance(value, list):
            fail('shape', key, 'expected array')
            return []
        clean = []
        for i, row in enumerate(value):
            if not isinstance(row, dict):
                fail('shape', f'{key}[{i}]', 'expected object')
            else:
                clean.append(row)
        return clean

    def index(records, label):
        result = {}
        for n, row in enumerate(records):
            ident = required(row, 'id', f'{label}[{n}]')
            if ident in result:
                fail('duplicate_id', label, ident)
            if ident:
                result[ident] = row
        return result

    def identifiers(row, field, where):
        value = row.get(field)
        if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
            fail('shape', where, f'{field} must be an array of nonempty strings')
            return []
        if len(set(value)) != len(value):
            fail('duplicate_reference', where, field)
        return value

    if not isinstance(data, dict):
        return ['shape: root: expected object']
    if type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        fail('schema_version', 'root', 'expected 1')
    product_rows, source_rows, claim_rows = rows('products'), rows('sources'), rows('claims')
    coverage, recommendation_rows = rows('coverage'), rows('recommendations')
    products, sources, claims = index(product_rows, 'products'), index(source_rows, 'sources'), index(claim_rows, 'claims')
    recommendations = index(recommendation_rows, 'recommendations')
    if not products:
        fail('products', 'root', 'at least one product required')

    identities = set()
    for pid, p in products.items():
        required(p, 'name', pid)
        platform, identity = required(p, 'platform', pid), required(p, 'identity', pid)
        key = (platform.casefold(), identity.casefold())
        if key in identities:
            fail('duplicate_identity', pid, 'same platform and identity')
        identities.add(key)
        if p.get('kind') not in ('app', 'system_feature', 'web'):
            fail('product_kind', pid, 'expected app, system_feature or web')

    for sid, s in sources.items():
        pid = required(s, 'product_id', sid)
        if pid not in products:
            fail('source_product', sid, 'unknown product')
        kind = required(s, 'kind', sid)
        if kind not in KINDS:
            fail('source_kind', sid, kind)
        required(s, 'locator', sid)
        required(s, 'version', sid)
        required(s, 'context', sid)
        observed = required(s, 'observed_at', sid)
        if observed != 'unknown':
            try:
                date.fromisoformat(observed)
            except ValueError:
                fail('date', sid, 'observed_at must be YYYY-MM-DD or unknown')
        if kind == 'static' and not re.fullmatch(r'[0-9a-fA-F]{64}', str(s.get('artifact_sha256', ''))):
            fail('artifact_hash', sid, 'static source requires artifact SHA-256')
        if 'local_path' in s:
            local = required(s, 'local_path', sid)
            if base_dir is not None and local:
                path = Path(base_dir) / local
                try:
                    if not path.is_file():
                        raise OSError('not a regular file')
                    if 'sha256' in s:
                        digest = hashlib.sha256()
                        with path.open('rb') as f:
                            for block in iter(lambda: f.read(1024 * 1024), b''):
                                digest.update(block)
                        if digest.hexdigest() != str(s['sha256']).lower():
                            fail('hash_mismatch', sid, local)
                except OSError as exc:
                    fail('local_file', sid, f'{local}: {exc}')

    def linked_sources(row, where):
        linked = []
        for sid in identifiers(row, 'source_ids', where):
            if sid not in sources:
                fail('unknown_source', where, sid)
            elif sources[sid].get('product_id') != row.get('product_id'):
                fail('source_product', where, f'{sid} belongs to another product')
            else:
                linked.append(sources[sid])
        return linked

    for cid, c in claims.items():
        pid = required(c, 'product_id', cid)
        if pid not in products:
            fail('claim_product', cid, 'unknown product')
        dimension = required(c, 'dimension', cid)
        status = required(c, 'status', cid)
        version = required(c, 'version', cid)
        required(c, 'text', cid)
        required(c, 'scope', cid)
        if dimension not in DIMENSIONS:
            fail('dimension', cid, dimension)
        if status not in STATUSES:
            fail('claim_status', cid, status)
        linked = linked_sources(c, cid)
        kinds = {s.get('kind') for s in linked if isinstance(s.get('kind'), str)}
        if status != 'unknown' and not linked:
            fail('claim_sources', cid, 'non-unknown claim needs evidence')
        needed = {'declared': {'official'}, 'static': {'static'}, 'reported': {'research_note'}}.get(status)
        if status == 'observed':
            needed = {'runtime', 'screenshot'} if dimension == 'ui' else {'runtime'}
        if needed is not None and not kinds.intersection(needed):
            fail('evidence_kind', cid, f'{status}/{dimension} needs {sorted(needed)}')
        if status in ('observed', 'static'):
            for s in linked:
                if s.get('kind') in ('runtime', 'static', 'screenshot') and s.get('version') not in (None, '', 'unknown', version):
                    fail('version_mismatch', cid, f'source {s.get("id")} version differs from claim')
        if status == 'inferred' and dimension == 'technology':
            alternatives = c.get('alternatives')
            if not isinstance(alternatives, list) or not alternatives or not all(isinstance(a, str) and a.strip() for a in alternatives):
                fail('inference_test', cid, 'technology inference needs alternatives')
            if not isinstance(c.get('verification'), str) or not c['verification'].strip():
                fail('inference_test', cid, 'technology inference needs distinguishing test')
        if 'measurement' in c:
            m = c['measurement']
            valid = (isinstance(m, dict) and type(m.get('n')) is int and m['n'] > 0
                     and all(isinstance(m.get(k), str) and m[k].strip() for k in ('unit', 'conditions', 'method')))
            if not valid or status != 'observed' or 'runtime' not in kinds:
                fail('measurement', cid, 'measurement requires observed runtime, positive n, unit, conditions and method')

    covered = set()
    for n, c in enumerate(coverage):
        where = f'coverage[{n}]'
        pid, dim = required(c, 'product_id', where), required(c, 'dimension', where)
        if pid not in products or dim not in DIMENSIONS:
            fail('coverage_identity', where, 'unknown product or dimension')
        key = (pid, dim)
        if key in covered:
            fail('coverage_duplicate', where, str(key))
        covered.add(key)
        status = required(c, 'status', where)
        required(c, 'reason', where)
        if status not in ('supported', 'partial', 'missing', 'out_of_scope'):
            fail('coverage_status', where, status)
        linked = linked_sources(c, where)
        if status in ('supported', 'partial') and not linked:
            fail('coverage_sources', where, 'supported/partial needs evidence')
    for pid in products:
        for dim in sorted(DIMENSIONS):
            if (pid, dim) not in covered:
                fail('coverage_missing', pid, dim)

    for rid, r in recommendations.items():
        for field in ('text', 'fit', 'tradeoff', 'validation'):
            required(r, field, rid)
        basis = identifiers(r, 'basis_claim_ids', rid)
        if not basis or any(c not in claims for c in basis):
            fail('recommendation_basis', rid, 'needs known claim IDs')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.ledger.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        print(f'ledger: {exc}', file=sys.stderr)
        return 1
    errors = validate(data, args.ledger.parent)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'PASS: {len(data["products"])} products, {len(data["claims"])} claims; structural audit, not semantic verification')
    return 0


if __name__ == '__main__':
    sys.exit(main())
