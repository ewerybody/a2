@echo off

set AHKdir=..\AutoHotkey\
set Ahk2Exe=%AHKdir%Compiler\Ahk2Exe.exe
set AhkExe=%AHKdir%Autohotkey.exe
set this_path=%~dp0
set lib_path=%this_path%..
set a2path=%lib_path%\..
set script=%lib_path%\_source\a2_uninstaller.ahk
set executable=%a2path%\Uninstall a2.exe

echo Calling %Ahk2Exe%
echo    /in: %script%
echo   /out: %executable%
echo ...

"%Ahk2Exe%" /in "%script%" /out "%executable%" /compress 0 /ahk "%AhkExe%"
