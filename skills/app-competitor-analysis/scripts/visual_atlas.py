"""Offline, evidence-linked product trees and directed graphs. Python 3.9+."""
from html import escape
import re
import unicodedata

STATES = ('observed', 'declared', 'static', 'reported', 'inferred', 'unknown')
GRAPHS = ('journey', 'screens', 'dataflow')


def esc(value):
    return escape(str(value), quote=True)


def required(obj, key):
    if not isinstance(obj.get(key), str) or not obj[key].strip():
        raise ValueError(f'visuals: {key} requires text')


def evidence(item, sources):
    if item.get('status') not in STATES:
        raise ValueError('visuals: invalid evidence status')
    refs = item.get('sources', [])
    if not isinstance(refs, list) or any(s not in sources for s in refs):
        raise ValueError('visuals: unknown source')
    if item['status'] not in ('inferred', 'unknown') and not refs:
        raise ValueError('visuals: factual nodes and edges require sources')


def validate_visuals(v, sources):
    if not isinstance(v, dict) or set(v) != {'features', *GRAPHS}:
        raise ValueError('visuals: features, journey, screens and dataflow required')
    for diagram in v.values():
        for key in ('title', 'summary'):
            required(diagram, key)
        if 'reading' in diagram:
            reading = diagram['reading']
            if not isinstance(reading, dict):
                raise ValueError('visuals: reading requires an object')
            required(reading, 'text')
            if not isinstance(reading.get('sources'), list) or any(s not in sources for s in reading['sources']):
                raise ValueError('visuals: reading contains an unknown source')
    modules = v['features'].get('modules')
    if not isinstance(modules, list) or not modules:
        raise ValueError('visuals: feature modules required')
    ids = set()
    for module in modules:
        required(module, 'label')
        if not isinstance(module.get('features'), list) or not module['features']:
            raise ValueError('visuals: each module requires features or an explicit gap')
        for node in module['features']:
            validate_node(node, sources, ids)
    if 'priority' in v['features']:
        p = v['features']['priority']
        if not isinstance(p, dict):
            raise ValueError('visuals: priority requires an object')
        for key in ('scope', 'rationale'):
            required(p, key)
        validate_annotation_sources(p, sources)
        groups = [p.get(k) for k in ('core', 'supporting', 'extension')]
        if any(not isinstance(g, list) for g in groups) or not groups[0]:
            raise ValueError('visuals: priority requires a core and explicit supporting/extension lists')
        assigned = [i for g in groups for i in g]
        if len(assigned) != len(ids) or set(assigned) != ids:
            raise ValueError('visuals: priority must cover every capability exactly once')
    for key in GRAPHS:
        graph = v[key]
        nodes, edges = graph.get('nodes'), graph.get('edges')
        if not isinstance(nodes, list) or not nodes or not isinstance(edges, list) or not edges:
            raise ValueError('visuals: graph nodes and directed edges required')
        ids, positions = set(), set()
        for node in nodes:
            validate_node(node, sources, ids)
            for axis in ('col', 'row'):
                if type(node.get(axis)) is not int or not 0 <= node[axis] <= 12:
                    raise ValueError('visuals: bounded integer grid positions required')
            pos = (node['col'], node['row'])
            if pos in positions:
                raise ValueError('visuals: overlapping graph nodes')
            positions.add(pos)
        for edge in edges:
            if edge.get('from') not in ids or edge.get('to') not in ids:
                raise ValueError('visuals: dangling edge')
            required(edge, 'label')
            evidence(edge, sources)
        if key == 'journey' and 'focus' in graph:
            f = graph['focus']
            if not isinstance(f, dict):
                raise ValueError('visuals: focus requires an object')
            for field in ('title', 'rationale'):
                required(f, field)
            validate_annotation_sources(f, sources)
            validate_focus(f.get('path'), graph)
        if key == 'dataflow' and 'contract' in graph:
            c = graph['contract']
            if not isinstance(c, dict):
                raise ValueError('visuals: contract requires an object')
            roles = c.get('roles')
            if not isinstance(roles, dict) or set(roles) != ids or any(r not in ('input', 'process', 'control', 'state', 'output', 'boundary') for r in roles.values()):
                raise ValueError('visuals: technical roles must cover each node using responsibility roles, not guessed deployment locations')
            validate_focus(c.get('focus'), graph)
            boundary = c.get('boundary')
            if not isinstance(boundary, dict):
                raise ValueError('visuals: technical boundary requires an object')
            for field in ('title', 'detail'):
                required(boundary, field)
            validate_annotation_sources(boundary, sources)


def validate_annotation_sources(item, sources):
    refs = item.get('sources')
    if not isinstance(refs, list) or not refs or any(s not in sources for s in refs):
        raise ValueError('visuals: semantic annotation requires known sources')


def validate_focus(path, graph):
    ids = {n['id'] for n in graph['nodes']}
    edges = {(e['from'], e['to']) for e in graph['edges']}
    if not isinstance(path, list) or len(path) < 2 or len(path) != len(set(path)) or any(i not in ids for i in path) or any(pair not in edges or sum((e['from'],e['to']) == pair for e in graph['edges']) != 1 for pair in zip(path, path[1:])):
        raise ValueError('visuals: focus must follow existing directed edges without inventing a bridge')


def validate_node(node, sources, ids):
    for key in ('id', 'label', 'detail'):
        required(node, key)
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]*', node['id']) or node['id'] in ids:
        raise ValueError('visuals: unsafe or duplicate node id')
    ids.add(node['id'])
    if 'caption' in node:
        required(node,'caption')
        if len(wrap_label(node['caption'],26))>2:
            raise ValueError('visuals: caption must fit two lines; retain full qualification in detail and map reading')
    evidence(node, sources)


def words(lang):
    zh = lang.startswith('zh')
    return dict(
        title='产品图解' if zh else 'Product atlas',
        tabs=['功能全景', '核心任务', '页面关系', '技术链路', '展开全部'] if zh else ['Feature map', 'Task flow', 'Screen map', 'Data flow', 'Show all'],
        states=dict(zip(STATES, ['运行/像素观察', '第一方声明', '静态证据', '历史资料', '分析推断', '待核实'] if zh else ['Observed', 'Declared', 'Static', 'Reported', 'Inferred', 'Unknown'])),
        short_states=dict(zip(STATES, ['已观察', '官方声明', '静态证据', '历史资料', '推断', '待核实'] if zh else ['Observed', 'Declared', 'Static', 'Reported', 'Inferred', 'Unknown'])),
        hint='点击节点查看说明和来源；关系图可横向移动或放大。' if zh else 'Select a node for details and sources. Scroll or zoom relationship diagrams.',
        grouping='按能力分组，不代表实际菜单；节点标签标明证据类型。' if zh else 'Capability grouping, not a menu reproduction. Nodes show evidence type.',
        select='选择图中节点，查看它在产品里的作用与证据。' if zh else 'Select a node to inspect its role and evidence.',
        reset='原始大小' if zh else 'Reset',
        fit='适应宽度' if zh else 'Fit width',
        zoom_in='放大图谱' if zh else 'Zoom in',
        zoom_out='缩小图谱' if zh else 'Zoom out',
        list='图中全部节点与关系（文字索引）' if zh else 'Accessible index of nodes and relationships',
        feature_index='全部功能说明与来源（文字索引）' if zh else 'All capability details and sources',
        scope='结构依据' if zh else 'Map scope',
        evidence='证据标记' if zh else 'Evidence key',
        modules='模块' if zh else 'modules',
        features='功能节点' if zh else 'capabilities',
        nodes='节点' if zh else 'nodes',
        edges='关系' if zh else 'relationships',
        node_index='节点说明' if zh else 'Node details',
        edge_index='关系与触发条件' if zh else 'Relationships and triggers',
        reading='关系清单' if zh else 'Relationship list',
        drawing='查看图示' if zh else 'Show diagram',
        disconnected='分开的图组没有已知连接；不将它们画成连续步骤。' if zh else 'Separate groups have no evidenced connection; they are not a single sequence.',
    )


def refs(item):
    return ' '.join(f'<a href="#source-{esc(s)}">{esc(s)}</a>' for s in item.get('sources', []))


def node_detail(node, w):
    return f'<strong>{esc(node["label"])}</strong><span class="atlas-status state-{esc(node["status"])}">{w["states"][node["status"]]}</span><p>{esc(node["detail"])}</p><div class="citations">{refs(node)}</div>'


def templates(nodes, prefix, w):
    return ''.join(f'<template class="node-template" id="{prefix}-{esc(n["id"])}">{node_detail(n, w)}</template>' for n in nodes)


def feature_tree(features, name, w):
    if 'priority' in features:
        from semantic_atlas import capability_landscape
        return capability_landscape(features, name, w)
    modules, index_modules = '', ''
    all_nodes = []
    for i, m in enumerate(features['modules'], 1):
        nodes = ''
        for n in m['features']:
            all_nodes.append(n)
            nodes += f'<li><a href="#features-index-{esc(n["id"])}" class="feature-node state-{esc(n["status"])}" data-node-detail="features-{esc(n["id"])}"><strong>{esc(n["label"])}</strong><span class="feature-meaning">{esc(n.get("caption",n["detail"]))}</span><small title="{w["states"][n["status"]]}">{w["short_states"][n["status"]]}</small><span class="feature-open" aria-hidden="true">↗</span></a></li>'
        modules += f'<li class="feature-module"><h4><span class="module-number">{i:02d}</span><span class="module-label">{esc(m["label"])}</span><small>{len(m["features"])} {w["features"]}</small></h4><ul>{nodes}</ul></li>'
        index_nodes = ''.join(f'<li id="features-index-{esc(n["id"])}">{node_detail(n, w)}</li>' for n in m['features'])
        index_modules += f'<h4>{esc(m["label"])}</h4><ul>{index_nodes}</ul>'
    count = f'{len(features["modules"])} {w["modules"]} · {len(all_nodes)} {w["features"]}'
    index = f'<details class="graph-index feature-index"><summary>{w["feature_index"]}</summary>{index_modules}</details>'
    return f'<p class="map-caption">{w["grouping"]}</p><div class="feature-tree"><div class="feature-root"><strong>{esc(name)}</strong><span>{count}</span></div><ul class="feature-branches" style="--modules:{len(features["modules"])}">{modules}</ul></div>' + templates(all_nodes, 'features', w) + index


def wrap_label(label, limit=22):
    lines, line, size = [], '', 0
    for ch in label:
        unit = 2 if unicodedata.east_asian_width(ch) in 'WF' else 1
        if size + unit > limit or ch == '\n':
            lines.append(line)
            line, size = '', 0
        if ch != '\n':
            line += ch
            size += unit
    if line:
        lines.append(line)
    return lines or ['']


def graph_components(graph):
    """Compact disconnected evidence without inventing links or changing its order."""
    neighbors = {n['id']: set() for n in graph['nodes']}
    for edge in graph['edges']:
        neighbors[edge['from']].add(edge['to'])
        neighbors[edge['to']].add(edge['from'])
    visited, components = set(), []
    for start in graph['nodes']:
        if start['id'] in visited:
            continue
        stack, ids = [start['id']], set()
        while stack:
            ident = stack.pop()
            if ident in ids:
                continue
            ids.add(ident);stack.extend(neighbors[ident] - ids)
        visited.update(ids)
        nodes = [n for n in graph['nodes'] if n['id'] in ids]
        cols = {v:i for i,v in enumerate(sorted({n['col'] for n in nodes}))}
        rows = {v:i for i,v in enumerate(sorted({n['row'] for n in nodes}))}
        components.append(dict(graph, nodes=[dict(n,col=cols[n['col']],row=rows[n['row']])for n in nodes],
                               edges=[e for e in graph['edges'] if e['from'] in ids]))
    return components


def graph_svg(graph, prefix, w):
    if prefix == 'journey' and 'focus' in graph:
        from semantic_atlas import journey_spine
        return journey_spine(graph, w)
    components = graph_components(graph)
    drawings = ''.join(_graph_drawing(part, prefix, w, f'{prefix}-arrow-{i}') for i,part in enumerate(components,1))
    controls = f'<div class="graph-toolbar"><p>{len(graph["nodes"])} {w["nodes"]}<span>·</span>{len(graph["edges"])} {w["edges"]}</p><div class="graph-controls"><span class="graph-zoom"><button type="button" data-zoom="out" aria-label="{w["zoom_out"]}">−</button><button type="button" data-zoom="in" aria-label="{w["zoom_in"]}">＋</button><button type="button" data-zoom="fit">{w["fit"]}</button><button type="button" data-zoom="reset">{w["reset"]}</button></span><button type="button" data-diagram-layout>{w["reading"]}</button></div></div>'
    index_nodes = ''
    by_id = {n['id']: n for n in graph['nodes']}
    for n in graph['nodes']:
        routes = ''.join(f'<li class="route-state-{esc(e["status"])}" aria-label="{esc(n["label"])} → {esc(by_id[e["to"]]["label"])}"><span aria-hidden="true">→</span><div><strong>{esc(e["label"])}</strong><a href="#{prefix}-index-{esc(e["to"])}">{esc(by_id[e["to"]]["label"])}</a><small>{w["short_states"][e["status"]]}</small>{refs(e)}</div></li>' for e in graph['edges'] if e['from']==n['id'])
        outgoing = f'<ul class="node-routes">{routes}</ul>' if routes else ''
        index_nodes += f'<li id="{prefix}-index-{esc(n["id"])}">{node_detail(n,w)}{outgoing}</li>'
    note = f'<p class="map-caption disconnected-note">{w["disconnected"]}</p>' if len(components)>1 else ''
    index = f'<details class="graph-index"><summary>{w["list"]}</summary><ul class="node-reading-list">{index_nodes}</ul></details>'
    semantic = ''
    if prefix == 'dataflow' and 'contract' in graph:
        from semantic_atlas import technical_contract
        semantic = technical_contract(graph, w)
    return semantic + controls + note + f'<div class="graph-collection">{drawings}</div>' + templates(graph['nodes'],prefix,w) + index


def place_connector_label(path, preferred, size, nodes, occupied):
    """Choose free space on this connector instead of covering another argument."""
    tokens=re.findall(r'[MHV]|-?[\d.]+',path)
    points=[];position=None;i=0
    while i<len(tokens):
        op=tokens[i];i+=1
        if op=='M':position=(float(tokens[i]),float(tokens[i+1]));i+=2;continue
        target=(float(tokens[i]),position[1])if op=='H'else(position[0],float(tokens[i]));i+=1
        for ratio in (.5,.25,.75,.12,.88):
            points.append((position[0]+(target[0]-position[0])*ratio,position[1]+(target[1]-position[1])*ratio))
        position=target
    w,h=size
    candidates=[preferred]+sorted(points,key=lambda p:abs(p[0]-preferred[0])+abs(p[1]-preferred[1]))
    def overlap(a,b,pad=6):
        return a[0]<b[0]+b[2]+pad and a[0]+a[2]+pad>b[0]and a[1]<b[1]+b[3]+pad and a[1]+a[3]+pad>b[1]
    for x,y in candidates:
        box=(x-w/2,y-h/2,w,h)
        if min(box[:2])<12:continue
        if not any(overlap(box,n)for n in nodes)and not any(overlap(box,other)for other in occupied):
            return x,y
    # Preserve the authored route for inspection; the geometry audit reports a
    # remaining collision rather than silently deleting its condition.
    return max(12+w/2,preferred[0]),max(12+h/2,preferred[1])


def _graph_drawing(graph, prefix, w, marker_id):
    nodes = graph['nodes']
    by_id = {n['id']: n for n in nodes}
    contract=graph.get('contract', {})
    focus=contract.get('focus', [])
    focused_edges=set(zip(focus,focus[1:]))
    # Geometry and the 16px/13px type ramp are one drawing contract.
    # The gutter reserves space for conditions beside the actual route.
    node_w,col_step=232,352
    node_h=max(128,max(32+23*len(wrap_label(n['label'],24))+18*len(wrap_label(n['caption'],26))+30 if n.get('caption') else 112 for n in nodes))
    row_step=node_h+112
    half_w, half_h = node_w / 2, node_h / 2
    width = 124 + max(n['col'] for n in nodes) * col_step + node_w
    # Reserve the final return-arrow lane and its labels below the last row.
    height = node_h+160 + max(n['row'] for n in nodes) * row_step
    svg_edges, svg_labels, svg_nodes, index_edges = '', '', '', ''
    label_bounds=[];occupied=[]
    node_boxes=[(60+n['col']*col_step,54+n['row']*row_step,node_w,node_h)for n in nodes]
    for i, edge in enumerate(graph['edges']):
        a, b = by_id[edge['from']], by_id[edge['to']]
        ax, ay = 60 + a['col'] * col_step, 54 + a['row'] * row_step
        bx, by = 60 + b['col'] * col_step, 54 + b['row'] * row_step
        if edge['from'] == edge['to']:
            # A self-loop must remain a loop, rather than a zero-length line.
            route = ax + node_w + 38
            lane = ay + node_h + 34
            path = f'M {ax+node_w} {ay+half_h} H {route} V {lane} H {ax+half_w} V {ay+node_h}'
            lx, ly = (ax+half_w+route)/2, lane
        elif a['col'] == b['col'] and a['row'] < b['row']:
            # Long skips run beside the column, never through intermediate nodes.
            if b['row'] == a['row'] + 1:
                path = f'M {ax+half_w} {ay+node_h} V {by}'
                lx, ly = ax+half_w, (ay+node_h+by)/2
            else:
                route = ax+node_w+72
                path = f'M {ax+node_w} {ay+half_h} H {route} V {by+half_h} H {bx+node_w}'
                lx, ly = route, (ay+by)/2+half_h
        elif b['col'] == a['col'] + 1:
            # Horizontal branches use a free gutter; authored grids keep it clear.
            mx = ax+node_w+72
            path = f'M {ax+node_w} {ay+half_h} H {mx} V {by+half_h} H {bx}'
            lx, ly = ((ax+node_w+bx)/2, ay+half_h) if ay == by else (mx, (ay+by)/2+half_h)
        elif a['row'] == b['row']:
            # A return or long skip goes below this row, not through siblings.
            lane = ay+node_h+32+(i % 3)*14
            path = f'M {ax+half_w} {ay+node_h} V {lane} H {bx+half_w} V {by+node_h}'
            lx, ly = (ax+bx)/2+half_w, lane
        else:
            # Long/backward links use an outer gutter and inter-row lanes.
            # This keeps arrows out of unrelated nodes even in dense maps.
            down = by > ay
            sy, ty = (ay+node_h, by) if down else (ay, by+node_h)
            lane1, lane2 = (ay+node_h+34, by-28) if down else (ay-28, by+node_h+34)
            route = 22+(i % 2)*10 if bx <= ax else width-26-(i % 2)*10
            path = f'M {ax+half_w} {sy} V {lane1} H {route} V {lane2} H {bx+half_w} V {ty}'
            lx, ly = (ax+half_w+route)/2, lane1
        uncertain = edge['status'] in ('inferred', 'unknown')
        edge_label = edge['label']
        label_lines = wrap_label(edge_label, 12)
        label_h = 18*len(label_lines)+8
        label_w = min(104, max(44, max(sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in l) for l in label_lines)*7+16))
        lx,ly=place_connector_label(path,(lx,ly),(label_w,label_h),node_boxes,occupied)
        occupied.append((lx-label_w/2,ly-label_h/2,label_w,label_h))
        label_bounds.append((lx+label_w/2,ly+label_h/2))
        emphasis=' focus-edge' if (edge['from'],edge['to']) in focused_edges else ''
        svg_edges += f'<g class="graph-edge {"uncertain" if uncertain else "supported"}{emphasis}" data-edge-from="{esc(edge["from"])}" data-edge-to="{esc(edge["to"])}"><title>{esc(edge["label"])} · {w["states"][edge["status"]]} · {esc(", ".join(edge.get("sources", [])))}</title><path d="{path}" marker-end="url(#{marker_id})"/></g>'
        svg_labels += f'<g class="graph-edge-label"><rect x="{lx-label_w/2}" y="{ly-label_h/2}" width="{label_w}" height="{label_h}" rx="4"/>'
        for j, line in enumerate(label_lines):
            svg_labels += f'<text x="{lx}" y="{ly-label_h/2+17+j*18}">{esc(line)}</text>'
        svg_labels += '</g>'
        index_edges += f'<li>{esc(a["label"])} → {esc(b["label"])}：{esc(edge["label"])} <small>({w["states"][edge["status"]]})</small> {refs(edge)}</li>'
    for n in nodes:
        x, y = 60+n['col']*col_step, 54+n['row']*row_step
        lines = wrap_label(n['label'], 24)
        if len(lines) > 3:
            raise ValueError('visuals: graph label too long; put explanation in detail')
        role=contract.get('roles',{}).get(n['id'])
        role_attr=f' data-semantic-role="{role}"' if role else ''
        role_class=f' role-{role}' if role else (' screen-surface' if prefix=='screens' else '')
        selected=' focus-node' if n['id'] in focus else ''
        radius=32 if role=='process' else 2 if role else 12
        svg_nodes += f'<a href="#{prefix}-index-{esc(n["id"])}" class="graph-node state-{esc(n["status"])}{role_class}{selected}"{role_attr} data-node-detail="{prefix}-{esc(n["id"])}" aria-label="{esc(n["label"])}: {w["states"][n["status"]]}"><rect x="{x}" y="{y}" width="{node_w}" height="{node_h}" rx="{radius}"/>'
        if role=='input':
            svg_nodes+=f'<path class="role-glyph" d="M {x+10} {y+4} H {x} V {y+node_h-4} H {x+10}"/>'
        elif role=='state':
            svg_nodes+=f'<path class="role-glyph" d="M {x} {y+9} C {x} {y-4} {x+node_w} {y-4} {x+node_w} {y+9} V {y+node_h-9} C {x+node_w} {y+node_h+4} {x} {y+node_h+4} {x} {y+node_h-9} Z M {x} {y+9} C {x} {y+22} {x+node_w} {y+22} {x+node_w} {y+9}"/>'
        elif role=='control':
            svg_nodes+=f'<path class="role-glyph" d="M {x+node_w-24} {y+node_h-28} l 6 6 l -6 6 l -6 -6 Z M {x} {y+node_h} H {x+node_w}"/>'
        elif role=='output':
            svg_nodes+=f'<path class="role-glyph" d="M {x+node_w} {y} V {y+node_h} M {x+node_w+5} {y} V {y+node_h}"/>'
        elif prefix=='screens':
            svg_nodes+=f'<path class="screen-chrome" d="M {x+12} {y+10} h 25"/>'
        for j, line in enumerate(lines):
            svg_nodes += f'<text class="node-label" x="{x+18}" y="{y+32+j*23}">{esc(line)}</text>'
        for j,line in enumerate(wrap_label(n['caption'],26) if n.get('caption')else []):
            svg_nodes+=f'<text class="node-caption" x="{x+18}" y="{y+36+len(lines)*23+j*18}">{esc(line)}</text>'
        svg_nodes += f'<circle class="node-state-dot" cx="{x+22}" cy="{y+node_h-20}" r="3"/><text class="node-state" x="{x+32}" y="{y+node_h-16}">{w["short_states"][n["status"]]}</text><path class="node-open" d="M {x+node_w-29} {y+node_h-24} h 9 v 9 m 0 -9 l -9 9"/></a>'
    width=max(width,max((x+20 for x,y in label_bounds),default=0))
    height=max(height,max((y+20 for x,y in label_bounds),default=0))
    return f'<div class="graph-scroll" tabindex="0" role="region" aria-label="{esc(graph["title"])}"><svg class="graph-svg" viewBox="0 0 {width} {height}" style="--diagram-width:{width}px" role="group" aria-label="{esc(graph["title"])}"><defs><marker id="{marker_id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker></defs>{svg_edges}{svg_labels}{svg_nodes}</svg></div>'


def render_integrated_map(v, key, name, lang):
    w=words(lang);i=('features',*GRAPHS).index(key)+1;d=v[key]
    titles=['功能结构','任务路径','界面关系','数据与处理'] if lang.startswith('zh') else ['Capability structure','Task paths','Screen relationships','Data and processing']
    reading=d.get('reading',{'text':d['summary'],'sources':[]})
    content=feature_tree(d,name,w) if key=='features' else graph_svg(d,key,w)
    scope=f'<details class="atlas-description"><summary>{w["scope"]}</summary><p>{esc(d["summary"])}</p></details>'
    return f'<section id="map-{key}" class="atlas-panel diagram-section" data-atlas-panel="{key}" aria-label="{esc(d["title"])}"><header class="diagram-heading"><div><h3>{titles[i-1]}</h3></div><p>{esc(reading["text"])}</p></header>{content}<div class="diagram-provenance">{refs(reading)}{scope}</div><div class="node-inspector" role="status" aria-live="polite"><p>{w["select"]}</p></div></section>'


def integrated_overview(v,name,lang):
    w=words(lang)
    links=''.join(f'<a href="#map-{key}"><span>{i:02d}</span>{label}<span aria-hidden="true">↗</span></a>'for i,(key,label)in enumerate(zip(('features',*GRAPHS),w['tabs'][:4]),1))
    legend=''.join(f'<span class="state-{key}">{value}</span>'for key,value in w['states'].items())
    return f'<section id="atlas" class="visual-atlas integrated-overview"><div class="chapter-title"><h2>{w["title"]}</h2></div><nav class="map-directory" aria-label="{w["title"]}">{links}</nav><details class="atlas-key"><summary>{w["evidence"]}</summary><div class="atlas-legend">{legend}</div></details>{render_integrated_map(v,"features",name,lang)}</section>'


def render_visuals(v, name, lang, compact=False):
    w = words(lang)
    buttons = ''.join(f'<button type="button" data-atlas-view="{key}" aria-pressed="false"><span aria-hidden="true">{f"{i:02d}" if key != "all" else "+"}</span>{label}</button>' for i, (key, label) in enumerate(zip(('features', *GRAPHS, 'all'), w['tabs']), 1))
    panels = ''
    for i, key in enumerate(('features', *GRAPHS), 1):
        d = v[key]
        content = feature_tree(d, name, w) if key == 'features' else graph_svg(d, key, w)
        description = ('<details class="atlas-description"><summary>'+('图谱范围' if lang.startswith('zh') else 'Map scope')+'</summary><p>'+esc(d['summary'])+'</p></details>') if compact else '<p>'+esc(d['summary'])+'</p>'
        panels += f'<section class="atlas-panel" data-atlas-panel="{key}" aria-label="{esc(d["title"])}"><header class="atlas-panel-head"><span>MAP {i:02d}</span><h3>{esc(d["title"])}</h3>{description}</header>{content}<div class="node-inspector" role="status" aria-live="polite"><p>{w["select"]}</p></div></section>'
    legend = ''.join(f'<span class="state-{key}">{value}</span>' for key, value in w['states'].items())
    return f'<section id="atlas" class="visual-atlas"><div class="chapter-title"><h2>{w["title"]}</h2></div><p class="atlas-hint">{w["hint"]}</p><div class="atlas-tabs" aria-label="{w["title"]}">{buttons}</div><details class="atlas-key"><summary>{w["evidence"]}</summary><div class="atlas-legend">{legend}</div></details>{panels}</section>'
