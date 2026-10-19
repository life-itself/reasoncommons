import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve, join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { sha256 } from './import.mjs';

export const APP = dirname(fileURLToPath(import.meta.url));
export const ROOT = resolve(APP, '../..');
export const LAB = join(ROOT, 'website/landing-lab');
export const RUNS = join(APP, '.runs');
export const readJSON = async path => JSON.parse(await readFile(path, 'utf8'));
export const writeJSON = async (path, value) => writeFile(path, JSON.stringify(value, null, 2) + '\n');
export const inputDigest = run => sha256(JSON.stringify({ registry: run.registry, registry_sha256: run.registry_sha256, config: run.config, rubric: run.rubric, facts: run.facts, source_hashes: run.source_hashes, hashes: run.hashes, runner_hashes: run.runner_hashes, captures: run.captures }));
export function verifyRunEvidence(run) {
  if (!run.input_sha256 || run.input_sha256 !== inputDigest(run)) throw new Error('Captured input evidence or contract has changed. Make a new capture instead of grading modified evidence.');
}
export const safeID = value => {
  if (!/^[a-zA-Z0-9][a-zA-Z0-9._-]{0,120}$/.test(value)) throw new Error(`Unsafe identifier: ${value}`);
  return value;
};

export async function contracts() {
  const files = ['eval.config.json', 'rubric.json', 'project-facts.json'];
  const values = await Promise.all(files.map(n => readJSON(join(APP, n))));
  const source_hashes = {};
  for (const fact of values[2].facts) {
    const path = resolve(ROOT, fact.source);
    if (!path.startsWith(ROOT + '/')) throw new Error('Fact source must stay inside the repository.');
    const bytes = await readFile(path);
    if (!bytes.toString().includes(fact.source_quote)) throw new Error(`Source quote has drifted: ${fact.id}. Review the fact before running.`);
    source_hashes[fact.source] = sha256(bytes);
  }
  const hashes = Object.fromEntries(await Promise.all(files.map(async n => [n, sha256(await readFile(join(APP, n)))])));
  const runner_hashes = Object.fromEntries(await Promise.all(['cli.mjs', 'import.mjs', 'capture.mjs', 'judge.mjs', 'report.mjs', 'package-lock.json'].map(async n => [n, sha256(await readFile(join(APP, n)))])));
  return { config: values[0], rubric: values[1], facts: values[2], source_hashes, hashes, runner_hashes };
}

export async function verifiedRegistry() {
  const bytes = await readFile(join(LAB, 'variants.json'));
  const registry = JSON.parse(bytes);
  const seen = new Set();
  for (const v of registry.variants) {
    safeID(v.id);
    if (seen.has(v.id)) throw new Error(`Duplicate candidate id ${v.id}`);
    seen.add(v.id);
    for (const [pathKey, hashKey] of [['source_path', 'source_sha256'], ['entry_path', 'entry_sha256'], ['phone_path', 'phone_sha256']]) {
      if (!v[pathKey]) continue;
      const path = resolve(LAB, v[pathKey]);
      if (!path.startsWith(LAB + '/') || sha256(await readFile(path)) !== v[hashKey]) throw new Error(`Candidate bytes have changed: ${v.id} ${pathKey}. Reimport or explicitly update the registry before capture.`);
    }
  }
  return { registry, registry_sha256: sha256(bytes) };
}

async function contentFrame(page) {
  let best;
  for (const frame of page.frames()) {
    try {
      const length = await frame.evaluate(() => document.body?.innerText.length || 0);
      if (!best || length > best.length) best = { frame, length };
    } catch { /* A bundle may replace its initial document while loading. */ }
  }
  return best;
}

export async function captureOne(browser, target, viewport, runDir, config) {
  const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height }, isMobile: viewport.isMobile, deviceScaleFactor: 1, reducedMotion: 'reduce', locale: 'en-GB', timezoneId: 'Europe/Berlin' });
  const page = await context.newPage();
  const errors = [], failures = [];
  page.on('pageerror', e => errors.push(e.message.slice(0, 1000)));
  page.on('requestfailed', r => failures.push({ url: r.url().replace(/\?.*$/, ''), reason: r.failure()?.errorText }));
  const started = Date.now();
  const id = safeID(`${target.id}--${viewport.id}${target.composition ? '--companion' : ''}`);
  const capture = { id, variant_id: target.id, name: target.name, viewport, composition: target.composition || 'primary', url: target.url, entry_sha256: target.entry_sha256 || null, source_sha256: target.source_sha256 || null, captured_at: new Date().toISOString(), images: [], errors, request_failures: failures };
  try {
    const response = await page.goto(target.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    capture.http_status = response?.status() ?? null;
    if (response) {
      capture.served_body_sha256 = sha256(await response.body());
      capture.served_body_matches_entry = target.entry_sha256 ? capture.served_body_sha256 === target.entry_sha256 : null;
    }
    let best;
    for (let i = 0; i < 60; i++) {
      best = await contentFrame(page);
      if (best?.length > 300 && !await best.frame.evaluate(() => /^.*This page requires JavaScript to display\. Loading/s.test(document.body.innerText))) break;
      await page.waitForTimeout(250);
    }
    if (!best || best.length < 300) throw new Error('Landing content did not become ready; do not grade the loading shell.');
    await page.waitForTimeout(config.capture.settle_ms);
    best = await contentFrame(page);
    try { await Promise.race([best.frame.evaluate(() => document.fonts.ready.then(() => true)), new Promise(r => setTimeout(r, 5000))]); } catch {}
    capture.content_frame = best.frame === page.mainFrame() ? 'main' : 'embedded';
    const measure = () => best.frame.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      const overflowing = [...document.body.querySelectorAll('*')].filter(e => {
        const r = e.getBoundingClientRect(), s = getComputedStyle(e);
        if (s.display === 'none' || s.visibility === 'hidden' || r.width <= 0 || r.height <= 0) return false;
        let p = e.parentElement;
        while (p && p !== document.body) { const ps = getComputedStyle(p); if (['auto', 'scroll', 'hidden', 'clip'].includes(ps.overflowX)) return false; p = p.parentElement; }
        return r.right > vw + 1 || r.left < -1;
      }).slice(0, 30).map(e => ({ tag: e.tagName.toLowerCase(), text: (e.innerText || '').slice(0, 100), right: Math.round(e.getBoundingClientRect().right) }));
      return { width: vw, scroll_width: document.documentElement.scrollWidth, height: document.documentElement.scrollHeight, overflowing };
    });
    capture.layout = await measure();
    capture.layout_viewport_matches = Math.abs(capture.layout.width - viewport.width) <= 1;
    const allText = await best.frame.locator('body').innerText();
    capture.text = allText.slice(0, config.capture.max_text_chars);
    capture.text_truncated = allText.length > capture.text.length;
    capture.links = await best.frame.locator('a[href]').evaluateAll(els => els.map(e => ({ text: (e.innerText || '').trim(), href: e.getAttribute('href'), visible: e.getClientRects().length > 0, anchor_exists: !e.hash || e.origin !== location.origin || e.pathname !== location.pathname || !!document.getElementById(decodeURIComponent(e.hash.slice(1))) })));
    capture.forms = await best.frame.locator('form').evaluateAll(els => els.map(e => ({ action: e.action, method: e.method })));
    const rootHeight = await page.evaluate(() => document.documentElement.scrollHeight);
    const stride = viewport.height - config.capture.overlap_px;
    const positions = [];
    for (let y = 0; y < rootHeight; y += stride) positions.push(Math.min(y, Math.max(0, rootHeight - viewport.height)));
    const unique = [...new Set(positions)];
    capture.visual_coverage_complete = unique.length <= config.capture.max_tiles;
    const selected = unique.slice(0, config.capture.max_tiles);
    for (let i = 0; i < selected.length; i++) {
      await page.evaluate(y => { document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo(0, y); }, selected[i]);
      await page.waitForTimeout(100);
      const file = `${id}-${String(i).padStart(2, '0')}.png`;
      const bytes = await page.screenshot({ path: join(runDir, file), animations: 'disabled', timeout: 15000 });
      const viewportText = await best.frame.evaluate(() => [...document.body.querySelectorAll('h1,h2,h3,p,li,button,a,label')].filter(e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.bottom > 0 && r.top < innerHeight && r.width > 0 && r.height > 0 && s.visibility !== 'hidden'; }).map(e => e.innerText).filter(Boolean).join('\n'));
      capture.images.push({ ref: `image-${i}`, file, sha256: sha256(bytes), y: selected[i], elapsed_ms: Date.now() - started, viewport_text: viewportText });
    }
    capture.layout_after_scroll = await measure();
    capture.dynamic_state_note = 'Reduced motion and disabled CSS screenshot animations; JavaScript interactions remain live. Per-tile text, timing and image hashes record the observed state. No form was submitted and no live account preview was invoked.';
    capture.ready = true;
  } catch (e) { capture.ready = false; capture.error = e.message; }
  finally { await context.close(); }
  return capture;
}

export async function captureRun(options) {
  const { chromium } = await import('playwright');
  const contract = await contracts();
  const { registry, registry_sha256 } = await verifiedRegistry();
  if (JSON.stringify(registry.study.questions) !== JSON.stringify(contract.config.visitor_questions.map(({ id, prompt }) => ({ id, prompt })))) throw new Error('Study questions have changed; reimport the registry before capture.');
  const runID = safeID(options.id || new Date().toISOString().replace(/[:.]/g, '-'));
  const runDir = join(RUNS, runID);
  await mkdir(RUNS, { recursive: true });
  await mkdir(runDir); // A run is immutable input evidence; never silently overwrite one.
  const base = options.base || 'http://127.0.0.1:8765/landing-lab/';
  const targets = registry.variants.filter(v => !options.variant || options.variant.split(',').includes(v.id)).map(v => ({ ...v, url: new URL(v.entry_path, base).href }));
  if (!targets.length) throw new Error('No matching candidates.');
  if (options.baseline) targets.push({ id: 'current-homepage', name: 'Current Homepage', url: options.baseline === true ? contract.config.baseline_url : options.baseline });
  if (options.companions) for (const v of registry.variants.filter(v => v.phone_path)) targets.push({ ...v, composition: 'supplied-phone', url: new URL(v.phone_path, base).href, entry_sha256: v.phone_sha256 });
  const browser = await chromium.launch({ channel: options.channel || 'chrome', headless: true });
  const run = { schema_version: 1, id: runID, captured_at: new Date().toISOString(), registry_sha256, registry, ...contract, browser: browser.version(), captures: [], judgments: [], visitor_judgments: [] };
  try {
    for (const target of targets) {
      for (const vp of contract.config.viewports.filter(v => !options.viewport || v.id === options.viewport)) {
        if (target.composition && vp.id !== 'phone') continue;
        const c = await captureOne(browser, target, vp, runDir, contract.config);
        run.captures.push(c);
        console.log(`${c.id}: ${c.ready ? `${c.images.length} tiles, ${c.text.length} text characters` : c.error}`);
        await writeJSON(join(runDir, 'run.json'), run);
      }
    }
  } finally { await browser.close(); }
  run.input_sha256 = inputDigest(run);
  await writeJSON(join(runDir, 'run.json'), run);
  return { run, runDir };
}
