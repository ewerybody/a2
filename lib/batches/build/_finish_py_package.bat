@echo off
set here=%~dp0
set a2path=%here%..\..\..
set source_path=%a2path%\lib\_source
set distroot=%a2path%\_ package
set distpath=%distroot%\a2
set Ahk2Exe="C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe"
set iconpath=%a2path%\ui\res\a2.ico

rem getting latest python path
set ahk_exe=%here%..\..\Autohotkey\Autohotkey.exe
set tmp_txt=_ sfdgsdfgsdfgsdfg.txt
"%ahk_exe%" %here%..\versions\get_Python_path.ahk > "%tmp_txt%"
set /p pypath= < "%tmp_txt%"
del "%tmp_txt%"
echo pypath: %pypath%

echo running py build script ...
%pypath%\python.exe %here%finish_package.py

echo building root a2ui executable ...
%Ahk2Exe% /in "%source_path%\a2ui_starter.ahk" /out "%distpath%\a2ui.exe" /icon %iconpath% /mpress 0

echo building root a2 executable ...
%Ahk2Exe% /in "%source_path%\a2_starter.ahk" /out "%distpath%\a2.exe" /icon %iconpath% /mpress 0

echo ######## Finish Py Package Done! ########
