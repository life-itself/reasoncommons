import { readFileSync } from "node:fs";
import vm from "node:vm";

const html = readFileSync(new URL("../dist/index.html", import.meta.url), "utf8");
const modules = [...html.matchAll(/<script type="module">([\s\S]*?)<\/script>/g)];

if (modules.length !== 1) {
  throw new Error(`expected one inline module in dist/index.html, found ${modules.length}`);
}
new vm.Script(modules[0][1]);

for (const reference of ['src="./assets/', 'href="./assets/']) {
  if (html.includes(reference)) {
    throw new Error(`dist/index.html still references an external build asset: ${reference}`);
  }
}

for (const projectFile of [
  "projects/manifest.json",
  "projects/second-renaissance/model.yaml",
]) {
  if (!html.includes(projectFile)) {
    throw new Error(`dist/index.html does not embed ${projectFile}`);
  }
}

console.log("Verified the self-contained dashboard build.");
