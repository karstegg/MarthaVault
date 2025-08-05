# Daily Report Data Validation Script
# Validates extracted report data against source WhatsApp data

param(
    [Parameter(Mandatory=$true)]
    [string]$ReportJsonPath,
    
    [Parameter(Mandatory=$true)]
    [string]$SourceDataPath,
    
    [Parameter(Mandatory=$true)]
    [string]$ReportDate  # Format: YYYY-MM-DD
)

function Write-ValidationResult {
    param($Field, $Expected, $Actual, $Status, $SourceLine = "N/A")
    Write-Host "[$Status] $Field" -ForegroundColor $(if($Status -eq "PASS") {"Green"} elseif($Status -eq "FAIL") {"Red"} else {"Yellow"})
    Write-Host "  Expected: $Expected (Source Line: $SourceLine)"
    Write-Host "  Actual:   $Actual"
    Write-Host ""
}

function Extract-DateFromWhatsApp {
    param($Content, $Date)
    
    # Convert date to different formats found in WhatsApp data
    $dateObj = [DateTime]::ParseExact($Date, "yyyy-MM-dd", $null)
    $formats = @(
        $dateObj.ToString("dd-MM-yyyy"),      # 07-07-2025
        $dateObj.ToString("dd/MM/yyyy"),      # 07/07/2025  
        $dateObj.ToString("dd MMM yyyy"),     # 07 Jul 2025
        $dateObj.ToString("d MMMM yyyy")      # 7 July 2025
    )
    
    $extractedData = @{}
    $lines = $Content -split "`n"
    
    for ($i = 0; $i -lt $lines.Length; $i++) {
        $line = $lines[$i]
        
        # Check if line contains any of our date formats
        $matchedFormat = $formats | Where-Object { $line -like "*$_*" }
        
        if ($matchedFormat) {
            Write-Host "Found report for $matchedFormat at line $($i+1)" -ForegroundColor Cyan
            
            # Extract engineer name from the line
            if ($line -match '\] ([^:]+):') {
                $extractedData.Engineer = $matches[1]
                $extractedData.EngineerLine = $i + 1
            }
            
            # Look ahead for production data (next 20 lines)
            for ($j = $i + 1; $j -lt [Math]::Min($i + 21, $lines.Length); $j++) {
                $dataLine = $lines[$j]
                
                # ROM data
                if ($dataLine -match 'ROM.*?(\d+).*?v.*?(\d+)') {
                    $extractedData.ROM_Actual = [int]$matches[1]
                    $extractedData.ROM_Target = [int]$matches[2]
                    $extractedData.ROM_Line = $j + 1
                }
                
                # Product data
                if ($dataLine -match 'Product.*?(\d+).*?v.*?(\d+)') {
                    $extractedData.Product_Actual = [int]$matches[1]
                    $extractedData.Product_Target = [int]$matches[2]
                    $extractedData.Product_Line = $j + 1
                }
                
                # TMM availability - DT
                if ($dataLine -match 'DT:\s*(\d+)/(\d+)') {
                    $extractedData.DT_Available = [int]$matches[1]
                    $extractedData.DT_Total = [int]$matches[2]
                    $extractedData.DT_Line = $j + 1
                }
                
                # Safety status
                if ($dataLine -match 'Safety.*Clear|All clear') {
                    $extractedData.Safety = "Clear"
                    $extractedData.Safety_Line = $j + 1
                }
            }
            break
        }
    }
    
    return $extractedData
}

Write-Host "=== Daily Report Data Validation ===" -ForegroundColor Yellow
Write-Host "Report: $ReportJsonPath"
Write-Host "Source: $SourceDataPath" 
Write-Host "Date: $ReportDate"
Write-Host ""

# Validate inputs exist
if (-not (Test-Path $ReportJsonPath)) {
    Write-Host "ERROR: Report JSON file not found: $ReportJsonPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $SourceDataPath)) {
    Write-Host "ERROR: Source data file not found: $SourceDataPath" -ForegroundColor Red
    exit 1
}

# Load JSON report
try {
    $reportData = Get-Content $ReportJsonPath | ConvertFrom-Json
    Write-Host "✓ JSON report loaded successfully" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to parse JSON report: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Load source data
try {
    $sourceContent = Get-Content $SourceDataPath -Raw
    Write-Host "✓ Source data loaded successfully" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to load source data: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Extract data from WhatsApp source
Write-Host "`n=== Extracting Source Data ===" -ForegroundColor Yellow
$sourceData = Extract-DateFromWhatsApp -Content $sourceContent -Date $ReportDate

if ($sourceData.Keys.Count -eq 0) {
    Write-Host "ERROR: No data found for date $ReportDate in source file" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Found source data with $($sourceData.Keys.Count) fields" -ForegroundColor Green

# Validation Results
Write-Host "`n=== Validation Results ===" -ForegroundColor Yellow
$validationsPassed = 0
$validationsFailed = 0
$validationScore = 0

# Validate Safety
if ($sourceData.Safety -and $reportData.safety.status) {
    if ($sourceData.Safety -eq $reportData.safety.status) {
        Write-ValidationResult "Safety Status" $sourceData.Safety $reportData.safety.status "PASS" $sourceData.Safety_Line
        $validationsPassed++
    } else {
        Write-ValidationResult "Safety Status" $sourceData.Safety $reportData.safety.status "FAIL" $sourceData.Safety_Line
        $validationsFailed++
    }
}

# Validate ROM Production
if ($sourceData.ROM_Actual -and $reportData.production.rom.actual) {
    if ($sourceData.ROM_Actual -eq $reportData.production.rom.actual) {
        Write-ValidationResult "ROM Production" $sourceData.ROM_Actual $reportData.production.rom.actual "PASS" $sourceData.ROM_Line
        $validationsPassed++
    } else {
        Write-ValidationResult "ROM Production" $sourceData.ROM_Actual $reportData.production.rom.actual "FAIL" $sourceData.ROM_Line
        $validationsFailed++
    }
}

# Validate Product Production  
if ($sourceData.Product_Actual -and $reportData.production.product.actual) {
    if ($sourceData.Product_Actual -eq $reportData.production.product.actual) {
        Write-ValidationResult "Product Production" $sourceData.Product_Actual $reportData.production.product.actual "PASS" $sourceData.Product_Line
        $validationsPassed++
    } else {
        Write-ValidationResult "Product Production" $sourceData.Product_Actual $reportData.production.product.actual "FAIL" $sourceData.Product_Line
        $validationsFailed++
    }
}

# Validate Engineer
if ($sourceData.Engineer -and $reportData.report_metadata.engineer) {
    # Clean up engineer names for comparison
    $sourceEngineer = $sourceData.Engineer -replace "Shaft Engineer", "" -replace "^\s+|\s+$", ""
    $reportEngineer = $reportData.report_metadata.engineer
    
    if ($sourceEngineer -like "*$reportEngineer*" -or $reportEngineer -like "*$sourceEngineer*") {
        Write-ValidationResult "Engineer" $sourceData.Engineer $reportData.report_metadata.engineer "PASS" $sourceData.EngineerLine
        $validationsPassed++
    } else {
        Write-ValidationResult "Engineer" $sourceData.Engineer $reportData.report_metadata.engineer "FAIL" $sourceData.EngineerLine
        $validationsFailed++
    }
}

# Calculate validation score
$totalValidations = $validationsPassed + $validationsFailed
if ($totalValidations -gt 0) {
    $validationScore = [Math]::Round(($validationsPassed / $totalValidations) * 100, 1)
}

# Final Results
Write-Host "=== VALIDATION SUMMARY ===" -ForegroundColor Yellow
Write-Host "Passed: $validationsPassed" -ForegroundColor Green
Write-Host "Failed: $validationsFailed" -ForegroundColor Red
Write-Host "Score:  $validationScore%" -ForegroundColor $(if($validationScore -ge 80) {"Green"} elseif($validationScore -ge 60) {"Yellow"} else {"Red"})

if ($validationScore -lt 80) {
    Write-Host "`nRECOMMENDATION: Report requires revision - validation score below 80%" -ForegroundColor Red
    exit 1
} elseif ($validationScore -lt 100) {
    Write-Host "`nRECOMMENDATION: Report acceptable but has minor issues" -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "`nRECOMMENDATION: Report passes all validations" -ForegroundColor Green
    exit 0
}
}