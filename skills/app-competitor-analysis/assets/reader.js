'use strict';
// Progressive reading workspace. One owner for URL, loading, history and inspection.
(()=>{
  const app=document.querySelector('.reader-app');if(!app)return;
  const zh=document.documentElement.lang.startsWith('zh'),word=(a,b)=>zh?a:b;
  const $=(s,root=document)=>root.querySelector(s),all=(s,root=document)=>[...root.querySelectorAll(s)];
  const rail=$('.competitor-sidebar'),library=all('.competitor-link',rail).map(a=>({path:new URL(a.href).pathname,id:a.dataset.productId,name:$('strong',a).textContent,category:a.title,search:a.closest('li').dataset.search}));
  const indexPath=new URL('index.html',location.href).pathname,known=new Set([indexPath,...library.map(p=>p.path)]);
  const anchors={overview:'reader-overview',capabilities:'atlas',interface:'ui',interaction:'interaction',technology:'technology',decisions:'business',sources:'sources',all:'reader-all'};
  const cache=new Map(),positions=new Map();let main=$('#main'),path=location.pathname,active='overview',request=0,controller=null,frame=0,sizing=null,gallery=[],dialogState=null,focusOrigin=null,closing=false;
  const dialog=document.createElement('dialog');dialog.className='reader-dialog';dialog.setAttribute('aria-labelledby','inspection-title');
  dialog.innerHTML='<header class="inspection-header"><button type="button" data-inspection-back hidden>'+word('← 返回','← Back')+'</button><h2 id="inspection-title"></h2><div class="inspection-actions"></div><button class="inspection-close" type="button" data-inspection-close aria-label="'+word('关闭查看','Close inspection')+'">×</button></header><div class="inspection-body"></div>';
  document.body.append(dialog);const dialogBody=$('.inspection-body',dialog);
  const status=document.createElement('div');status.className='workspace-status';status.setAttribute('role','status');status.setAttribute('aria-live','polite');status.hidden=true;document.body.append(status);
  document.documentElement.classList.add('workspace-ready');
  function cachePut(key,value){cache.delete(key);cache.set(key,value);while(cache.size>3)cache.delete(cache.keys().next().value);}
  function recordPage(doc){return{main:$('#main',doc).outerHTML,title:doc.title,header:$('.app-header',doc).outerHTML,spec:$('#design-document',doc)?.outerHTML||'',collection:!!$('.reader-collection',doc)};}
  cachePut(path,recordPage(document));
  function state(){return{workspace:true,path,view:active,scroll:[scrollX,scrollY],hash:location.hash||'#'+anchors[active],detail:dialogState,filters:{query:$('#search',main)?.value||'',category:$('#category',main)?.value||''}};}
  function remember(){if(!main||location.pathname!==path)return;if(dialogState)dialogState.bodyScroll=dialogBody.scrollTop;positions.set(path+':'+active,[scrollX,scrollY]);history.replaceState(state(),'');}
  function decode(hash){try{return decodeURIComponent(hash.replace(/^#/,''));}catch{return '';}}
  function original(id){return document.getElementById(id);}
  function routeTarget(hash){return original(decode(hash));}
  function viewFor(target){return target?.closest('[data-reader-view]')?.dataset.readerView||'overview';}
  function showView(key){
    if(!Object.hasOwn(anchors,key))key='overview';active=key;
    all('[data-reader-view]',main).forEach(v=>{v.hidden=key!=='all'&&v.dataset.readerView!==key;});
    all('[data-reader-link]',main).forEach(a=>{if(a.dataset.readerLink===key)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
    const select=$('[data-reader-select]',main);if(select)select.value=key;main.dataset.readerActive=key;
  }
  function offset(){const h=$('.app-header')?.getBoundingClientRect().height||0,v=$('.reader-viewbar',main)?.getBoundingClientRect().height||0;document.documentElement.style.setProperty('--anchor-offset',h+v+20+'px');}
  function scrollTarget(target,focus=false){
    if(!target)return;let parent=target.parentElement;while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}
    cancelAnimationFrame(frame);frame=requestAnimationFrame(()=>{offset();target.scrollIntoView({block:'start',behavior:'instant'});if(focus){target.setAttribute('tabindex','-1');target.focus({preventScroll:true});}remember();});
  }
  function cancelLoad(){request++;controller?.abort();controller=null;main?.removeAttribute('aria-busy');message('');}
  function message(text,errorUrl){
    (dialog.open?dialog:document.body).append(status);status.replaceChildren();status.hidden=!text;if(!text)return;
    const label=document.createElement('span');label.textContent=text;status.append(label);
    if(errorUrl){const retry=document.createElement('button');retry.type='button';retry.textContent=word('重试','Retry');retry.dataset.retryReport=errorUrl;const link=document.createElement('a');link.href=errorUrl;link.target='_blank';link.rel='noopener';link.textContent=word('单独打开','Open document');const close=document.createElement('button');close.type='button';close.textContent=word('关闭','Dismiss');close.dataset.dismissStatus='';status.append(retry,link,close);}
  }
  function restoreFocus(){
    const trigger=focusOrigin;focusOrigin=null;
    if(trigger?.isConnected&&!trigger.closest('[hidden]'))trigger.focus({preventScroll:true});
    else{const fallback=(innerWidth<=820?$('[data-reader-select]',main):$('[data-reader-link][aria-current="page"]',main))||$('h1,h2',main);if(fallback&&!fallback.matches('a,button,select'))fallback.tabIndex=-1;fallback?.focus({preventScroll:true});}
  }
  function dismissUI(restore=false){
    closing=true;document.body.append(status);if(dialog.open)dialog.close();dialogBody.replaceChildren();dialogState=null;document.body.classList.remove('inspection-open');all('.workspace-selected').forEach(n=>n.classList.remove('workspace-selected'));closing=false;if(restore)restoreFocus();
  }
  function closeInspection(){
    cancelLoad();const d=dialogState;if(!d)return;
    if(d.depth>0){history.go(-d.depth);return;}
    const hash=d.baseHash||'#'+anchors[active],scroll=d.baseScroll||[scrollX,scrollY];dismissUI(true);history.replaceState({...state(),detail:null,scroll,hash},'',hash);window.scrollTo({left:scroll[0],top:scroll[1],behavior:'instant'});
  }
  function nodeTrigger(id){return all('[data-node-detail]',main).find(n=>n.dataset.nodeDetail===id);}
  function detailForHash(hash){
    const id=decode(hash);if(id==='design-document'&&original(id))return{kind:'design',id};
    if(id.startsWith('source-')&&original(id))return{kind:'source',id};
    const node=original(id)?.hasAttribute('data-node-detail')?original(id):all('[data-node-detail]',main).find(n=>n.getAttribute('href')==='#'+id);if(node)return{kind:'node',id:node.dataset.nodeDetail};
    if(id.startsWith('inspect-map-'))return{kind:'map',id:id.slice('inspect-'.length)};
    if(id.startsWith('inspect-image-'))return{kind:'image',id:Number(id.slice(14))};
    if(id==='switch-competitor')return{kind:'library',id};return null;
  }
  function detailHash(d){
    if(d.kind==='node')return nodeTrigger(d.id)?.getAttribute('href')||'#'+anchors[active];
    if(d.kind==='map')return'#inspect-'+d.id;if(d.kind==='image')return'#inspect-image-'+d.id;
    if(d.kind==='library')return'#switch-competitor';return'#'+d.id;
  }
  function openInspection(d,trigger,{restore=false}={}){
    if(!restore){cancelLoad();remember();focusOrigin=focusOrigin||trigger||document.activeElement;const previous=dialogState;d={...d,baseHash:previous?.baseHash||location.hash||'#'+anchors[active],baseScroll:previous?.baseScroll||[scrollX,scrollY],depth:(previous?.depth||0)+1};history.pushState({...state(),detail:d},'',detailHash(d));}
    renderInspection(d);
  }
  function inspectionButton(label,attr,value=''){const button=document.createElement('button');button.type='button';button.textContent=label;button.setAttribute(attr,value);return button;}
  function renderInspection(d){
    dialogState=d;dialogBody.replaceChildren();dialogBody.classList.remove('image-actual');const actions=$('.inspection-actions',dialog);actions.replaceChildren();let title='';dialog.className='reader-dialog inspection-'+d.kind;
    $('[data-inspection-back]',dialog).hidden=!(d.depth>1);let focus=$('[data-inspection-close]',dialog);
    if(d.kind==='node'){
      const template=original(d.id);if(!template?.content){dismissUI();return;}
      const fragment=template.content.cloneNode(true);title=$('h4,h3,strong',fragment)?.textContent||word('功能说明','Node details');dialogBody.append(fragment);nodeTrigger(d.id)?.classList.add('workspace-selected');
    }else if(d.kind==='source'){
      const source=original(d.id);if(!source){dismissUI();return;}title=word('证据与来源','Evidence');const clone=source.cloneNode(true);clone.removeAttribute('id');all('details',clone).forEach(x=>x.open=true);dialogBody.append(clone);
    }else if(d.kind==='design'){
      const source=original('design-document');title=source.dataset.title;dialogBody.append(source.content.cloneNode(true));
      const file=$('.design-download',main).cloneNode(true);file.removeAttribute('class');file.textContent=word('Markdown 文件 ↗','Markdown file ↗');file.dataset.nativeLink='';actions.append(file);
    }else if(d.kind==='map'){
      const source=original(d.id);if(!source){dismissUI();return;}title=$('.diagram-heading h3,.atlas-panel-head h3',source)?.textContent||word('完整图谱','Complete map');
      const clone=source.cloneNode(true);clone.removeAttribute('id');all('[id]',clone).forEach(n=>n.removeAttribute('id'));all('template,.node-inspector,.diagram-provenance',clone).forEach(n=>n.remove());clone.classList.remove('is-reading');clone.dataset.viewerMap='';dialogBody.append(clone);if(d.mapList){clone.classList.add('is-reading');all('.graph-index',clone).forEach(x=>x.open=true);}if(d.mapZoom){clone.dataset.zoom=d.mapZoom;all('.graph-svg',clone).forEach(svg=>svg.style.width=svg.viewBox.baseVal.width*d.mapZoom+'px');}
      if($('.graph-index',clone))actions.append(inspectionButton(word('图 / 清单','Diagram / list'),'data-viewer-list'));if($('.graph-svg',clone))actions.append(inspectionButton('−','data-viewer-zoom','out'),inspectionButton(word('适合宽度','Fit width'),'data-viewer-zoom','fit'),inspectionButton('＋','data-viewer-zoom','in'));all('[data-viewer-zoom]',actions).forEach(b=>b.setAttribute('aria-label',b.dataset.viewerZoom==='out'?word('缩小图谱','Zoom out'):b.dataset.viewerZoom==='in'?word('放大图谱','Zoom in'):word('适合宽度','Fit width')));
    }else if(d.kind==='image'){
      const item=gallery[d.id];if(!item){dismissUI();return;}title=word('界面原图','Original evidence')+' '+(d.id+1)+' / '+gallery.length;
      const image=document.createElement('img');image.src=item.src;image.alt=item.alt;image.className='inspection-image';const stage=document.createElement('div');stage.className='inspection-image-stage';stage.append(image);const caption=document.createElement('p');caption.className='inspection-caption';caption.textContent=item.alt;dialogBody.append(stage,caption);
      if(gallery.length>1){const previous=inspectionButton('←','data-image-step','-1'),next=inspectionButton('→','data-image-step','1');previous.disabled=d.id===0;next.disabled=d.id===gallery.length-1;previous.setAttribute('aria-label',word('上一张原图','Previous image'));next.setAttribute('aria-label',word('下一张原图','Next image'));actions.append(previous,next);}
      actions.append(inspectionButton(word('实际尺寸','Actual size'),'data-image-size'));const originalLink=document.createElement('a');originalLink.href=item.src;originalLink.target='_blank';originalLink.rel='noopener';originalLink.dataset.nativeLink='';originalLink.textContent=word('原文件 ↗','Original file ↗');actions.append(originalLink);
    }else if(d.kind==='library'){
      title=word('切换竞品','Switch competitor');const label=document.createElement('label');label.className='library-search';label.textContent=word('搜索名称或类别','Search name or category');const input=document.createElement('input');input.type='search';input.placeholder=word('输入竞品名称…','Search competitors…');input.dataset.librarySearch='';label.append(input);const list=document.createElement('nav');list.className='library-results';list.setAttribute('aria-label',word('选择竞品','Choose competitor'));
      for(const product of library){const link=document.createElement('a');link.href=product.path;link.dataset.libraryItem=product.search;link.dataset.productId=product.id;const name=document.createElement('strong'),category=document.createElement('span');name.textContent=product.name;category.textContent=product.category;link.append(name,category);if(product.path===path)link.setAttribute('aria-current','page');list.append(link);}
      const empty=document.createElement('p');empty.className='library-empty';empty.hidden=true;empty.textContent=word('没有匹配的竞品，请更换关键词。','No matches. Try another search.');dialogBody.append(label,list,empty);focus=input;
    }
    $('#inspection-title',dialog).textContent=title;dialogBody.scrollTop=0;document.body.classList.add('inspection-open');if(!dialog.open)dialog.showModal();focus.focus({preventScroll:true});if(d.bodyScroll)dialogBody.scrollTop=d.bodyScroll;
  }
  function updateRail(){all('.competitor-link',rail).forEach(a=>{if(new URL(a.href).pathname===path)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});const summary=$('.competitor-switcher summary strong',rail);if(summary)summary.textContent=library.find(p=>p.path===path)?.name||word('全部竞品','All competitors');}
  function prepareMain(){
    sizing?.disconnect();sizing=null;gallery=[];main=$('#main');main.classList.add('workspace-main');
    all('figure',main).forEach(figure=>{const visible=$(':scope > .media-view',figure),image=$('.original-image img',figure)||$('img',figure);if(!visible||!image)return;
      let index=gallery.findIndex(x=>x.src===image.getAttribute('src'));if(index<0){index=gallery.length;gallery.push({src:image.getAttribute('src'),alt:image.alt});}
      const link=document.createElement('a');link.className='evidence-image-link';link.href=image.getAttribute('src');link.dataset.mediaIndex=String(index);link.setAttribute('aria-label',word('查看原图：','Inspect original: ')+image.alt);visible.replaceWith(link);link.append(visible);
      const button=inspectionButton(word('查看原图 ↗','Inspect original ↗'),'data-media-index',String(index));button.className='media-open';figure.append(button);
    });
    all('[data-atlas-panel]',main).forEach(panel=>{panel.hidden=false;if(innerWidth<=820&&$('.graph-svg',panel)){panel.classList.add('is-reading');all('.graph-index',panel).forEach(x=>x.open=true);}const button=inspectionButton(word('展开查看','Expand map'),'data-expand-map',panel.id);button.className='map-expand';const heading=$('.diagram-heading,.atlas-panel-head',panel);heading?.append(button);});
    if('ResizeObserver'in window){sizing=new ResizeObserver(offset);all('.app-header,.reader-viewbar').forEach(x=>sizing.observe(x));}offset();updateRail();filterIndex();
    const input=$('[data-competitor-search]',rail);if(input)filterRail(input.value);
  }
  function applyState(saved,{initial=false,focus=false}={}){
    const hash=saved?.hash||location.hash||'#reader-overview',target=routeTarget(hash),d=saved?.detail||detailForHash(hash);
    const view=saved?.view||(d?.kind==='design'?'interface':d?.kind==='node'?viewFor(nodeTrigger(d.id)):d?.kind==='image'?'interface':d?.kind==='map'?viewFor(original(d.id)):d?.kind==='source'?'sources':hash==='#reader-all'?'all':viewFor(target));
    dismissUI();showView(view);if(saved?.filters&&$('#search',main)){$('#search',main).value=saved.filters.query;$('#category',main).value=saved.filters.category;filterIndex();}
    if(saved?.scroll){window.scrollTo({left:saved.scroll[0],top:saved.scroll[1],behavior:'instant'});}else if(d){scrollTarget(d.kind==='node'?nodeTrigger(d.id)?.closest('[data-atlas-panel]'):original(anchors[active]),focus);}else scrollTarget(target||original(anchors[active])||main,focus);
    if(d)renderInspection({...d,depth:saved?.detail?.depth||0,baseHash:d.baseHash||'#'+anchors[active],baseScroll:d.baseScroll||saved?.scroll||[0,0]});
    else if(!initial&&focusOrigin)restoreFocus();
  }
  async function navigateReport(url,{pop=false,saved=null,replace=false}={}){
    const dest=new URL(url,location.href);if(!known.has(dest.pathname))return false;
    if(dest.pathname===path){cancelLoad();if(pop)applyState(saved);else navigateHash(dest.hash||'#reader-overview');return true;}
    if(location.protocol==='file:'){location.assign(dest.href);return true;}
    if(!pop)remember();const token=++request;controller?.abort();controller=new AbortController();main.setAttribute('aria-busy','true');
    message(word('正在打开 ','Opening ')+(library.find(x=>x.path===dest.pathname)?.name||word('研究档案','Library'))+'…');
    performance.clearMarks('reader-switch-start');performance.clearMarks('reader-switch-end');performance.clearMeasures('reader-switch');performance.mark('reader-switch-start');
    try{
      let record=cache.get(dest.pathname);
      if(!record){const response=await fetch(dest.pathname,{signal:controller.signal,credentials:'same-origin'});if(!response.ok)throw Error('HTTP '+response.status);const html=await response.text();if(token!==request)return true;const parsed=new DOMParser().parseFromString(html,'text/html');if(!$('#main',parsed)||!$('.reader-app',parsed))throw Error('Invalid report');const current=$('.competitor-link[aria-current="page"]',parsed);if(dest.pathname!==indexPath&&current?.dataset.productId!==library.find(x=>x.path===dest.pathname)?.id)throw Error('Report identity mismatch');record=recordPage(parsed);cachePut(dest.pathname,record);}
      if(token!==request)return true;dismissUI();const fragment=new DOMParser().parseFromString(record.main+record.header+record.spec,'text/html');main.replaceWith($('#main',fragment));$('.app-header').replaceWith($('.app-header',fragment));original('design-document')?.remove();const template=$('#design-document',fragment);if(template)document.body.append(template);document.title=record.title;app.classList.toggle('reader-collection',record.collection);path=dest.pathname;prepareMain();
      if(!pop){history[replace?'replaceState':'pushState'](null,'',dest.pathname+dest.hash);}
      applyState(saved||{hash:dest.hash||'#reader-overview'},{focus:!pop});message('');main.removeAttribute('aria-busy');performance.mark('reader-switch-end');performance.measure('reader-switch','reader-switch-start','reader-switch-end');
    }catch(error){if(error.name==='AbortError'||token!==request)return true;main.removeAttribute('aria-busy');message(word('暂时无法打开，当前报告已保留。','Could not open the report. Your current reading is preserved.'),dest.href);if(pop)history.replaceState(state(),'',path+'#'+anchors[active]);}
    return true;
  }
  function navigateHash(hash,trigger){
    cancelLoad();const d=detailForHash(hash);if(d){openInspection(d,trigger);return;}
    const target=routeTarget(hash);if(!target)return;remember();dismissUI();const oldView=active,view=hash==='#reader-all'?'all':viewFor(target),position=positions.get(path+':'+view),isView=Object.values(anchors).includes(decode(hash));
    history.pushState(null,'',hash);showView(view);
    if(isView&&position&&view!==oldView){window.scrollTo({left:position[0],top:position[1],behavior:'instant'});remember();}else scrollTarget(target,true);
  }
  function filterRail(query){let count=0;all('[data-competitor-item]',rail).forEach(item=>{item.hidden=!item.dataset.search.includes(query.trim().toLocaleLowerCase());if(!item.hidden)count++;});$('[data-competitor-count]',rail).textContent=count+' / '+library.length;$('.nav-empty',rail).hidden=count!==0;$('[data-competitor-clear]',rail).hidden=!query;try{sessionStorage.setItem('reader-search:'+rail.dataset.collectionKey,query);}catch{}}
  function filterIndex(){const input=$('#search',main),category=$('#category',main);if(!input||!category)return;let count=0;const cards=all('.report-card',main);cards.forEach(card=>{card.hidden=!(card.dataset.search.includes(input.value.trim().toLocaleLowerCase())&&(!category.value||category.value===card.dataset.category));if(!card.hidden)count++;});$('#result-count',main).textContent=count+' / '+cards.length;$('#empty-results',main).hidden=count!==0;}
  function changeImage(step){const d={...dialogState,id:dialogState.id+step};if(!gallery[d.id])return;history.replaceState({...state(),detail:d},'',detailHash(d));renderInspection(d);}
  document.addEventListener('click',event=>{
    const target=event.target instanceof Element?event.target:event.target?.parentElement;if(!target||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
    const button=target.closest('button');
    if(button){
      if(button.matches('[data-inspection-close]')){closeInspection();return;}
      if(button.matches('[data-inspection-back]')){cancelLoad();history.back();return;}
      if(button.matches('[data-dismiss-status]')){message('');return;}
      if(button.matches('[data-retry-report]')){navigateReport(button.dataset.retryReport,{replace:dialogState?.kind==='library'});return;}
      if(button.matches('[data-open-library]')){openInspection({kind:'library',id:'switch-competitor'},button);return;}
      if(button.matches('[data-expand-map]')){openInspection({kind:'map',id:button.dataset.expandMap},button);return;}
      if(button.matches('[data-media-index]')){openInspection({kind:'image',id:Number(button.dataset.mediaIndex)},button);return;}
      if(button.matches('[data-image-step]')){changeImage(Number(button.dataset.imageStep));return;}
      if(button.matches('[data-image-size]')){dialogBody.classList.toggle('image-actual');button.setAttribute('aria-pressed',String(dialogBody.classList.contains('image-actual')));return;}
      if(button.matches('[data-viewer-list]')){const map=$('[data-viewer-map]',dialog);map.classList.toggle('is-reading');all('.graph-index',map).forEach(x=>x.open=map.classList.contains('is-reading'));dialogState.mapList=map.classList.contains('is-reading');button.setAttribute('aria-pressed',String(dialogState.mapList));remember();return;}
      if(button.matches('[data-viewer-zoom]')){const map=$('[data-viewer-map]',dialog);const mode=button.dataset.viewerZoom;let ratio=Number(map.dataset.zoom||1);ratio=mode==='fit'?Math.min(1,...all('.graph-svg',map).map(svg=>svg.closest('.graph-scroll').clientWidth/svg.viewBox.baseVal.width)):Math.min(2.5,Math.max(.4,ratio+(mode==='in'?.2:-.2)));map.dataset.zoom=ratio;dialogState.mapZoom=ratio;remember();all('.graph-svg',map).forEach(svg=>svg.style.width=svg.viewBox.baseVal.width*ratio+'px');return;}
      if(button.matches('.print-button')){window.print();return;}
      if(button.matches('[data-competitor-clear]')){const input=$('[data-competitor-search]',rail);input.value='';filterRail('');input.focus();return;}
    }
    const a=target.closest('a');if(!a||a.dataset.nativeLink!==undefined||a.hasAttribute('download'))return;
    if(a.matches('.design-download')){event.preventDefault();openInspection({kind:'design',id:'design-document'},a);return;}
    if(a.dataset.mediaIndex!==undefined){event.preventDefault();openInspection({kind:'image',id:Number(a.dataset.mediaIndex)},a);return;}
    if(a.matches('[data-spec-image]')){event.preventDefault();let id=gallery.findIndex(x=>new URL(x.src,location.href).href===a.href);if(id<0){id=gallery.length;gallery.push({src:a.getAttribute('href'),alt:a.textContent});}openInspection({kind:'image',id},a);return;}
    if(a.dataset.nodeDetail){event.preventDefault();openInspection({kind:'node',id:a.dataset.nodeDetail},a);return;}
    const url=new URL(a.href,location.href);if(url.origin!==location.origin||(a.target&&a.target!=='_self'))return;
    if(dialog.open&&url.hash.startsWith('#design-section-')){const section=dialogBody.querySelector(url.hash);if(section){event.preventDefault();section.scrollIntoView({block:'start',behavior:'instant'});section.tabIndex=-1;section.focus({preventScroll:true});}return;}
    if(a.hasAttribute('data-library-item')&&url.pathname===path){event.preventDefault();closeInspection();return;}
    if(known.has(url.pathname)&&url.pathname!==path){event.preventDefault();const fromLibrary=a.hasAttribute('data-library-item'),context=a.matches('.competitor-link')||fromLibrary;url.hash=context?'#'+anchors[active]:url.hash;navigateReport(url.href,{replace:fromLibrary});return;}
    if(url.pathname===path&&url.hash&&routeTarget(url.hash)){event.preventDefault();navigateHash(url.hash,a);}
  });
  document.addEventListener('input',event=>{const input=event.target;if(input.matches('[data-competitor-search]'))filterRail(input.value);if(input.matches('#search'))filterIndex();if(input.matches('[data-library-search]')){let count=0;all('[data-library-item]',dialog).forEach(a=>{a.hidden=!a.dataset.libraryItem.includes(input.value.trim().toLocaleLowerCase());if(!a.hidden)count++;});$('.library-empty',dialog).hidden=count!==0;}});
  document.addEventListener('change',event=>{if(event.target.matches('#category'))filterIndex();if(event.target.matches('[data-reader-select]'))navigateHash('#'+anchors[event.target.value]);});
  document.addEventListener('keydown',event=>{if((event.metaKey||event.ctrlKey)&&event.key.toLowerCase()==='k'){event.preventDefault();openInspection({kind:'library',id:'switch-competitor'},event.target);}if(dialog.open&&dialogState?.kind==='image'&&!event.target.matches('input,textarea,select')){if(event.key==='ArrowLeft'){event.preventDefault();changeImage(-1);}if(event.key==='ArrowRight'){event.preventDefault();changeImage(1);}}});
  dialog.addEventListener('cancel',event=>{event.preventDefault();closeInspection();});dialog.addEventListener('click',event=>{if(event.target===dialog){const box=dialog.getBoundingClientRect();if(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom)closeInspection();}});
  dialog.addEventListener('close',()=>{if(!closing&&!dialog.open&&dialogState)closeInspection();});
  window.addEventListener('popstate',event=>{cancelLoad();const saved=event.state;if(location.pathname!==path)navigateReport(location.href,{pop:true,saved});else applyState(saved);});
  window.addEventListener('hashchange',()=>{if(location.pathname===path&&history.state?.hash!==location.hash&&!history.state?.detail)applyState(null);});
  window.addEventListener('pagehide',remember);window.addEventListener('scrollend',()=>{if(!dialog.open)remember();},{passive:true});if('scrollRestoration'in history)history.scrollRestoration='manual';
  let printClosed=null;window.addEventListener('beforeprint',()=>{if(printClosed===null){printClosed=all('details:not([open])',main);printClosed.forEach(d=>d.open=true);}});window.addEventListener('afterprint',()=>{printClosed?.forEach(d=>d.open=false);printClosed=null;});
  // The mobile picker is always in the sticky bar; the original rail remains for no-script fallback.
  const railSearch=$('[data-competitor-search]',rail);try{railSearch.value=sessionStorage.getItem('reader-search:'+rail.dataset.collectionKey)||'';}catch{}
  rail.classList.add('navigator-enhanced');$('.competitor-switcher',rail).open=true;prepareMain();applyState(history.state?.workspace?history.state:null,{initial:true});
  window.reportWorkspace={active:()=>active,cacheSize:()=>cache.size};window.reportReader={active:()=>active,anchor:()=>anchors[active]};
})();
