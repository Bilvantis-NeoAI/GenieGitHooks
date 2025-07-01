@echo off
REM Genie GitHooks - Post-commit Hook (Windows Batch Wrapper)
REM This allows Windows GUI tools (VSCode, GitHub Desktop) to execute the hook

REM Find Python executable
where python.exe >nul 2>&1
if %errorlevel% == 0 (
    set python_cmd=python.exe
    goto :run_hook
)

where python3.exe >nul 2>&1
if %errorlevel% == 0 (
    set python_cmd=python3.exe
    goto :run_hook
)

where py.exe >nul 2>&1
if %errorlevel% == 0 (
    set python_cmd=py.exe
    goto :run_hook
)

echo WARNING: Python 3 not found. Post-commit hook will be skipped.
exit /b 0

:run_hook
REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Execute the Python post-commit script
"%python_cmd%" "%SCRIPT_DIR%post-commit.py" %* 