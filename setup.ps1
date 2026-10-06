# Claude OS setup check. Windows PowerShell 5.1+. Run from the repo root: .\setup.ps1
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$fail = $false

function Fail($msg) { Write-Host "FAIL  $msg" -ForegroundColor Red; $script:fail = $true }
function Ok($msg)   { Write-Host "ok    $msg" -ForegroundColor Green }

# 1. Python >= 3.8 as `python`
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Fail "python not found on PATH. Install Python 3.8+ from python.org and tick 'Add to PATH'."
} else {
    $ver = & python -c "import sys; print('%d.%d' % sys.version_info[:2])" 2>$null
    if (-not $ver) { Fail "python on PATH doesn't run (Microsoft Store stub?). Install Python 3.8+ from python.org."; exit 1 }
    $ver = "$ver".Trim()
    $parts = $ver.Split('.')
    if ([int]$parts[0] -lt 3 -or ([int]$parts[0] -eq 3 -and [int]$parts[1] -lt 8)) {
        Fail "python $ver found, need 3.8+."
    } else {
        Ok "python $ver"
    }
}

# 2. Claude Code (warn only)
if (Get-Command claude -ErrorAction SilentlyContinue) {
    Ok "claude on PATH"
} else {
    Write-Host "warn  claude not on PATH. Install Claude Code (https://claude.com/claude-code), or use the editor extension." -ForegroundColor Yellow
}

if ($fail) { Write-Host "`nFix the errors above and re-run .\setup.ps1" -ForegroundColor Red; exit 1 }

# Area folders are not tracked by git when empty; projects.py needs them.
foreach ($a in 'explore', 'build', 'manage') {
    New-Item -ItemType Directory -Force -Path (Join-Path $root $a) | Out-Null
}

# 3. Project guard self-test (it imports project_guard, so run from its directory)
Push-Location (Join-Path $root '.claude\hooks')
try {
    & python test_project_guard.py
    if ($LASTEXITCODE -ne 0) { Fail "project guard tests failed." } else { Ok "project guard tests" }
} finally { Pop-Location }

# 4. Routing index
Push-Location $root
try {
    Write-Host "`nProjects:"
    & python system\projects.py
    if ($LASTEXITCODE -ne 0) { Fail "system\projects.py failed." } else { Ok "routing index" }
} finally { Pop-Location }

if ($fail) { exit 1 }

Write-Host @"

Next steps
  1. Open this folder in Claude Code:  claude   (or open it in your editor extension)
  2. Run /hooks and approve the project hook when prompted.
  3. Try:  /tune <a rough request>
  4. Start your own project: copy system\templates\* into build\<name>\ (see README).
"@
exit 0
