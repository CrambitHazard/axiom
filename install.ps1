# Axiom Installer Script
# Adds Axiom to PATH so it can be used system-wide

Write-Host "Axiom Installer" -ForegroundColor Cyan
Write-Host "===============" -ForegroundColor Cyan
Write-Host ""

# Get the directory where this script is located
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$axiomPath = (Resolve-Path $scriptPath).Path

Write-Host "Installing Axiom from: $axiomPath" -ForegroundColor Yellow
Write-Host ""

# Check if already in PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -like "*$axiomPath*") {
    Write-Host "Axiom is already in your PATH!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To use it, close and reopen your terminal, then run: axiom --help" -ForegroundColor Yellow
    exit 0
}

# Add to PATH
try {
    $newPath = $currentPath
    if ($newPath -and -not $newPath.EndsWith(";")) {
        $newPath += ";"
    }
    $newPath += $axiomPath
    
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    
    Write-Host "[OK] Successfully added Axiom to PATH!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Close and reopen your terminal/PowerShell" -ForegroundColor White
    Write-Host "  2. Navigate to any Git repository" -ForegroundColor White
    Write-Host "  3. Run: axiom init" -ForegroundColor White
    Write-Host ""
    Write-Host "To verify installation, run: axiom --help" -ForegroundColor Yellow
} catch {
    Write-Host "[ERROR] Error adding to PATH: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "You may need to run this script as Administrator." -ForegroundColor Yellow
    exit 1
}
