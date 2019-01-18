@echo off

set a2path=%~dp0..\..
set iconpath=%a2path%\ui\res\a2.ico
set Ahk2Exe="C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe"
set source_path=%a2path%\lib\_source
set distroot=%a2path%\_ package
set distpath=%distroot%\a2

set sevenpath=%~dp0\7zr
set sevenx=%sevenpath%\7zr.exe
set sevensfx=%sevenpath%\7zSD.sfx
set archive=%distroot%\archive.7z
set config=%distroot%\config.txt
set installerx=%distroot%\a2_setup.exe

echo building installer script ...
%Ahk2Exe% /in "%source_path%\setup.ahk" /out "%distpath%\setup.exe" /icon %iconpath% /mpress 0

echo packing installer archive
"%sevenx%" a "%archive%" "%distpath%" -m0=BCJ2 -m1=LZMA:d25:fb255 -m2=LZMA:d19 -m3=LZMA:d19 -mb0:1 -mb0s1:2 -mb0s2:3 -mx

echo building installer executable ...
copy /b "%sevensfx%" + "%config%" + "%archive%" "%installerx%"

echo Done!
pause
