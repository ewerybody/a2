@echo off
:: get name from filename without path and ext
set name=%~n0
echo ========= %name% =========

:: cut away the suffix "_build"
set name=%name:~0,-6%
set pypath=C:\Python27\Scripts
::set buildpath=%temp%
set buildpath=%~dp0

if not exist %name%.py (
    echo ERROR: "%name%.py" does not exist here!
    pause
    exit /b
)

%pypath%\pyinstaller.exe --onefile -y %~dp0%name%.py --distpath=%~dp0 --workpath=%buildpath% --specpath=%buildpath%
