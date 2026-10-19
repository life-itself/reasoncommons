import { readFile, mkdir, copyFile } from 'node:fs/promises';
import { join } from 'node:path';
import { randomInt, randomUUID } from 'node:crypto';
import { readJSON, writeJSON, verifyRunEvidence } from './capture.mjs';
import { sha256 } from './import.mjs';
import { SYSTEM, schemas, selectImages, validateAssessment } from './judge.mjs';

export const actualJudgment = j => j.valid && ['live', 'codex'].includes(j.mode);
export async function exportCodexPacket(runDir, packetDir, { pair, reverse = false, batch = randomUUID() } = {}) {
  const run = await readJSON(join(runDir, 'run.json')); verifyRunEvidence(run);
  const primary = run.captures.filter(c => c.ready && c.composition !== 'supplied-phone');
  let tasks;
  if (pair) {
    tasks = run.config.viewports.map(v => ({kind:'pairwise',captures:(reverse ? [...pair].reverse() : pair).map(id => primary.find(c=>c.variant_id===id && c.viewport.id===v.id))}));
    if (tasks.some(t=>t.captures.some(c=>!c))) throw new Error('Missing pair capture.');
  } else {
    tasks = primary.map(c=>({kind:'individual', captures:[c]}));
    for(let i=tasks.length-1;i>0;i--){const j=randomInt(i+1);[tasks[i],tasks[j]]=[tasks[j],tasks[i]];}
  }
  await mkdir(packetDir,{recursive:true});
  const cases=[], mapping=[];
  for (let n=0;n<tasks.length;n++) {
    const task=tasks[n], id=`case-${String(n+1).padStart(2,'0')}`, candidates=[];
    const selected=task.captures.map(c=>selectImages(c.images,run.config.judge.max_images_per_candidate));
    for(let k=0;k<task.captures.length;k++) {
      const c=task.captures[k], label=['A','B'][k], images=[];
      for(const i of selected[k]) {
        const bytes=await readFile(join(runDir,i.file)); if(sha256(bytes)!==i.sha256) throw new Error('Image hash mismatch.');
        const file=`${id}-${label}-${i.ref}.png`; await copyFile(join(runDir,i.file),join(packetDir,file));
        images.push({ref:i.ref,file,sha256:i.sha256,y:i.y,viewport_text:i.viewport_text});
      }
      candidates.push({label,viewport:c.viewport,layout:c.layout,visible_text:c.text,text_scope:'Full-document CSS-visible text, which may extend beyond the initial viewport or a horizontal overflow.',images,captured_image_count:c.images.length,coverage_note:'Only these selected images are supplied; do not claim visual inspection of omitted regions.'});
    }
    const item={case_id:id,kind:task.kind,candidates}; await writeJSON(join(packetDir,`${id}.json`),item); cases.push({case_id:id,file:`${id}.json`,sha256:sha256(JSON.stringify(item,null,2)+'\n')});
    mapping.push({case_id:id,kind:task.kind,capture_ids:task.captures.map(c=>c.id),selected});
  }
  const packet={version:1,system:SYSTEM,audience:run.config.audience,objective:run.config.objective,primary_action:run.config.primary_action,rubric:run.rubric,facts:run.facts,schemas,cases,instructions:'Read every case and actually inspect every supplied PNG using view_image. Return {packet_sha256, assessments:[{case_id, inspected_images:[filenames], assessment:<individual or pairwise schema>}]}. Each case exactly once. Cite only supplied image refs or exact visible-text substrings; text evidence ref must be exactly visible-text. Presentation judgments require an image reference. Do not browse or inspect other files, other judges, identities or scores. Do not infer functionality from screenshots alone. No source changes. Save your result to the requested output path.'};
  await writeJSON(join(packetDir,'packet.json'),packet);
  const packetHash=sha256(await readFile(join(packetDir,'packet.json')));
  await writeJSON(`${packetDir}.mapping.json`,{batch,packet_sha256:packetHash,input_sha256:run.input_sha256,mapping});
  return {packetDir,packet_sha256:packetHash,cases:cases.length};
}
export async function importCodexJudgments(runDir, packetDir, outputFile, agentID) {
  const run=await readJSON(join(runDir,'run.json')); verifyRunEvidence(run);
  const map=await readJSON(`${packetDir}.mapping.json`), packet=await readJSON(join(packetDir,'packet.json')), output=await readJSON(outputFile);
  if(map.input_sha256!==run.input_sha256 || sha256(await readFile(join(packetDir,'packet.json')))!==map.packet_sha256 || output.packet_sha256!==map.packet_sha256) throw new Error('Packet/run identity mismatch.');
  if(!agentID || !Array.isArray(output.assessments) || output.assessments.length!==map.mapping.length || new Set(output.assessments.map(x=>x.case_id)).size!==map.mapping.length) throw new Error('Missing or duplicate cases.');
  if(run.judgments.some(j=>j.mode==='codex'&&j.agent_id===agentID)) throw new Error('Agent already imported.');
  const records=[];
  for(const m of map.mapping) {
    const expected=packet.cases.find(x=>x.case_id===m.case_id), bytes=await readFile(join(packetDir,expected.file));
    if(sha256(bytes)!==expected.sha256) throw new Error('Case changed.');
    const item=JSON.parse(bytes), out=output.assessments.find(x=>x.case_id===m.case_id);
    const files=item.candidates.flatMap(c=>c.images.map(i=>i.file));
    if(!out || !Array.isArray(out.inspected_images) || files.length!==out.inspected_images.length || files.some(f=>!out.inspected_images.includes(f))) throw new Error(`Incomplete image inspection: ${m.case_id}`);
    for(const c of item.candidates) for(const i of c.images) if(sha256(await readFile(join(packetDir,i.file)))!==i.sha256) throw new Error('Packet image changed.');
    const captures=m.capture_ids.map(id=>run.captures.find(c=>c.id===id)); validateAssessment(out.assessment,m.kind,run,captures,m.selected);
    const presentation=out.assessment.criteria.find(c=>c.id==='presentation');
    if((m.kind==='individual' ? presentation?.score!==null : presentation?.winner!=='insufficient-evidence')&&presentation&&!presentation.evidence.some(e=>e.kind==='image')) throw new Error('Presentation requires image evidence.');
    records.push({id:randomUUID(),batch_id:map.batch,mode:'codex',kind:m.kind,at:new Date().toISOString(),agent_id:agentID,requested_model:'Inherited Codex runtime',resolved_model:null,model_note:'Exact serving model snapshot not exposed by native agent tooling; contexts share the configured model family.',packet_sha256:map.packet_sha256,input_sha256:run.input_sha256,raw_output_sha256:sha256(await readFile(outputFile)),adapter_sha256:sha256(await readFile(new URL('./codex-judge.mjs',import.meta.url))),repetition:1,capture_ids:m.capture_ids,image_refs:m.selected.map(xs=>xs.map(({ref,file,sha256})=>({ref,file,sha256}))),assessment:out.assessment,valid:true});
  }
  run.judgments.push(...records); await writeJSON(join(runDir,'run.json'),run);return records;
}
