$ErrorActionPreference = "Stop"

# Set environment variables
$swiplPath = "C:\Program Files\swipl\bin"
$swiplHome = "C:\Program Files\swipl"

# Add to PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (!$userPath.Contains($swiplPath)) {
    [Environment]::SetEnvironmentVariable(
        "Path", 
        "$userPath;$swiplPath", 
        "User"
    )
}

# Set SWIPL_HOME
[Environment]::SetEnvironmentVariable(
    "SWIPL_HOME",
    $swiplHome,
    "User"
)

Write-Host "Installation complete. Please restart your terminal."