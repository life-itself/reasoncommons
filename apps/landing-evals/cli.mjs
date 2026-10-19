#!/usr/bin/env node
import { createServer } from 'node:http';
import { readFile, stat, realpath, mkdir } from 'node:fs/promises';
import { resolve, join, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { APP, LAB, RUNS, ROOT, safeID, captureRun, verifiedRegistry } from './capture.mjs';
import { exportCodexPacket, importCodexJudgments } from './codex-judge.mjs';
import { importPages } from './import.mjs';
import { judgeRun } from './judge.mjs';
import { makeReport, makePublicReport } from './report.mjs';

export function parseArgs(args) {
  const options = {};
  while (args.length) {
    const arg = args.shift();
    if (!arg.startsWith('--')) throw new Error(`Expected an option, got ${arg}`);
    const [key, inline] = arg.slice(2).split(/=(.*)/s);
    options[key] = inline ?? (args[0] && !args[0].startsWith('--') ? args.shift() : true);
  }
  return options;
}

export async function startServer(port = 8765) {
  await mkdir(RUNS, { recursive: true });
  const mime = { '.html': 'text/html; charset=utf-8', '.json': 'application/json; charset=utf-8', '.png': 'image/png', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml' };
  const server = createServer(async (req, res) => {
    try {
      const path = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
      if (path === '/') { res.writeHead(302, { Location: '/landing-lab/index.html' }); res.end(); return; }
      if (!['GET', 'HEAD'].includes(req.method)) { res.writeHead(405); res.end(); return; }
      const isRuns = path.startsWith('/runs/');
      const prefix = isRuns ? '/runs/' : '/landing-lab/';
      if (!path.startsWith(prefix)) throw new Error('Not found');
      const root = isRuns ? RUNS : LAB;
      let target = resolve(root, path.slice(prefix.length));
      if (target !== root && !target.startsWith(root + sep)) throw new Error('Not found');
      if ((await stat(target)).isDirectory()) target = join(target, 'index.html');
      target = await realpath(target);
      if (!target.startsWith(await realpath(root) + sep)) throw new Error('Not found');
      const bytes = await readFile(target);
      res.writeHead(200, { 'Content-Type': mime[extname(target)] || 'application/octet-stream', 'Content-Length': bytes.length, 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
      res.end(req.method === 'HEAD' ? undefined : bytes);
    } catch { res.writeHead(404, { 'Content-Type': 'text/plain' }); res.end('Not found'); }
  });
  await new Promise((yes, no) => { server.once('error', no); server.listen(Number(port), '127.0.0.1', yes); });
  return server;
}

async function main() {
  const [command = 'help', ...args] = process.argv.slice(2);
  const options = parseArgs(args);
  if (command === 'serve') {
    const server = await startServer(options.port || 8765);
    console.log(`Gallery: http://127.0.0.1:${server.address().port}/landing-lab/index.html\nStudy: http://127.0.0.1:${server.address().port}/landing-lab/study.html\nReports: http://127.0.0.1:${server.address().port}/runs/<run-id>/report.html`);
  } else if (command === 'import') {
    if (!options.from || options.from === true) throw new Error('Use --from /absolute/path/to/the/supplied/files');
    const registry = await importPages(options.from, LAB);
    console.log(`Imported ${registry.variants.length} distinct designs from ${registry.supplied_file_count} files.`);
  } else if (command === 'verify') {
    const { registry } = await verifiedRegistry();
    console.log(`Source, entry and companion hashes verified for ${registry.variants.length} candidates.`);
  } else if (command === 'capture') {
    let server;
    try {
      if (!options.base) {
        server = await startServer(0);
        options.base = `http://127.0.0.1:${server.address().port}/landing-lab/`;
      }
      const { runDir } = await captureRun(options);
      console.log((await makeReport(runDir)).path);
    } finally { if (server) await new Promise(r => server.close(r)); }
  } else if (['codex-export', 'codex-import', 'publish-results'].includes(command)) {
    if (!options.run || !options.packet && command !== 'publish-results') throw new Error('Use --run ID and --packet NAME.');
    const runDir = join(RUNS, safeID(options.run));
    const packetDir = options.packet && join(runDir, safeID(options.packet));
    if (command === 'codex-export') console.log(await exportCodexPacket(runDir, packetDir, {pair:options.pair?.split(','), reverse:!!options.reverse, batch:options.batch}));
    else if (command === 'codex-import') console.log(`${(await importCodexJudgments(runDir, packetDir, resolve(options.output), options.agent)).length} validated native judgments imported.`);
    else console.log((await makePublicReport(runDir, JSON.parse(await readFile(resolve(options.decision), 'utf8')))).output);
  } else if (['judge', 'report'].includes(command)) {
    if (!options.run || options.run === true) throw new Error('Use --run <run-id> from a capture.');
    const runDir = join(RUNS, safeID(options.run));
    if (command === 'judge') await judgeRun(runDir, options);
    const report = await makeReport(runDir, options);
    console.log(report.path);
  } else {
    console.log(`Landing evaluation lab\n\n  npm start\n  node cli.mjs import --from /path/to/downloads\n  node cli.mjs verify\n  node cli.mjs capture --id first-pass [--baseline] [--companions]\n  node cli.mjs judge --run first-pass                 # plans calls; no API use\n  node cli.mjs judge --run first-pass --fixture       # plumbing check; no scores\n  node cli.mjs judge --run first-pass --live --model MODEL\n  node cli.mjs judge --run first-pass --mode pairwise --pair ID,ID --live --model MODEL\n  node cli.mjs judge --run first-pass --visitors /path/to/response-files --live --model MODEL\n  node cli.mjs report --run first-pass [--labels /path/to/human-labels.json]\n\nNative Codex: codex-export --run ID --packet NAME [--pair ID,ID --reverse --batch GROUP]\n  codex-import --run ID --packet NAME --output FILE --agent AGENT\n  publish-results --run ID --decision FILE\n\nOptions: --variant ID[,ID] --viewport desktop|phone --repeat N --max-calls N\nCapture: --base URL --channel chrome|chromium. Evidence lives in .runs/ and is not published.`);
  }
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main().catch(e => { console.error(e.message); process.exitCode = 1; });
