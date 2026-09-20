#!/usr/bin/env node
// Render a repo Markdown page to a standalone HTML file, roughly as Flowershow
// would, so a session with no preview site can look at it in a browser.
//
//   node scripts/render-preview.mjs <file.md> [out.html]
//
// It is an approximation, not the real theme: a content column of the same
// width, the theme's colour variables, and the repo's custom.css. That is
// enough to catch the things that actually go wrong — raw HTML blocks broken
// by a blank line (AGENTS.md), figures overflowing at phone width, and a
// component that doesn't look like it was meant to. Check the real thing with
// `fl . --yes` before it goes live.
//
// Needs `npm i marked` somewhere on NODE_PATH; the cloud sessions install it
// into a scratch directory and run with NODE_PATH set.
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, dirname, relative } from 'node:path';
import { createRequire } from 'node:module';

const [src, out = 'preview.html'] = process.argv.slice(2);
if (!src) { console.error('usage: render-preview.mjs <file.md> [out.html]'); process.exit(2); }

const require = createRequire(import.meta.url);
const { marked } = require('marked');

const raw = readFileSync(src, 'utf8');
const body = raw.replace(/^---\n[\s\S]*?\n---\n/, '');
const title = (raw.match(/^title:\s*(.+)$/m) || [, 'Preview'])[1];
const repoRoot = resolve(dirname(new URL(import.meta.url).pathname), '..');
const css = relative(dirname(resolve(out)), resolve(repoRoot, 'custom.css')) || 'custom.css';

const html = `<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<link rel="stylesheet" href="${css}">
<style>
  /* Stand-in for the lessflowery theme: the variables custom.css reads, and a
     content column of about the width the real theme gives it. */
  :root {
    --color-background: #fdfbf7;
    --color-background-surface: #f1ece3;
    --color-foreground: #252113;
    --color-foreground-100: #e4ded1;
    --color-foreground-300: #b9b2a0;
    --color-foreground-500: #7a7360;
    --color-foreground-600: #5f5947;
    --color-foreground-700: #4a4534;
    --color-accent: #327e09;
    --font-weight-headings: 600;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--color-background);
    color: var(--color-foreground);
    font-family: ui-serif, Georgia, "Times New Roman", serif;
    font-size: 1.05rem;
    line-height: 1.65;
  }
  main { max-width: 42rem; margin: 0 auto; padding: 2.5rem 1rem 6rem; }
  h1 { font-size: clamp(1.8rem, 1.2rem + 2.6vw, 2.5rem); line-height: 1.15; margin: 0 0 1rem; }
  h2, h3 { line-height: 1.25; margin: 2.25rem 0 0.75rem; }
  h3 { font-size: 1.15rem; }
  p { margin: 0 0 1.15rem; }
  a { color: #a8482a; }
  blockquote {
    margin: 1.5rem 0; padding: 0.2rem 0 0.2rem 1.1rem;
    border-left: 3px solid var(--color-foreground-300);
    color: var(--color-foreground-700); font-style: italic;
  }
  img { max-width: 100%; height: auto; }
</style>
</head><body><main>
${marked.parse(body)}
</main></body></html>
`;

writeFileSync(out, html);
console.log('wrote', out);
