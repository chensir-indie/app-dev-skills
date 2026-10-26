"""Evidence-derived visual primitives; they illustrate objects, not unseen app UI."""
from html import escape

def esc(x):return escape(str(x),quote=True)


def object_glyph(role):
    shapes={
      'input':'<path d="M10 14h35v35H10z M17 7h35v35"/><path d="m15 41 10-12 8 7 7-10"/><circle cx="22" cy="23" r="3"/>',
      'process':'<circle cx="31" cy="29" r="21"/><circle cx="31" cy="29" r="12"/><path d="M31 1v7m0 42v7M3 29h7m42 0h7M11 9l5 5m31 30 5 5M11 49l5-5M47 14l5-5"/>',
      'control':'<path d="M8 15h45M8 43h45"/><circle cx="22" cy="15" r="6"/><circle cx="41" cy="43" r="6"/>',
      'state':'<ellipse cx="31" cy="12" rx="21" ry="8"/><path d="M10 12v34c0 10 42 10 42 0V12M10 28c0 10 42 10 42 0"/>',
      'output':'<path d="M16 4h24l10 11v39H16z M39 4v12h11 M23 29h20 M23 37h20 M23 45h12"/>',
      'boundary':'<path stroke-dasharray="4 4" d="M20 5H8v48h12M42 5h12v48H42"/><path d="M31 16v17m0 8v3"/>'
    }
    return '<svg class="object-glyph glyph-'+esc(role)+'" viewBox="0 0 62 60" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">'+shapes[role]+'</svg>'


def route_excerpt(graph,lang='zh-CN',compact=False):
    """Consecutive nodes only; every connector is the original directed edge."""
    focus=graph.get('focus')
    if not focus:return ''
    zh=lang.startswith('zh');nodes={n['id']:n for n in graph['nodes']};ids=focus['path'][:3 if compact else 4]
    from visual_atlas import words
    states=words(lang)['short_states']
    rows=''
    for i,ident in enumerate(ids):
        n=nodes[ident]
        glyph='<svg class="scene-glyph" viewBox="0 0 80 80" fill="none" stroke="currentColor" aria-hidden="true"><circle cx="40" cy="40" r="24"/><path d="M8 27V8h19m26 0h19v19m0 26v19H53m-26 0H8V53"/><circle cx="40" cy="40" r="5"/></svg>'
        transfer=''
        if i<len(ids)-1:
            edge=next(e for e in graph['edges']if e['from']==ident and e['to']==ids[i+1])
            transfer='<span class="scene-transfer state-'+edge['status']+'"><i aria-hidden="true">→</i><small>'+esc(edge['label'])+'</small></span>'
        rows+='<li class="scene-stage state-'+n['status']+'"><span class="scene-number">'+f'{i+1:02d}'+'</span>'+glyph+'<strong>'+esc(n['label'])+'</strong><small>'+states[n['status']]+'</small>'+transfer+'</li>'
    label=('路径摘录'if zh else 'Selected route')+f' · {len(ids)}/{len(focus["path"])}'
    return '<div class="route-excerpt'+(' compact-route'if compact else '')+'"><span class="scene-label">'+label+'</span><ol style="--scene-steps:'+str(len(ids))+'">'+rows+'</ol></div>'
