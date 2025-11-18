@echo off
REM Debug build script for Martha Agent

cd /d "%~dp0"

echo ============================================
echo Martha Agent - Build Diagnostic
echo ============================================
echo.

echo Current directory: %cd%
echo.

REM Check esbuild.config.mjs
echo Checking esbuild.config.mjs...
type esbuild.config.mjs | findstr "external"
echo.

REM Check if xterm is installed
echo Checking xterm installation...
if exist node_modules\xterm (
    echo [OK] xterm found in node_modules
) else (
    echo [ERROR] xterm NOT found in node_modules
)
echo.

REM Check package.json
echo Checking dependencies in package.json...
type package.json | findstr "xterm"
echo.

REM Run build with verbose output
echo Running build...
npm run build
echo.

REM Check output size
echo Build complete. File size:
dir main.js | findstr "main.js"
echo.

REM Expected: ~439,000 bytes
echo Expected size: ~439,000 bytes
echo If size is ~17,000 bytes, xterm is NOT bundled
echo.

pause
