@echo off
set PYTHON_EXE="C:\Program Files\Python312\python.exe"
set SCRIPT_PATH="C:\Scripts\compress_video\extract_audio.py"

echo Running video trim for: %1
%PYTHON_EXE% %SCRIPT_PATH% %1
echo.
echo Audio extraction complete.
pause > nul