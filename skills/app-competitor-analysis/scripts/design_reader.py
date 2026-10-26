"""Readable HTML for the exact generated Design.md dialect (not arbitrary Markdown)."""
from html import escape
import re
from urllib.parse import urlsplit
from design_spec import design_markdown


def inline(value):
    # Escape everything except the renderer's small, explicit inline dialect.
    out=[];pos=0
    for m in re.finditer(r'\[([^\]]+)\]\(([^\s)]+)\)|\*\*([^*]+)\*\*|`([^`]+)`',value):
        out.append(escape(value[pos:m.start()]))
        if m[1] is not None:
            label,url=m[1],m[2]
            if url.startswith('../../'):url=url[6:]
            parsed=urlsplit(url)
            safe=(parsed.scheme in ('http','https')or(not parsed.scheme and not url.startswith('//')and not any(x=='..'for x in parsed.path.split('/'))))
            if safe:
                media=' data-spec-image'if re.fullmatch(r'assets/[a-f0-9]{64}\.(?:png|jpg|webp)',parsed.path)else ''
                external=' target="_blank" rel="noopener noreferrer"'if parsed.scheme else ''
                out.append('<a href="'+escape(url,quote=True)+'"'+media+external+'>'+escape(label)+'</a>')
            else:out.append(escape(label))
        elif m[3] is not None:out.append('<strong>'+escape(m[3])+'</strong>')
        else:out.append('<code>'+escape(m[4])+'</code>')
        pos=m.end()
    out.append(escape(value[pos:]));return ''.join(out).replace('&lt;br&gt;','<br>')


def markdown_html(md):
    lines=md.splitlines();out=[];outline=[];i=0;section=0
    def cells(line):return [x.strip().replace('\\|','|')for x in re.split(r'(?<!\\)\|',line)]
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        heading=re.match(r'^(#{1,4}) (.+)$',line)
        if heading:
            level=len(heading[1]);anchor=''
            if level==2:
                section+=1;ident='design-section-'+str(section);anchor=' id="'+ident+'"';outline.append((ident,heading[2]))
            out.append(f'<h{level}{anchor}>'+inline(heading[2])+f'</h{level}>');i+=1;continue
        if i+1<len(lines)and re.fullmatch(r'[\s|:-]+',lines[i+1])and '---'in lines[i+1]:
            header=cells(line);i+=2;rows=[]
            while i<len(lines)and lines[i].strip()and ' | 'in lines[i]:rows.append(cells(lines[i]));i+=1
            out.append('<div class="spec-table" tabindex="0"><table><thead><tr>'+''.join('<th>'+inline(x)+'</th>'for x in header)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(x)+'</td>'for x in row)+'</tr>'for row in rows)+'</tbody></table></div>');continue
        if re.match(r'^(?:- |\d+\. )',line):
            numbered=bool(re.match(r'^\d+\. ',line));tag='ol'if numbered else'ul';items=[]
            while i<len(lines)and re.match(r'^\s*\d+\. 'if numbered else r'^\s*- ',lines[i]):
                # The generated dialect uses flat lists; indented source metadata follows as prose.
                items.append(re.sub(r'^\s*(?:- |\d+\. )','',lines[i]));i+=1
            out.append('<'+tag+'>'+''.join('<li>'+inline(x)+'</li>'for x in items)+'</'+tag+'>');continue
        paragraph=[line];i+=1
        while i<len(lines)and lines[i].strip()and not re.match(r'^(?:#|\s*- |\d+\. )',lines[i]):
            if i+1<len(lines)and '---'in lines[i+1]and '|'in lines[i+1]:break
            paragraph.append(lines[i].strip());i+=1
        out.append('<p>'+inline('<br>'.join(paragraph))+'</p>')
    return ''.join(out),outline


def design_template(p,base_dir,lang):
    md,_=design_markdown(p,base_dir,lang);content,outline=markdown_html(md);zh=lang.startswith('zh')
    nav='<nav class="spec-outline" aria-label="'+('规格目录'if zh else'Specification contents')+'">'+''.join('<a href="#'+ident+'">'+escape(title)+'</a>'for ident,title in outline)+'</nav>'
    return '<template id="design-document" data-title="'+escape(p['name']+' · Design.md',quote=True)+'"><div class="spec-reader">'+nav+'<article class="spec-prose">'+content+'</article></div></template>'
