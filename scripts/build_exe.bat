@echo off
REM Construit dist\quiz_revision.exe (Windows) avec quiz\questions embarqué.
REM Usage : scripts\build_exe.bat
setlocal
cd /d "%~dp0\.."
if "%PYTHON%"=="" set "PYTHON=python"

REM Séparateur de --add-data : ';' sur Windows (':' sur macOS/Linux).
"%PYTHON%" -m PyInstaller --noconfirm --clean --onefile --name quiz_revision --add-data "quiz\questions;questions" quiz\quiz_app.py
if errorlevel 1 (
    echo ECHEC du build.
    exit /b 1
)

echo Build OK : dist\quiz_revision.exe
endlocal
