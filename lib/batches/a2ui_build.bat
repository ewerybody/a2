set Ahk2Exe="C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe"
set this_path=%~dp0
set lib_path=%this_path%..
set a2path=%lib_path%\..
set script=%lib_path%\a2ui.ahk
set executable=%a2path%\a2ui.exe
set icon=%a2path%\ui\res\a2.ico

cd %lib_path%

%Ahk2Exe% /in "%script%" /out "%executable%" /icon %icon% /mpress 1

cd %this_path%