// Browser-observed implementation inventory. Never writes reference geometry or acceptance.
// node inventory_page.cjs /absolute/path/to/page /absolute/path/to/playwright
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {pathToFileURL} = require('node:url');

const root = fs.realpathSync(path.resolve(process.argv[2] || ''));
const playwright = process.argv[3] || 'playwright';
const reference = path.join(root, 'reference', 'source.png');
const html = path.join(root, 'index.html');
if (!fs.existsSync(reference) || !fs.existsSync(html)) {
  throw new Error('Page must contain index.html and reference/source.png');
}
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const pngSize = file => {
  const bytes = fs.readFileSync(file);
  if (bytes.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
    throw new Error('Native PNG reference required: ' + file);
  }
  return {width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20)};
};

(async () => {
  const {chromium} = require(playwright);
  const {width, height} = pngSize(reference);
  const configPath = path.join(root, 'render-config.json');
  const config = fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath, 'utf8')) : {};
  const browser = await chromium.launch({channel: process.env.PLAYWRIGHT_CHANNEL || undefined, headless: true});
  try {
    const page = await browser.newPage({viewport: {width, height}, deviceScaleFactor: 1,
      locale: config.locale || 'zh-TW', colorScheme: config.colorScheme || 'light',
      reducedMotion: config.reducedMotion ? 'reduce' : 'no-preference'});
    await page.goto(pathToFileURL(html).href, {waitUntil: 'load'});
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map(image => image.decode().catch(() => null)));
      window.scrollTo(0, 0);
    });
    await page.addStyleTag({content: '*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}'});
    const inventory = await page.evaluate(() => {
      const root = document.querySelector('[data-artboard]');
      if (!root) throw new Error('Missing [data-artboard]');
      const origin = root.getBoundingClientRect();
      const controls = 'button,a,input,select,textarea,summary,[role="button"],[role="link"]';
      const rect = element => {
        const r = element.getBoundingClientRect();
        return {x: r.x-origin.x, y: r.y-origin.y, width: r.width, height: r.height};
      };
      const visible = element => {
        const r = element.getBoundingClientRect();
        if (r.width < 1 || r.height < 1 || r.right <= origin.left || r.left >= origin.right ||
            r.bottom <= origin.top || r.top >= origin.bottom) return false;
        for (let node=element; node; node=node.parentElement) {
          const style=getComputedStyle(node);
          if (style.display==='none' || style.visibility==='hidden' || Number(style.opacity)<.05) return false;
        }
        return true;
      };
      const selector = element => {
        if (element.id) return `#${CSS.escape(element.id)}`;
        const parts=[];
        for (let node=element; node && node!==root; node=node.parentElement) {
          if (node.id) {parts.unshift(`#${CSS.escape(node.id)}`); break;}
          let index=1;
          for (let sibling=node.previousElementSibling; sibling; sibling=sibling.previousElementSibling) {
            if (sibling.tagName===node.tagName) index++;
          }
          parts.unshift(`${node.tagName.toLowerCase()}:nth-of-type(${index})`);
        }
        return `[data-artboard] > ${parts.join(' > ')}`;
      };
      const style = element => {
        const s=getComputedStyle(element);
        return Object.fromEntries(['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing',
          'color','opacity','textAlign','backgroundColor','backgroundImage','borderRadius',
          'borderColor','borderWidth','clipPath','filter','zIndex'].map(key=>[key,s[key]]));
      };
      const item=(element,type,text='')=>({type,selector:selector(element),
        bounds:rect(element),text:text.trim().slice(0,240),style:style(element),
        tag:element.tagName.toLowerCase()});
      const candidates=[];
      for (const element of root.querySelectorAll(controls)) {
        if (!visible(element)) continue;
        candidates.push({...item(element,'button',element.innerText || element.value ||
          element.getAttribute('aria-label') || element.getAttribute('placeholder') || ''),
          ariaLabel:element.getAttribute('aria-label') || ''});
      }
      const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
      const seen=new Set();
      while (walker.nextNode()) {
        const node=walker.currentNode, element=node.parentElement;
        const value=node.textContent.trim();
        if (!value || !element || element.closest(controls) ||
            ['SCRIPT','STYLE','NOSCRIPT','TEMPLATE'].includes(element.tagName) ||
            !visible(element)) continue;
        const range=document.createRange(); range.selectNodeContents(node);
        const r=range.getBoundingClientRect();
        if (!r.width || !r.height) continue;
        const key=selector(element);
        if (!seen.has(key)) {candidates.push(item(element,'text',value)); seen.add(key);}
      }
      for (const element of root.querySelectorAll('img,svg')) {
        if (!visible(element)) continue;
        candidates.push({...item(element,element.tagName.toLowerCase()==='img'?'raster':'svg'),
          assetRole:element.dataset.assetRole || null,
          source:element.getAttribute('src') || null,
          loaded:element.tagName.toLowerCase()==='img' ? element.complete && element.naturalWidth>0 : true});
      }
      const area=origin.width*origin.height;
      for (const element of root.querySelectorAll('*')) {
        if (!visible(element) || element.matches(controls+',img,svg') ||
            element.getBoundingClientRect().width*element.getBoundingClientRect().height < area*.01) continue;
        const s=getComputedStyle(element);
        const panel=s.backgroundColor!=='rgba(0, 0, 0, 0)' || s.backgroundImage!=='none' ||
          s.clipPath!=='none' || s.borderTopWidth!=='0px';
        if (panel) candidates.push(item(element,'css-shape'));
      }
      return {url:location.href,viewport:{width:innerWidth,height:innerHeight},dpr:devicePixelRatio,
        fontsReady:document.fonts.status==='loaded',
        imagesReady:[...root.querySelectorAll('img')].every(i=>i.complete && i.naturalWidth>0),
        candidates};
    });
    const evidence=path.join(root,'evidence');
    fs.mkdirSync(evidence,{recursive:true});
    const screenshot=path.join(evidence,'inventory-native.png');
    await page.screenshot({path:screenshot,fullPage:false,animations:'disabled',caret:'hide',scale:'css'});
    const output={schema:1,kind:'implementation-inventory-only',reference:{path:'reference/source.png',
      sha256:sha(reference),width,height},screenshot:{path:'evidence/inventory-native.png',
      sha256:sha(screenshot)},browserVersion:browser.version(),...inventory};
    const report=path.join(evidence,'implementation-inventory.json');
    fs.writeFileSync(report,JSON.stringify(output,null,2)+'\n');
    console.log(JSON.stringify({report,screenshot,candidates:inventory.candidates.length,
      text:inventory.candidates.filter(c=>c.type==='text').length,
      controls:inventory.candidates.filter(c=>c.type==='button').length,
      unloadedAssets:inventory.candidates.filter(c=>c.type==='raster'&&!c.loaded).length}));
    if (!inventory.imagesReady || !inventory.fontsReady) process.exitCode=1;
  } finally {
    await browser.close();
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
