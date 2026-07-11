param(
    [string]$RemoteUrl = "",
    [string]$Tag = "v3.0.0"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path "pyproject.toml") -or -not (Test-Path "copier.yml")) {
    throw "Run this script from the Planning Lite central repository root."
}

if (-not (Test-Path ".git")) {
    git init
}

git add .

$hasHead = $true
git rev-parse --verify HEAD *> $null
if ($LASTEXITCODE -ne 0) {
    $hasHead = $false
}

if (-not $hasHead) {
    git commit -m "Create Planning Lite central template"
}
elseif (git status --porcelain) {
    git commit -m "Update Planning Lite central template"
}

git branch -M main

if ($RemoteUrl) {
    $existing = git remote get-url origin 2>$null
    if ($LASTEXITCODE -eq 0) {
        git remote set-url origin $RemoteUrl
    }
    else {
        git remote add origin $RemoteUrl
    }
}

$tagExists = git tag --list $Tag
if (-not $tagExists) {
    git tag $Tag
}

Write-Host "Central repository prepared."
Write-Host "Current tag: $Tag"
if ($RemoteUrl) {
    Write-Host "Next commands:"
    Write-Host "  git push -u origin main"
    Write-Host "  git push origin $Tag"
}
