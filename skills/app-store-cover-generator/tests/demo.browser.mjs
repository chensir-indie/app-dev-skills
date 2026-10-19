import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {chromium} from 'playwright';
import {createDemoProject} from '../scripts/demo-project.mjs';
import {serve} from '../scripts/server.mjs';
import {auditCover} from '../scripts/audit.mjs';

test('all translated demo cells fit native canvases and the picker exposes every locale',async()=>{
  const tmp=await mkdtemp(path.join(tmpdir(),'cover-demo-browser-'));
  let server,browser;
  try {
    const result=await createDemoProject(path.join(tmp,'project'),'app-store');
    const p=JSON.parse(await readFile(path.join(result.directory,'project.json'),'utf8'));
    server=await serve(result.directory);
    browser=await chromium.launch();
    const page=await browser.newPage();
    await page.goto(server.url);
    await page.waitForFunction(()=>window.coverReady);
    assert.equal(await page.locator('#locale option').count(),50);
    assert.match(await page.locator('#locale option[value="ja"]').textContent(),/日本語.*ja/);
    await page.selectOption('#locale','zh-Hant');
    await page.waitForURL('**/?locale=zh-Hant&device=iphone&slide=capture');
    await page.waitForFunction(()=>window.coverReady);
    assert.equal(await page.locator('#headline [data-text]').textContent(),p.slides[0].copy['zh-Hant'].headline);
    const failures=[];
    for(const locale of p.locales)for(const device of p.devices)for(const slide of p.slides){
      await page.setViewportSize({width:device.width,height:device.height});
      await page.goto(`${server.url}/?${new URLSearchParams({locale:locale.id,device:device.id,slide:slide.id,export:'1'})}`);
      await page.waitForFunction(()=>window.coverReady);
      const rendered=await page.evaluate(()=>({lang:document.documentElement.lang,dir:document.documentElement.dir,copy:Object.fromEntries(['headline','support','uiTitle','uiBody'].map(id=>[id,document.querySelector(`#${id} [data-text]`).textContent]))}));
      assert.equal(rendered.lang,locale.id);
      assert.equal(rendered.dir,locale.direction);
      assert.deepEqual(rendered.copy,slide.copy[locale.id]);
      const audit=await page.evaluate(auditCover,p.minTextScale);
      if(audit.issues.length)failures.push({locale:locale.id,device:device.id,slide:slide.id,issues:audit.issues});
    }
    assert.deepEqual(failures,[]);
  } finally {
    await browser?.close();
    await server?.close();
    await rm(tmp,{recursive:true,force:true});
  }
});
