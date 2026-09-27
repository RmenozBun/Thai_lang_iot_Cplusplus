@echo off
cd /d "%~dp0"

REM --------------------------
REM FIX PATH (สำคัญมากสำหรับ Win11)
REM --------------------------
set PATH=%~dp0mingw64\bin;%PATH%

REM (เผื่อใช้ python ในโฟลเดอร์)
set PATH=%~dp0python;%PATH%

REM (สำหรับ Arduino CLI data แบบ portable)
set ARDUINO_DATA_DIR=%~dp0arduino-cli\data

echo === Step 1: Compile Thai ===
.\python\python.exe compiler.py program.thai

echo === Step 2: Detect Mode ===

for /f %%a in ('python -c "f=open('program.thai',encoding='utf-8');print(f.readline().split()[1])"') do set MODE=%%a

echo MODE = %MODE%

echo === Step 3 ===

if /i "%MODE%"=="arduino" (
    echo Arduino Mode

    REM --------------------------
    REM Compile Arduino
    REM --------------------------
    arduino-cli\arduino-cli.exe compile --fqbn arduino:avr:uno output

    REM --------------------------
    REM Upload (ต้องมีบอร์ด)
    REM --------------------------
    arduino-cli\arduino-cli.exe upload -p COM3 --fqbn arduino:avr:uno output

) else (
    echo C++ Mode

    REM --------------------------
    REM Compile C++
    REM --------------------------
    mingw64\bin\g++.exe output.cpp -o program.exe -finput-charset=UTF-8 -fexec-charset=UTF-8

    echo Run Program
    program.exe
)

pause