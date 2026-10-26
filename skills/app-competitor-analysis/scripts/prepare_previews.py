#!/usr/bin/env python3
"""Optional, local-only display derivatives. Originals are never rewritten.

Requires Pillow only for this optional command. The renderer remains standard
library only and uses capability summaries when no bounded catalog image exists.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys


def prepare(bundle, base, output):
    try:
        from PIL import Image, ImageOps
    except ImportError:
        raise ValueError('Optional preview preparation requires Pillow in this interpreter. Use existing image tooling or render without previews; no automatic installation.')
    if output.exists() and any(output.iterdir()):
        raise ValueError('preview output must be new or empty; existing work is preserved')
    output.mkdir(parents=True, exist_ok=True)
    result = copy.deepcopy(bundle); receipts = []; cache = {}
    for product in result['products']:
        for section in product['sections']:
            for block in section['blocks']:
                if block['type'] != 'image':
                    continue
                source = (base / block['path']).resolve(); raw = source.read_bytes()
                digest = hashlib.sha256(raw).hexdigest()
                viewport=block.get('viewport')
                context=hashlib.sha256((digest+json.dumps(viewport,sort_keys=True)).encode()).hexdigest()
                if context not in cache:
                    with Image.open(source) as opened:
                        opened.load()
                        display=ImageOps.exif_transpose(opened)
                        if viewport:
                            v=viewport
                            if display.size != (v['source_width'],v['source_height']):
                                raise ValueError('documented viewport dimensions do not match the source')
                            display=display.crop((v['x'],v['y'],v['x']+v['width'],v['y']+v['height']))
                        variants = {}
                        for role, bound in [('thumbnail_path',480),('preview_path',1600)]:
                            if not viewport and max(display.size)<=bound and len(raw)<=120*1024:
                                continue
                            image = display.copy(); image.thumbnail((bound,bound),getattr(Image,'Resampling',Image).LANCZOS)
                            alpha = image.mode in ('RGBA','LA') or 'transparency' in image.info
                            ext = '.png' if alpha else '.jpg'
                            path = output / (context+'-'+str(bound)+ext)
                            if alpha:
                                image.convert('RGBA').save(path,optimize=True)
                            else:
                                image.convert('RGB').save(path,quality=85,optimize=True)
                            variants[role] = str(path.resolve())
                            variants[role.replace('_path','_framed')]=bool(viewport)
                            receipts.append({'original_sha256':digest,'original_path':str(source),'original_size':list(opened.size),'original_bytes':len(raw),'documented_viewport':viewport,'role':role,'path':str(path.resolve()),'size':list(image.size),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'identity':'reading derivative, not a new app capture; exact source remains embedded'})
                    cache[context] = variants
                block['path'] = str(source)
                block.update(cache[context])
                if hashlib.sha256(source.read_bytes()).hexdigest() != digest:
                    raise ValueError('original changed during preparation')
    return result, receipts


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('bundle',type=Path); ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--bundle-output',required=True,type=Path)
    args = ap.parse_args()
    if args.bundle_output.exists():
        ap.exit(1,'bundle output already exists; preserve it and choose a new path\n')
    try:
        bundle, receipts = prepare(json.loads(args.bundle.read_text()),args.bundle.parent,args.output)
        args.bundle_output.write_text(json.dumps(bundle,ensure_ascii=False,indent=2)+'\n')
        (args.output/'media-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
    except (OSError,ValueError) as e:
        ap.exit(1,str(e)+'\n')
    print(f'Prepared {len(receipts)} reading derivatives; originals unchanged. Bundle: {args.bundle_output}')


if __name__ == '__main__':
    main()
