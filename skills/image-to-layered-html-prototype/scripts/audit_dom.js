/* Convert this trusted local source to a function, then page.evaluate(audit, manifest).
 * Returns observations, not an automatic visual-quality verdict.
 */
(manifest) => {
  const root = document.querySelector('[data-artboard]');
  if (!root) throw new Error('Missing [data-artboard]');
  const origin = root.getBoundingClientRect();
  const layers = manifest.layers.map(layer => {
    const matches = document.querySelectorAll(layer.selector);
    const el = matches[0];
    if (!el) return {id: layer.id, count: 0, visible: false};
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    let opacity = 1, hidden = false;
    for (let p = el; p; p = p.parentElement) {
      const s = getComputedStyle(p);
      opacity *= Number(s.opacity);
      hidden ||= s.display === 'none' || s.visibility === 'hidden';
    }
    const range = document.createRange();
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()].filter(v => v.width && v.height);
    const center = [r.left+r.width/2, r.top+r.height/2];
    const hit = document.elementFromPoint(...center);
    return {
      id: layer.id, count: matches.length, tag: el.tagName.toLowerCase(),
      text: el.textContent.trim(), value: typeof el.value === 'string' ? (el.type==='password' ? '•'.repeat(el.value.length) : el.value) : null, inputType: el instanceof HTMLInputElement ? el.type : null, placeholder: el.getAttribute('placeholder'), disabled: !!el.disabled, readOnly: !!el.readOnly, visible: !hidden && opacity > .05 && r.width > 1 && r.height > 1,
      centerUncovered: !!hit && (el.contains(hit) || hit.contains(el)),
      bounds: {x:r.x-origin.x, y:r.y-origin.y, width:r.width, height:r.height},
      opacity, textRects: rects.map(v => ({x:v.x-origin.x,y:v.y-origin.y,width:v.width,height:v.height})),
      style: Object.fromEntries(['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','color',
        'borderRadius','backgroundImage','clipPath','zIndex','textAlign'].map(k => [k, cs[k]]))
    };
  });
  const media = [...root.querySelectorAll('img,canvas,svg image')].map(el => {
    const r=el.getBoundingClientRect();
    return {tag:el.tagName.toLowerCase(), src:el.currentSrc || el.getAttribute('href') || '',
      role:el.dataset.assetRole || null, areaRatio:r.width*r.height/(origin.width*origin.height)};
  });
  const backgrounds = [...root.querySelectorAll('*'),root].filter(el => getComputedStyle(el).backgroundImage.includes('url('))
    .map(el => ({selector:el.id, background:getComputedStyle(el).backgroundImage,role:el.dataset.assetRole||null}));
  const declared = manifest.layers.map(layer => ({
    type:layer.type, element:document.querySelector(layer.selector)
  }));
  const withinArtboard = r => r.width > 1 && r.height > 1 &&
    r.right > origin.left && r.left < origin.right && r.bottom > origin.top && r.top < origin.bottom;
  const visiblyRendered = el => {
    for (let p=el; p; p=p.parentElement) {
      const s=getComputedStyle(p);
      if (s.display==='none' || s.visibility==='hidden' || Number(s.opacity)<.05) return false;
    }
    return true;
  };
  const unlistedText=[];
  const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node=walker.currentNode, value=node.textContent.trim(), parent=node.parentElement;
    if (!value || !parent || !visiblyRendered(parent) ||
        ['SCRIPT','STYLE','NOSCRIPT','TEMPLATE'].includes(parent.tagName)) continue;
    const range=document.createRange(); range.selectNodeContents(node);
    const r=range.getBoundingClientRect();
    if (!withinArtboard(r)) continue;
    if (declared.some(v=>v.element?.contains(node) &&
        ['text','button','control','svg','svg-path'].includes(v.type))) continue;
    unlistedText.push({text:value.slice(0,80),x:r.x-origin.x,y:r.y-origin.y});
  }
  const unlistedControls=[...root.querySelectorAll('button,a,input,select,textarea,summary,[role="button"],[role="link"]')]
    .filter(el=>visiblyRendered(el) && withinArtboard(el.getBoundingClientRect()) &&
      !declared.some(v=>['button','control'].includes(v.type) && v.element?.contains(el)))
    .map(el=>({tag:el.tagName.toLowerCase(),text:(el.textContent||el.getAttribute('aria-label')||'').trim().slice(0,80)}));
  return {schema:1,url:location.href,viewport:{width:innerWidth,height:innerHeight},
    dpr:devicePixelRatio,fontsReady:document.fonts.status==='loaded',
    imagesReady:[...root.querySelectorAll('img')].every(i=>i.complete && i.naturalWidth>0),
    layers,media,backgrounds,unlistedText,unlistedControls};
}
