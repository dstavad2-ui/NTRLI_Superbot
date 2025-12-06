# NTRLI Superbot Finalizer - PowerShell Version (FIXED)
# No encoding issues - simple and clean

param(
    [switch]$UpdateOnly,
    [switch]$LaunchOnly,
    [switch]$CheckHealth
)

# Ensure UTF-8 output
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Function to display status messages
function Write-NTRLIStatus {
    param(
        [string]$Message,
        [ValidateSet("Success","Warning","Error","Info")] 
        [string]$Type
    )

    switch ($Type) {
        "Success" { Write-Host "[OK] $Message" -ForegroundColor Green }
        "Warning" { Write-Host "[!!] $Message" -ForegroundColor Yellow }
        "Error"   { Write-Host "[XX] $Message" -ForegroundColor Red }
        "Info"    { Write-Host "[..] $Message" -ForegroundColor Cyan }
    }
}

# Function to run Python scripts
function Run-PythonScript {
    param(
        [string]$ScriptPath,
        [string]$Args = ""
    )

    if (-not (Test-Path $ScriptPath)) {
        Write-NTRLIStatus "$ScriptPath not found" "Error"
        return $false
    }

    Write-NTRLIStatus "Running: $ScriptPath" "Info"
    python "$ScriptPath" $Args
    
    if ($LASTEXITCODE -eq 0) {
        Write-NTRLIStatus "Completed successfully" "Success"
        return $true
    } else {
        Write-NTRLIStatus "Failed with exit code $LASTEXITCODE" "Error"
        return $false
    }
}

# ================================================
# MAIN LOGIC
# ================================================

Write-Host ""
Write-Host "========================================================"
Write-Host "  NTRLI SUPERBOT FINALIZER"
Write-Host "========================================================"
Write-Host ""

# Full Update + Launch
if (-not $UpdateOnly -and -not $LaunchOnly -and -not $CheckHealth) {
    Write-NTRLIStatus "Running Full Update + Launch" "Info"
    Write-Host ""
    
    if (-not (Run-PythonScript ".\update.py")) {
        Write-Host ""
        Write-NTRLIStatus "Update failed. Aborting." "Error"
        exit 1
    }
    
    Write-Host ""
    Write-NTRLIStatus "Update complete. Starting bot..." "Success"
    Write-Host ""
    
    Run-PythonScript ".\launch.py"
    exit $LASTEXITCODE
}

# Update Only
if ($UpdateOnly) {
    Write-NTRLIStatus "Running Update Only" "Info"
    Write-Host ""
    Run-PythonScript ".\update.py"
    exit $LASTEXITCODE
}

# Launch Only
if ($LaunchOnly) {
    Write-NTRLIStatus "Launching Bot System" "Info"
    Write-Host ""
    Run-PythonScript ".\launch.py"
    exit $LASTEXITCODE
}

# Health Check Only
if ($CheckHealth) {
    Write-NTRLIStatus "Running Health Check" "Info"
    Write-Host ""
    
    if (Test-Path ".\health_check.py") {
        Run-PythonScript ".\health_check.py"
    } else {
        Write-NTRLIStatus "health_check.py not found" "Warning"
    }
    
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "========================================================"
Write-Host "  Done"
Write-Host "========================================================"