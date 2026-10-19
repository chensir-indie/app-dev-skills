// Capture one native-size state and bind its screenshot/DOM audit to current sources.
// node capture_native.cjs /absolute/path/to/prototype /path/to/playwright [state-id]
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {pathToFileURL} = require('node:url');

const root = fs.realpathSync(path.resolve(process.argv[2] || ''));
const playwright = process.argv[3] || 'playwright';
const stateId = process.argv[4] || 'home';
if (!fs.existsSync(path.join(root, 'index.html'))) {
  throw new Error('Prototype directory with index.html required');
}
const {chromium} = require(playwright);
const read = name => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'));
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const sharedDirs = (read('render-config.json').sharedRuntimeDirs || []).map(entry => {
  const dir = fs.realpathSync(path.resolve(root, entry));
  if (!entry.startsWith('../') || path.dirname(dir) !== path.dirname(root) ||
      ['reference','evidence'].includes(path.basename(dir)) || !fs.statSync(dir).isDirectory()) {
    throw new Error('Invalid shared runtime directory: ' + entry);
  }
  return dir;
});
const safePath = name => {
  const file = fs.realpathSync(path.resolve(root, name));
  const inside = file.startsWith(root + path.sep) ||
    sharedDirs.some(dir => file.startsWith(dir + path.sep));
  if (!inside || !fs.statSync(file).isFile()) {
    throw new Error('Missing or nonlocal capture source: ' + name);
  }
  return file;
};
const walkRuntime = (folder, found=[]) => {
  for (const entry of fs.readdirSync(folder, {withFileTypes:true})) {
    if (['evidence','reference','node_modules','.git'].includes(entry.name)) continue;
    const file=path.join(folder,entry.name);
    if (entry.isDirectory()) walkRuntime(file,found);
    else if (/\.(css|js|svg|woff2?)$/i.test(entry.name)) found.push(path.relative(root,file));
  }
  return found;
};

(async () => {
  const manifest = read('layer-manifest.json');
  const states = read('state-matrix.json');
  if (!states.some(state=>state.id===stateId)) throw new Error('Unknown state: '+stateId);
  const {width,height}=manifest.reference;
  const browser=await chromium.launch({channel:process.env.PLAYWRIGHT_CHANNEL || undefined,headless:true});
  try {
    const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
    const url=pathToFileURL(path.join(root,'index.html')).href;
    await page.goto(url,{waitUntil:'load'});
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map(image=>image.decode()));
      window.scrollTo(0,0);
    });
    await page.addStyleTag({content:'*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}'});
    const auditSource=fs.readFileSync(path.join(__dirname,'audit_dom.js'),'utf8');
    const audit=new Function('return ('+auditSource+')')();
    const observed=await page.evaluate(audit,manifest);
    const dir=path.join(root,'evidence');
    fs.mkdirSync(dir,{recursive:true});
    const screenshot=`evidence/native-${stateId}.png`;
    const dom=`evidence/dom-${stateId}.json`;
    const capture=`evidence/capture-${stateId}.json`;
    await page.screenshot({path:path.join(root,screenshot),fullPage:false,
      animations:'disabled',caret:'hide',scale:'css'});
    fs.writeFileSync(path.join(root,dom),JSON.stringify(observed,null,2)+'\n');
    const assets=read('asset-manifest.json').map(asset=>asset.source);
    const sources=[...new Set(['index.html','layer-manifest.json','design-tokens.json',
      'render-config.json','asset-manifest.json','state-matrix.json',
      ...walkRuntime(root),
      ...sharedDirs.flatMap(dir=>walkRuntime(dir)
        .filter(name=>/\.(css|js|woff2?)$/i.test(name))
        .map(name=>path.relative(root,path.join(dir,name)))),
      ...assets])];
    const sourceHashes=Object.fromEntries(sources.sort().map(name=>[name,sha(safePath(name))]));
    const receipt={schema:1,browserVersion:browser.version(),url:observed.url,
      viewport:observed.viewport,dpr:observed.dpr,screenshot,
      screenshotSha256:sha(path.join(root,screenshot)),dom,domSha256:sha(path.join(root,dom)),
      sources:sourceHashes};
    fs.writeFileSync(path.join(root,capture),JSON.stringify(receipt,null,2)+'\n');
    console.log(JSON.stringify({screenshot,dom,capture,browserVersion:receipt.browserVersion,
      unlistedText:observed.unlistedText.length,unlistedControls:observed.unlistedControls.length}));
  } finally {
    await browser.close();
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
