import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const page = readFileSync(new URL('./index.html', import.meta.url), 'utf8');

assert.match(page, /Can the world switch to clean energy in time\?/);
assert.match(page, /https:\/\/www\.iea\.org\/reports\/net-zero-roadmap-a-global-pathway-to-keep-the-15-c-goal-in-reach\/executive-summary/);
assert.match(page, /more than 80% of the emissions reductions needed by 2030/);
assert.match(page, /11 000 gigawatts by 2030/);
assert.match(page, /https:\/\/www\.iea\.org\/reports\/electricity-grids-and-secure-energy-transitions\/executive-summary/);
assert.match(page, /over 80 million kilometres of grids by 2040/);
assert.match(page, /1 500 GW are in advanced stages/);
assert.match(page, /https:\/\/www\.iea\.org\/reports\/nuclear-power-and-secure-energy-transitions\/executive-summary/);
assert.match(page, /USD 500 billion more investment/);
assert.match(page, /data-src="p-path"/);
assert.match(page, /srcId: 'p-path', nodeId: 'whom-ic'/);
assert.match(page, /srcId: 'p-grid-build', nodeId: 'tasks-solo'/);
assert.match(page, /srcId: 'p-nuclear-cost', nodeId: 'tasks-creative'/);

assert.match(page, /href="#more-examples"/);
assert.match(page, /id="more-examples"/);
assert.match(page, /Two more questions, same method/);
assert.match(page, /Can humans stay in control of advanced AI\?/);
assert.match(page, /https:\/\/metr\.org\/blog\/2026-05-19-frontier-risk-report\//);
assert.match(page, /plausibly had the means, motive, and opportunity/);
assert.match(page, /https:\/\/internationalaisafetyreport\.org\/publication\/international-ai-safety-report-2025/);
assert.match(page, /https:\/\/time\.com\/6266923\/ai-eliezer-yudkowsky-open-letter-not-enough\//);
assert.match(page, /Does remote work increase productivity\?/);
assert.match(page, /https:\/\/www\.aeaweb\.org\/articles\?id=10\.1257\/aer\.20131516/);

assert.doesNotMatch(page, /topicData/);
assert.doesNotMatch(page, /URLSearchParams/);
assert.doesNotMatch(page, /#topic=/);
