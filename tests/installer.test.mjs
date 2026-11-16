import assert from 'node:assert/strict';
import { mkdtemp, readFile, readdir, rm, stat, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import test from 'node:test';
import { copyCustomSkill, runInstaller } from '../scripts/install.mjs';

const agents = [
  { id: 'codex', name: 'Codex', projectSkillsDir: '.agents/skills', globalSkillsDir: '/example/.agents/skills' },
  { id: 'cursor', name: 'Cursor', projectSkillsDir: '.cursor/skills', globalSkillsDir: '/example/.cursor/skills' },
  { id: 'eve', name: 'Eve', projectSkillsDir: 'agent/skills', globalSkillsDir: null },
];

async function simulate(answers, settings = {}) {
  const calls = [], output = [], questions = [];
  const code = await runInstaller({
    ask: async (question) => {
      questions.push(question);
      assert.ok(answers.length, `Unexpected prompt: ${question}`);
      return answers.shift();
    },
    log: (line) => output.push(line),
    api: {
      getSupportedAgents: () => agents,
      installSkills: async (...args) => {
        calls.push(args);
        return settings.result ?? { installed: [{ path: '/example/skill' }], failed: [], skipped: [] };
      },
    },
    ...settings,
  });
  return { code, calls, output, questions };
}

test('always asks; installs only the selected agent after confirmation', async () => {
  const result = await simulate(['cursor', 'yes']);
  assert.equal(result.questions[0], 'Your agent: ');
  assert.equal(result.calls.length, 1);
  assert.equal(result.calls[0][0], 'kett1m/albanian-humanizer-skill');
  assert.deepEqual(result.calls[0][1].agents, ['cursor']);
  assert.equal(result.calls[0][1].scope, 'global');
  assert.equal(result.calls[0][1].mode, 'copy');
});

test('blank, unknown, and mixed invalid choices do not silently choose an agent', async () => {
  const result = await simulate(['', 'no-such-agent', '1,999', '1,2,1', 'y']);
  assert.deepEqual(result.calls[0][1].agents, ['codex', 'cursor']);
  assert.equal(result.questions.filter((q) => q === 'Your agent: ').length, 4);
});

test('declining, EOF-style blank confirmation, and q make no install call', async () => {
  for (const answers of [['q'], ['1', 'no'], ['1', '']]) {
    assert.equal((await simulate(answers)).calls.length, 0);
  }
});

test('more lists all agents without selecting one', async () => {
  const result = await simulate(['more', 'q']);
  assert.ok(result.output.some((line) => line.includes('Eve (eve)')));
  assert.equal(result.calls.length, 0);
});

test('project-only agent asks for an existing project, preserving spaces', async () => {
  const cwd = await mkdtemp(join(tmpdir(), 'humanizer project '));
  try {
    const result = await simulate(['eve', cwd, 'y']);
    assert.equal(result.calls[0][1].scope, 'project');
    assert.equal(result.calls[0][1].cwd, cwd);
    assert.deepEqual(result.calls[0][1].agents, ['eve']);
  } finally { await rm(cwd, { recursive: true, force: true }); }
});

test('--project confines installation to the selected project', async () => {
  const result = await simulate(['1', 'y'], { cwd: '/example/project', project: true });
  assert.equal(result.calls[0][1].cwd, '/example/project');
  assert.equal(result.calls[0][1].scope, 'project');
  assert.ok(result.output.some((line) => line.includes('/example/project/.agents/skills/albanian-humanizer')));
});

test('partial failures and skipped targets do not report success', async () => {
  for (const result of [
    { installed: [], skipped: [], failed: [{ agent: 'codex', message: 'unwritable' }] },
    { installed: [], skipped: [{ agent: 'codex', reason: 'missing-agent-directory' }], failed: [] },
  ]) assert.equal((await simulate(['1', 'y'], { result })).code, 1);
});

test('custom installation preserves every resource and refuses existing destinations', async () => {
  const parent = await mkdtemp(join(tmpdir(), 'humanizer-custom-'));
  const destination = join(parent, 'albanian-humanizer');
  const source = resolve('skills/albanian-humanizer');
  try {
    await copyCustomSkill(source, destination);
    for (const name of await readdir(source, { recursive: true })) {
      const original = join(source, name);
      if ((await stat(original)).isFile()) assert.deepEqual(await readFile(join(destination, name)), await readFile(original));
    }
    await writeFile(join(destination, 'personal.txt'), 'keep');
    await assert.rejects(copyCustomSkill(source, destination), { code: 'EEXIST' });
    assert.equal(await readFile(join(destination, 'personal.txt'), 'utf8'), 'keep');
  } finally { await rm(parent, { recursive: true, force: true }); }
});

test('custom choice and cancellation leave the destination untouched', async () => {
  const parent = await mkdtemp(join(tmpdir(), 'humanizer-cancel-'));
  try {
    const result = await simulate(['0', parent, 'n']);
    assert.equal(result.calls.length, 0);
    assert.deepEqual(await readdir(parent), []);
  } finally { await rm(parent, { recursive: true, force: true }); }
});
