"""Authored hierarchy and path emphasis; no product facts are inferred by layout."""
from visual_atlas import esc, refs, node_detail, templates, graph_components
from visual_composition import object_glyph


def labels(w):
    zh=w['nodes']=='节点'
    return dict(zh=zh,core='核心任务能力'if zh else 'Core task',supporting='支撑与前置'if zh else 'Support and prerequisites',extension='扩展与独立任务'if zh else 'Extensions and separate tasks',scope='本图分析范围'if zh else 'Analysis scope',analysis='按所选任务分层 · 分析判断，不代表使用频次或实际菜单'if zh else 'Task-based analysis, not usage ranking or navigation',main='重点路径'if zh else 'Selected path',branches='分支与回路'if zh else 'Branches and returns',other='其他入口与并行步骤'if zh else 'Other entries and parallel steps',limit='职责边界 / 证据止点'if zh else 'Responsibility / evidence boundary',technical='重点数据路径'if zh else 'Selected data path')


def feature_index(features,w):
    return '<details class="graph-index feature-index"><summary>'+w['feature_index']+'</summary>'+''.join('<h4>'+esc(m['label'])+'</h4><ul>'+''.join(f'<li id="features-index-{esc(n["id"])}">{node_detail(n,w)}</li>'for n in m['features'])+'</ul>'for m in features['modules'])+'</details>'


def capability_landscape(features,name,w):
    p=features['priority'];l=labels(w)
    nodes={n['id']:n for m in features['modules']for n in m['features']}
    groups={n['id']:i for i,m in enumerate(features['modules'])for n in m['features']}
    def leaf(ident):
        n=nodes[ident]
        return f'<li><a href="#features-index-{esc(ident)}" class="capability-item state-{esc(n["status"])}" data-node-detail="features-{esc(ident)}"><span class="capability-symbol" aria-hidden="true"></span><span class="capability-copy"><strong>{esc(n["label"])}</strong><span class="feature-meaning">{esc(n.get("caption",n["detail"]))}</span><small class="capability-evidence">{w["short_states"][n["status"]]}</small></span><span class="capability-open" aria-hidden="true">↗</span></a></li>'
    tiers=''
    for tier in ('core','supporting','extension'):
        if not p[tier]:continue
        # Group containment by actual original module; never draw task arrows here.
        cluster_ids={}
        for ident in p[tier]:cluster_ids.setdefault(groups[ident],[]).append(ident)
        clusters=''
        for i,(group,idents) in enumerate(cluster_ids.items(),1):
            clusters+=f'<section class="capability-cluster" data-module-index="{group}"><header><h5>{esc(features["modules"][group]["label"])}</h5></header><ul>'+''.join(leaf(ident)for ident in idents)+'</ul></section>'
        tiers+=f'<section class="capability-tier tier-{tier}" aria-label="{l[tier]}"><header><span class="tier-mark" aria-hidden="true">'+({'core':'●','supporting':'◐','extension':'○'}[tier])+f'</span><h4>{l[tier]}</h4></header><div class="capability-clusters">'+clusters+'</div></section>'
    basis='分层依据'if l['zh']else 'Basis of grouping'
    intro=f'<div class="capability-scope"><p class="semantic-eyebrow">{l["scope"]}</p><p class="semantic-statement">{esc(p["scope"])}</p><p>{esc(p["rationale"])}</p><div class="semantic-footnote">{l["analysis"]} <span>{len(nodes)} {w["features"]}</span></div><details class="semantic-basis"><summary>{basis}</summary><div class="citations">{refs(p)}</div></details></div>'
    return '<div class="capability-landscape">'+intro+tiers+'</div>'+templates(list(nodes.values()),'features',w)+feature_index(features,w)


def journey_spine(graph,w):
    f=graph['focus'];path=f['path'];l=labels(w);prefix='journey'
    by_id={n['id']:n for n in graph['nodes']}
    primary=set(zip(path,path[1:]));route={(e['from'],e['to']):e for e in graph['edges']}
    def node(n,stage=None):
        mark=f'{stage:02d}'if stage is not None else '↳'
        return f'<a id="journey-stage-{esc(n["id"])}" href="#journey-index-{esc(n["id"])}" class="journey-action state-{n["status"]}" data-node-detail="journey-{esc(n["id"])}"><span class="journey-stop" aria-hidden="true">{mark}</span><span><strong>{esc(n["label"])}</strong><span class="journey-caption">{esc(n.get("caption",n["detail"]))}</span><small>{w["short_states"][n["status"]]}</small></span><span class="journey-open" aria-hidden="true">↗</span></a>'
    def branch(e):
        return f'<li class="graph-edge journey-branch state-{e["status"]}" data-edge-from="{esc(e["from"])}" data-edge-to="{esc(e["to"])}"><span class="branch-symbol" aria-hidden="true">↳</span><div><strong>{esc(e["label"])}</strong><a href="#journey-stage-{esc(e["to"])}">{esc(by_id[e["to"]]["label"])}</a><small>{w["short_states"][e["status"]]}</small><span class="branch-refs">{refs(e)}</span></div></li>'
    rows='';branch_groups=''
    for i,ident in enumerate(path):
        n=by_id[ident];nextedge=route.get((ident,path[i+1]))if i<len(path)-1 else None
        connector=''
        if nextedge:
            continued=('接'if l['zh']else 'Next')+f' {i+2:02d}'
            connector=f'<div class="graph-edge spine-connector state-{nextedge["status"]}" data-edge-from="{esc(ident)}" data-edge-to="{esc(path[i+1])}"><span class="spine-line" aria-hidden="true"></span><span>{esc(nextedge["label"])}<small>{w["short_states"][nextedge["status"]]}</small><span class="step-next">{continued}</span></span></div>'
        outgoing=[e for e in graph['edges']if e['from']==ident and(e['from'],e['to'])not in primary]
        if outgoing:
            branch_groups+='<section class="journey-side"><h5><a href="#journey-stage-'+esc(ident)+'">'+esc(n['label'])+'</a></h5><ul>'+''.join(branch(e)for e in outgoing)+'</ul></section>'
        rows+=f'<li class="journey-row">{node(n,i+1)}{connector}</li>'
    extra=[n for n in graph['nodes']if n['id']not in path]
    extras=''
    if extra:
        groups=''
        for component in graph_components(graph):
            remaining=[n for n in component['nodes']if n['id']not in path]
            if not remaining:continue
            items=''
            for n in remaining:
                outgoing=[e for e in graph['edges']if e['from']==n['id']]
                items+='<li>'+node(n)+'<ul class="parallel-edges">'+''.join(branch(e)for e in outgoing)+'</ul></li>'
            groups+='<section class="parallel-group"><h5>'+esc(remaining[0]['label'])+'</h5><ul>'+items+'</ul></section>'
        extras=f'<section class="journey-parallel"><h4>{l["other"]}</h4><div>{groups}</div></section>'
    index=''
    for n in graph['nodes']:
        outgoing=''.join(f'<li><strong>{esc(e["label"])}</strong> → <a href="#journey-index-{esc(e["to"])}">{esc(by_id[e["to"]]["label"])}</a> <small>{w["short_states"][e["status"]]}</small> {refs(e)}</li>'for e in graph['edges']if e['from']==n['id'])
        index+=f'<li id="journey-index-{esc(n["id"])}">{node_detail(n,w)}<ul class="node-routes">{outgoing}</ul></li>'
    gap=any(route[pair]['status']in('inferred','unknown')for pair in zip(path,path[1:]))
    qualifier=('虚线段为推断或缺口；重点路径不等于已验证闭环。'if l['zh']else 'Dashed segments remain inferred or unknown; this is not a verified end-to-end flow.')if gap else ('路径为材料记载；本轮未据此宣称运行验收。'if l['zh']else 'The route follows the evidence, not a new runtime acceptance test.')
    rationale='<p>'+esc(f['rationale'])+'</p>'if f['rationale']!=graph.get('reading',{}).get('text')else ''
    branches=f'<section class="journey-branches"><h4>{l["branches"]}</h4><div>{branch_groups}</div></section>'if branch_groups else ''
    return f'<div class="journey-story"><header class="semantic-intro"><span class="semantic-eyebrow">{l["main"]}</span><h4>{esc(f["title"])}</h4>{rationale}<p class="semantic-footnote">{qualifier}</p></header><ol class="journey-spine" style="--steps:{len(path)}">{rows}</ol>{branches}{extras}</div>'+templates(graph['nodes'],prefix,w)+f'<details class="graph-index"><summary>{w["list"]}</summary><ul class="node-reading-list">{index}</ul></details>'


def technical_contract(graph,w):
    c=graph['contract'];b=c['boundary'];l=labels(w);by_id={n['id']:n for n in graph['nodes']}
    role_labels=dict(zip(('input','process','control','state','output','boundary'),('输入','变换','控制','保留状态','输出','未决边界')if l['zh']else('Input','Transform','Control','Retained state','Output','Unresolved')))
    chain=''
    for i,ident in enumerate(c['focus']):
        n=by_id[ident];role=c['roles'][ident]
        if i:
            edge=next(e for e in graph['edges']if e['from']==c['focus'][i-1]and e['to']==ident)
            chain+=f'<li class="contract-transfer state-{edge["status"]}"><span aria-hidden="true">→</span><small>{esc(edge["label"])}</small><small>{w["short_states"][edge["status"]]}</small></li>'
        chain+=f'<li class="contract-object role-{role}"><span class="technical-role">{role_labels[role]}</span>{object_glyph(role)}<a href="#dataflow-index-{esc(ident)}">{esc(n["label"])}</a><small>{w["short_states"][n["status"]]}</small></li>'
    key=''.join(f'<span class="role-key role-{r}"><i aria-hidden="true"></i>{label}</span>'for r,label in role_labels.items()if r in c['roles'].values())
    plate_class='technology-plate'+(' long-chain'if len(c['focus'])>4 else '')
    overview=f'<div class="contract-overview"><h4>{l["technical"]}</h4><ol class="contract-chain" tabindex="0" aria-label="{l["technical"]}">{chain}</ol></div>'
    boundary=f'<div class="technical-boundary"><div class="boundary-symbol" aria-hidden="true">⊣</div><div><span class="semantic-eyebrow">{l["limit"]}</span><h4>{esc(b["title"])}</h4><p>{esc(b["detail"])}</p><div class="citations">{refs(b)}</div></div></div>'
    return f'<div class="{plate_class}">{overview}<div class="technical-key">{key}</div>{boundary}</div>'
