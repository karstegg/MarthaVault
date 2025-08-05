# Quick validation test for July 7th report
param(
    [string]$JsonPath = "daily_production\data\2025-07-07_nchwaning2.json",
    [string]$SourcePath = "00_Inbox\Raw Whatsap Data for Daily Reports.md"
)

Write-Host "=== Validation Test ===" -ForegroundColor Yellow

# Load JSON
$json = Get-Content $JsonPath | ConvertFrom-Json
Write-Host "JSON ROM: $($json.production.rom.actual)" -ForegroundColor Cyan

# Load source and search for July 7th data
$source = Get-Content $SourcePath -Raw
$july7Lines = $source -split "`n" | Select-String "07-07-2025" -Context 5,15

Write-Host "`nSource data around July 7th:" -ForegroundColor Yellow
$july7Lines | ForEach-Object { Write-Host $_.Line -ForegroundColor White }

# Check if ROM values match
if ($source -match "ROM.*?(\d+)\s+v") {
    $sourceROM = [int]$matches[1]
    Write-Host "`nSource ROM: $sourceROM" -ForegroundColor Green
    Write-Host "JSON ROM:   $($json.production.rom.actual)" -ForegroundColor Green
    
    if ($sourceROM -eq $json.production.rom.actual) {
        Write-Host "✓ ROM values match!" -ForegroundColor Green
    } else {
        Write-Host "✗ ROM values DO NOT match!" -ForegroundColor Red
    }
} else {
    Write-Host "Could not extract ROM from source" -ForegroundColor Red
}