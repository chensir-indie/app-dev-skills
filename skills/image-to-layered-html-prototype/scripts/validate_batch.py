#!/usr/bin/env python3
"""Run the strict prototype gate on every page in a multi-screen delivery."""
import argparse
import json
from pathlib import Path
from typing import Optional

from validate_prototype import check


def read_expected_pages(path: Path) -> list[str]:
    content = path.read_text(encoding='utf-8')
    pages = json.loads(content) if path.suffix.lower() == '.json' else [
        line.strip() for line in content.splitlines() if line.strip() and not line.lstrip().startswith('#')
    ]
    if not isinstance(pages, list) or not pages or any(
            not isinstance(page, str) or not page or page in {'.', '..'} or
            '/' in page or '\\' in page for page in pages):
        raise ValueError('expected pages must be a nonempty list of directory names')
    if len(set(pages)) != len(pages):
        raise ValueError('expected page IDs must be unique')
    return pages


def next_step(errors: list[str]) -> tuple[str, str]:
    if not errors:
        return 'passed', 'No further repair required; retain the recorded manual review.'
    joined = '\n'.join(errors)
    if ('missing or nonlocal artifact' in joined or 'incomplete/invalid contract' in joined or
            'manifest' in joined or
            'reference hash' in joined or 'fidelity profile' in joined or
            'ROI role' in joined or 'role ROI does not cover' in joined or
            'reference geometry missing' in joined or 'reference geometry invalid' in joined):
        return 'contract', 'Create or repair the page-specific tokens, layer manifest, reference and asset contracts.'
    if ('visual limits' in joined or 'ROI failed' in joined or
            'ROI contour/edge failed' in joined or 'one-to-one ceiling' in joined):
        return 'visual', 'Inspect the worst failed ROI; fix its source asset, geometry, contour, color or typography, then recapture.'
    if 'capture' in joined or 'DOM audit' in joined or 'stale artifact' in joined:
        return 'evidence', 'Recapture screenshot, DOM and source receipt from the current HTML, then refresh artifact hashes.'
    if ('text metric' in joined or 'font family' in joined or 'geometry differs' in joined or
            'reference geometry differs' in joined or 'unlisted visible' in joined):
        return 'layers', 'Measure and correct the declared DOM layers; add any missing visible text and controls.'
    return 'review', 'Resolve the listed proof, interaction or manual review findings, then rerun strict validation.'


def validate_batch(root: Path, pattern: str = '*', expected_pages: Optional[list[str]] = None) -> dict:
    pages = []
    folders = ([root / name for name in expected_pages] if expected_pages is not None
               else sorted(root.glob(pattern)))
    for folder in folders:
        if not folder.is_dir() or not (folder / 'index.html').is_file():
            if expected_pages is not None:
                pages.append({
                    'id': folder.name, 'status': 'pending', 'stage': 'missing',
                    'nextAction': 'Create the expected page and its index.html before visual validation.',
                    'errors': ['expected page or index.html is missing'],
                })
            continue
        errors = check(folder.resolve())
        stage, action = next_step(errors)
        pages.append({
            'id': folder.name,
            'status': 'passed' if not errors else 'pending',
            'stage': stage,
            'nextAction': action,
            'errors': errors,
        })
    passed = sum(page['status'] == 'passed' for page in pages)
    unlisted = sorted(folder.name for folder in root.iterdir()
                      if folder.is_dir() and (folder / 'reference' / 'source.png').is_file()
                      and expected_pages is not None and folder.name not in expected_pages)
    return {
        'status': 'passed' if pages and passed == len(pages) and not unlisted else 'pending',
        'pageCount': len(pages),
        'passedCount': passed,
        'pendingCount': len(pages) - passed,
        'unlistedReferencePages': unlisted,
        'pages': pages,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path, help='directory containing one folder per page')
    parser.add_argument('--pattern', default='*', help='glob for page directories')
    parser.add_argument('--expected-pages', type=Path,
                        help='frozen JSON array or one page directory name per line; missing pages fail')
    parser.add_argument('--out', type=Path, help='write the complete JSON result here')
    args = parser.parse_args()
    try:
        expected = read_expected_pages(args.expected_pages) if args.expected_pages else None
        report = validate_batch(args.root.resolve(), args.pattern, expected)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"{report['status'].upper()}: {report['passedCount']}/{report['pageCount']} pages passed strict visual acceptance")
    if report['unlistedReferencePages']:
        print('  Unlisted reference pages: ' + ', '.join(report['unlistedReferencePages']))
    for page in report['pages']:
        detail = f" — {page['errors'][0]}" if page['errors'] else ''
        print(f"  {page['id']}: {page['status']} [{page['stage']}] — {page['nextAction']}{detail}")
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
