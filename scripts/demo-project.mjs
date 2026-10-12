import {cp, mkdir, readFile, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {selectLocales} from './localization.mjs';
import {validateProject} from './contract.mjs';
import {outsideSource} from './files.mjs';

const starter=fileURLToPath(new URL('../assets/starter/',import.meta.url));

export async function createDemoProject(target, selection) {
  const p=JSON.parse(await readFile(path.join(starter,'project.json'),'utf8'));
  const demo=JSON.parse(await readFile(new URL('../assets/locales/demo-copy.json',import.meta.url),'utf8'));
  p.locales=selectLocales(selection??p.locales.map(l=>l.id).join(','));
  for(const slide of p.slides) {
    slide.copy=Object.fromEntries(p.locales.map(({id})=>{
      const copy=demo.copy[id]?.[slide.id];
      if(!copy)throw new Error(`No bundled demo translation for ${id}/${slide.id}. Use locales.mjs add for a product project and provide its own copy.`);
      return [id,copy];
    }));
  }
  p.demo={translationReview:demo.translationReview,purpose:demo.purpose,regionalCopyDecision:demo.regionalCopyDecision};
  validateProject(p);
  const {target:dest}=await outsideSource(starter,target);
  await mkdir(dest); // Validate first and preserve any existing project.
  await cp(starter,dest,{recursive:true});
  await writeFile(path.join(dest,'project.json'),JSON.stringify(p,null,2)+'\n');
  return {directory:dest,locales:p.locales.length};
}
