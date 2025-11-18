@echo off
REM Martha Agent - Windows Installation Helper
REM This script installs node-pty prebuilt binaries without compiling from source

echo ============================================
echo Martha Agent - Installing Dependencies
echo ============================================
echo.

cd /d "%~dp0"

echo Current directory: %cd%
echo.

REM Check if npm is available
where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: npm not found in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo Node.js/npm found!
echo.

REM Clean up old installations
if exist node_modules\node-pty (
    echo Cleaning up old node-pty...
    rmdir /s /q node_modules\node-pty 2>nul
)

REM Create node_modules directory if it doesn't exist
if not exist node_modules mkdir node_modules

REM Install node-pty with prebuilt binaries
echo.
echo Installing node-pty (this may take a minute)...
echo.

REM Try to use prebuilt binaries from npm
npm install node-pty@1.0.0 --ignore-scripts --no-save

if %errorlevel% neq 0 (
    echo.
    echo WARNING: Failed to install node-pty without building
    echo Trying with build from source...
    echo.
    npm install node-pty@1.0.0 --no-save

    if %errorlevel% neq 0 (
        echo.
        echo ERROR: node-pty installation failed
        echo.
        echo Possible solutions:
        echo 1. Install Visual Studio Build Tools with Spectre libraries
        echo 2. Use Windows Subsystem for Linux WSL
        echo 3. Try installing from a local drive ^(not Google Drive^)
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo Files installed:
dir node_modules\node-pty /b 2>nul | find "." >nul && (
    echo   - node_modules\node-pty [OK]
) || (
    echo   - node_modules\node-pty [MISSING]
)

echo.
echo Next steps:
echo 1. Open Obsidian
echo 2. Settings ^> Community Plugins
echo 3. Enable "Martha Agent"
echo 4. Click terminal icon or use Command Palette
echo.

pause
