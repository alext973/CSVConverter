@echo off
REM Warte, bis main.exe beendet ist
:loop
tasklist | find /I "main.exe" >nul
if not errorlevel 1 (
    timeout /t 1 >nul
    goto loop
)
REM Ersetze main.exe durch main_new.exe
move /Y main_new.exe main.exe
REM Starte die neue main.exe
start "" main.exe
exit