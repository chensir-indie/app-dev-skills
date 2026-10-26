// Legacy standalone atlas behavior; the reading workspace owns enhanced pages.
(()=>{if(window.reportWorkspace)return;
'use strict';
const zh = document.documentElement.lang.startsWith('zh');
const inspectorTriggers = new WeakMap();
const closeInspectors = (restoreFocus=false) => {
  let focusTarget = null;
  document.querySelectorAll('.node-inspector.is-active').forEach(inspector => {
    const trigger = inspectorTriggers.get(inspector);
    if (restoreFocus && (inspector.contains(document.activeElement) || document.activeElement === trigger)) {
      focusTarget = trigger;
    }
    inspector.classList.remove('is-active');
    inspector.closest('[data-atlas-panel]')?.querySelectorAll('.selected').forEach(node=>node.classList.remove('selected'));
    inspector.replaceChildren();
    inspectorTriggers.delete(inspector);
    const hint=document.createElement('p');hint.textContent=inspector.dataset.hint || '';inspector.append(hint);
  });
  if (focusTarget?.isConnected) focusTarget.focus({preventScroll:true});
};
document.addEventListener('keydown',event=>{if(event.key==='Escape')closeInspectors(true);});
function inspectNode(node){
  const panel=node?.closest('[data-atlas-panel]');
  const inspector=panel?.querySelector('.node-inspector');
  const template=node&&document.getElementById(node.dataset.nodeDetail);
  if(!inspector||!template)return;
  closeInspectors();inspector.replaceChildren(template.content.cloneNode(true));
  const close=document.createElement('button');close.type='button';close.className='inspector-close';close.textContent='×';
  close.setAttribute('aria-label',zh?'关闭节点详情':'Close node details');close.addEventListener('click',()=>closeInspectors(true));
  inspectorTriggers.set(inspector,node);inspector.prepend(close);inspector.classList.add('is-active');node.classList.add('selected');
}
document.querySelectorAll('.visual-atlas:not(.integrated-overview),[data-atlas-mode="integrated"]').forEach(atlas => {
  atlas.classList.add('atlas-enhanced');
  const integrated=atlas.dataset.atlasMode==='integrated';
  const panels = Array.from(atlas.querySelectorAll('[data-atlas-panel]'));
  const buttons = Array.from(atlas.querySelectorAll('[data-atlas-view]'));
  const zooms = new Map();
  const minimumZooms = new Map();
  function fit(panel, exact=false){
    const svgs=Array.from(panel.querySelectorAll('.graph-svg'));
    if(!svgs.length||panel.hidden)return;
    // Keep labels readable by default; only an explicit Fit action shrinks a map.
    // Default display already has an authored width. Measuring after unhiding
    // each map forces a synchronous layout of the long report unnecessarily.
    const ratio=exact?Math.min(1,...svgs.map(svg=>svg.closest('.graph-scroll').clientWidth/svg.viewBox.baseVal.width)):1;
    svgs.forEach(svg=>{svg.style.width=`${svg.viewBox.baseVal.width*ratio}px`;});zooms.set(panel,ratio);
    minimumZooms.set(panel,Math.min(.7,ratio));
  }
  const show = view => {
    closeInspectors();
    panels.forEach(panel => {panel.hidden=view!=='all'&&panel.dataset.atlasPanel!==view;if(!panel.hidden&&!zooms.has(panel))fit(panel);});
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.atlasView === view)));
  };
  buttons.forEach(button => button.addEventListener('click', () => show(button.dataset.atlasView)));
  if(!integrated)show('features');
  panels.forEach(panel => {
    const layoutButton=panel.querySelector('[data-diagram-layout]');
    if(layoutButton){
      const index=panel.querySelector('.graph-index'),phone=matchMedia('(max-width:720px)');
      let layoutChosen=false;
      const setLayout=reading=>{
        panel.classList.toggle('is-reading',reading);index.open=reading;
        layoutButton.textContent=reading?(zh?'查看图示':'Show diagram'):(zh?'关系清单':'Relationship list');
      };
      setLayout(integrated&&phone.matches);
      phone.addEventListener('change',()=>{if(!layoutChosen)setLayout(integrated&&phone.matches);});
      layoutButton.addEventListener('click',()=>{layoutChosen=true;closeInspectors();setLayout(!panel.classList.contains('is-reading'));});
    }
    const inspector=panel.querySelector('.node-inspector');inspector.dataset.hint=inspector.textContent.trim();
    panel.querySelectorAll('[data-node-detail]').forEach(node => node.addEventListener('click', event => {
      event.preventDefault();inspectNode(node);
    }));
    panel.querySelectorAll('[data-zoom]').forEach(button => button.addEventListener('click', () => {
      if(button.dataset.zoom==='fit'){fit(panel,true);return;}
      if(button.dataset.zoom==='reset')minimumZooms.set(panel,.7);
      const zoom=button.dataset.zoom==='reset'?1:Math.min(2,Math.max(minimumZooms.get(panel)??.7,(zooms.get(panel)||1)+(button.dataset.zoom==='in'?.2:-.2)));
      panel.querySelectorAll('.graph-svg').forEach(svg=>{svg.style.width=`${svg.viewBox.baseVal.width*zoom}px`;});zooms.set(panel,zoom);
    }));
  });
});
// One owner for same-page navigation. Native hash scrolling followed by two
// deferred scrollIntoView calls used to restart long, competing animations.
let anchorFrame=null,lastNavigationURL=location.href;
const targetForHash=hash=>{try{return document.getElementById(decodeURIComponent(hash.slice(1)));}catch{return null;}};
function openTarget(target){
  window.reportReader?.reveal(target);
  let parent=target.parentElement;while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}
  if(target.matches('.source')){const detail=target.querySelector('details');if(detail)detail.open=true;}
  const panel=target.closest('[data-atlas-panel]');
  if(panel&&panel.hidden){const button=panel.closest('.visual-atlas').querySelector(`[data-atlas-view="${panel.dataset.atlasPanel}"]`);if(button)button.click();}
}
function navigateHash(hash,focus=false){
  const target=targetForHash(hash);if(!target)return;
  closeInspectors();openTarget(target);
  if(anchorFrame!==null)cancelAnimationFrame(anchorFrame);
  anchorFrame=requestAnimationFrame(()=>{
    anchorFrame=null;target.scrollIntoView({block:'start',behavior:'instant'});
    if(focus){if(!target.hasAttribute('tabindex'))target.tabIndex=-1;target.focus({preventScroll:true});}
    scheduleReadingLocation();
  });
  lastNavigationURL=location.href;
}
function rememberPosition(){
  const inspector=document.querySelector('.node-inspector.is-active');
  const node=inspector&&inspectorTriggers.get(inspector);
  const view=document.querySelector('[data-atlas-view][aria-pressed="true"]')?.dataset.atlasView;
  history.replaceState({...history.state,reportScroll:[scrollX,scrollY],readerView:window.reportReader?.active(),reportView:view,reportNode:node?.dataset.nodeDetail},'');
}
document.addEventListener('click',event=>{
  if(event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
  const a=event.target.closest('a[href^="#"]');
  if(!a||a.hasAttribute('download')||(a.target&&a.target!=='_self'))return;
  const hash=a.getAttribute('href');if(!targetForHash(hash))return;
  event.preventDefault();rememberPosition();
  if(hash!==location.hash)history.pushState(null,'',hash);
  const readerLink=a.closest('[data-reader-link]');if(readerLink)window.reportReader?.show(readerLink.dataset.readerLink);
  navigateHash(hash,true);
});
window.addEventListener('hashchange',()=>{if(lastNavigationURL!==location.href)navigateHash(location.hash);});
function restorePosition(state){
  if(state.readerView)window.reportReader?.show(state.readerView);
  closeInspectors();if(anchorFrame!==null){cancelAnimationFrame(anchorFrame);anchorFrame=null;}
  const view=Array.from(document.querySelectorAll('[data-atlas-view]')).find(e=>e.dataset.atlasView===state.reportView);view?.click();
  const node=state.reportNode&&Array.from(document.querySelectorAll('[data-node-detail]')).find(e=>e.dataset.nodeDetail===state.reportNode);inspectNode(node);
  window.scrollTo({left:state.reportScroll[0],top:state.reportScroll[1],behavior:'instant'});node?.focus({preventScroll:true});scheduleReadingLocation();
}
// UA history restoration can run after popstate and undo an otherwise correct
// node restore. Own both the saved position and restoration, including bfcache.
if('scrollRestoration'in history)history.scrollRestoration='manual';
window.addEventListener('pagehide',rememberPosition);
window.addEventListener('pageshow',()=>{if(history.state?.reportScroll)restorePosition(history.state);});
window.addEventListener('scrollend',rememberPosition,{passive:true});
window.addEventListener('popstate',event=>{
  lastNavigationURL=location.href;
  if(event.state?.reportScroll)restorePosition(event.state);
  else navigateHash(location.hash);
});
document.addEventListener('pointerdown',event=>{if(!event.target.closest('.node-inspector,[data-node-detail]'))closeInspectors();});
if('IntersectionObserver'in window){
  const mapObserver=new IntersectionObserver(entries=>{
    for(const entry of entries){
      if(!entry.isIntersecting&&entry.target.querySelector('.node-inspector.is-active')){
        const box=entry.target.getBoundingClientRect();
        if(box.bottom<=0||box.top>=innerHeight)closeInspectors();
      }
    }
  });
  document.querySelectorAll('[data-atlas-panel]').forEach(panel=>mapObserver.observe(panel));
}
const readingSections = Array.from(document.querySelectorAll('main .chapter,main .integrated-overview'));
const readingLinks=Array.from(document.querySelectorAll('[data-section-nav]:not(.reader-navigation) a'));
let locationFrame=null,currentSection=null,readingObserver=null;
function updateReadingLocation(){
  locationFrame = null;
  const threshold = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--anchor-offset'))+12;
  const active = readingSections.filter(section=>!section.closest('[hidden]')&&section.getBoundingClientRect().top<=threshold).at(-1);
  if(active===currentSection)return;currentSection=active;
  readingLinks.forEach(link=>{
    if(active && link.getAttribute('href')==='#'+active.id)link.setAttribute('aria-current','location');
    else link.removeAttribute('aria-current');
  });
}
function scheduleReadingLocation(){
  if(readingSections.length&&locationFrame===null)locationFrame=requestAnimationFrame(updateReadingLocation);
}
function updateAnchorOffset(){
  const bar=document.querySelector('.app-header,.topbar');
  const viewbar=document.querySelector('.reader-viewbar');
  const offset=bar&&getComputedStyle(bar).position==='sticky'?bar.getBoundingClientRect().height+(viewbar?.getBoundingClientRect().height||0)+24:20;
  document.documentElement.style.setProperty('--anchor-offset',`${offset}px`);scheduleReadingLocation();
  // Observe a one-pixel reading line instead of querying every chapter's
  // geometry on every scroll frame. Explicit navigation still updates it.
  if(readingSections.length&&'IntersectionObserver'in window){
    readingObserver?.disconnect();
    readingObserver=new IntersectionObserver(scheduleReadingLocation,{rootMargin:`-${offset}px 0px -${Math.max(0,innerHeight-offset-1)}px 0px`});
    readingSections.forEach(section=>readingObserver.observe(section));
  }
}
if(readingSections.length&&!('IntersectionObserver'in window))window.addEventListener('scroll',scheduleReadingLocation,{passive:true});
window.addEventListener('resize',updateAnchorOffset);
if('ResizeObserver'in window){const sizing=new ResizeObserver(updateAnchorOffset);document.querySelectorAll('.app-header,.topbar,.reader-viewbar').forEach(bar=>sizing.observe(bar));}
updateAnchorOffset();
if(location.hash)navigateHash(location.hash);
scheduleReadingLocation();
document.querySelectorAll('.print-button').forEach(button=>button.addEventListener('click',()=>window.print()));
let closedBeforePrint=null;
window.addEventListener('beforeprint',()=>{closeInspectors();if(closedBeforePrint===null){closedBeforePrint=Array.from(document.querySelectorAll('details:not([open])'));closedBeforePrint.forEach(d=>{d.open=true;});}});
window.addEventListener('afterprint',()=>{if(closedBeforePrint!==null){closedBeforePrint.forEach(d=>{d.open=false;});closedBeforePrint=null;}});
const search=document.getElementById('search'),category=document.getElementById('category');
if(search&&category){const cards=Array.from(document.querySelectorAll('.report-card'));const filter=()=>{const query=search.value.trim().toLocaleLowerCase();let count=0;cards.forEach(card=>{card.hidden=!(card.dataset.search.includes(query)&&(!category.value||card.dataset.category===category.value));if(!card.hidden)count++;});document.getElementById('result-count').textContent=`${count} / ${cards.length}`;document.getElementById('empty-results').hidden=count!==0;};search.addEventListener('input',filter);category.addEventListener('change',filter);}

// The collection rail uses native file links and loads one report at a time.
// Storage is optional (file:// and privacy modes may deny it).
document.querySelectorAll('.competitor-sidebar').forEach(sidebar=>{
  sidebar.classList.add('navigator-enhanced');
  const chooser=sidebar.querySelector('.competitor-switcher'),list=sidebar.querySelector('.competitor-list');
  const input=sidebar.querySelector('[data-competitor-search]'),clear=sidebar.querySelector('[data-competitor-clear]');
  const items=Array.from(list.querySelectorAll('[data-competitor-item]'));
  const count=sidebar.querySelector('[data-competitor-count]'),empty=list.querySelector('.nav-empty');
  const phone=matchMedia('(max-width:820px)'),key='app-studies-nav:'+sidebar.dataset.collectionKey;
  let saved=null;
  try{saved=JSON.parse(sessionStorage.getItem(key));}catch{}
  if(typeof saved?.query==='string')input.value=saved.query.slice(0,160);
  const save=()=>{try{sessionStorage.setItem(key,JSON.stringify({query:input.value.slice(0,160),scroll:list.clientHeight?list.scrollTop:(saved?.scroll||0)}));}catch{}};
  function filter(){
    const query=input.value.trim().toLocaleLowerCase();let total=0;
    items.forEach(item=>{item.hidden=!item.dataset.search.includes(query);if(!item.hidden)total++;});
    count.textContent=`${total} / ${items.length}`;empty.hidden=total!==0;clear.hidden=!input.value;
  }
  function restoreRail(){
    if(!list.clientHeight)return;
    if(Number.isFinite(saved?.scroll))list.scrollTop=Math.max(0,saved.scroll);
    const active=list.querySelector('[aria-current="page"]');
    if(active&&!active.closest('[hidden]')){
      const box=active.getBoundingClientRect(),frame=list.getBoundingClientRect();
      if(box.top<frame.top||box.bottom>frame.bottom)list.scrollTop+=box.top-frame.top-(list.clientHeight-active.clientHeight)/2;
    }
  }
  filter();chooser.open=!phone.matches;requestAnimationFrame(restoreRail);
  phone.addEventListener('change',()=>{chooser.open=!phone.matches;requestAnimationFrame(restoreRail);});
  chooser.addEventListener('toggle',()=>{if(chooser.open)requestAnimationFrame(restoreRail);});
  input.addEventListener('input',()=>{filter();list.scrollTop=0;saved=null;save();});
  clear.addEventListener('click',()=>{input.value='';filter();saved=null;restoreRail();save();input.focus();});
  window.addEventListener('pagehide',save);
  const contexts=new Set(['reader-overview','reader-all','atlas','overview','ui','interaction','technology','business','strengths','decisions','validation','sources','map-features','map-journey','map-screens','map-dataflow']);
  list.querySelectorAll('.competitor-link').forEach(link=>{
    const base=link.getAttribute('href');
    link.addEventListener('click',()=>{
      const hash=location.hash.slice(1);
      const context=contexts.has(hash)?hash:window.reportReader?.anchor()||currentSection?.id;
      link.setAttribute('href',base+(contexts.has(context)?'#'+context:''));save();
      if(phone.matches)chooser.open=false;
    });
  });
});
document.querySelectorAll('.section-menu').forEach(menu=>{
  const trigger=menu.querySelector('summary');
  menu.open=false;
  menu.addEventListener('click',event=>{if(event.target.closest('nav a'))menu.open=false;});
  document.addEventListener('pointerdown',event=>{if(!menu.contains(event.target))menu.open=false;});
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&menu.open){menu.open=false;trigger.focus();}});
});
document.querySelectorAll('.competitor-switcher').forEach(menu=>{
  menu.addEventListener('keydown',event=>{if(event.key==='Escape'&&matchMedia('(max-width:820px)').matches&&menu.open){menu.open=false;menu.querySelector('summary').focus();}});
});

})();
