$ErrorActionPreference = "Stop"

$swiplHome = "C:\Program Files\swipl"
$swiplBin = Join-Path $swiplHome "bin"
$swiplLib = Join-Path $swiplHome "lib"

Write-Host "Verifying SWI-Prolog installation..."
Write-Host "Checking paths:"
Write-Host "SWIPL_HOME: $swiplHome"
Write-Host "SWIPL_BIN: $swiplBin"
Write-Host "SWIPL_LIB: $swiplLib"

# List all files in lib directory
Write-Host "`nListing files in lib directory:"
Get-ChildItem -Path $swiplLib -Filter "*.dll" | ForEach-Object {
    Write-Host "Found DLL: $($_.FullName)"
}

if (-not (Test-Path $swiplHome)) {
    Write-Host "Error: SWI-Prolog home directory not found at $swiplHome"
    exit 1
}

$swiplExe = Join-Path $swiplBin "swipl.exe"
if (-not (Test-Path $swiplExe)) {
    Write-Host "Error: swipl.exe not found at $swiplExe"
    exit 1
}

$libswiplDll = Join-Path $swiplLib "libswipl.dll"
if (-not (Test-Path $libswiplDll)) {
    Write-Host "Error: libswipl.dll not found at $libswiplDll"
    Write-Host "Searching for libswipl.dll in alternative locations..."
    
    # Search in bin directory
    $altPath = Join-Path $swiplBin "libswipl.dll"
    if (Test-Path $altPath) {
        Write-Host "Found libswipl.dll in bin directory: $altPath"
        $libswiplDll = $altPath
    }
}

Write-Host "`nFile details for libswipl.dll:"
if (Test-Path $libswiplDll) {
    Get-Item $libswiplDll | Select-Object FullName, Length, LastWriteTime
} else {
    Write-Host "Could not find libswipl.dll in any location"
    exit 1
}

Write-Host "`nVerifying Prolog functionality..."
try {
    $version = & "$swiplExe" --version
    Write-Host "SWI-Prolog version: $version"
    Write-Host "Installation verified successfully"
} catch {
    Write-Host "Error testing Prolog: $_"
    exit 1
}