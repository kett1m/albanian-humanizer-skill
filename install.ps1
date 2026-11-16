# PowerShell 5.1 and 7. No Node, npm, Git, Python, or execution-policy changes.
param([switch]$Project, [string]$Source, [switch]$List, [switch]$DryRun)
$ErrorActionPreference = 'Stop'

function Get-HumanizerPath([string]$Value) {
    if ($Value -eq '~') { return $HOME }
    if ($Value.StartsWith('~/') -or $Value.StartsWith('~\')) { $Value = Join-Path $HOME $Value.Substring(2) }
    return $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Value)
}
function Get-HumanizerGlobalPath([string]$Template) {
    $parts = $Template.Split(':', 2)
    $base = $HOME
    switch ($parts[0]) {
        'home' { }
        'config' { $base = Join-Path $HOME '.config'; if ($env:XDG_CONFIG_HOME) { $base = $env:XDG_CONFIG_HOME } }
        'claude' { $base = Join-Path $HOME '.claude'; if ($env:CLAUDE_CONFIG_DIR) { $base = $env:CLAUDE_CONFIG_DIR } }
        'autohand' { $base = Join-Path $HOME '.autohand'; if ($env:AUTOHAND_HOME) { $base = $env:AUTOHAND_HOME } }
        'grok' { $base = Join-Path $HOME '.grok'; if ($env:GROK_HOME) { $base = $env:GROK_HOME } }
        'hermes' { $base = Join-Path $HOME '.hermes'; if ($env:HERMES_HOME) { $base = $env:HERMES_HOME } }
        'vibe' { $base = Join-Path $HOME '.vibe'; if ($env:VIBE_HOME) { $base = $env:VIBE_HOME } }
        'reasonix' {
            $base = Join-Path $HOME '.reasonix'
            if ($env:APPDATA) { $base = Join-Path $env:APPDATA 'reasonix' }
            if ($env:REASONIX_HOME) { $base = $env:REASONIX_HOME }
        }
        'openclaw' {
            $base = Join-Path $HOME '.openclaw'
            foreach ($name in @('.openclaw', '.clawdbot', '.moltbot')) {
                $candidate = Join-Path $HOME $name
                if (Test-Path -LiteralPath $candidate -PathType Container) { $base = $candidate; break }
            }
        }
        default { throw "Unknown directory template: $Template" }
    }
    return Join-Path $base $parts[1]
}
function Show-HumanizerAgents($Agents, [int]$Count) {
    for ($i = 0; $i -lt $Count; $i++) { Write-Host ('  {0}. {1} ({2})' -f ($i + 1), $Agents[$i].Name, $Agents[$i].Id) }
}
function Install-Humanizer {
    $temp = $null
    $stage = $null
    try {
        if (-not $List -and [Console]::IsInputRedirected) { throw 'Open a terminal to choose your agent.' }
        if (-not $Source -and $PSScriptRoot -and (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'installer/agents.txt'))) { $Source = $PSScriptRoot }
        if (-not $Source) {
            $temp = Join-Path ([IO.Path]::GetTempPath()) ('albanian-humanizer-' + [Guid]::NewGuid().ToString('N'))
            New-Item -ItemType Directory -Path $temp | Out-Null
            $archive = Join-Path $temp 'source.zip'
            Write-Host 'Downloading Shqip & English Humanizer...'
            [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
            Invoke-WebRequest -UseBasicParsing 'https://codeload.github.com/kett1m/albanian-humanizer-skill/zip/refs/heads/main' -OutFile $archive
            Expand-Archive -LiteralPath $archive -DestinationPath $temp
            $Source = Join-Path $temp 'albanian-humanizer-skill-main'
        }
        $Source = Get-HumanizerPath $Source
        $skill = Join-Path $Source 'skills/albanian-humanizer'
        foreach ($file in @('SKILL.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', 'licenses/blader-MIT.txt', 'agents/openai.yaml',
            'references/editing.md', 'references/albanian.md', 'references/sq-standard.md', 'references/sq-gheg.md',
            'references/sq-tosk.md', 'references/sq-kosovo.md', 'references/english.md', 'references/levels-and-translation.md',
            'references/narrative.md', 'references/sources.md')) {
            if (-not (Test-Path -LiteralPath (Join-Path $skill $file) -PathType Leaf)) { throw "Incomplete skill: $file" }
        }
        $agents = @(Get-Content -LiteralPath (Join-Path $Source 'installer/agents.txt') -Encoding UTF8 | ConvertFrom-Csv -Delimiter '|' -Header Id, Name, ProjectPath, GlobalPath)
        if ($List) { Show-HumanizerAgents $agents $agents.Count; return }
        Write-Host "`nShqip & English Humanizer`nWhich AI agent or app do you use?"
        Show-HumanizerAgents $agents 8
        Write-Host "  more: show all agents`n  0: another agent / custom skills folder`n  q: cancel"
        Write-Host 'Choose a number or agent ID. Separate multiple choices with commas.'
        $selected = @()
        $destinations = @()
        while ($true) {
            $answer = (Read-Host 'Your agent').Trim()
            if ($answer -in @('q', 'quit')) { Write-Host 'Cancelled.'; return }
            if ($answer -eq 'more') { Show-HumanizerAgents $agents $agents.Count; continue }
            if ($answer -eq '0') {
                $folder = Read-Host 'Parent skills folder (blank to cancel)'
                if (-not $folder) { Write-Host 'Cancelled.'; return }
                $destinations = @(Join-Path (Get-HumanizerPath $folder) 'albanian-humanizer')
                break
            }
            if ($answer -eq 'all') { $selected = $agents; break }
            $selected = @()
            $valid = $true
            foreach ($choice in $answer.Split(',')) {
                $match = @()
                for ($i = 0; $i -lt $agents.Count; $i++) {
                    if ($choice.Trim() -in @([string]($i + 1), $agents[$i].Id, $agents[$i].Name)) { $match = @($agents[$i]); break }
                }
                if ($match.Count -eq 0) { $valid = $false; break }
                $selected += $match
            }
            if ($valid -and $selected.Count) { break }
            Write-Host 'Choose a listed number or name, or type more.'
        }
        if (-not $destinations.Count) {
            $projectFolder = (Get-Location).Path
            if (-not $Project -and @($selected | Where-Object GlobalPath -eq '-').Count) {
                Write-Host 'One of the selected agents requires a project folder.'
                $folder = Read-Host 'Project folder (blank to cancel)'
                if (-not $folder) { Write-Host 'Cancelled.'; return }
                $projectFolder = Get-HumanizerPath $folder
                if (-not (Test-Path -LiteralPath $projectFolder -PathType Container)) { throw "Project folder not found: $projectFolder" }
                $Project = $true
            }
            foreach ($agent in $selected) {
                if ($Project) { $base = Join-Path $projectFolder $agent.ProjectPath }
                else { $base = Get-HumanizerGlobalPath $agent.GlobalPath }
                $destinations += Join-Path $base 'albanian-humanizer'
            }
            $destinations = @($destinations | Select-Object -Unique)
        }
        Write-Host "`nInstall to:"
        foreach ($destination in $destinations) {
            Write-Host "  $destination"
            if (Test-Path -LiteralPath $destination) {
                $existing = Get-Item -LiteralPath $destination -Force
                if (-not $existing.PSIsContainer -or ($existing.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw "Destination must be a real directory: $destination" }
            }
        }
        if ($DryRun) { Write-Host 'Dry run: no skill files changed.'; return }
        Write-Host 'Existing copies will be saved in a backup folder before replacement.'
        if ((Read-Host 'Install? [y/N]') -notin @('y', 'yes')) { Write-Host 'Cancelled.'; return }
        foreach ($destination in $destinations) {
            $parent = Split-Path -Parent $destination
            [IO.Directory]::CreateDirectory($parent) | Out-Null
            $stage = Join-Path $parent ('.albanian-humanizer-stage.' + [Guid]::NewGuid().ToString('N'))
            New-Item -ItemType Directory -Path $stage | Out-Null
            Get-ChildItem -LiteralPath $skill -Force | Copy-Item -Destination $stage -Recurse -Force
            $backup = $null
            if (Test-Path -LiteralPath $destination) {
                $backup = Join-Path $parent ('.albanian-humanizer-backup.' + [Guid]::NewGuid().ToString('N'))
                New-Item -ItemType Directory -Path $backup | Out-Null
                Move-Item -LiteralPath $destination -Destination $backup
                Write-Host "Backup: $(Join-Path $backup 'albanian-humanizer')"
            }
            try { Move-Item -LiteralPath $stage -Destination $destination }
            catch {
                if ($backup -and -not (Test-Path -LiteralPath $destination)) { Move-Item -LiteralPath (Join-Path $backup 'albanian-humanizer') -Destination $destination }
                throw
            }
            $stage = $null
            Write-Host "Installed: $destination"
        }
        Write-Host "`nDone. Restart your agent and ask it to use albanian-humanizer."
    }
    finally {
        if ($stage -and (Test-Path -LiteralPath $stage)) { Remove-Item -LiteralPath $stage -Recurse -Force }
        if ($temp -and (Test-Path -LiteralPath $temp)) { Remove-Item -LiteralPath $temp -Recurse -Force }
    }
}
Install-Humanizer
