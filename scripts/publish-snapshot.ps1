param(
    [string]$Message = "snapshot: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from the repository root."
}

$branch = git branch --show-current
if ([string]::IsNullOrWhiteSpace($branch)) {
    throw "Cannot determine current branch."
}

# Warn, but do not block: the caller must confirm the tree is public-safe.
$dirty = git status --porcelain
if ($dirty) {
    Write-Host "Working tree contains changes; they will be included in the snapshot:" -ForegroundColor Yellow
    $dirty | ForEach-Object { Write-Host "  $_" }
}

git branch -D snapshot-temp 2>$null | Out-Null
git checkout --orphan snapshot-temp
git add -A
git commit -m $Message
git branch -M main
git push --force origin main

Write-Host "Published snapshot: $Message" -ForegroundColor Green
Write-Host "Remote main now points to a single root commit." -ForegroundColor Green
