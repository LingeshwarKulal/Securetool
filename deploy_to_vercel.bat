@echo off
REM Vercel Deployment Script for Windows
REM This script automates the deployment process to fix the 404 error

echo 🚀 Deploying Secure File Encryption Tool to Vercel...
echo This will fix the 404 NOT_FOUND error you're experiencing.
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js not found. Please install Node.js from https://nodejs.org/
    echo Then run this script again.
    pause
    exit /b 1
)

REM Check if Vercel CLI is installed
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Vercel CLI not found. Installing...
    npm install -g vercel
)

echo ✅ Vercel CLI is ready
echo.

REM Deploy to Vercel
echo 🔄 Deploying to Vercel...
echo When prompted:
echo   - Framework Preset: Select 'Other'
echo   - Build Command: Leave empty (press Enter)
echo   - Output Directory: Leave empty (press Enter)
echo   - Install Command: pip install -r requirements.txt
echo.

REM Run Vercel deployment
vercel --prod

echo.
echo 🎉 Deployment complete!
echo.
echo Your Secure File Encryption Tool should now be accessible at the Vercel URL provided above.
echo The 404 error should be resolved, and you'll see a modern web interface for file encryption.
echo.
echo Features of the deployed web app:
echo   ✅ Modern drag-and-drop interface
echo   ✅ AES-256 encryption (same as desktop version)
echo   ✅ Mobile-friendly responsive design
echo   ✅ Real-time file processing
echo   ✅ Automatic file downloads
echo.
echo If you encounter any issues, check the VERCEL_DEPLOYMENT_GUIDE.md file for troubleshooting.
echo.
pause
