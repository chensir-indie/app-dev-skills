// Shared runtime checks for this skill's browser CLIs. Never installs dependencies.
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const quote = value => "'" + value.replaceAll("'", "'\\''") + "'";
function fail(message) {
  console.error('Environment error: ' + message);
  console.error('Check: sh ' + quote(path.join(__dirname, 'doctor.sh')) + ' --scope browser');
  console.error('Run repairs from the directory printed by doctor. Skill directory: ' + root);
  process.exit(2);
}
function getChromium(spec = 'playwright') {
  if (Number(process.versions.node.split('.')[0]) < 22) fail('Node.js 22+ is required. Install from https://nodejs.org/en/download');
  try { return require(spec).chromium; }
  catch (error) { fail('Playwright could not load: ' + error.message.split('\n')[0]); }
}
async function launchChromium(chromium) {
  try {
    return await chromium.launch({channel: process.env.PLAYWRIGHT_CHANNEL || undefined, headless: true, timeout: 15000});
  } catch (error) { fail('Browser could not start: ' + error.message.split('\n')[0]); }
}
module.exports = {getChromium, launchChromium};
