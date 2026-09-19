#!/usr/bin/env node
// Check a page at real phone width. Headless Chrome won't size a window below
// 500px, so a plain `--window-size=375,...` screenshot is a cropped 500px layout
// and shows clipping that isn't there. This emulates the device via DevTools.
//
//   node scripts/phone-check.mjs <url> [out.png] [width=375]
//
// Prints elements whose right edge passes the viewport; writes a full-page
// screenshot if out.png is given. Needs Google Chrome and Node 22+.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [url, out, w = '375'] = process.argv.slice(2);
if (!url) { console.error('usage: phone-check.mjs <url> [out.png] [width]'); process.exit(2); }
const width = +w;
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const port = 9300 + Math.floor(Math.random() * 500);
const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', `--remote-debugging-port=${port}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), 'phone-check-'))}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));

let targets;
for (let i = 0; i < 50 && !targets; i++) {
  await sleep(200);
  try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); } catch {}
}
const page = targets.find(t => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const waiting = new Map();
ws.addEventListener('message', e => { const m = JSON.parse(e.data); if (waiting.has(m.id)) { waiting.get(m.id)(m.result); waiting.delete(m.id); } });
const send = (method, params = {}) => new Promise(r => { waiting.set(++id, r); ws.send(JSON.stringify({ id, method, params })); });

await send('Emulation.setDeviceMetricsOverride', { width, height: 800, deviceScaleFactor: 2, mobile: true });
await send('Page.enable');
await send('Page.navigate', { url });
await sleep(4000);
const { result } = await send('Runtime.evaluate', { returnByValue: true, expression: `(() => {
  const vw = document.documentElement.clientWidth, o = [];
  document.querySelectorAll('body *').forEach(e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e);
    if (r.right > vw + 1 && r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.position !== 'fixed')
      o.push(e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\\s+/).slice(0, 4).join('.') : '') + '  right=' + Math.round(r.right) + ' width=' + Math.round(r.width)); });
  return { vw, scrollWidth: document.documentElement.scrollWidth, height: document.documentElement.scrollHeight, over: o.slice(0, 25) };
})()` });
const v = result.value;
console.log(`${url}\n  viewport ${v.vw}px, page scrollWidth ${v.scrollWidth}px, ${v.over.length ? v.over.length + ' overflowing element(s):' : 'no overflow'}`);
v.over.forEach(l => console.log('   ', l));
if (out) {
  await send('Emulation.setDeviceMetricsOverride', { width, height: Math.min(v.height, 12000), deviceScaleFactor: 1, mobile: true });
  await sleep(800);
  const shot = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(out, Buffer.from(shot.data, 'base64'));
  console.log('  screenshot:', out);
}
ws.close(); chrome.kill();
process.exit(v.over.length ? 1 : 0);
