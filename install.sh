#!/usr/bin/env bash
# Bash 3.2+ (including macOS). Downloads only this repository; no package runtime.
set -eo pipefail

ah_fail() { printf 'Install failed: %s\n' "$*" >&2; exit 1; }
ah_cancel() { printf '\nCancelled.\n'; exit 0; }
ah_ask() { printf '%s' "$1"; IFS= read -r AH_REPLY <&3 || ah_cancel; }
ah_expand() {
  # Match a literal tilde supplied by the user; do not evaluate shell input.
  # shellcheck disable=SC2088
  case "$1" in
    '~') printf '%s\n' "$HOME" ;;
    '~/'*) printf '%s/%s\n' "$HOME" "${1:2}" ;;
    /*) printf '%s\n' "$1" ;;
    *) printf '%s/%s\n' "$PWD" "$1" ;;
  esac
}
ah_global() {
  local base template=$1
  case "${template%%:*}" in
    home) base=$HOME ;;
    config) base=${XDG_CONFIG_HOME:-$HOME/.config} ;;
    claude) base=${CLAUDE_CONFIG_DIR:-$HOME/.claude} ;;
    autohand) base=${AUTOHAND_HOME:-$HOME/.autohand} ;;
    grok) base=${GROK_HOME:-$HOME/.grok} ;;
    hermes) base=${HERMES_HOME:-$HOME/.hermes} ;;
    vibe) base=${VIBE_HOME:-$HOME/.vibe} ;;
    reasonix) base=${REASONIX_HOME:-$HOME/.reasonix} ;;
    openclaw)
      base=$HOME/.openclaw
      if [[ ! -d "$base" ]]; then
        if [[ -d "$HOME/.clawdbot" ]]; then base=$HOME/.clawdbot
        elif [[ -d "$HOME/.moltbot" ]]; then base=$HOME/.moltbot; fi
      fi ;;
    *) ah_fail "Unknown directory template: $template" ;;
  esac
  printf '%s/%s\n' "$base" "${template#*:}"
}
ah_cleanup() {
  [[ -z ${AH_STAGE:-} ]] || rm -rf -- "$AH_STAGE"
  [[ -z ${AH_TMP:-} ]] || rm -rf -- "$AH_TMP"
  return 0
}
ah_menu() {
  local i limit=$1
  for ((i=0; i<limit; i++)); do
    printf '  %s. %s (%s)\n' "$((i+1))" "${AH_NAMES[$i]}" "${AH_IDS[$i]}"
  done
}
ah_main() {
  local source='' project=0 list=0 dry=0 i j choice found duplicate base dest backup item
  local script_dir=''
  AH_TMP='' AH_STAGE=''
  trap ah_cleanup EXIT
  trap 'exit 130' INT TERM
  while (($#)); do
    case "$1" in
      --source) (($# >= 2)) || ah_fail '--source needs a repository directory'; source=$2; shift ;;
      --project) project=1 ;;
      --list) list=1 ;;
      --dry-run) dry=1 ;;
      --help) printf 'Usage: bash install.sh [--project] [--source DIR] [--list] [--dry-run]\nChoose your agent, review the destination, then confirm.\n'; return ;;
      *) ah_fail "Unknown option: $1" ;;
    esac
    shift
  done
  if (( ! list )); then
    # The script itself may arrive on stdin through curl. Answers come from the TTY.
    { exec 3<>/dev/tty; } 2>/dev/null || ah_fail 'Open a terminal to choose your agent.'
  fi
  if [[ -z "$source" && -n ${BASH_SOURCE[0]:-} && -f ${BASH_SOURCE[0]} ]]; then
    script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
    [[ ! -f "$script_dir/installer/agents.txt" ]] || source=$script_dir
  fi
  if [[ -z "$source" ]]; then
    command -v curl >/dev/null || ah_fail 'Install curl, then run this command again.'
    command -v tar >/dev/null || ah_fail 'Install tar, then run this command again.'
    AH_TMP=$(mktemp -d "${TMPDIR:-/tmp}/albanian-humanizer.XXXXXX")
    printf 'Downloading Shqip & English Humanizer...\n'
    curl -fLsS --retry 2 --connect-timeout 15 --max-time 120 \
      https://codeload.github.com/kett1m/albanian-humanizer-skill/tar.gz/refs/heads/main \
      -o "$AH_TMP/source.tar.gz" || ah_fail 'Cannot download the repository. Public access and an internet connection are required.'
    mkdir "$AH_TMP/source"
    tar -xzf "$AH_TMP/source.tar.gz" -C "$AH_TMP/source"
    source=$AH_TMP/source/albanian-humanizer-skill-main
  fi
  [[ -d "$source" ]] || ah_fail "Source directory not found: $source"
  source=$(cd -- "$source" && pwd)
  [[ -f "$source/installer/agents.txt" ]] || ah_fail 'Agent directory catalog is missing.'
  for item in SKILL.md LICENSE THIRD_PARTY_NOTICES.md agents/openai.yaml licenses/blader-MIT.txt \
    references/{editing,albanian,sq-standard,sq-gheg,sq-tosk,sq-kosovo,english,levels-and-translation,narrative,sources}.md; do
    [[ -f "$source/skills/albanian-humanizer/$item" ]] || ah_fail "Incomplete skill: $item"
  done
  AH_IDS=() AH_NAMES=() AH_PROJECTS=() AH_GLOBALS=() AH_SELECTED=() AH_DESTS=()
  while IFS='|' read -r i j base dest; do
    AH_IDS+=("$i"); AH_NAMES+=("$j"); AH_PROJECTS+=("$base"); AH_GLOBALS+=("$dest")
  done < "$source/installer/agents.txt"
  if (( list )); then ah_menu "${#AH_IDS[@]}"; return; fi
  printf '\nShqip & English Humanizer\nWhich AI agent or app do you use?\n'
  ah_menu 8
  printf '  more: show all agents\n  0: another agent / custom skills folder\n  q: cancel\n'
  printf 'Choose a number or agent ID. Separate multiple choices with commas.\n'
  while :; do
    ah_ask 'Your agent: '
    case "$AH_REPLY" in
      q|quit) ah_cancel ;;
      more) ah_menu "${#AH_IDS[@]}"; continue ;;
      0)
        ah_ask 'Parent skills folder (blank to cancel): '
        [[ -n "$AH_REPLY" ]] || ah_cancel
        base=$(ah_expand "$AH_REPLY")
        AH_DESTS=("${base%/}/albanian-humanizer")
        break ;;
      all) for ((i=0; i<${#AH_IDS[@]}; i++)); do AH_SELECTED+=("$i"); done; break ;;
    esac
    AH_SELECTED=()
    IFS=',' read -r -a choices <<< "$AH_REPLY"
    found=1
    [[ -n "$AH_REPLY" && "$AH_REPLY" != *, ]] || found=0
    for choice in "${choices[@]}"; do
      choice=$(printf '%s' "$choice" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
      j=-1
      for ((i=0; i<${#AH_IDS[@]}; i++)); do
        if [[ "$choice" == "$((i+1))" || "$choice" == "${AH_IDS[$i]}" || "$choice" == "${AH_NAMES[$i]}" ]]; then j=$i; break; fi
      done
      if ((j < 0)); then found=0; break; fi
      AH_SELECTED+=("$j")
    done
    if ((found && ${#AH_SELECTED[@]})); then break; fi
    printf 'Choose a listed number or name, or type more.\n'
  done
  if ((${#AH_DESTS[@]} == 0)); then
    base=$PWD
    if (( ! project )); then
      for i in "${AH_SELECTED[@]}"; do
        if [[ ${AH_GLOBALS[$i]} == '-' ]]; then
          printf '%s needs a project folder.\n' "${AH_NAMES[$i]}"
          ah_ask 'Project folder (blank to cancel): '
          [[ -n "$AH_REPLY" ]] || ah_cancel
          base=$(ah_expand "$AH_REPLY")
          [[ -d "$base" ]] || ah_fail "Project folder not found: $base"
          project=1; break
        fi
      done
    fi
    for i in "${AH_SELECTED[@]}"; do
      if ((project)); then dest=$base/${AH_PROJECTS[$i]}/albanian-humanizer
      else dest=$(ah_global "${AH_GLOBALS[$i]}")/albanian-humanizer; fi
      duplicate=0
      for item in "${AH_DESTS[@]}"; do [[ "$item" != "$dest" ]] || duplicate=1; done
      ((duplicate)) || AH_DESTS+=("$dest")
    done
  fi
  printf '\nInstall to:\n'
  for dest in "${AH_DESTS[@]}"; do
    printf '  %s\n' "$dest"
    [[ ! -L "$dest" ]] || ah_fail 'Destination is a symlink; choose a custom folder or manage the existing link first.'
    [[ ! -e "$dest" || -d "$dest" ]] || ah_fail "Destination is not a directory: $dest"
  done
  if ((dry)); then printf 'Dry run: no skill files changed.\n'; return; fi
  printf 'Existing copies will be saved in a backup folder before replacement.\n'
  ah_ask 'Install? [y/N]: '
  case "$AH_REPLY" in y|Y|yes|YES) ;; *) ah_cancel ;; esac
  for dest in "${AH_DESTS[@]}"; do
    base=$(dirname -- "$dest")
    mkdir -p -- "$base"
    AH_STAGE=$(mktemp -d "$base/.albanian-humanizer-stage.XXXXXX")
    cp -R "$source/skills/albanian-humanizer/." "$AH_STAGE/"
    backup=''
    if [[ -d "$dest" ]]; then
      backup=$(mktemp -d "$base/.albanian-humanizer-backup.XXXXXX")
      mv -- "$dest" "$backup/albanian-humanizer"
      printf 'Backup: %s/albanian-humanizer\n' "$backup"
    fi
    if ! mv -- "$AH_STAGE" "$dest"; then
      if [[ -n "$backup" && ! -e "$dest" ]]; then mv -- "$backup/albanian-humanizer" "$dest"; fi
      ah_fail "Could not install to $dest"
    fi
    AH_STAGE=''
    printf 'Installed: %s\n' "$dest"
  done
  printf '\nDone. Restart your agent and ask it to use albanian-humanizer.\n'
}

# Keep execution at the end so a truncated download cannot start an installation.
ah_main "$@"
