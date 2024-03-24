@ECHO OFF
IF "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    REM Running under 64-bit CMD.EXE on 64-bit Windows...
    SET builtin_python_path="python-3.6.0-embed-amd64"
) ELSE (
    IF "%PROCESSOR_ARCHITECTURE%"=="x86" IF "%PROCESSOR_ARCHITEW6432%"=="AMD64" (
        REM Running under 32-bit CMD.EXE on 64-bit Windows...
        SET builtin_python_path="python-3.6.0-embed-amd64"
    ) ELSE (
        REM Running under 32-bit CMD.EXE on 32-bit Windows...
        SET builtin_python_path="python-3.6.0-embed-win32"
    )
)





SET mypath=%~dp0








IF Exist "%mypath%\%builtin_python_path%\python.exe" (
  "%mypath%\%builtin_python_path%\python.exe" "%mypath%\start.py"
) else (
  
  
  
	py -3.6 -V

	if %errorlevel% equ 0 (
	  py -3.6 "%mypath%\start.py"
	) else (
	  py -3 "%mypath%\start.py"
	)  
  
  
  
  
)











echo Press any key to exit...



pause >nul