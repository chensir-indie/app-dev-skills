"""Report reader composition. Domain analysis and diagram renderers stay separate."""
from html import escape

def report_frame(*,product,number,count,lang,library,hero,chapters,atlas,sources,context,footer,print_label):
    zh=lang.startswith('zh');e=lambda x:escape(str(x),quote=True)
    definitions=[
        ('overview','概览'if zh else'Overview','reader-overview',hero+chapters['overview']),
        ('capabilities','功能'if zh else'Capabilities','atlas',atlas),
        ('interface','界面'if zh else'Interface','ui',chapters['ui']),
        ('interaction','交互'if zh else'Interaction','interaction',chapters['interaction']),
        ('technology','技术'if zh else'Technology','technology',chapters['technology']),
        ('decisions','取舍'if zh else'Decisions','business',''.join(chapters[x]for x in ['business','strengths','decisions','validation'])),
        ('sources','来源'if zh else'Sources','sources',sources+context)]
    links=''.join(f'<a href="#{anchor}" data-reader-link="{key}">{label}</a>'for key,label,anchor,_ in definitions)
    links+='<a href="#reader-all" data-reader-link="all" class="reader-all-link">'+('连续阅读'if zh else'Read all')+'</a>'
    selector='<label class="reader-chapter-select">'+('章节'if zh else'Chapter')+'<select aria-label="'+('分析章节'if zh else'Analysis chapter')+'" data-reader-select>'+''.join('<option value="'+key+'">'+label+'</option>'for key,label,_,_ in definitions)+'<option value="all">'+('连续阅读'if zh else'Read all')+'</option></select></label>'
    views=''.join(f'<div class="reader-view" id="reader-{key}" data-reader-view="{key}" aria-label="{label}">{content}</div>'for key,label,_,content in definitions)
    return f'''<a class="skip" href="#main">{'跳到内容'if zh else'Skip to content'}</a>
<header class="app-header"><a class="app-brand" href="index.html"><span aria-hidden="true">◈</span>{'竞品研究'if zh else'App Studies'}</a><div class="app-actions"><a href="index.html">{'全部产品'if zh else'All products'} ↗</a><button class="print-button" type="button">{print_label}</button></div></header>
<div class="reader-app editorial-report">{library}<main id="main" class="reader-main" data-atlas-mode="integrated" data-reader>
<header class="reader-viewbar"><div class="reader-product"><strong>{e(product['name'])}</strong><small>{e(product['category'])}</small><button class="reader-switch-button" type="button" data-open-library>{'切换竞品'if zh else'Switch app'}</button></div><nav class="reader-navigation" data-section-nav aria-label="{'分析视图'if zh else'Analysis views'}">{links}</nav>{selector}</header><span id="reader-all" tabindex="-1"></span>{views}{footer}</main></div>'''
