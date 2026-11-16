# Copy-and-paste installation

The skill is `albanian-humanizer`; its GitHub repository is
[`kett1m/albanian-humanizer-skill`](https://github.com/kett1m/albanian-humanizer-skill).
The skill itself is plain text. Choose native installation for agents that
support skills, or the [standalone prompt](#any-other-agent-or-chat-tool) for a
host that accepts instructions but has no skill loader.

## One line: Linux and macOS

With Git and Node.js **22.20 or newer** installed, paste this into Bash or Zsh:

```bash
npx --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --skill albanian-humanizer --agent "*" --global --copy --yes
```

This is the same skill-install command on openSUSE Tumbleweed, Leap, Slowroll,
Ubuntu, Debian, Linux Mint, Pop!_OS, elementary OS, Zorin OS, KDE neon, Kali,
Parrot, MX Linux, Fedora, RHEL, Rocky Linux, AlmaLinux, CentOS Stream, Oracle
Linux, Arch, Manjaro, EndeavourOS, Garuda, CachyOS, Gentoo, Void, Alpine, and
macOS. Their prerequisite installation differs; current supported OS releases
and a working Node runtime are required.

## One line: Windows

In **Windows PowerShell 5.1**, **PowerShell 7**, or **Command Prompt**:

```powershell
npx.cmd --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --skill albanian-humanizer --agent "*" --global --copy --yes
```

`npx.cmd` avoids PowerShell's `.ps1` execution-policy issue. `--copy` avoids
requiring symlink privileges. In Git Bash, use the Linux/macOS line. In WSL, use
the Linux line and install Linux prerequisites inside WSL; this targets the WSL
agent environment, separately from native Windows installations.

## What the flags do

`skills@1.9.0` pins the tested installer version. Its
[package manifest](https://github.com/vercel-labs/skills/blob/v1.9.0/package.json)
requires Node.js 22.20+. A current Node LTS release is a suitable choice.
`--skill albanian-humanizer` selects this skill. `--agent "*"` selects all hosts
the CLI knows; keep the quotes so your shell does not expand the wildcard.
`--global` means your user account, not a root-owned system installation.
`--copy` installs independent complete copies. The two `--yes` flags approve
npx's package download and the Skills CLI's installation prompts respectively.

This installs into the supported agents' skill directories, including agents
you may not use. It does not install agent applications. The global wildcard
skips hosts with no global directory, such as Eve and PromptScript in CLI 1.9.0.
For those, run this **inside the intended project**:

```bash
npx --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --skill albanian-humanizer --agent "*" --copy --yes
```

Use `npx.cmd` instead of `npx` for every Windows command below. The shared flags
follow the [official CLI reference](https://github.com/vercel-labs/skills/blob/v1.9.0/docs/commands.md).
Do not run the skill-install command with `sudo`: it should install for your own
account. Only OS package setup below needs elevated privileges.

## GitHub access

The repository is currently **private**. The owner and invited collaborators can
install it; an unauthenticated stranger cannot. These commands do not change
repository visibility. If Git access is already configured, skip this setup.

With [GitHub CLI](https://cli.github.com/) installed, authenticate once:

```bash
gh auth login --hostname github.com --git-protocol https
```

Then configure Git to use that login:

```bash
gh auth setup-git --hostname github.com
```

Both commands work in Bash, Zsh, PowerShell, and Command Prompt. `gh auth login`
is interactive; follow its browser/device prompts. Use an account with repository
access. Existing SSH credentials also work. Do not paste an access token into an
installation URL, shell history, or this repository.

Check access and discover the skill without installing:

```bash
npx --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --list
```

## openSUSE Tumbleweed

After GitHub access is configured, this one line installs Git, Node.js 24 and
npm, then installs the skill for all supported global agent targets:

```bash
sudo zypper install -y git nodejs24 npm24 && npx --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --skill albanian-humanizer --agent "*" --global --copy --yes
```

The package names were checked in the
[official Tumbleweed repository](https://download.opensuse.org/tumbleweed/repo/oss/x86_64/).
This uses your configured distribution repositories. It does not add a third-party
RPM repository or run a distribution upgrade. If a shell version manager already
selects an older Node, switch it to a current LTS first; installing an RPM does
not override your shell's PATH. Confirm with `node --version` and `npx --version`.

For **Leap or Slowroll**, use that same native line when your release provides
`nodejs24` and `npm24`. Otherwise use the Bash/current-LTS route below rather
than adding Tumbleweed repositories to a different distribution.

## macOS prerequisites

With [Homebrew](https://brew.sh/) installed, this is a combined prerequisite and
skill-install line; GitHub access must already be configured:

```bash
brew install node git && npx --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --skill albanian-humanizer --agent "*" --global --copy --yes
```

Homebrew's [Node formula](https://formulae.brew.sh/formula/node) includes npm and
npx. Homebrew may first need its documented shell setup on a fresh installation.
Alternatively, use the [official Node.js installer](https://nodejs.org/en/download)
and install Git, then use the short install line. Follow the supported OS and
architecture choices for your Mac; the skill files themselves are architecture-neutral.

## Windows prerequisites

On a Windows installation with [WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/install),
install Node LTS, Git, and GitHub CLI in one line:

```powershell
winget install OpenJS.NodeJS.LTS Git.Git GitHub.cli --source winget --accept-package-agreements --accept-source-agreements
```

Reopen the terminal so the new PATH entries are visible. Authenticate if needed,
then paste the Windows skill-install line. The documented Node package identifier
is [OpenJS.NodeJS.LTS](https://github.com/microsoft/winget-pkgs/tree/master/manifests/o/OpenJS/NodeJS/LTS).
If WinGet is unavailable, install Node LTS, Git, and optionally GitHub CLI from
their official installers. No change to PowerShell execution policy is needed.

## Linux prerequisites across distributions

Already have a suitable `node`, `npx`, and `git`? Use the short install command.
Otherwise, the following table installs the basic tools for the current-LTS
bootstrap below. It deliberately avoids relying on an old distro Node package:
for example, the checked [Ubuntu 24.04](https://packages.ubuntu.com/noble/nodejs)
and [Debian stable](https://packages.debian.org/stable/nodejs) packages are below
the tested CLI's Node minimum.

| Distribution family | Basic-tools setup, one line |
| --- | --- |
| Ubuntu, Debian, Mint, Pop!_OS, elementary, Zorin, KDE neon, Kali, Parrot, MX | `sudo apt-get update && sudo apt-get install -y bash curl git ca-certificates` |
| Fedora, RHEL, Rocky, AlmaLinux, CentOS Stream, Oracle Linux | `sudo dnf install -y bash curl git ca-certificates` |
| Arch, Manjaro, EndeavourOS, Garuda, CachyOS | `sudo pacman -S --needed --noconfirm bash curl git ca-certificates` |
| openSUSE Tumbleweed, Leap, Slowroll | `sudo zypper install -y bash curl git ca-certificates` |
| Gentoo | `sudo emerge --ask app-shells/bash net-misc/curl dev-vcs/git app-misc/ca-certificates` |
| Void Linux, glibc edition | `sudo xbps-install -S -y bash curl git ca-certificates` |

Use your release's configured repositories and normal package-management process.
These setup lines do not install the skill or authenticate GitHub. Once those
tools and repository access are ready, this **one line** installs per-user nvm,
selects current Node LTS, and installs the skill:

```bash
bash -o pipefail -c 'export NVM_DIR="${NVM_DIR:-$HOME/.nvm}" && mkdir -p "$NVM_DIR" && curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.41.0/install.sh | bash && . "$NVM_DIR/nvm.sh" && nvm install --lts && npx --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --skill albanian-humanizer --agent "*" --global --copy --yes'
```

This follows [nvm's installation and LTS usage](https://github.com/nvm-sh/nvm/tree/v0.41.0).
It installs/updates nvm in `NVM_DIR` (or `~/.nvm`) and may add its loader to your
shell profile. Run it as your normal user. It requires a current supported
glibc-based Linux system and network access to GitHub, Node downloads, and npm.
For a machine managed by an organization, an existing approved Node installation
can be used instead. For musl-based systems, use native packages as below.

**Alpine Linux** (with `doas` configured; Node/npm repositories available):

```bash
doas apk add git nodejs npm && npx --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --skill albanian-humanizer --agent "*" --global --copy --yes
```

Alpine provides separate [Node](https://pkgs.alpinelinux.org/packages?name=nodejs)
and [npm](https://pkgs.alpinelinux.org/packages?name=npm) packages. Check your stable
release offers Node 22.20+; use a supported release, not a mixture of stable and
edge repositories. If `doas` is unavailable, have an administrator install the
three packages, then run npx as your user.

**Void Linux**, including its musl edition, can use its native Node package:

```bash
sudo xbps-install -S -y git nodejs && npx --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --skill albanian-humanizer --agent "*" --global --copy --yes
```

**NixOS or Linux/macOS with Nix**, using a temporary tool environment:

```bash
nix --extra-experimental-features "nix-command flakes" shell nixpkgs#nodejs_24 nixpkgs#git --command npx --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --skill albanian-humanizer --agent "*" --global --copy --yes
```

This requires a configured `nixpkgs` registry with those packages. It temporarily
provides tools; the copied skill files persist in your user directories. For an
immutable/container-based desktop, run the tool setup and npx inside the same
development environment and user account as the agent that should discover it.

## Choose agents and scope

**Choose interactively:**

```bash
npx --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --skill albanian-humanizer --global --copy
```

**Codex only:**

```bash
npx --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --skill albanian-humanizer --agent codex --global --copy --yes
```

**Several agents:**

```bash
npx --yes skills@1.9.0 add kett1m/albanian-humanizer-skill --skill albanian-humanizer --agent claude-code cursor github-copilot gemini-cli opencode windsurf --global --copy --yes
```

Other supported identifiers include `cline`, `roo`, `kilo`, `amp`, `goose`,
`continue`, `pi`, `openhands`, `openclaw`, `aider-desk`, `antigravity`, `augment`,
`crush`, `droid`, `kiro-cli`, `qwen-code`, `replit`, `trae`, `warp`, and `zed`.
Consult the [agent table for CLI 1.9.0](https://github.com/vercel-labs/skills/blob/v1.9.0/docs/agents.md)
for all supported names and paths. The wildcard covers that entire list, subject
to the requested scope. It does not mean every future agent has native support.

## Any other agent or chat tool

For a custom framework, local model, or chat UI with no skill loader, generate
the **self-contained prompt** and **uploadable skill ZIP**. This route needs Git
access and Python 3.10+, but no Node. Run it in a directory where the two output
names below do not already exist.

Linux/macOS, one line:

```bash
git clone --depth 1 https://github.com/kett1m/albanian-humanizer-skill.git albanian-humanizer-skill && python3 albanian-humanizer-skill/scripts/package_skill.py --output albanian-humanizer-export
```

Windows PowerShell 5.1 or 7, one line (with the Python `py` launcher installed):

```powershell
git clone --depth 1 https://github.com/kett1m/albanian-humanizer-skill.git albanian-humanizer-skill; if ($LASTEXITCODE -eq 0) { py -3 albanian-humanizer-skill/scripts/package_skill.py --output albanian-humanizer-export }
```

Attach or load `albanian-humanizer-export/albanian-humanizer-prompt.md` as the
host's task instructions, or upload `albanian-humanizer-export/albanian-humanizer.zip`
where uploaded skills are supported. Include your text and language/level choices
separately. This is a prompt-based fallback; it does not automatically register a
skill in a host with no skill loader. Copying only `SKILL.md` would omit resources.

## Verify, update, and remove

List user-level installations:

```bash
npx --yes skills@1.9.0 list --global
```

Reload the agent's skill discovery or start a new session. Ask it to use
`albanian-humanizer`; Codex also supports `$albanian-humanizer`, and slash-skill
hosts may expose `/albanian-humanizer`. Give a short text and a target profile.

Update this skill only:

```bash
npx --yes skills@1.9.0 update albanian-humanizer --global --yes
```

Remove this skill from all supported user-level targets:

```bash
npx --yes skills@1.9.0 remove albanian-humanizer --agent "*" --global --yes
```

For project installations, run from that project and omit `--global` (`update`
also accepts `--project`). Copy mode means that editing this repository does not
change installed copies until you update them. Back up any edits made directly
to installed copies before reinstalling. If npx cannot find Node, reopen the
terminal or activate your intended Node version; do not install the skill as root.

## Validation scope

On 2026-11-16, the remote install command was exercised on openSUSE Tumbleweed in
an isolated project with `--agent "*" --copy --yes`, without `--global`. CLI 1.9.0
reported all **79 supported targets**; they used **53 distinct skill folders**.
Instruction bodies and parsed metadata matched, and all supporting resources and
licenses were present. One host normalized YAML formatting without changing its
values. No agent application was launched. No OS prerequisite installer was run,
and Windows/macOS execution was not tested. The Bash examples were syntax-checked;
package names and flags were checked against official documentation or repositories.
