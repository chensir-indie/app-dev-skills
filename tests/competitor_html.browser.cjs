const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');
const { execFile } = require('node:child_process');
const { promisify } = require('node:util');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');
const run = promisify(execFile);
const skill = path.resolve(__dirname, '../skills/app-competitor-analysis');

async function withReport(check, prepare) {
  const folder = await fs.mkdtemp(path.join(os.tmpdir(), 'teardown-html-'));
  let browser;
  try {
    const bundle = prepare ? await prepare(folder) : await prepareLegacyAtlas(folder);
    await run('python3', [path.join(skill, 'scripts/render_reports.py'),
      bundle, '--output', path.join(folder, 'reports')]);
    browser = await chromium.launch({ channel: process.env.PLAYWRIGHT_CHANNEL || undefined });
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const base = pathToFileURL(path.join(folder, 'reports')).href;
    await check(page, base);
  } finally {
    if (browser) await browser.close();
    await fs.rm(folder, { recursive: true, force: true });
  }
}

// Keep the original graph/zoom fixtures explicit; the public example now also
// contains authored semantic priorities. New semantic collections get CUA review
// and the switcher regression below.
async function prepareLegacyAtlas(folder) {
  const b=JSON.parse(await fs.readFile(path.join(skill,'assets/report-bundle.example.json'),'utf8'));
  for(const p of b.products){delete p.visuals.features.priority;delete p.visuals.journey.focus;delete p.visuals.dataflow.contract;}
  const file=path.join(folder,'legacy-atlas.json');await fs.writeFile(file,JSON.stringify(b));return file;
}
async function visitChapter(page,id){
  const views={atlas:'capabilities',ui:'interface',interaction:'interaction',technology:'technology',business:'decisions',sources:'sources','reader-overview':'overview','reader-all':'all'};
  const select=page.locator('[data-reader-select]');
  if(await select.isVisible())await select.selectOption(views[id]);
  else await page.locator(`[data-reader-link="${views[id]}"]`).click();
}
async function settled(page){await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));}
async function prepareImageFixture(folder) {
  // Original solid-color PNGs exercise framing without using competitor media.
  await run('python3', ['-c', `
import copy, json, pathlib, struct, sys, zlib
folder = pathlib.Path(sys.argv[1])
bundle = json.loads(pathlib.Path(sys.argv[2]).read_text())
original = bundle['products'][0]
bundle['products'] = []
def chunk(kind, payload):
    return struct.pack('>I', len(payload)) + kind + payload + struct.pack('>I', zlib.crc32(kind + payload) & 0xffffffff)
for name, width, height in [('portrait', 240, 520), ('landscape', 520, 240), ('square', 240, 240)]:
    pixels = b''.join(b'\\0' + bytes([80, 120, 180]) * width for _ in range(height))
    image = b'\\x89PNG\\r\\n\\x1a\\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(pixels)) + chunk(b'IEND', b'')
    (folder / (name + '.png')).write_bytes(image)
    product = copy.deepcopy(original)
    product.update(id=name, name='Original ' + name + ' fixture')
    product['sections'][1]['blocks'].append(dict(type='image', path=name + '.png', alt='Original layout fixture', caption='Synthetic fixture, not app UI', sources=['E1'],
        viewport=dict(x=0, y=0, width=width, height=height, source_width=width, source_height=height)))
    bundle['products'].append(product)
(folder / 'bundle.json').write_text(json.dumps(bundle))
`, folder, path.join(skill, 'assets/report-bundle.example.json')]);
  return path.join(folder, 'bundle.json');
}

test('index image windows preserve full portrait, landscape and square framing at each layout', async () => {
  await withReport(async (page, base) => {
    for (const width of [1440, 1000, 900, 390]) {
      await page.setViewportSize({ width, height: 1000 });
      await page.goto(base + '/index.html');
      for (const media of ['screen', 'print']) {
        await page.emulateMedia({ media });
        const frames = await page.locator('.card-media').evaluateAll(cards => cards.map(card => {
          const frame = card.querySelector('.media-view.viewport');
          const box = card.getBoundingClientRect(), image = frame.getBoundingClientRect();
          const style = getComputedStyle(card);
          const [sourceWidth, sourceHeight] = frame.style.getPropertyValue('--media-ratio').split('/').map(Number);
          return {
            name: card.getAttribute('aria-label'),
            top: image.top - box.top - parseFloat(style.borderTopWidth) - parseFloat(style.paddingTop),
            bottom: box.bottom - image.bottom - parseFloat(style.borderBottomWidth) - parseFloat(style.paddingBottom),
            left: image.left - box.left - parseFloat(style.borderLeftWidth) - parseFloat(style.paddingLeft),
            right: box.right - image.right - parseFloat(style.borderRightWidth) - parseFloat(style.paddingRight),
            ratio: image.width / image.height, expectedRatio: sourceWidth / sourceHeight,
          };
        }));
        for (const frame of frames) {
          for (const side of ['top', 'bottom', 'left', 'right']) {
            assert.ok(frame[side] >= -1, `${frame.name} ${side} must remain inside the ${width}px ${media} card content area: ${frame[side]}`);
          }
          assert.ok(Math.abs(frame.ratio - frame.expectedRatio) < .01, 'The image window must preserve source aspect ratio');
        }
      }
      await page.emulateMedia({ media: 'screen' });
    }
  }, prepareImageFixture);
});

test('wide UI evidence uses the full figure width with observations and stays within the phone page', async () => {
  await withReport(async (page, base) => {
    for (const width of [1440, 390]) {
      await page.setViewportSize({ width, height: 1000 });
      await page.goto(base + '/landscape.html#ui');
      const board = page.locator('#ui .ui-board-wide');
      assert.equal(await board.count(), 1);
      assert.equal(await board.locator('.ui-observation').count(), 2);
      const frame = board.locator('figure .media-view.viewport');
      await frame.scrollIntoViewIfNeeded();
      await frame.locator('img').evaluate(image => image.decode());
      const layout = await frame.evaluate(element => {
        const figure = element.closest('figure');
        const style = getComputedStyle(figure), box = figure.getBoundingClientRect();
        const window = element.getBoundingClientRect(), image = element.querySelector('img').getBoundingClientRect();
        return {
          availableWidth: box.width - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight)
            - parseFloat(style.borderLeftWidth) - parseFloat(style.borderRightWidth),
          width: window.width, ratio: window.width / window.height,
          edges: ['left', 'right', 'top', 'bottom'].map(side => image[side] - window[side]),
        };
      });
      assert.ok(Math.abs(layout.width - layout.availableWidth) < 1,
        `The ${width}px wide UI image must use the figure content width instead of a portrait-width cap`);
      if (width === 1440) assert.ok(layout.width > 340, 'Desktop landscape evidence must not inherit the 340px portrait limit');
      assert.ok(Math.abs(layout.ratio - 520 / 240) < .01, 'Landscape evidence must preserve the source ratio');
      assert.ok(layout.edges.every(delta => Math.abs(delta) < 1), 'The full source image must remain inside the display window');
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    }
  }, async folder => {
    const filename = await prepareImageFixture(folder);
    const bundle = JSON.parse(await fs.readFile(filename, 'utf8'));
    const landscape = bundle.products.find(product => product.id === 'landscape');
    landscape.sections.find(section => section.id === 'ui').blocks.push({
      type: 'table',
      columns: ['Region', 'Visible structure', 'Task implication'],
      rows: [
        ['Full-width evidence', 'Original landscape PNG', 'Inspect the entire image without a portrait-width limit.'],
        ['Annotations', 'Adjacent source-linked observations', 'Keep the analysis readable at desktop and phone widths.'],
      ],
      sources: ['E1'],
    });
    await fs.writeFile(filename, JSON.stringify(bundle));
    return filename;
  });
});

test('node → source → back → Escape preserves focus and the reading context', async()=>{
 await withReport(async(page,base)=>{
  await page.goto(base+'/example-notes.html#atlas');
  const node=page.locator('#map-features [data-node-detail]').first();
  await node.click();await settled(page);
  const title=await page.locator('#inspection-title').innerText();
  const position=await page.evaluate(()=>scrollY);
  for(let i=0;i<3;i++){
   await page.locator('dialog a[href="#source-E1"]').click();
   assert.ok(page.url().endsWith('#source-E1'));
   await page.locator('[data-inspection-back]').click();await settled(page);
   assert.equal(await page.locator('dialog').getAttribute('open'),'');
   assert.equal(await page.locator('#inspection-title').innerText(),title);
  }
  await page.keyboard.press('Escape');await settled(page);
  assert.equal(await page.locator('dialog').getAttribute('open'),null);
  assert.equal(await node.evaluate(n=>document.activeElement===n),true);
  assert.ok(Math.abs(await page.evaluate(()=>scrollY)-position)<2);
 });
});
test('phone chapter selection and desktop tabs reveal the target below sticky controls',async()=>{
 await withReport(async(page,base)=>{
  for(const width of[1280,390,320]){
   await page.setViewportSize({width,height:900});await page.goto(base+'/example-notes.html');
   for(const id of['ui','technology','interaction']){
    await visitChapter(page,id);await settled(page);
    const geometry=await page.locator('#'+id).evaluate(n=>({top:n.getBoundingClientRect().top,bar:document.querySelector('.reader-viewbar').getBoundingClientRect().bottom}));
    assert.ok(geometry.top>=geometry.bar-2,JSON.stringify(geometry));
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
   }
   await visitChapter(page,'reader-all');assert.equal(await page.locator('[data-reader-view]:visible').count(),7);
  }
 });
});
test('expanded map supports zoom, text alternative, nested node return and focus restoration',async()=>{
 await withReport(async(page,base)=>{
  await page.goto(base+'/example-notes.html#map-journey');
  await page.locator('[data-expand-map="map-journey"]').click();
  const svg=page.locator('dialog .graph-svg').first();
  await page.locator('[data-viewer-zoom="in"]').click();
  const width=await svg.evaluate(n=>n.getBoundingClientRect().width);
  await page.locator('dialog [data-node-detail]').first().click();
  await page.locator('[data-inspection-back]').click();await settled(page);
  assert.ok(Math.abs(await svg.evaluate(n=>n.getBoundingClientRect().width)-width)<1);
  await page.locator('[data-viewer-zoom="fit"]').click();
  await page.locator('[data-viewer-list]').click();
  assert.equal(await page.locator('dialog .graph-collection').isVisible(),false);
  assert.equal(await page.locator('dialog .graph-index').getAttribute('open'),'');
  await page.keyboard.press('Escape');await settled(page);
  assert.equal(await page.locator('[data-expand-map="map-journey"]').evaluate(n=>document.activeElement===n),true);
 });
});
test('original media viewer has explicit sizing, Escape and exact source access',async()=>{
 await withReport(async(page,base)=>{
  await page.goto(base+'/landscape.html#ui');
  await page.locator('#ui .media-open').click();
  assert.equal(await page.locator('.inspection-image-stage img').evaluate(n=>n.naturalWidth),520);
  await page.locator('[data-image-size]').click();
  assert.equal(await page.locator('[data-image-size]').getAttribute('aria-pressed'),'true');
  assert.ok(await page.locator('dialog a[data-native-link]').getAttribute('href'));
  await page.keyboard.press('Escape');await settled(page);
  assert.equal(await page.locator('dialog').getAttribute('open'),null);
 },prepareImageFixture);
});
test('portable library search has an empty state and native report links work without HTTP',async()=>{
 await withReport(async(page,base)=>{
  const remote=[],errors=[];page.on('request',r=>{if(/^https?:/.test(r.url()))remote.push(r.url())});page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(base+'/index.html');await page.locator('#search').fill('nomatches');assert.equal(await page.locator('#empty-results').isVisible(),true);
  await page.locator('#search').fill('Example');await page.locator('.report-card:visible h2 a').click();
  await page.locator('[data-open-library]').click();await page.locator('[data-library-search]').fill('nomatches');assert.equal(await page.locator('.library-empty').isVisible(),true);
  await page.locator('[data-library-search]').fill('Example');await page.locator('[data-library-item]:visible').click();await settled(page);
  assert.equal(await page.locator('dialog').getAttribute('open'),null);
  assert.deepEqual(remote,[]);assert.deepEqual(errors,[]);
 });
});
test('printing restores disclosure states and retains all seven views',async()=>{
 await withReport(async(page,base)=>{
  await page.goto(base+'/example-notes.html#ui');
  const closed=await page.locator('main details:not([open])').count();
  await page.evaluate(()=>{dispatchEvent(new Event('beforeprint'));dispatchEvent(new Event('beforeprint'));});await page.emulateMedia({media:'print'});
  assert.equal(await page.locator('[data-reader-view]:visible').count(),7);
  assert.equal(await page.locator('.competitor-sidebar').isVisible(),false);
  assert.equal(await page.locator('main details:not([open])').count(),0);
  await page.evaluate(()=>dispatchEvent(new Event('afterprint')));await page.emulateMedia({media:'screen'});
  assert.equal(await page.locator('main details:not([open])').count(),closed);
 });
});
test('200 percent text and reduced motion retain usable navigation',async()=>{
 await withReport(async(page,base)=>{
  await page.emulateMedia({reducedMotion:'reduce'});
  for(const width of[1280,390,320]){
   await page.setViewportSize({width,height:900});await page.goto(base+'/example-notes.html#ui');
   await page.evaluate(()=>document.documentElement.style.fontSize='200%');
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
   await page.locator('[data-open-library]').click();
   assert.equal(await page.locator('[data-library-search]').isVisible(),true);
   await page.keyboard.press('Escape');await settled(page);
   assert.equal(await page.locator('[data-open-library]').evaluate(n=>document.activeElement===n),true);
  }
 });
});
// HTTP loading, cancellation, history and error recovery are additionally checked
// against the final collection using its manifest-checked preview server via CUA.
