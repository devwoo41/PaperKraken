#!/usr/bin/env node
// PaperKraken deterministic PDF renderer.
// Usage: node render_pdf.mjs <report.html> <out.pdf>
// Waits for the template's window.__PK_DONE flag (set after MathJax typeset
// + Paged.js pagination complete), then prints. Env: PK_TIMEOUT ms (default 120000).
import { createRequire } from 'module';
import { execSync } from 'child_process';
import { existsSync, readdirSync } from 'fs';
import { resolve } from 'path';
import os from 'os';

const [html, out] = process.argv.slice(2);
if (!html || !out) {
  console.error('usage: node render_pdf.mjs <report.html> <out.pdf>');
  process.exit(1);
}
if (!existsSync(html)) {
  console.error(`ERROR: HTML not found: ${html}`);
  process.exit(1);
}

const globalRoot = execSync('npm root -g').toString().trim();
const require = createRequire(globalRoot + '/');
const { chromium } = require(globalRoot + '/playwright-core');

function findBrowser() {
  const cache = `${os.homedir()}/.cache/ms-playwright`;
  const pick = (prefix, suffix) => {
    if (!existsSync(cache)) return null;
    const dirs = readdirSync(cache).filter((d) => d.startsWith(prefix)).sort();
    for (let i = dirs.length - 1; i >= 0; i--) {
      const p = `${cache}/${dirs[i]}/${suffix}`;
      if (existsSync(p)) return p;
    }
    return null;
  };
  return (
    pick('chromium_headless_shell-', 'chrome-headless-shell-linux64/chrome-headless-shell') ||
    pick('chromium-', 'chrome-linux/chrome') ||
    ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].find(existsSync) ||
    null
  );
}

const executablePath = findBrowser();
if (!executablePath) {
  console.error('ERROR: no Chromium found. Run: npx playwright install chromium');
  process.exit(2);
}

const timeout = parseInt(process.env.PK_TIMEOUT || '120000', 10);

const browser = await chromium.launch({
  executablePath,
  args: ['--no-sandbox', '--allow-file-access-from-files', '--disable-dev-shm-usage'],
});
try {
  const page = await browser.newPage();
  page.on('pageerror', (e) => console.error(`PAGE ERROR: ${e.message}`));
  await page.goto('file://' + resolve(html), { waitUntil: 'networkidle', timeout });
  try {
    await page.waitForFunction('window.__PK_DONE === true', { timeout });
  } catch {
    console.error(
      'WARN: __PK_DONE flag never set (template without the flag, or MathJax/Paged.js failed). Printing current state.'
    );
  }
  const pages = await page.evaluate(
    () => document.querySelectorAll('.pagedjs_page').length
  );
  await page.pdf({
    path: out,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  console.log(`OK: ${out} (${pages > 0 ? pages + ' paged.js pages' : 'no paged.js pagination'})`);
} finally {
  await browser.close();
}
