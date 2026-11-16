# Install from a raw script

Paste one command into your terminal. The script downloads the skill, asks
**“Which AI agent or app do you use?”**, shows the installation paths, and waits
for **y** before writing. Type a number or agent ID, **more** for all profiles,
**0** for another agent's skills folder, or **q** to cancel. Multiple choices
can be separated with commas.

## Linux and macOS

```bash
curl -fsSL https://raw.githubusercontent.com/kett1m/albanian-humanizer-skill/main/install.sh | bash
```

Works with Bash 3.2+, curl, tar, and gzip. No Node, npm, npx, Python, Git, or
GitHub CLI is required. The same command works on openSUSE Tumbleweed, Leap,
Slowroll, Ubuntu, Debian, Mint, Pop!_OS, elementary OS, Zorin, KDE neon, Kali,
Parrot, MX, Fedora, RHEL, Rocky, AlmaLinux, CentOS Stream, Oracle Linux, Arch,
Manjaro, EndeavourOS, Garuda, CachyOS, Alpine, Gentoo, Void, and macOS when those
basic tools are available. WSL uses this Linux route.

## Windows PowerShell

In Windows PowerShell 5.1 or PowerShell 7:

```powershell
irm https://raw.githubusercontent.com/kett1m/albanian-humanizer-skill/main/install.ps1 | iex
```

`irm` downloads the script from the raw URL; `iex` runs it. The script uses
PowerShell's built-in download, ZIP extraction, and file-copy commands.
No execution-policy change or administrator session is needed for this command.
From Command Prompt, open PowerShell first. Native Windows and WSL have separate
agent environments; install in the environment where your agent runs.

## Repository access

**The repository is currently private.** Anonymous raw and archive URLs cannot
serve it until the owner makes it public. The raw commands above are ready for
public access; a private repository returns an error instead. The installer
does not change repository visibility or embed credentials.

From an authorized local checkout, install without downloading anything:

```bash
bash install.sh
```

On Windows, run `./install.ps1` if your local script policy permits it. To inspect
before running, open [install.sh](../install.sh) or [install.ps1](../install.ps1).

## openSUSE Tumbleweed, Leap, and Slowroll

If the basic tools are missing, install them and start the installer in one line:

```bash
sudo zypper install -y bash curl tar gzip ca-certificates && curl -fsSL https://raw.githubusercontent.com/kett1m/albanian-humanizer-skill/main/install.sh | bash
```

Use your distribution's configured repositories. No Node package, additional
RPM repository, or distribution upgrade is needed. Run the installer as your
normal user; `sudo` is only for installing OS prerequisites.

## Other distribution prerequisites

Most desktop installations already have these tools. Install missing tools with
your normal package manager, then paste the raw-script command above.

| Distribution | Basic tools |
| --- | --- |
| Debian, Ubuntu, Mint, Pop!_OS, elementary, Zorin, KDE neon, Kali, Parrot, MX | `sudo apt-get update && sudo apt-get install -y bash curl tar gzip ca-certificates` |
| Fedora, RHEL, Rocky, AlmaLinux, CentOS Stream, Oracle Linux | `sudo dnf install -y bash curl tar gzip ca-certificates` |
| Arch, Manjaro, EndeavourOS, Garuda, CachyOS | `sudo pacman -S --needed --noconfirm bash curl tar gzip ca-certificates` |
| Alpine, with doas configured | `doas apk add bash curl tar gzip ca-certificates` |
| Gentoo | `sudo emerge --ask app-shells/bash net-misc/curl app-arch/tar app-arch/gzip app-misc/ca-certificates` |
| Void, glibc or musl | `sudo xbps-install -S -y bash curl tar gzip ca-certificates` |
| macOS | Bash, curl, tar, and gzip are included; use the main command |

On NixOS, or another system with Nix, use a temporary tool environment:

```bash
nix --extra-experimental-features "nix-command flakes" shell nixpkgs#bash nixpkgs#curl nixpkgs#gnutar nixpkgs#gzip nixpkgs#cacert --command bash -c 'curl -fsSL https://raw.githubusercontent.com/kett1m/albanian-humanizer-skill/main/install.sh | bash'
```

## Agent choice and scope

The default installs for your user account, across projects. The catalog has
79 profiles, including a generic skills-folder target. Its paths are a snapshot
of the [Vercel Skills directory catalog](https://github.com/vercel-labs/skills/blob/v1.9.0/docs/agents.md),
with the data and license retained in [installer/agents.txt](../installer/agents.txt)
and [installer/vercel-skills-LICENSE.txt](../installer/vercel-skills-LICENSE.txt).
Neither installer runs the Vercel CLI or installs a package runtime.

Some agents share directories and may discover the same copy. Agents without a
global skills directory prompt for an existing project folder. Type **all** only
if you want every profile; this includes project-only agents. Choice **0** accepts
a custom parent skills folder and creates `albanian-humanizer` inside it.

For a project-only install, run inside the intended project:

```bash
curl -fsSL https://raw.githubusercontent.com/kett1m/albanian-humanizer-skill/main/install.sh | bash -s -- --project
```

Windows PowerShell:

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/kett1m/albanian-humanizer-skill/main/install.ps1))) -Project
```

The scripts honor the applicable `XDG_CONFIG_HOME`, `CLAUDE_CONFIG_DIR`,
`AUTOHAND_HOME`, `GROK_HOME`, `HERMES_HOME`, `VIBE_HOME`, and `REASONIX_HOME`
overrides. Use a custom folder for another app-specific configuration. There is
no claim that every host/version supports native skills; the catalog records
known paths, and the model still needs to support the skill's instructions.

## Updates and backups

Rerun the same raw command and choose the same agent to update. An existing
`albanian-humanizer` directory is moved to a uniquely named
`.albanian-humanizer-backup.*` folder beside it before replacement. The installer
prints the backup path. Symlink destinations are refused so the script does not
replace or write through someone else's managed link.

The installation uses complete copies and does not modify shell profiles, agent
settings, or another project's instruction files. It does not update the old
Skills CLI lock files from earlier installer versions; use this installer for
future updates. Remove the displayed `albanian-humanizer` directory to uninstall;
keep any backup you still need.

For a preview from a local checkout, run `bash install.sh --dry-run` or
`./install.ps1 -DryRun`. `--list` / `-List` shows the agent catalog. The normal
picker requires an interactive terminal. Bash reads answers from `/dev/tty`, so
it still prompts when the script itself arrives through `curl | bash`.

After installation, restart your agent and ask it to use `albanian-humanizer`.
In Codex, use `$albanian-humanizer`; some other hosts expose `/albanian-humanizer`.

## Any other agent or chat tool

Use choice **0** when the agent has a skills folder. For a chat app with no skill
loader, build the standalone prompt from a local checkout with Python 3.10+:

```bash
python3 scripts/package_skill.py --output dist
```

Attach `dist/albanian-humanizer-prompt.md` as task instructions, or upload
`dist/albanian-humanizer.zip` where skill uploads are supported. Include your text
and language/level choices separately. Python is only needed for this optional
export, not for either installer.

## Design references and validation

The raw-download pattern follows established standalone installers such as
[uv](https://docs.astral.sh/uv/getting-started/installation/) and
[Ollama](https://github.com/ollama/ollama/blob/main/README.md). These projects are
references for installation UX, not dependencies or endorsements.

The Bash installer passed syntax and ShellCheck checks and terminal-based tests
on openSUSE Tumbleweed, including piped input, explicit agent choice, cancellation,
multiple agents, all profiles, custom paths, backups, failed downloads, and
symlink refusal. All installed skill resources and notices were byte-compared
with the source. No real user-level agent installation or OS dependency install
was performed. PowerShell 7.7 also installed all 53 distinct project folders on Linux, with
all 15 skill files preserved in each. Native Windows/macOS execution has not been
tested. Details are in [the validation record](../evals/VALIDATION.md).
