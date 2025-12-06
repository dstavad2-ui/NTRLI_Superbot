# ntrli_finalizer.ps1
# ================================================
# NTRLI Superbot Finalizer - PowerShell Version
# ================================================

param(
    [switch]$UpdateOnly,
    [switch]$LaunchOnly,
    [switch]$CheckHealth
)

# Ensure UTF-8 output
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Function to display status messages
function Write-NTRLIStatus {
    param(
        [string]$Message,
        [ValidateSet("Success","Warning","Error","Info")] 
        [string]$Type
    )

    switch ($Type) {
        "Success" { Write-Host "  ✅ $Message" -ForegroundColor Green }
        "Warning" { Write-Host "  ⚠️ $Message" -ForegroundColor Yellow }
        "Error"   { Write-Host "  ❌ $Message" -ForegroundColor Red }
        "Info"    { Write-Host "  ℹ️ $Message" -ForegroundColor Cyan }
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

    Write-NTRLIStatus "Running Python script: $ScriptPath" "Info"
    python "$ScriptPath" $Args
    if ($LASTEXITCODE -eq 0) {
        Write-NTRLIStatus "Python script completed successfully" "Success"
        return $true
    } else {
        Write-NTRLIStatus "Python script failed with exit code $LASTEXITCODE" "Error"
        return $false
    }
}

# ================================================
# MAIN LOGIC
# ================================================

# Full Update + Launch
if (-not $UpdateOnly -and -not $LaunchOnly -and -not $CheckHealth) {
    Write-NTRLIStatus "Running Full Update + Launch..." "Info"
    Run-PythonScript ".\update.py"
    Run-PythonScript ".\launch.py"
    exit 0
}

# Update Only
if ($UpdateOnly) {
    Write-NTRLIStatus "Running Update Only..." "Info"
    Run-PythonScript ".\update.py"
    exit 0
}

# Launch Only
if ($LaunchOnly) {
    Write-NTRLIStatus "Launching Bot System..." "Info"
    Run-PythonScript ".\launch.py"
    exit 0
}

# Health Check Only
if ($CheckHealth) {
    Write-NTRLIStatus "Running Health Check..." "Info"
    Run-PythonScript ".\health_check.py"
    exit 0
}
