"""Source-linked Design.md export and concise UI/UX reader components.

Only renders authored records. No visual tokens or UX judgments are inferred here.
"""
import hashlib
from html import escape
from pathlib import Path
from media_info import dimensions

RULES={'color':'颜色与语义','typography':'文字层级','spacing':'布局与间距','shape':'形状与层次','iconography':'图标与标签','imagery':'图像与内容','motion':'动效与反馈','responsive':'适配与方向','accessibility':'可访问性'}
EN_RULES=dict(zip(RULES,['Color roles','Typography','Layout and spacing','Shape and layering','Icons and labels','Imagery and content','Motion and feedback','Responsive behavior','Accessibility']))
STATES={'observed':'图像观察','declared':'来源声明','inferred':'分析推断','unknown':'未确认','measured':'实测取值','reported':'历史记录'}
EN_STATES={'observed':'Observed pixels','declared':'Declared','inferred':'Inferred','unknown':'Unknown','measured':'Measured','reported':'Historical record'}

def text(obj,key):
    if not isinstance(obj.get(key),str)or not obj[key].strip():raise ValueError('design: '+key+' must be nonempty text')

def validate_design(p):
    if 'design'not in p:return
    d=p['design'];known={x['id']for x in p['sources']}
    if not isinstance(d,dict):raise ValueError('design must be an object')
    for key in ('scope','intent'):text(d,key)
    if d.get('coverage')not in ('partial','available_material_complete','no_ui_pixels'):raise ValueError('design coverage invalid')
    def evidence(x):
        if x.get('status')not in STATES:raise ValueError('design status invalid')
        if not isinstance(x.get('sources'),list)or any(s not in known for s in x['sources']):raise ValueError('design unknown source')
        if x['status']not in ('unknown','inferred')and not x['sources']:raise ValueError('design source required')
    for key in ('regions','rules','components'):
        if not isinstance(d.get(key),list):raise ValueError('design '+key+' array required')
    if sorted(x.get('category','')for x in d['rules'])!=sorted(RULES):raise ValueError('design all rule categories required once')
    for x in d['rules']:
        evidence(x)
        if x['status']=='unknown':
            if x.get('value')is not None:raise ValueError('design unknown value must be null')
            text(x,'verify')
        else:text(x,'value')
        if x['status']=='measured':text(x,'method')
    for x in d['regions']:
        evidence(x)
        for k in ('name','role'):text(x,k)
        if not isinstance(x.get('elements'),list)or not x['elements']or any(not isinstance(s,str)or not s.strip()for s in x['elements']):raise ValueError('design region elements required')
    for x in d['components']:
        evidence(x)
        for k in ('name','anatomy','shown','unknown','verify'):text(x,k)
    u=d.get('ux')
    if not isinstance(u,dict):raise ValueError('design ux required')
    for k in ('goal','entry','object','choice','feedback','recovery','completion'):text(u,k)
    if not isinstance(u.get('findings'),list)or not u['findings']:raise ValueError('design ux findings required')
    for f in u['findings']:
        evidence(f)
        for k in ('title','observation','consequence','alternative','decision'):text(f,k)
        protocol=f.get('protocol')
        if not isinstance(protocol,dict)or protocol.get('status')!='not_run':raise ValueError('design protocol is a planned check; results belong in study records')
        for k in ('start','action','pass_result','reverse'):text(protocol,k)


def e(value):return escape(str(value),quote=True)
def refs(record,zh=True):
    sources=record.get('sources',[])
    if not sources:return ''
    return '<details class="design-evidence"><summary>'+('依据'if zh else'Evidence')+'</summary><span class="design-citations">'+''.join('<a href="#source-'+e(s)+'">'+e(s)+'</a>'for s in sources)+'</span></details>'

def download_link(p):
    return '<a class="design-download" href="design/'+e(p["id"])+'/Design.md" target="_blank" rel="noopener">Design.md ↗</a>'

def design_panel(p,lang):
    d=p['design'];zh=lang.startswith('zh');labels=RULES if zh else EN_RULES;states=STATES if zh else EN_STATES
    cards=''.join('<article><h4>'+e(x['name'])+'</h4><ul>'+''.join('<li>'+e(y)+'</li>'for y in x['elements'])+'</ul><p>'+e(x['role'])+'</p>'+refs(x,zh)+'</article>'for x in d['regions'])
    rules=''.join('<div><dt>'+labels[x['category']]+'</dt><dd>'+e(x.get('value')or x['verify'])+'<span class="design-state">'+states[x['status']]+'</span>'+refs(x,zh)+'</dd></div>'for x in d['rules'])
    # Focus visible facts; the complete inventory has a native disclosure and MD export.
    return '<section class="design-study" id="design-system"><header><div><h3>'+('界面设计系统'if zh else'Interface design system')+'</h3><p>'+e(d['intent'])+'</p></div></header><p class="design-boundary">'+e(d['scope'])+'</p>'+(('<div class="design-regions">'+cards+'</div>')if cards else '')+'<details class="design-rules"><summary>'+('视觉规则与未确认状态'if zh else'Visual rules and open states')+'</summary><dl>'+rules+'</dl></details></section>'

def ux_panel(p,lang):
    u=p['design']['ux'];zh=lang.startswith('zh')
    summaries=[('关键选择'if zh else'Choice',u['choice']),('反馈与完成'if zh else'Feedback and result',u['feedback']+' '+u['completion']),('恢复与连续使用'if zh else'Recovery',u['recovery'])]
    cards=''.join('<article><h4>'+a+'</h4><p>'+e(b)+'</p></article>'for a,b in summaries)
    findings=''
    for f in u['findings']:
        pr=f['protocol'];pairs=[('另一种解释'if zh else'Alternative',f['alternative']),('取舍'if zh else'Decision',f['decision']),('验证起点'if zh else'Start',pr['start']),('验证动作'if zh else'Action',pr['action']),('通过条件'if zh else'Pass',pr['pass_result']),('推翻条件'if zh else'Reversal',pr['reverse'])]
        findings+='<article class="ux-finding"><h4>'+e(f['title'])+'</h4><p>'+e(f['observation'])+'</p><p class="ux-judgment">'+e(f['consequence'])+'</p>'+refs(f,zh)+'<details><summary>'+('反解释、取舍与验证'if zh else'Alternatives, decision and validation')+'</summary><dl>'+''.join('<div><dt>'+a+'</dt><dd>'+e(b)+'</dd></div>'for a,b in pairs)+'</dl><p class="design-state">'+('验证尚未执行'if zh else'Planned; not run')+'</p></details></article>'
    return '<section class="ux-review" id="ux-review"><h3>'+('用户要完成什么'if zh else'The user’s goal')+'</h3><p class="ux-goal">'+e(u['goal'])+'</p><div class="ux-priorities">'+cards+'</div>'+findings+'</section>'


def md_text(v):return str(v).replace('|','\\|').replace('\n','<br>')
def table(head,rows):return '\n'+' | '.join(head)+'\n'+' | '.join('---'for _ in head)+'\n'+'\n'.join(' | '.join(md_text(v)for v in row)for row in rows)+'\n'

def design_markdown(p,base_dir,lang):
    d=p['design'];u=d['ux'];zh=lang.startswith('zh');states=STATES if zh else EN_STATES;labels=RULES if zh else EN_RULES
    pid=p['id'];report='../../'+pid+'.html';assets={}
    def citations(x):return ' '.join('['+s+']('+report+'#source-'+s+')'for s in x.get('sources',[]))
    def title(cn,en):return cn if zh else en
    out=['# '+p['name']+' · Design.md','',d['intent'],'',
         '**'+title('覆盖边界','Coverage')+'** — '+d['scope'],'',
         title('本文是基于现有证据的设计拆解；未确认的字体、数值与运行状态保留未知，不构成完整应用复刻规范。','This is an evidence-bounded teardown, not a verified reconstruction of every application state.'),'',
         '- '+p['platform']+' · '+p['version'],'- '+p['identity'],
         '- ['+title('完整报告','Full report')+']('+report+'#ui) · ['+title('功能图','Capabilities')+']('+report+'#map-features) · ['+title('技术图','Technology')+']('+report+'#map-dataflow)',
         '\n## '+title('设计意图与核心对象','Intent and core object'),'\n'+u['goal'],'\n'+title('入口：','Entry: ')+u['entry'],'\n'+title('持续对象：','Persistent object: ')+u['object'],
         '\n## '+title('已检查图像','Inspected imagery')]
    seen=set()
    for s in p['sections']:
        if s['id']!='ui':continue
        for b in s['blocks']:
            if b['type']!='image'or b['path']in seen:continue
            seen.add(b['path']);raw=(Path(base_dir)/b['path']).read_bytes();suffix='.png'if raw.startswith(b'\x89PNG')else'.jpg'if raw.startswith(b'\xff\xd8')else'.webp'
            path='assets/'+hashlib.sha256(raw).hexdigest()+suffix;assets[path]=raw
            w,h=dimensions(raw);out+=['\n['+b['alt']+'](../../'+path+') — '+str(w)+' × '+str(h)+' px. '+b['caption']+' '+citations(b)]
    if not seen:out+=['\n'+title('无可检查的应用界面像素；以下文档声明不补成视觉事实。','No inspectable app pixels; documented controls remain declarations.')]
    out+=['\n## '+title('页面与状态清单','Screen and state inventory')]
    graph=p['visuals']['screens'];out+=[table([title('区域/状态','Screen / state'),title('内容与边界','Content and boundary'),title('证据','Evidence')],[(n['label'],n['detail'],states.get(n['status'],n['status'])+' '+citations(n))for n in graph['nodes']])]
    out+=['\n## '+title('逐区域元素与信息层级','Elements and hierarchy')]
    for i,r in enumerate(d['regions'],1):
        out+=['\n### '+str(i)+'. '+r['name'],'\n'+r['role'],'\n'+'\n'.join('- '+x for x in r['elements']),'\n'+states[r['status']]+' · '+citations(r)]
    if not d['regions']:out+=['\n'+title('当前材料不足以列出真实可见控件；补图后按完整区域顺序复核。','Visible controls cannot be inventoried from the current evidence.')]
    out+=['\n## '+title('设计规则与语义变量','Design rules and semantic tokens')]
    for r in d['rules']:
        out+=['\n### '+labels[r['category']],'\n'+(r.get('value')or title('未确认 / null','Unknown / null')),'\n'+states[r['status']]+' '+citations(r)]
        if r.get('method'):out+=['\n'+title('测量方法：','Method: ')+r['method']]
        if r.get('verify'):out+=['\n'+title('补齐方式：','Next observation: ')+r['verify']]
    out+=['\n## '+title('组件结构与状态矩阵','Component anatomy and states')]
    for c in d['components']:
        out+=['\n### '+c['name'],table([title('字段','Field'),title('合同','Contract')],[(title('结构','Anatomy'),c['anatomy']),(title('已有状态','Shown'),c['shown']),(title('待证状态','Unknown states'),c['unknown']),(title('验证方法','Check'),c['verify']),(title('证据','Evidence'),states[c['status']]+' '+citations(c))])]
    out+=['\n## '+title('UX 交互评审','UX interaction review'),table([title('关注点','Concern'),title('本产品判断','Product-specific record')],[(title('任务与入口','Task and entry'),u['goal']+' '+u['entry']),(title('心智对象与选择','Mental model and choice'),u['object']+' '+u['choice']),(title('系统反馈与控制','Feedback and control'),u['feedback']),(title('恢复与连续使用','Recovery and continuity'),u['recovery']),(title('完成与信任','Completion and trust'),u['completion'])])]
    for f in u['findings']:
        pr=f['protocol'];out+=['\n### '+f['title'],table([title('推理环节','Reasoning'),title('记录','Record')],[(title('证据','Evidence'),f['observation']+' '+citations(f)),(title('影响假设','Consequence hypothesis'),f['consequence']),(title('反解释','Alternative'),f['alternative']),(title('取舍','Decision'),f['decision']),(title('验证起点','Start'),pr['start']),(title('动作','Action'),pr['action']),(title('通过条件','Pass'),pr['pass_result']),(title('推翻条件','Reversal'),pr['reverse']),(title('执行状态','Execution'),'not_run')])]
    out+=['\n## '+title('完整任务与设计研究','Full task and design research'), '\n['+title('完整任务、分支与回路','Task, branches and returns')+']('+report+'#map-journey)']
    # Preserve authored detailed observations, including all evidence qualifiers.
    for s in p['sections']:
        if s['id']not in ('ui','interaction'):continue
        out+=['\n### '+s['title']]
        for b in s['blocks']:
            kind=b['type']
            if kind=='image':continue
            if kind=='table':out+=[table(b['columns'],b['rows'])]
            elif kind=='list':out+=['\n'+'\n'.join('- '+v for v in b['items'])]
            elif kind=='flow':out+=['\n'+'\n'.join(str(i)+'. '+v['title']+' — '+v['detail']for i,v in enumerate(b['items'],1))]
            else:out+=['\n'+('#### 'if kind=='heading'else'')+b['text']]
            if b.get('sources'):out+=['\n'+citations(b)]
    out+=['\n## '+title('来源与后续取证','Sources and next evidence'), '\n['+title('验证协议与待补证据','Validation protocols and gaps')+']('+report+'#validation)']
    for s in p['sources']:
        out+=['\n- **'+s['id']+'** · '+s['title']+' · '+s['date']+' · '+s['kind'], '  '+s['context']]
        if s.get('url'):out+=['  ['+title('原始来源','Original source')+']('+s['url']+')']
        out+=['  '+title('定位：','Locator: ')+s['locator']]
    return '\n'.join(out)+'\n',assets
