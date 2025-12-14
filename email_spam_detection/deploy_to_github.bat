@echo off
echo ========================================
echo GitHub Deployment Script
echo ========================================
echo.

set /p GITHUB_USERNAME="Enter your GitHub username: "
set /p REPO_NAME="Enter repository name (default: email_spam_detection): "

if "%REPO_NAME%"=="" set REPO_NAME=email_spam_detection

echo.
echo Repository URL will be: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
echo.
set /p CONFIRM="Is this correct? (Y/N): "

if /i not "%CONFIRM%"=="Y" (
    echo Deployment cancelled.
    pause
    exit /b 1
)

echo.
echo Checking for existing remote...
git remote show origin >nul 2>&1
if %errorlevel%==0 (
    echo Remote 'origin' already exists. Removing it...
    git remote remove origin
)

echo.
echo Adding remote repository...
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

echo.
echo Renaming branch to 'main'...
git branch -M main

echo.
echo ========================================
echo Ready to push!
echo ========================================
echo.
echo You will be prompted for your GitHub credentials.
echo For password, use a Personal Access Token (not your GitHub password).
echo.
echo To generate a token, visit: https://github.com/settings/tokens
echo.
set /p PUSH_NOW="Push to GitHub now? (Y/N): "

if /i "%PUSH_NOW%"=="Y" (
    echo.
    echo Pushing to GitHub...
    git push -u origin main
    
    if %errorlevel%==0 (
        echo.
        echo ========================================
        echo SUCCESS! Your code has been pushed to GitHub!
        echo ========================================
        echo.
        echo Repository URL: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
        echo.
    ) else (
        echo.
        echo ========================================
        echo ERROR: Failed to push to GitHub
        echo ========================================
        echo.
        echo Common issues:
        echo 1. Authentication failed - Use a Personal Access Token
        echo 2. Repository doesn't exist - Create it on GitHub first
        echo 3. Network issues - Check your internet connection
        echo.
    )
) else (
    echo.
    echo You can push manually later using:
    echo   git push -u origin main
    echo.
)

pause

