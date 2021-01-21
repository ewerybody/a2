@echo off
set Ahk2Exe="C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe"
set this_path=%~dp0..\
set script=%this_path%a2_uninstaller.ahk
set executable=%this_path%Uninstall a2.exe
set a2path=%this_path%..\..\
set icon=%a2path%ui\res\a2x.ico

set a2data=%LOCALAPPDATA%\a2
echo a2data: %a2data%

set a2backup=%a2data% - Backup
if not exist "%a2backup%" (
    echo creating backup ... %a2backup%
    pause
    ROBOCOPY "%a2data%" "%a2backup%" /E
)
if not exist "%a2data%" (
    echo restoring ... %a2data%
    REM ROBOCOPY "%a2backup%" "%a2data%" /E /NFL /NDL
    ROBOCOPY "%a2backup%" "%a2data%" /E > nul
    REM XCOPY "%a2backup%\*" "%a2data%\*" /E
)
echo creating executable %executable%...
%Ahk2Exe% /in "%script%" /out "%executable%" /mpress 0
echo copy executable to a2data ...
copy "%executable%" "%a2data%"
pause
