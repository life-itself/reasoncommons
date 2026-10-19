import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { createHash } from 'node:crypto';
import { gunzipSync } from 'node:zlib';

export const sha256 = data => createHash('sha256').update(data).digest('hex');
export const definitions = [
  { id: 'test-the-assumption', name: 'Test the Assumption', files: ['Reason Commons (5).html'], framing: 'Find the assumption to test before adding more effort.', note: 'Original export contains separate desktop and phone boards. The phone companion is the supplied composition; primary phone captures test the actual desktop entry at phone width.' },
  { id: 'make-work-add-up', name: 'Make Work Add Up', files: ['# Reason Commons Landing Page.html'], framing: 'Connect a team’s work to its goals and reasoning.', note: 'The export has team, builder and facilitator message states. Capture the default state and record visible text; hidden alternatives are not visitor evidence.' },
  { id: 'untangle-the-problem', name: 'Untangle the Problem', files: ['Reason Commons (4).html', 'Reason Commons (3).html'], framing: 'Guided reasoning for recurring problems and stuck decisions.', note: 'Two supplied files are byte-identical. The live Claude-account preview depends on its original host; ordinary browser availability must be checked.' },
  { id: 'common-sense-renaissance', name: 'A Renaissance of Common Sense', files: ['Reason Commons Landing Page – Landing page (1).html'], framing: 'A broader movement, illustrated through a hospital bottleneck exercise.', note: 'A movement-oriented concept evaluated against the same stated audience and objective as the other pages.' },
  { id: 'check-the-because', name: 'Check the Because', files: ['Reason Commons landing page – Landing page.html'], framing: 'A volunteer kitchen example examines competing explanations.', note: 'Worked example with a funder section; record its purpose without changing the common evaluation contract.' }
];

export function bundleJSON(html, type) {
  const scripts = html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi);
  for (const [, attrs, body] of scripts) {
    const match = attrs.match(/\btype\s*=\s*["']([^"']+)["']/i);
    if (match?.[1] === type) return JSON.parse(body);
  }
  throw new Error(`Missing bundle section ${type}`);
}

export function unpackBoard(bytes) {
  const html = bytes.toString('utf8');
  const manifest = bundleJSON(html, '__bundler/manifest');
  const template = bundleJSON(html, '__bundler/template');
  const ids = [...template.matchAll(/<iframe\b[^>]*\bsrc=["']about:blank#([a-f0-9-]+)["']/gi)].map(m => m[1]);
  if (ids.length !== 2) throw new Error('Expected the supplied desktop and phone boards; refuse a guessed extraction.');
  return ids.map(id => {
    const entry = manifest[id];
    if (entry?.mime !== 'text/html') throw new Error(`Missing HTML board ${id}`);
    const decoded = Buffer.from(entry.data, 'base64');
    return entry.compressed ? gunzipSync(decoded) : decoded;
  });
}

export function normalizeEnvelope(bytes) {
  const html = bytes.toString('utf8');
  if (!html.includes('__bundler/manifest')) return bytes;
  const outerHead = html.slice(0, html.indexOf('<script'));
  if (/<meta\b[^>]*\bname\s*=\s*["']viewport["']/i.test(outerHead)) return bytes;
  // Download wrappers otherwise lock mobile Chrome into its initial 980px layout
  // even after the embedded template adds its own viewport metadata.
  return Buffer.from(html.replace(/<head\b[^>]*>/i, '$&\n<meta name="viewport" content="width=device-width,initial-scale=1">'));
}

export async function importPages(downloads, lab) {
  await mkdir(join(lab, 'sources'), { recursive: true });
  const variants = [];
  for (const def of definitions) {
    const bytes = await readFile(resolve(downloads, def.files[0]));
    for (const alias of def.files.slice(1)) {
      if (sha256(await readFile(resolve(downloads, alias))) !== sha256(bytes)) throw new Error(`Duplicate has changed: ${alias}; revise the registry before importing.`);
    }
    await writeFile(join(lab, 'sources', `${def.id}.html`), bytes);
    await mkdir(join(lab, def.id), { recursive: true });
    const [rawEntry, rawPhone] = def.id === 'test-the-assumption' ? unpackBoard(bytes) : [bytes, null];
    const entry = normalizeEnvelope(rawEntry), phone = rawPhone ? normalizeEnvelope(rawPhone) : null;
    await writeFile(join(lab, def.id, 'index.html'), entry);
    if (phone) await writeFile(join(lab, def.id, 'phone.html'), phone);
    variants.push({ id: def.id, name: def.name, framing: def.framing, notes: def.note, original_files: def.files, source_path: `sources/${def.id}.html`, source_sha256: sha256(bytes), source_bytes: bytes.length, entry_path: `${def.id}/index.html`, entry_sha256: sha256(entry), envelope_normalization: sha256(entry) !== sha256(rawEntry) ? 'Added viewport metadata to the outer download wrapper. Page copy, styling, scripts and embedded resources are unchanged.' : 'None', ...(phone ? { phone_path: `${def.id}/phone.html`, phone_sha256: sha256(phone) } : {}) });
  }
  const config = JSON.parse(await readFile(new URL('./eval.config.json', import.meta.url), 'utf8'));
  const registry = { schema_version: 1, study_id: config.study_id, study: { exposure_seconds: 20, questions: config.visitor_questions.map(({ id, prompt }) => ({ id, prompt })) }, imported_at: new Date().toISOString(), supplied_file_count: definitions.reduce((n, d) => n + d.files.length, 0), variants };
  const registryText = JSON.stringify(registry, null, 2) + '\n';
  await writeFile(join(lab, 'variants.json'), registryText);
  for (const name of ['index.html', 'study.html']) {
    const path = join(lab, name);
    try {
      const html = await readFile(path, 'utf8');
      const island = `<script type="application/json" id="registry-source" data-sha256="${sha256(registryText)}">${JSON.stringify(registryText).replaceAll('<', '\\u003c')}</script>`;
      await writeFile(path, html.replace(/<script type="application\/json" id="registry-source"[^>]*>[\s\S]*?<\/script>/, () => island));
    } catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  return registry;
}
