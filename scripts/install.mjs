#!/usr/bin/env node
import { cp, mkdir, readdir, rm, stat } from 'node:fs/promises';
import { realpathSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { createInterface } from 'node:readline/promises';
import { fileURLToPath } from 'node:url';

const SKILL = 'albanian-humanizer';
const SOURCE = 'kett1m/albanian-humanizer-skill';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const GUIDE = 'https://github.com/kett1m/albanian-humanizer-skill/blob/main/docs/INSTALL.md';
const POPULAR = ['codex', 'claude-code', 'cursor', 'github-copilot', 'gemini-cli', 'opencode', 'windsurf', 'cline'];

function expandPath(value, cwd) {
  if (value === '~') return homedir();
  if (/^~[/\\]/.test(value)) return resolve(homedir(), value.slice(2));
  return resolve(cwd, value);
}

export function selectAgents(answer, agents) {
  const input = answer.trim().toLowerCase();
  if (input === 'all') return agents;
  const selected = input.split(',').map((value) => {
    value = value.trim();
    if (/^[1-9]\d*$/.test(value)) return agents[Number(value) - 1];
    return agents.find((agent) => agent.id === value || agent.name.toLowerCase() === value);
  });
  if (selected.some((agent) => !agent)) return null;
  return [...new Map(selected.map((agent) => [agent.id, agent])).values()];
}

export async function copyCustomSkill(skillRoot, destination) {
  // Reserve a new directory; never merge into or replace an existing installation.
  await mkdir(dirname(destination), { recursive: true });
  await mkdir(destination);
  try {
    for (const name of await readdir(skillRoot)) {
      await cp(join(skillRoot, name), join(destination, name), { recursive: true, force: false, errorOnExist: true });
    }
  } catch (error) {
    await rm(destination, { recursive: true, force: true });
    throw error;
  }
}

export async function runInstaller({ ask, log, api, cwd = process.cwd(), project = false, root = ROOT }) {
  const catalog = api.getSupportedAgents();
  const agents = [
    ...POPULAR.map((id) => catalog.find((agent) => agent.id === id)).filter(Boolean),
    ...catalog.filter((agent) => !POPULAR.includes(agent.id)).sort((a, b) => a.name.localeCompare(b.name)),
  ];
  const showAgents = (list) => list.forEach((agent) => log(`  ${agents.indexOf(agent) + 1}. ${agent.name} (${agent.id})`));
  log('\nShqip & English Humanizer');
  log('Which AI agent or app do you use?');
  showAgents(agents.slice(0, POPULAR.length));
  log('  more: show every supported agent');
  log('  0: another agent / custom skills folder');
  log('  q: cancel');
  log('Choose a number or agent name. For several, separate choices with commas.');
  let selected;
  let custom = false;
  while (!selected) {
    const answer = (await ask('Your agent: ')).trim();
    if (/^q(uit)?$/i.test(answer)) { log('Cancelled.'); return 0; }
    if (/^more$/i.test(answer)) { showAgents(agents); continue; }
    if (answer === '0') { custom = true; break; }
    selected = selectAgents(answer, agents);
    if (!selected) log('Please choose a listed number or name, or type more.');
  }
  if (custom) {
    log('Enter the parent skills folder used by your agent. A new albanian-humanizer folder will be created inside it.');
    log(`For a chat app with no skills folder, use the standalone prompt: ${GUIDE}#any-other-agent-or-chat-tool`);
    const answer = (await ask('Skills folder (blank to cancel): ')).trim();
    if (!answer) { log('Cancelled.'); return 0; }
    const destination = join(expandPath(answer, cwd), SKILL);
    log(`Install complete skill to: ${destination}`);
    if (!/^(y|yes)$/i.test((await ask('Install here? [y/N]: ')).trim())) { log('Cancelled.'); return 0; }
    try { await copyCustomSkill(join(root, 'skills', SKILL), destination); }
    catch (error) {
      if (error.code === 'EEXIST') throw new Error(`Folder already exists: ${destination}. Choose a new folder or manage the existing installation first.`);
      throw error;
    }
    log(`Installed: ${destination}`);
    log('Restart your agent and ask it to use albanian-humanizer. Custom copies are updated manually.');
    return 0;
  }
  let scope = project ? 'project' : 'global';
  const projectOnly = selected.filter((agent) => !agent.globalSkillsDir);
  if (projectOnly.length && !project) {
    log(`${projectOnly.map((agent) => agent.name).join(', ')} requires a project folder.`);
    const answer = (await ask('Project folder (blank to cancel): ')).trim();
    if (!answer) { log('Cancelled.'); return 0; }
    cwd = expandPath(answer, cwd);
    if (!(await stat(cwd)).isDirectory()) throw new Error(`Not a project directory: ${cwd}`);
    scope = 'project';
  }
  log(`\nSelected: ${selected.map((agent) => agent.name).join(', ')}`);
  log(scope === 'global' ? 'Available across your projects, in your user account.' : `Project: ${cwd}`);
  for (const path of new Set(selected.map((agent) => join(scope === 'global' ? agent.globalSkillsDir : resolve(cwd, agent.projectSkillsDir), SKILL)))) log(`  ${path}`);
  log('Existing copies of this skill at these locations will be updated.');
  if (!/^(y|yes)$/i.test((await ask('Install? [y/N]: ')).trim())) { log('Cancelled.'); return 0; }
  log('Installing…');
  const result = await api.installSkills(SOURCE, {
    cwd, scope, agents: selected.map((agent) => agent.id), skills: [SKILL],
    mode: 'copy', telemetry: false,
    onWarning: (warning) => log(`Notice: ${warning.message}`),
  });
  for (const item of result.installed) log(`Installed: ${item.path}`);
  for (const item of result.skipped) log(`Skipped ${item.agent}: ${item.reason}`);
  for (const item of result.failed) log(`Failed ${item.agent}: ${item.message}`);
  if (result.failed.length || result.skipped.length || !result.installed.length) return 1;
  log('\nDone. Restart your agent and ask it to use albanian-humanizer.');
  return 0;
}

async function main() {
  if (process.argv.includes('--help')) {
    console.log('albanian-humanizer-install [--project]\nPrompts for your agent, shows destinations, then asks to install.\nDefault: your user account. --project: the current project.');
    return 0;
  }
  if (process.argv.slice(2).some((arg) => arg !== '--project')) throw new Error('Unknown option. Use --help.');
  if (!process.stdin.isTTY || !process.stdout.isTTY) throw new Error('Open a terminal and paste the install command there so you can choose your agent.');
  const [major, minor] = process.versions.node.split('.').map(Number);
  if (major < 22 || (major === 22 && minor < 20)) throw new Error('Install Node.js 22.20 or newer, then run this command again.');
  const api = await import('skills');
  const terminal = createInterface({ input: process.stdin, output: process.stdout });
  const controller = new AbortController();
  const cancel = () => controller.abort();
  terminal.on('SIGINT', cancel);
  terminal.on('close', cancel);
  try {
    return await runInstaller({
      ask: (question) => terminal.question(question, { signal: controller.signal }),
      log: console.log, api, project: process.argv.includes('--project'),
    });
  } catch (error) {
    if (error.name === 'AbortError') { console.log('\nCancelled.'); return 0; }
    throw error;
  } finally { terminal.close(); }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === realpathSync(process.argv[1])) {
  main().then((code) => { process.exitCode = code; }).catch((error) => {
    console.error(`Install failed: ${error.message}`);
    console.error(`Help: ${GUIDE}`);
    process.exitCode = 1;
  });
}
