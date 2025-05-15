@echo off

set here=%~dp0
set AHKdir=..\AutoHotkey\
set Ahk2Exe=%AHKdir%Compiler\Ahk2Exe.exe
set AhkExe=%AHKdir%AutoHotkey.exe
set lib_path=%here%..\
set a2path=%lib_path%..\
set script=%lib_path%_source\a2_uninstaller.ahk
set executable=%a2path%Uninstall a2.exe
set icon_path=%a2path%ui\res\a2x.ico

echo Calling %Ahk2Exe%
echo    /in: %script%
echo   /out: %executable%
echo ...

"%Ahk2Exe%" /in "%script%" /out "%executable%" /compress 0 /ahk "%AhkExe%" /icon "%icon_path%"
