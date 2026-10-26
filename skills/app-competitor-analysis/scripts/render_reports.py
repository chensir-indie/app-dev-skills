#!/usr/bin/env python3
"""Render authored analysis into one offline HTML per product plus an index.

Python 3.9+, standard library. This renderer does not author or verify claims.
"""
import sys

if sys.version_info < (3, 9):
    sys.exit('Python 3.9+ is required. Run sh scripts/doctor.sh for setup guidance.')

import argparse
import base64
import hashlib
from html import escape
import json
import math
from pathlib import Path
import re
from urllib.parse import urlsplit

# Support both standalone execution and importlib-based portable tests.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from visual_atlas import validate_visuals, render_visuals, render_integrated_map, integrated_overview, words as atlas_words
from delivery_assets import link_resources
from media_info import dimensions
from reader_shell import report_frame
from design_spec import validate_design, design_panel, ux_panel, design_markdown, download_link
from design_reader import design_template
from visual_composition import route_excerpt, object_glyph

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
SECTIONS = ('overview', 'ui', 'interaction', 'technology', 'business', 'strengths', 'decisions', 'validation')
DIMENSIONS = ('ui', 'interaction', 'technology', 'business')
KINDS = {'runtime', 'screenshot', 'official', 'static', 'research_note', 'concept'}
BLOCKS = {'paragraph', 'callout', 'heading', 'list', 'table', 'flow', 'image'}


def esc(value):
    return escape(str(value), quote=True)


def text_field(obj, key):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{key}: nonempty text required')
    return value


def safe_id(value):
    return isinstance(value, str) and re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]*', value)


def validate_bundle(data):
    if not isinstance(data, dict):
        raise ValueError('bundle must be an object')
    for key in ('title', 'date', 'summary'):
        text_field(data, key)
    products = data.get('products')
    if not isinstance(products, list) or not products:
        raise ValueError('products: nonempty array required')
    seen = set()
    for p in products:
        for key in ('id', 'name', 'category', 'platform', 'identity', 'version', 'tagline', 'verdict', 'scope'):
            text_field(p, key)
        if 'positioning' in p:
            if not isinstance(p['positioning'],dict):
                raise ValueError('positioning must be an object')
            text_field(p['positioning'],'summary')
        pid = p['id']
        if 'presentation' in p:
            if not isinstance(p['presentation'], dict):
                raise ValueError('presentation must be an object')
            if 'lead' in p['presentation']:
                text_field(p['presentation'], 'lead')
        if 'brief' in p:
            if not isinstance(p['brief'], dict):
                raise ValueError('brief must be an object')
            for key in ('headline', 'deck'):
                text_field(p['brief'], key)
        if not safe_id(pid) or pid.casefold() in {'index', 'manifest'}:
            raise ValueError(f'unsafe product id: {pid}')
        if pid.casefold() in seen:
            raise ValueError(f'duplicate product id: {pid}')
        seen.add(pid.casefold())
        coverage = p.get('coverage', [])
        if not isinstance(coverage, list) or sorted(c.get('dimension', '') for c in coverage) != sorted(DIMENSIONS):
            raise ValueError(f'{pid}: coverage requires each dimension once')
        for c in coverage:
            if c.get('status') not in {'supported', 'partial', 'missing', 'out_of_scope'}:
                raise ValueError('coverage: invalid status')
            text_field(c, 'detail')
        sources = p.get('sources', [])
        if not isinstance(sources, list) or not sources:
            raise ValueError(f'{pid}: sources required')
        source_ids = set()
        for s in sources:
            sid = text_field(s, 'id')
            if not safe_id(sid) or sid in source_ids:
                raise ValueError('source: unsafe or duplicate id')
            source_ids.add(sid)
            for key in ('title', 'locator', 'context', 'date'):
                text_field(s, key)
            if s.get('kind') not in KINDS:
                raise ValueError('source: invalid kind')
            if s.get('url'):
                url = urlsplit(s['url'])
                if url.scheme not in ('https', 'http') or not url.netloc:
                    raise ValueError('source URL must use http or https')
        validate_visuals(p.get('visuals'), source_ids)
        validate_design(p)
        if p.get('positioning'):
            refs=p['positioning'].get('sources',[])
            if not isinstance(refs,list)or any(ref not in source_ids for ref in refs):
                raise ValueError(f'{pid}: unknown positioning source')
        sections = p.get('sections', [])
        if not isinstance(sections, list) or sorted(s.get('id', '') for s in sections) != sorted(SECTIONS):
            raise ValueError(f'{pid}: sections require each report chapter once')
        for section in sections:
            text_field(section, 'title')
            blocks = section.get('blocks')
            if not isinstance(blocks, list) or not blocks:
                raise ValueError('section blocks must not be empty; explain a gap instead')
            if 'lead_blocks' in section and (type(section['lead_blocks']) is not int
                    or not 0 <= section['lead_blocks'] <= len(blocks)):
                raise ValueError('lead_blocks must be an integer within the section block count')
            for key in ('summary_title', 'detail_label'):
                if key in section: text_field(section, key)
            summaries = section.get('summary_blocks', [])
            if not isinstance(summaries, list):
                raise ValueError('summary_blocks must be an array')
            if 'summary_blocks' in section and not summaries:
                raise ValueError('summary_blocks must not be empty')
            for b in blocks + summaries:
                kind = b.get('type')
                if kind not in BLOCKS:
                    raise ValueError(f'unsupported block: {kind}')
                refs = b.get('sources', [])
                if not isinstance(refs, list) or any(ref not in source_ids for ref in refs):
                    raise ValueError(f'{pid}: unknown source citation')
                if kind in ('paragraph', 'callout', 'heading'):
                    text_field(b, 'text')
                elif kind == 'image':
                    for key in ('path', 'alt', 'caption'):
                        text_field(b, key)
                    for key in ('preview_path', 'thumbnail_path'):
                        if key in b:
                            text_field(b, key)
                    for key in ('preview_framed','thumbnail_framed'):
                        if key in b and type(b[key])is not bool:
                            raise ValueError('framed preview flag must be boolean')
                    if 'viewport' in b:
                        v = b['viewport']
                        keys = ('x', 'y', 'width', 'height', 'source_width', 'source_height')
                        if (not isinstance(v, dict) or any(type(v.get(k)) not in (int, float)
                            or not math.isfinite(v[k]) for k in keys)
                            or min(v['x'], v['y']) < 0
                            or min(v['width'], v['height'], v['source_width'], v['source_height']) <= 0
                            or v['x'] + v['width'] > v['source_width']
                            or v['y'] + v['height'] > v['source_height']):
                            raise ValueError('image viewport must fit inside its documented source dimensions')
                elif kind in ('list', 'flow'):
                    items = b.get('items')
                    if not isinstance(items, list) or not items:
                        raise ValueError('nonempty items required')
                    for item in items:
                        if kind == 'flow':
                            text_field(item, 'title')
                            text_field(item, 'detail')
                        elif not isinstance(item, str) or not item.strip():
                            raise ValueError('list items must be text')
                elif kind == 'table':
                    columns, rows = b.get('columns'), b.get('rows')
                    if (not isinstance(columns, list) or not columns or not all(isinstance(c, str) for c in columns)
                            or not isinstance(rows, list) or not rows
                            or any(not isinstance(row, list) or len(row) != len(columns)
                                   or any(not isinstance(v, str) for v in row) for row in rows)):
                        raise ValueError('table requires text columns and matching rows')


def citations(block):
    links = ''.join(f'<a href="#source-{esc(s)}">{esc(s)}</a>' for s in block.get('sources', []))
    status = f'<span class="evidence-tag">{esc(block["status"])}</span>' if block.get('status') else ''
    return f'<div class="citations">{status}{links}</div>' if status or links else ''


def image_html(b, base_dir, preview=False, original=False, catalog=False):
    selected = b['path'] if original else b.get('thumbnail_path' if catalog else 'preview_path', b['path'])
    path = Path(base_dir) / selected
    try:
        raw = path.read_bytes()
    except OSError as e:
        raise ValueError(f'image: {path}: {e}') from e
    if len(raw) > 20 * 1024 * 1024:
        raise ValueError(f'image over 20 MiB: {path}')
    mime = ('image/png' if raw.startswith(b'\x89PNG\r\n\x1a\n') else
            'image/jpeg' if raw.startswith(b'\xff\xd8\xff') else
            'image/webp' if raw.startswith(b'RIFF') and raw[8:12] == b'WEBP' else None)
    if not mime:
        raise ValueError('image must be PNG, JPEG or WebP')
    width, height = dimensions(raw)
    if width <= 0 or height <= 0:
        raise ValueError('image dimensions must be positive')
    # An absent lightweight preview is not a reason to decode the full evidence
    # image in a tiny catalog tile. The report still embeds the exact original.
    if catalog and (width*height > 960*960 or len(raw) > 120*1024):
        return None
    encoded = base64.b64encode(raw).decode('ascii')
    viewport = b.get('viewport')
    framed = (not original and selected != b['path'] and b.get('thumbnail_framed'if catalog else'preview_framed',False))
    if framed and abs(width - height * viewport['width'] / viewport['height']) > max(2, 2 * viewport['width'] / viewport['height']):
        raise ValueError('framed preview does not match its documented viewport; regenerate reading derivatives')
    style, wrapper_style = '', ''
    if viewport:
        v = viewport
        wrapper_style = f' style="--media-ratio:{v["width"]}/{v["height"]}"'
        style = ' style="width:100%;left:0;top:0"'if framed else(f' style="width:{v["source_width"]/v["width"]*100:.6f}%;'
                 f'left:{-v["x"]/v["width"]*100:.6f}%;top:{-v["y"]/v["height"]*100:.6f}%"')
    img = f'<img src="data:{mime};base64,{encoded}" alt="{esc(b["alt"])}" width="{width}" height="{height}" decoding="async" loading="{"eager" if preview else "lazy"}"{style}>'
    return f'<div class="media-view{" viewport" if viewport else ""}"{wrapper_style}>{img}</div>'


def first_image(product):
    images = [b for s in product['sections'] if s['id'] == 'ui' for b in s['blocks'] if b['type'] == 'image']
    return images[0] if images else None


def block_html(b, base_dir):
    kind, refs = b['type'], citations(b)
    if kind in ('paragraph', 'callout'):
        return f'<div class="{kind}"><p>{esc(b["text"])}</p>{refs}</div>'
    if kind == 'heading':
        return f'<h3>{esc(b["text"])}</h3>{refs}'
    if kind == 'list':
        return '<ul class="findings">' + ''.join(f'<li>{esc(t)}</li>' for t in b['items']) + '</ul>' + refs
    if kind == 'flow':
        return '<ol class="flow">' + ''.join(
            f'<li><span class="step">{i:02d}</span><strong>{esc(v["title"])}</strong><p>{esc(v["detail"])}</p></li>'
            for i, v in enumerate(b['items'], 1)) + '</ol>' + refs
    if kind == 'table':
        header = ''.join(f'<th scope="col">{esc(c)}</th>' for c in b['columns'])
        rows = ''.join('<tr>' + ''.join(f'<td data-label="{esc(b["columns"][i])}">{esc(c)}</td>' for i, c in enumerate(row)) + '</tr>' for row in b['rows'])
        return f'<div class="table-scroll" tabindex="0" role="region" aria-label="{esc(b.get("label", "分析表格 / Analysis table"))}"><table><thead><tr>{header}</tr></thead><tbody>{rows}</tbody></table></div>{refs}'
    original = ''
    if b.get('viewport') or b.get('preview_path'):
        full = {k: v for k, v in b.items() if k != 'viewport'}
        original = '<details class="original-image"><summary>完整原图 / Full source image</summary>'+image_html(full,base_dir,original=True)+'</details>'
    preview_note=''  # Full-source action already communicates the available original.
    return f'<figure>{image_html(b,base_dir)}<figcaption>{esc(b["caption"]+preview_note)}{refs}</figcaption>{original}</figure>'


def abstract_preview(p, lang):
    """A labelled product structure, never a fabricated app screenshot."""
    priority=p['visuals']['features'].get('priority')
    if priority:
        by_id={n['id']:n for m in p['visuals']['features']['modules']for n in m['features']}
        title='核心能力摘录'if lang.startswith('zh')else 'Selected core capabilities'
        states=atlas_words(lang)['short_states']
        items=''.join('<li><span aria-hidden="true">●</span><div><strong>'+esc(by_id[i]['label'])+'</strong><small>'+states[by_id[i]['status']]+'</small></div></li>'for i in priority['core'][:4])
        return f'<div class="abstract-preview semantic-preview"><span class="media-label">{title}</span><h3>{esc(priority["scope"])}</h3><ul>{items}</ul><a href="#map-features">'+('查看完整功能分层'if lang.startswith('zh')else 'Explore all capability tiers')+' ↓</a></div>'
    title = '功能结构概览' if lang.startswith('zh') else 'Capability overview'
    groups = ''.join(f'<div><strong>{esc(m["label"])}</strong><p>{" · ".join(esc(n["label"]) for n in m["features"][:3])}</p></div>' for m in p['visuals']['features']['modules'][:4])
    return f'<div class="abstract-preview"><span class="media-label">{title}</span>{groups}</div>'


def section_html(section, number, base_dir, lang):
    zh = lang.startswith('zh')
    sid, blocks = section['id'], section['blocks']
    rendered = [block_html(b, base_dir) for b in blocks]
    if section.get('summary_blocks'):
        summary = section['summary_blocks']
        refs = list(dict.fromkeys(s for b in summary for s in b.get('sources', [])))
        # The authored reading copy and the full research are distinct layers.
        # Keep claim text intact; the renderer never invents a shorter argument.
        reading = ''.join(block_html({k:v for k,v in b.items() if k!='sources'}, base_dir) for b in summary)
        if sid=='ui' and any(b['type']=='image'for b in summary):
            media=''.join(block_html({k:v for k,v in b.items()if k!='sources'},base_dir)for b in summary if b['type']=='image')
            notes=''.join(block_html({k:v for k,v in b.items()if k!='sources'},base_dir)for b in summary if b['type']!='image')
            sparse=len([b for b in summary if b['type']!='image'])<=1
            density=' sparse-notes'if sparse else ''
            note_label=''
            reading=f'<div class="ui-evidence-board{density}"><div class="ui-evidence-media">{media}</div><div class="ui-evidence-notes">{note_label}{notes}</div></div>'
        if refs:
            reading += ('<details class="evidence-refs"><summary>'+
                        ('查看依据' if zh else 'Evidence')+f'<span>{len(refs):02d}</span></summary>'+citations({'sources':refs})+'</details>')
        title = section.get('summary_title', section['title'])
        detail = section.get('detail_label', '完整分析与取证记录' if zh else 'Full analysis and evidence')
        return (f'<section class="chapter chapter-{esc(sid)}" id="{esc(sid)}">'
                f'<div class="chapter-title"><h2>{esc(title)}</h2></div>'
                f'<div class="reading-copy">{reading}</div><details class="chapter-more research-detail">'
                f'<summary>{esc(detail)}<span>＋</span></summary><div>{"".join(rendered)}</div></details></section>')
    if sid == 'ui':
        # Keep the inspected region beside its observations. Retain every
        # label, qualification and citation; grouping does not change evidence.
        for i in range(len(blocks) - 1):
            image, notes = blocks[i:i + 2]
            if image['type'] != 'image' or notes['type'] != 'table' or len(notes['columns']) != 3:
                continue
            annotations = ''.join(
                '<article class="ui-observation">'
                f'<h3><span>{j:02d}</span>{esc(row[0])}</h3>'
                f'<dl><dt>{esc(notes["columns"][1])}</dt><dd>{esc(row[1])}</dd>'
                f'<dt>{esc(notes["columns"][2])}</dt><dd>{esc(row[2])}</dd></dl></article>'
                for j, row in enumerate(notes['rows'], 1))
            viewport = image.get('viewport')
            layout = '' if viewport and viewport['width'] < viewport['height'] else ' ui-board-wide'
            rendered[i] = (f'<div class="ui-board{layout}">{rendered[i]}'
                           f'<div class="ui-observations" aria-label="{esc(notes["columns"][0])}">'
                           f'{annotations}{citations(notes)}</div></div>')
            rendered[i + 1] = ''
    details_label = '展开补充分析与证据' if zh else 'Supporting analysis and evidence'
    # A per-product presentation hint can demote repetitive supplemental material
    # without deleting it from the self-contained report or print output.
    keep = section.get('lead_blocks', len(rendered))
    keep = max(0, min(len(rendered), keep)) if type(keep) is int else len(rendered)
    if sid == 'validation':
        # An authored evidence/decision summary takes precedence over the
        # compact default. Keep protocols disclosed without hiding the finding.
        if 'lead_blocks' not in section:
            keep = min(1, len(rendered))
        details_label = '查看逐项问题、采集记录与下一步' if zh else 'Questions, acquisition records and next steps'
    tail = ''.join(rendered[keep:])
    body = ''.join(rendered[:keep]) + (f'<details class="chapter-more"><summary>{details_label}<span>＋</span></summary><div>{"".join(rendered[keep:])}</div></details>' if tail else '')
    return f'<section class="chapter chapter-{esc(sid)}" id="{esc(sid)}"><div class="chapter-title"><h2>{esc(section["title"])}</h2></div>{body}</section>'


def labels(lang):
    if lang.startswith('zh'):
        return dict(back='全部竞品', toc='报告目录', sources='证据与来源', print='打印 / PDF',
                    coverage='本报告的证据覆盖', dimensions=dict(ui='UI 风格', interaction='核心交互', technology='核心技术', business='商业与约束'),
                    status=dict(supported='已有支持', partial='部分覆盖', missing='材料缺失', out_of_scope='范围外'),
                    search='搜索名称、身份或机制', category='全部分类', count='份独立报告', empty='没有符合条件的报告。', read='阅读报告',
                    scope='阅读边界', key='核心判断', offline='离线 HTML · 无外部脚本、字体或图片依赖', source_note='外部网页是出处链接；本文件不自动加载，也不代表本轮重新访问。')
    return dict(back='All competitors', toc='Contents', sources='Evidence and sources', print='Print / PDF',
                coverage='Evidence coverage', dimensions=dict(ui='UI style', interaction='Interaction', technology='Technology', business='Business'),
                status=dict(supported='Supported', partial='Partial', missing='Missing', out_of_scope='Out of scope'),
                search='Search name, identity or mechanism', category='All categories', count='individual reports', empty='No matching reports.', read='Read report',
                scope='Reading boundary', key='Key finding', offline='Offline HTML · no external script, font or image dependency', source_note='External pages are source links; they are not loaded or reverified by this report.')


def shell(title, lang, body):
    css = (ASSETS / 'report.css').read_text(encoding='utf-8')
    css += '\n' + (ASSETS / 'atlas.css').read_text(encoding='utf-8')
    css += '\n' + (ASSETS / 'editorial.css').read_text(encoding='utf-8')
    css += '\n' + (ASSETS / 'reader.css').read_text(encoding='utf-8')
    css += '\n' + (ASSETS / 'design-spec.css').read_text(encoding='utf-8')
    css += '\n' + (ASSETS / 'workspace.css').read_text(encoding='utf-8')
    js = (ASSETS / 'reader.js').read_text(encoding='utf-8')+'\n'+(ASSETS / 'report.js').read_text(encoding='utf-8')
    return f'<!doctype html>\n<html lang="{esc(lang)}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"><title>{esc(title)}</title><style>{css}</style></head><body class="app-reader">{body}<script>{js}</script></body></html>'


def competitor_navigation(bundle, current=None):
    """One text-only, offline-capable collection navigator shared by all pages."""
    zh=bundle.get('lang','zh-CN').startswith('zh');products=bundle['products']
    name=next((p['name']for p in products if p['id']==current),'全部竞品'if zh else 'All competitors')
    items=''
    for i,p in enumerate(products,1):
        active=' aria-current="page"'if p['id']==current else ''
        search=' '.join((p['name'],p['category'],p['identity'])).casefold()
        items+=f'<li data-competitor-item data-search="{esc(search)}"><a class="competitor-link" href="{esc(p["id"])}.html" data-product-id="{esc(p["id"])}" title="{esc(p["category"])}"{active}><span>{i:02d}</span><strong>{esc(p["name"])}</strong></a></li>'
    collection_key=hashlib.sha256('\0'.join(p['id']for p in products).encode()).hexdigest()[:12]
    return f'''<aside class="competitor-sidebar" data-collection-key="{collection_key}"><details class="competitor-switcher" open><summary><span>{"切换竞品"if zh else "Switch competitor"}</span><strong>{esc(name)}</strong><span aria-hidden="true">⌄</span></summary><div class="competitor-panel"><div class="competitor-heading"><a href="index.html">{"研究档案"if zh else "Research library"}</a><span>{len(products):02d}</span></div><label class="competitor-search-label">{"搜索竞品"if zh else "Search competitors"}<input type="search" data-competitor-search placeholder="{"名称 / 类别"if zh else "Name / category"}" autocomplete="off"></label><div class="competitor-results"><span data-competitor-count role="status" aria-live="polite">{len(products)} / {len(products)}</span><button type="button" data-competitor-clear hidden>{"清除"if zh else "Clear"}</button></div><nav class="competitor-list" aria-label="{"竞品列表"if zh else "Competitor list"}"><ul>{items}</ul><p class="nav-empty" hidden>{"没有匹配的竞品"if zh else "No matching competitors"}</p></nav><p class="competitor-hint">{"切换报告时保留当前章节"if zh else "Switch reports at the current chapter"}</p></div></details></aside>'''


def report_page(bundle, product, number, base_dir):
    lang = bundle.get('lang', 'zh-CN')
    zh = lang.startswith('zh')
    l = labels(lang)
    p = product
    cov = ''.join(f'<div class="coverage-item {esc(c["status"])}"><span>{l["dimensions"][c["dimension"]]}</span><strong>{l["status"][c["status"]]}</strong><p>{esc(c["detail"])}</p></div>' for c in p['coverage'])
    chapters={}
    for i,s in enumerate(p['sections'],1):
        if p.get('design') and s['id']=='ui' and s.get('summary_blocks'):
            # Authored region inventory replaces the older duplicate bullet/flow
            # summary. Full research blocks and their sources remain untouched.
            s=dict(s,summary_title='界面分析'if zh else'Interface analysis',
                   summary_blocks=[dict(b,caption='')if b['type']=='image'else b for b in s['summary_blocks']if b['type']not in ('flow','list','table')])
        if p.get('design') and s['id']=='interaction':
            s=dict(s,summary_title='UX 交互分析'if zh else'UX interaction analysis')
        chapter=section_html(s,i,base_dir,lang)
        if p.get('design') and s['id']=='ui':
            chapter=chapter.replace('</h2></div>', '</h2>'+download_link(p)+'</div>', 1)
        if p.get('design') and s['id'] in ('ui','interaction'):
            panel=design_panel(p,lang) if s['id']=='ui' else ux_panel(p,lang)
            support=chapter.find('<details class="chapter-more')
            if s['id']=='interaction' and '<div class="reading-copy">' in chapter:
                start=chapter.index('<div class="reading-copy">')
                chapter=chapter[:start]+panel+chapter[support:]
            else:
                chapter=chapter[:support]+panel+chapter[support:] if support>=0 else chapter[:-10]+panel+'</section>'
        map_key={'ui':'screens','interaction':'journey','technology':'dataflow'}.get(s['id'])
        if map_key:
            chart=render_integrated_map(p['visuals'],map_key,p['name'],lang)
            if p.get('design') and s['id']=='interaction':
                support=chapter.find('<details class="chapter-more')
                chapter=chapter[:support]+chart+chapter[support:]
            elif s['id']in ('interaction','technology')and '<div class="reading-copy">'in chapter:
                chapter=chapter.replace('<div class="reading-copy">',chart+'<div class="reading-copy">',1)
            else:
                support=chapter.find('<details class="chapter-more')
                chapter=chapter[:support]+chart+chapter[support:]if support>=0 else chapter[:-len('</section>')]+chart+'</section>'
        chapters[s['id']]=chapter
    sources = ''
    for source in p['sources']:
        title = f'<a href="{esc(source["url"])}" target="_blank" rel="noopener noreferrer">{esc(source["title"])} ↗</a>' if source.get('url') else esc(source['title'])
        sources += f'<article class="source" id="source-{esc(source["id"])}"><div class="source-meta"><span class="source-id">{esc(source["id"])}</span><span>{esc(source["kind"])} · {esc(source["date"])}</span></div><h3>{title}</h3><details class="source-details"><summary>{"来源范围与定位" if zh else "Context and locator"}</summary><p>{esc(source["context"])}</p><code>{esc(source["locator"])}</code></details></article>'
    img = first_image(p)
    visual = (f'<a class="hero-image" href="#ui" aria-label="{esc("查看界面证据与分析" if zh else "Inspect interface evidence")}">{image_html(img,base_dir,True)}</a><div class="hero-media-caption"><span>{esc(img.get("status","已检查的图像材料" if zh else "Inspected visual evidence"))}</span><a href="#ui">{"查看分析" if zh else "View analysis"} ↗</a></div>' if img else route_excerpt(p["visuals"]["journey"],lang)or abstract_preview(p,lang))
    if img: visual+=route_excerpt(p['visuals']['journey'],lang,True)
    lead = p.get('presentation',{}).get('lead') or p['verdict'].split(' 需要权衡：')[0]
    purpose = ('<p class="product-purpose">'+esc(p['positioning']['summary'])+'</p>'+citations({'status':'公开资料归纳'if zh else 'Synthesis of product evidence','sources':p['positioning'].get('sources',[])})+'<span class="finding-label">'+('本报告发现'if zh else 'Study finding')+'</span>')if p.get('positioning')else ''
    headline = ''
    if p.get('brief'):
        purpose = ''
        lead = p['brief']['deck']
        headline = '<p class="hero-headline">'+esc(p['brief']['headline'])+'</p>'
    hero=f'''<header class="report-hero"><div class="hero-copy"><h1>{esc(p['name'])}</h1>{headline}{purpose}<p class="hero-lead">{esc(lead)}</p><div class="hero-actions"><a class="primary-link" href="#atlas">{"拆解产品" if zh else "Explore the product"}<span>↓</span></a><a href="#decisions">{"借鉴与取舍" if zh else "Product decisions"} ↗</a></div></div><div class="hero-visual {"has-evidence" if img else "capability-cover"}">{visual}</div></header>'''
    source_section=f'''<section id="sources" class="chapter"><div class="chapter-title"><h2>{l['sources']}</h2></div><p class="muted">{l['source_note']}</p><div class="source-list">{sources}</div></section>'''
    context=f'''<div class="study-context"><details class="scope"><summary>{l['scope']}</summary><p>{esc(p['scope'])}</p><div class="identity">{esc(p['identity'])}<br>{esc(p['version'])}</div></details><details class="evidence-overview"><summary>{l['coverage']}<span>{len(p['sources'])} {'条来源'if zh else'sources'}</span></summary><section class="coverage" aria-label="{l['coverage']}">{cov}</section></details></div>'''
    footer=f'''<footer><p>{esc(bundle["date"])}</p><a href="#sources">{l["sources"]}</a><a href="index.html">← {l["back"]}</a></footer>'''
    body=report_frame(product=p,number=number,count=len(bundle['products']),lang=lang,library=competitor_navigation(bundle,p['id']),hero=hero,chapters=chapters,atlas=integrated_overview(p['visuals'],p['name'],lang),sources=source_section,context=context,footer=footer,print_label=l['print'])
    return shell(f'{p["name"]} — {bundle["title"]}',lang,body+(design_template(p,base_dir,lang)if p.get('design')else''))


def index_page(bundle, base_dir=None):
    lang = bundle.get('lang','zh-CN');zh=lang.startswith('zh');l=labels(lang)
    products=bundle['products'];base_dir=Path(base_dir or '.')
    categories=list(dict.fromkeys(p['category'] for p in products))
    options=''.join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in categories)
    cover_items=[];cover_categories=set()
    for product in products:
        img=first_image(product)
        if img and product['category']not in cover_categories:
            preview=image_html(img,base_dir,catalog=True)
            if preview:
                cover_categories.add(product['category']);cover_items.append(f'<a class="collection-cover-item" href="{esc(product["id"])}.html">{preview}<span>{esc(product["name"])}</span></a>')
        if len(cover_items)==3:break
    collection_cover='<div class="collection-cover" aria-label="'+('已检查的产品图像摘录'if zh else 'Selected inspected product imagery')+'">'+''.join(cover_items)+'</div>'if cover_items else ''
    cards=''
    for i,p in enumerate(products,1):
        img=first_image(p)
        preview=image_html(img,base_dir,catalog=True) if img else None
        has_preview=bool(preview)
        if not preview:
            priority=p['visuals']['features'].get('priority')
            if priority:
                by_id={n['id']:n for m in p['visuals']['features']['modules']for n in m['features']}
                states=atlas_words(lang)['short_states']
                preview='<div class="catalog-mini semantic-mini">'+''.join(f'<div><span aria-hidden="true">●</span><div><strong>{esc(by_id[ident]["label"])}</strong><small>{states[by_id[ident]["status"]]}</small></div></div>'for ident in priority['core'][:3])+'</div>'
            else:
                groups = p['visuals']['features']['modules'][:3]
                preview = '<div class="catalog-mini">'+''.join(f'<div><span>{j:02d}</span><strong>{esc(m["label"])}</strong></div>' for j,m in enumerate(groups,1))+'</div>'
        if not has_preview and p['visuals']['journey'].get('focus'):
            preview=route_excerpt(p['visuals']['journey'],lang,True)
        if has_preview:
            preview='<div class="catalog-evidence">'+preview+'</div>'+route_excerpt(p['visuals']['journey'],lang,True)
        media_label='图像预览' if has_preview and zh else '功能概览' if zh else 'Image preview' if has_preview else 'Capability overview'
        if not has_preview and p['visuals']['features'].get('priority'):
            media_label=('任务路径摘录'if zh else 'Selected task route')if p['visuals']['journey'].get('focus')else('核心能力摘录'if zh else 'Selected core capabilities')
        search=' '.join(p[k] for k in ('name','identity','category','tagline','verdict'))
        lead=p.get('brief',{}).get('deck')or p.get('positioning',{}).get('summary')or p.get('presentation',{}).get('lead') or p['verdict'].split(' 需要权衡：')[0]
        n=sum(len(m['features']) for m in p['visuals']['features']['modules'])
        cards+=f'''<article class="report-card" data-search="{esc(search.casefold())}" data-category="{esc(p['category'])}"><a class="card-media" href="{esc(p['id'])}.html" aria-label="{esc(p['name'])}">{preview}<span class="card-media-label">{media_label}</span></a><div class="card-meta"><span>{esc(p['category'])}</span><span>{i:02d}</span></div><h2><a href="{esc(p['id'])}.html">{esc(p['name'])}</a></h2><div class="card-content"><p class="card-lead">{esc(lead)}</p><div class="card-bottom"><span>{n} {"功能节点" if zh else "capabilities"} · 4 {"张图" if zh else "maps"}</span><a href="{esc(p['id'])}.html">{l['read']} ↗</a></div></div></article>'''
    body=f'''<a class="skip" href="#main">{"跳到报告" if zh else "Skip to reports"}</a><header class="app-header"><span class="app-brand"><span aria-hidden="true">◈</span>{"竞品研究" if zh else "App Studies"}</span><span class="edition">{esc(bundle['date'])}</span></header><main class="reader-main index-main editorial-index" id="main"><header class="index-hero"><div><div class="eyebrow">{"产品、交互与技术" if zh else "Product, interaction and technology"}</div><h1>{esc(bundle['title'])}</h1><p>{"看清产品如何工作，<br>再决定什么值得借鉴。" if zh else "Understand how products work.<br>Decide what is worth adopting."}</p></div>{collection_cover}<div class="index-stat"><strong>{len(products):02d}</strong><span>{l['count']}<br>{len(categories)} {"种产品类别" if zh else "categories"}</span></div></header><details class="index-scope"><summary>{"研究范围与证据说明" if zh else "Research scope and evidence"}</summary><p>{esc(bundle['summary'])}</p></details><form class="filters" onsubmit="return false"><label>{l['search']}<input type="search" id="search" placeholder="{l['search']}" autocomplete="off"></label><label>{l['category']}<select id="category"><option value="">{l['category']}</option>{options}</select></label><span id="result-count" role="status" aria-live="polite">{len(products)} / {len(products)}</span></form><div class="report-grid">{cards}</div><p id="empty-results" hidden>{l['empty']}</p><footer><span>APP STUDIES</span><p>{esc(bundle['date'])} · {l['offline']}</p></footer></main>'''
    body=body.replace('<main class="reader-main index-main editorial-index"', '<div class="reader-app reader-collection">'+competitor_navigation(bundle)+'<main class="reader-main index-main editorial-index"',1)
    return shell(bundle['title'],lang,body+'</div>')


def render_bundle(data, output, base_dir=None, delivery_format="standalone"):
    validate_bundle(data)
    if delivery_format not in ("standalone", "linked"):
        raise ValueError("delivery format must be standalone or linked")
    output = Path(output)
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError('output must be a new or empty directory; existing work is preserved')
    base_dir = Path(base_dir or '.')
    pages = {p['id'] + '.html': report_page(data, p, i, base_dir) for i, p in enumerate(data['products'], 1)}
    pages['index.html'] = index_page(data, base_dir)
    assets = {}
    documents = {}
    for p in data['products']:
        if p.get('design'):
            md, images = design_markdown(p, base_dir, data.get('lang','zh-CN'))
            documents['design/'+p['id']+'/Design.md'] = md
            assets.update(images)
    if delivery_format == 'linked':
        pages, linked_assets = link_resources(pages)
        assets.update(linked_assets)
    manifest = {'schema_version': 1, 'date': data['date'], 'reports': [
        {'id': p['id'], 'name': p['name'], 'file': p['id'] + '.html', 'sha256': hashlib.sha256(pages[p['id'] + '.html'].encode()).hexdigest()}
        for p in data['products']], 'index_sha256': hashlib.sha256(pages['index.html'].encode()).hexdigest(),
        'input_sha256': hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
        'boundary': 'HTML delivery integrity, not semantic or runtime validation'}
    manifest['design_documents'] = [{'file':name,'sha256':hashlib.sha256(md.encode()).hexdigest()} for name,md in documents.items()]
    manifest['delivery_format'] = delivery_format
    manifest['assets'] = [{'file': name, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)} for name, raw in sorted(assets.items())]
    output.mkdir(parents=True, exist_ok=True)
    for name, raw in assets.items():
        asset_path = output / name
        asset_path.parent.mkdir(parents=True, exist_ok=True)
        asset_path.write_bytes(raw)
    for name, html in pages.items():
        (output / name).write_text(html, encoding='utf-8')
    for name,md in documents.items():
        target=output/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(md,encoding='utf-8')
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--format', dest='delivery_format', choices=('linked', 'standalone'), default='linked', help='linked (default): portable cached local assets; standalone: embed resources in each HTML')
    args = parser.parse_args()
    try:
        result = render_bundle(json.loads(args.bundle.read_text(encoding='utf-8')), args.output, args.bundle.parent, delivery_format=args.delivery_format)
    except (OSError, ValueError, TypeError, KeyError) as e:
        print(str(e), file=sys.stderr)
        return 1
    print(f'Wrote {len(result["reports"])} individual HTML reports plus index: {args.output}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
