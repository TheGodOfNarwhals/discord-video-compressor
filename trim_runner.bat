@echo off
set PYTHON_EXE="C:\Program Files\Python312\python.exe"
set SCRIPT_PATH="C:\Scripts\compress_video\trim_video.py"

echo Running video trim for: %1
%PYTHON_EXE% %SCRIPT_PATH% %1
echo.
echo Compression complete.
pause > nul