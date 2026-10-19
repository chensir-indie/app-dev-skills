import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp, readFile, rm, access} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {execFile,spawn} from 'node:child_process';
import {once} from 'node:events';
import {promisify} from 'node:util';
import {catalog, coverage} from '../scripts/localization.mjs';
import {validateProject, cells} from '../scripts/contract.mjs';
const run=promisify(execFile);
const repo=new URL('../',import.meta.url);

test('global demo initialization contains explicit copy for all store locales',async()=>{
  const dir=await mkdtemp(path.join(tmpdir(),'cover-demo-'));
  try {
    const target=path.join(dir,'global');
    await run(process.execPath,['scripts/init.mjs',target,'--locales','app-store'],{cwd:repo});
    const p=validateProject(JSON.parse(await readFile(path.join(target,'project.json'),'utf8')));
    assert.deepEqual(p.locales.map(l=>l.id),catalog.locales);
    assert.equal(cells(p).length,200);
    assert.deepEqual(coverage(p).missing,[]);
    for(const slide of p.slides)assert.deepEqual(Object.keys(slide.copy),catalog.locales);
    assert.notEqual(p.slides[0].copy.ja.headline,p.slides[0].copy['en-US'].headline);
    assert.equal(p.demo.translationReview,'draft');
    await assert.rejects(run(process.execPath,['scripts/init.mjs',target,'--locales','app-store'],{cwd:repo}),/EEXIST/);
  } finally {await rm(dir,{recursive:true,force:true});}
});

test('selected demo locales are exact; unsupported demo translations fail before writing',async()=>{
  const dir=await mkdtemp(path.join(tmpdir(),'cover-demo-'));
  try {
    const target=path.join(dir,'selected');
    await run(process.execPath,['scripts/init.mjs',target,'--locales','ja,fr-CA,ur-PK'],{cwd:repo});
    const p=validateProject(JSON.parse(await readFile(path.join(target,'project.json'),'utf8')));
    assert.deepEqual(p.locales.map(l=>l.id),['ja','fr-CA','ur-PK']);
    assert.equal(p.locales[2].direction,'rtl');
    for(const args of [['--locales','fa-IR'],['--unknown'],['--locales','ja,ja']]) {
      const invalid=path.join(dir,'invalid');
      await assert.rejects(run(process.execPath,['scripts/init.mjs',invalid,...args],{cwd:repo}));
      await assert.rejects(access(invalid));
    }
  } finally {await rm(dir,{recursive:true,force:true});}
});

test('demo command serves all locales and removes its temporary project on shutdown',async()=>{
  const child=spawn(process.execPath,['scripts/demo.mjs'],{cwd:repo,stdio:['ignore','pipe','pipe']});
  const exit=once(child,'exit');
  let output='';
  const timeout=setTimeout(()=>child.kill('SIGTERM'),10000);
  try {
    for await (const chunk of child.stdout) {
      output+=chunk;
      if(output.includes('Temporary project:'))break;
    }
    const url=output.match(/http:\/\/127\.0\.0\.1:\d+/)?.[0];
    const directory=output.match(/Temporary project: (.+)/)?.[1];
    assert.ok(url&&directory,'demo must report its URL and project');
    const p=await (await fetch(url+'/project.json')).json();
    assert.deepEqual(p.locales.map(l=>l.id),catalog.locales);
    child.kill('SIGTERM');
    assert.equal((await exit)[0],0);
    await assert.rejects(access(directory));
  } finally {
    clearTimeout(timeout);
    if(child.exitCode===null)child.kill('SIGTERM');
    await exit;
  }
});
