@ECHO OFF
SETLOCAL DisableDelayedExpansion

IF "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    SET "builtin_python_path=python-3.6.0-embed-amd64"
) ELSE (
    IF "%PROCESSOR_ARCHITEW6432%"=="AMD64" (
        SET "builtin_python_path=python-3.6.0-embed-amd64"
    ) ELSE (
        SET "builtin_python_path=python-3.6.0-embed-win32"
    )
)

SET "mypath=%~dp0"

IF EXIST "%mypath%%builtin_python_path%\python.exe" (
    "%mypath%%builtin_python_path%\python.exe" "%mypath%start.py"
) ELSE (
    py -3.6 -V >nul 2>&1

    IF %errorlevel% equ 0 (
        echo "Found Python 3.6"
        py -3.6 "%mypath%start.py"
    ) ELSE (
        echo "Found Python 3+"
        py -3 "%mypath%start.py"
    )
)

echo Press any key to exit...
pause >nul

ENDLOCAL
