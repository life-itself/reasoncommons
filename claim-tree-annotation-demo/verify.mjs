import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const page = readFileSync(new URL('./index.html', import.meta.url), 'utf8');

assert.match(page, /Can the world switch to clean energy in time\?/);
assert.match(page, /ai:/);
assert.match(page, /'remote-work':/);
assert.match(page, /https:\/\/www\.ipcc\.ch\/report\/ar6\/wg3\/chapter\/chapter-6\//);
assert.match(page, /https:\/\/internationalaisafetyreport\.org\/publication\/international-ai-safety-report-2025/);
assert.match(page, /https:\/\/time\.com\/6266923\/ai-eliezer-yudkowsky-open-letter-not-enough\//);
assert.match(page, /topic === 'ai'/);
assert.match(page, /#topic=remote-work/);
assert.match(page, /sourceUrl/);
assert.match(page, /key:\s*'s'/);
assert.match(page, /key:\s*'c'/);
assert.match(page, /window\.location\.hash\.slice\(1\)/);
