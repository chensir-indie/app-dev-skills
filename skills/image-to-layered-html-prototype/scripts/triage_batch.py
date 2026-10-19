#!/usr/bin/env python3
"""Rank real browser-page gaps even before page contracts are complete.

This is a repair queue, never an acceptance result. Strict status always comes
from validate_batch.py / validate_prototype.py.
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

from diagnose_visual import score
from validate_batch import read_expected_pages, validate_batch
from validate_prototype import FILES, ONE_TO_ONE_CEILINGS


def visual_gap(reference: Path, actual: Path, tile_size: int = 256) -> dict:
    with Image.open(reference) as source, Image.open(actual) as rendered:
        source, rendered = source.convert('RGB'), rendered.convert('RGB')
        if source.size != rendered.size:
            return {'dimensionError': {'reference': list(source.size),
                                       'actual': list(rendered.size)}}
        width, height = source.size
        full = score(source, rendered, (0, 0, width, height),
                     ONE_TO_ONE_CEILINGS['channelThreshold'])
        diff = ImageChops.difference(source, rendered)
        tiles = []
        for top in range(0, height, tile_size):
            for left in range(0, width, tile_size):
                box = (left, top, min(left + tile_size, width), min(top + tile_size, height))
                crop = diff.crop(box)
                mae = sum(ImageStat.Stat(crop).mean) / 3
                tiles.append({'box': list(box), 'mae': round(mae, 2),
                              'errorMass': round(mae * crop.width * crop.height)})
        tiles.sort(key=lambda item: item['errorMass'], reverse=True)
        return {
            'mae': full['mae'],
            'gapToFullPageCeiling': round(max(0, full['mae'] - ONE_TO_ONE_CEILINGS['maxMAE']), 2),
            'changedPixelRatio': full['changedPixelRatio'],
            'edgeDisagreementRatio': full['edgeDisagreementRatio'],
            'topTiles': tiles[:5],
            'warning': 'Whole-page metrics are diagnostic; only frozen role ROIs and strict validation can pass.',
        }


def triage_batch(root: Path, expected_pages=None, tile_size: int = 256) -> dict:
    root = root.resolve()
    strict = validate_batch(root, expected_pages=expected_pages)
    pages = []
    for page in strict['pages']:
        folder = root / page['id']
        missing = [name for name in (*FILES, 'reference/source.png',
                                     'evidence/native.png', 'acceptance.json')
                   if not (folder / name).is_file()]
        reference = folder / 'reference/source.png'
        actual = folder / 'evidence/native.png'
        visual = None
        if reference.is_file() and actual.is_file():
            try:
                visual = visual_gap(reference, actual, tile_size)
            except (OSError, ValueError) as exc:
                visual = {'error': str(exc)}
        pages.append({**page, 'missingArtifacts': missing, 'visual': visual})
    priority = sorted(
        (page for page in pages if page['status'] != 'passed' and
         page['visual'] and 'mae' in page['visual']),
        key=lambda page: page['visual']['gapToFullPageCeiling'], reverse=True,
    )
    # Finish the page closest to a complete visual contract before expanding
    # a batch of unmeasured drafts. The highest-error pages remain in the
    # separate visualRepairOrder for deciding what to fix within that page.
    candidates = [page for page in pages if page['status'] != 'passed' and
                  page.get('visual') and 'mae' in page['visual']]
    stage_rank = {'review': 0, 'visual': 1, 'layers': 2, 'evidence': 3,
                  'contract': 4, 'missing': 5}
    candidates.sort(key=lambda page: (
        stage_rank.get(page['stage'], 6), len(page['missingArtifacts']),
        page['visual']['mae']))
    next_candidate = None
    if candidates:
        page = candidates[0]
        next_candidate = {
            'id': page['id'], 'stage': page['stage'],
            'nextAction': page['nextAction'],
            'missingArtifacts': page['missingArtifacts'],
            'mae': page['visual']['mae'],
            'worstTile': page['visual']['topTiles'][0] if page['visual']['topTiles'] else None,
        }
    return {
        'status': strict['status'], 'expectedPageCount': strict['pageCount'],
        'strictPassedCount': strict['passedCount'],
        'unlistedReferencePages': strict['unlistedReferencePages'],
        'pages': pages,
        'nextAcceptanceCandidate': next_candidate,
        'visualRepairOrder': [page['id'] for page in priority],
        'warning': 'This report never grants visual acceptance; run strict validation for every expected page.',
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--expected-pages', type=Path, required=True,
                        help='frozen JSON array or one expected page directory per line')
    parser.add_argument('--tile-size', type=int, default=256)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if args.tile_size < 16:
        parser.error('--tile-size must be at least 16')
    try:
        report = triage_batch(args.root, read_expected_pages(args.expected_pages),
                              args.tile_size)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    output = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding='utf-8')
    print(f"STRICT {report['strictPassedCount']}/{report['expectedPageCount']} pages; "
          f"visual repair order: {', '.join(report['visualRepairOrder'][:8])}")
    candidate = report['nextAcceptanceCandidate']
    if candidate:
        print(f"NEXT ACCEPTANCE CANDIDATE: {candidate['id']} [{candidate['stage']}], "
              f"missing {len(candidate['missingArtifacts'])} artifacts, "
              f"MAE {candidate['mae']:.2f}")
        print(f"  {candidate['nextAction']}")
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
