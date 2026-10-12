import {mkdtemp, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {createDemoProject} from './demo-project.mjs';
import {serve} from './server.mjs';

const tmp=await mkdtemp(path.join(tmpdir(),'store-cover-demo-'));
let server;
try {
  const result=await createDemoProject(path.join(tmp,'project'),'app-store');
  server=await serve(result.directory,Number(process.argv[2]||0));
  console.log(`${server.url}\n${result.locales} languages/regions · 2 stories · phone + tablet\nDemo translations are drafts. Temporary project: ${result.directory}`);
} catch(error) {
  await rm(tmp,{recursive:true,force:true});
  throw error;
}
let closing=false;
for(const signal of ['SIGINT','SIGTERM'])process.on(signal,async()=>{
  if(closing)return;
  closing=true;
  await server.close();
  await rm(tmp,{recursive:true,force:true});
  process.exit(0);
});
