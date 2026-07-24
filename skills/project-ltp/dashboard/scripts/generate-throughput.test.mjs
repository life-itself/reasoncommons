import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { parse, stringify } from "yaml";
import {
  diffModels,
  generateAll,
} from "./generate-throughput.mjs";

function model(entities, links = [], views = {}) {
  return { project: { name: "Test" }, entities, links, views };
}

test("semantic node diff counts stable-ID creates, updates, and deletes", () => {
  const previous = model([
    { id: "A", type: "goal", statement: "A", evidence: ["E2", "E1"] },
    { id: "B", type: "condition", statement: "B" },
  ]);
  const next = model([
    { evidence: ["E1", "E2"], statement: "A revised", type: "goal", id: "A" },
    { id: "C", type: "condition", statement: "C" },
  ]);

  assert.deepEqual(diffModels(previous, next), {
    created: ["C"],
    updated: ["A"],
    deleted: ["B"],
    throughput: 3,
  });
});

test("formatting and set-like list reordering do not count", () => {
  const previous = model([
    { id: "A", type: "goal", statement: "A", evidence: ["E2", "E1"] },
  ]);
  const next = model([
    { statement: "A", evidence: ["E1", "E2"], id: "A", type: "goal" },
  ]);
  assert.equal(diffModels(previous, next).throughput, 0);
});

test("causal-link and view-membership changes update affected nodes", () => {
  const entities = [
    { id: "A", type: "condition", statement: "A" },
    { id: "B", type: "goal", statement: "B" },
  ];
  const previous = model(
    entities,
    [{ id: "L-1", from: "A", to: "B", relation: "causes" }],
    { "goal-tree": { entities: ["B"], links: [] } },
  );
  const next = model(
    entities,
    [{ id: "L-1", from: "A", to: "B", relation: "necessary_for" }],
    { "goal-tree": { entities: ["A", "B"], links: ["L-1"] } },
  );
  assert.deepEqual(diffModels(previous, next).updated, ["A", "B"]);
});

test("view-link membership and referenced evidence changes update nodes", () => {
  const entities = [
    { id: "A", type: "condition", statement: "A", evidence: ["E-1"] },
    { id: "B", type: "goal", statement: "B" },
  ];
  const links = [{ id: "L-1", from: "A", to: "B", relation: "causes" }];
  const previous = {
    ...model(entities, links, {
      "goal-tree": { entities: ["A", "B"], links: [] },
    }),
    evidence: [{ id: "E-1", observation: "Initial evidence" }],
  };
  const next = {
    ...model(entities, links, {
      "goal-tree": { entities: ["A", "B"], links: ["L-1"] },
    }),
    evidence: [{ id: "E-1", observation: "Revised evidence" }],
  };

  assert.deepEqual(diffModels(previous, next).updated, ["A", "B"]);
});

function runGit(root, args, authoredAt) {
  const environment = authoredAt
    ? {
        ...process.env,
        GIT_AUTHOR_DATE: authoredAt,
        GIT_COMMITTER_DATE: authoredAt,
      }
    : process.env;
  return execFileSync("git", ["-C", root, ...args], {
    encoding: "utf8",
    env: environment,
  }).trim();
}

function commitModel(root, value, message, authoredAt) {
  writeFileSync(join(root, "ltp", "ltp-model.yaml"), stringify(value), "utf8");
  runGit(root, ["add", "ltp/ltp-model.yaml"]);
  runGit(root, ["commit", "-m", message], authoredAt);
  return runGit(root, ["rev-parse", "HEAD"]);
}

test("generator derives weekly recipient throughput from source Git history", () => {
  const root = mkdtempSync(join(tmpdir(), "project-ltp-throughput-"));
  mkdirSync(join(root, "ltp"), { recursive: true });
  mkdirSync(join(root, "public", "source"), { recursive: true });
  mkdirSync(join(root, "public", "recipient"), { recursive: true });
  runGit(root, ["init", "-q"]);
  runGit(root, ["config", "user.name", "Test"]);
  runGit(root, ["config", "user.email", "test@example.com"]);

  const baseline = model([
    { id: "A", type: "goal", statement: "A" },
    { id: "B", type: "condition", statement: "B" },
  ]);
  const baselineRevision = commitModel(
    root,
    baseline,
    "baseline",
    "2026-07-20T10:00:00Z",
  );
  commitModel(
    root,
    model([
      { id: "A", type: "goal", statement: "A revised" },
      { id: "B", type: "condition", statement: "B" },
      { id: "C", type: "condition", statement: "C" },
    ]),
    "create and update",
    "2026-07-21T10:00:00Z",
  );
  const headModel = model([
    { id: "A", type: "goal", statement: "A revised" },
    { id: "C", type: "condition", statement: "C" },
  ]);
  commitModel(root, headModel, "delete", "2026-07-22T10:00:00Z");
  writeFileSync(join(root, "README.md"), "No model change.\n", "utf8");
  runGit(root, ["add", "README.md"]);
  runGit(root, ["commit", "-m", "unrelated documentation"], "2026-08-03T10:00:00Z");

  const configPath = join(root, "throughput.config.json");
  writeFileSync(
    configPath,
    JSON.stringify({
      tracks: [
        {
          recipient_project: "recipient",
          source_project: "source",
          source_model: "ltp/ltp-model.yaml",
          published_model: "public/source/model.yaml",
          output: "public/recipient/throughput.yaml",
          baseline_revision: baselineRevision,
          definition: {
            name: "Adopted tree changes",
            unit: "node changes",
            period: "week",
          },
        },
      ],
    }),
    "utf8",
  );

  const [result] = generateAll(configPath, root);
  assert.deepEqual(result.throughput.periods, [
    {
      date: "2026-07-20",
      throughput: 3,
      created: 1,
      updated: 1,
      deleted: 1,
    },
    {
      date: "2026-07-27",
      throughput: 0,
      created: 0,
      updated: 0,
      deleted: 0,
    },
    {
      date: "2026-08-03",
      throughput: 0,
      created: 0,
      updated: 0,
      deleted: 0,
    },
  ]);
  assert.equal(result.throughput.revisions.length, 2);
  assert.deepEqual(parse(readFileSync(join(root, "public/source/model.yaml"), "utf8")), headModel);
  assert.equal(
    parse(readFileSync(join(root, "public/recipient/throughput.yaml"), "utf8"))
      .definition.source_project,
    "source",
  );
});
