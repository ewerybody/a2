@echo off

set Ahk2Exe="C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe"
set this_path=%~dp0
set lib_path=%this_path%..
set a2path=%lib_path%\..
set script=%lib_path%\_source\a2_uninstaller.ahk
set executable=%a2path%\Uninstall a2.exe
set icon=%a2path%\ui\res\a2x.ico

echo Calling %Ahk2Exe%
echo    /in: %script%
echo   /out: %executable%
echo  /icon: %icon%\n
echo ...

%Ahk2Exe% /in "%script%" /out "%executable%" /icon %icon% /mpress 0
