@echo off
set PYTHON_EXE="C:\Program Files\Python312\python.exe"
set SCRIPT_PATH="C:\Scripts\compress_video\compress_video.py"

echo Running video compression for: %1
%PYTHON_EXE% %SCRIPT_PATH% %1
echo.
echo Compression complete.
pause > nul