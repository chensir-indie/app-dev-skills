// Integration smoke test with Playwright Chromium (or PLAYWRIGHT_CHANNEL).
// node test_dom.cjs /absolute/path/to/node_modules/playwright
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {chromium} = require(process.argv[2] || 'playwright');
(async () => {
  const browser = await chromium.launch({channel: process.env.PLAYWRIGHT_CHANNEL || undefined, headless: true});
  try {
    const page = await browser.newPage({viewport:{width:400,height:500},deviceScaleFactor:1});
    await page.setContent('<main data-artboard style="position:relative;width:400px;height:500px"><h1 id="title">今日養護</h1><button id="action">識別</button><input id="name" value="龜背竹"><textarea id="note">Notes</textarea><select id="room"><option value="living">客廳</option><option value="balcony">陽台</option></select><svg id="panel" width="120" height="80"><path d="M0 40 Q20 0 50 0 L120 50 V80 H0Z" fill="green"/></svg></main>');
    const manifest = {layers:[
      {id:'title',selector:'#title',type:'text'}, {id:'action',selector:'#action',type:'button'},
      {id:'panel',selector:'#panel',type:'svg'}, {id:'name',selector:'#name',type:'control'}, {id:'note',selector:'#note',type:'control'}, {id:'room',selector:'#room',type:'control'}
    ]};
    const source = fs.readFileSync(path.join(__dirname,'audit_dom.js'),'utf8');
    const audit = new Function('return (' + source + ')')();
    const first = await page.evaluate(audit, manifest);
    assert.equal(first.layers[0].text,'今日養護');
    assert.equal(first.layers[0].visible,true);
    assert.equal(first.layers[1].tag,'button');
    assert.equal(first.layers[2].tag,'svg');
    assert.deepEqual(first.unlistedText,[]);
    assert.deepEqual(first.unlistedControls,[]);
    assert.equal(first.layers[3].value,'龜背竹');
    assert.equal(first.layers[3].inputType,'text');
    assert.equal(first.layers[3].disabled,false);
    assert.equal(first.layers[3].readOnly,false);
    await page.locator('#name').fill('新植物');
    await page.locator('#note').fill('New note');
    await page.locator('#room').selectOption('balcony');
    const formEdited=await page.evaluate(audit,manifest);
    assert.equal(formEdited.layers[3].value,'新植物');
    assert.equal(formEdited.layers[4].value,'New note');
    assert.equal(formEdited.layers[5].value,'balcony');
    assert.deepEqual(formEdited.unlistedControls,[]);
    await page.locator('[data-artboard]').evaluate(e => {
      e.insertAdjacentHTML('beforeend','<span id="forgotten">Forgotten</span><button id="extra">Extra</button>');
    });
    const incomplete = await page.evaluate(audit,manifest);
    assert(incomplete.unlistedText.some(item=>item.text==='Forgotten'));
    assert(incomplete.unlistedControls.some(item=>item.text==='Extra'));
    await page.locator('#forgotten,#extra').evaluateAll(elements=>elements.forEach(e=>e.remove()));
    await page.locator('#title').evaluate(e => e.style.display='none');
    const hidden = await page.evaluate(audit, manifest);
    assert.equal(hidden.layers[0].visible,false);
    await page.locator('#title').evaluate(e => {e.style.display='block';e.textContent='新的文字';});
    const changed = await page.evaluate(audit,manifest);
    assert.equal(changed.layers[0].text,'新的文字');
    await page.locator('#title').evaluate(e => {
      const overlay=document.createElement('div');
      overlay.style='position:absolute;inset:0;z-index:100;background:white';
      e.parentElement.append(overlay);
    });
    const covered = await page.evaluate(audit,manifest);
    assert.equal(covered.layers[0].centerUncovered,false);
    console.log(JSON.stringify({browser:browser.version(),domTests:'passed',
      observations:['visible CJK text','semantic button','SVG layer','unlisted text/control','hidden text','edited text','covered text','native input/textarea/select values','real fill/select interaction']}));
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error);process.exit(1);});
