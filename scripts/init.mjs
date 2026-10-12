import {createDemoProject} from './demo-project.mjs';
const [target,flag,selection,...extra]=process.argv.slice(2);
if(!target||extra.length||(flag!==undefined&&(flag!=='--locales'||!selection)))
  throw new Error('Usage: node scripts/init.mjs NEW_DIRECTORY [--locales app-store|ja,fr-CA,ur-PK]');
const result=await createDemoProject(target,selection);
console.log(
  `Created ${result.directory} (${result.locales} demo locales); edit project.json and style.css. Demo translations are drafts.`,
);
