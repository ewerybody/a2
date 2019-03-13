@echo off

set a2path=%~dp0..\..
set iconpath=%a2path%\ui\res\a2.ico
set Ahk2Exe=C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe
set source_path=%a2path%\lib\_source
set distroot=%a2path%\_ package
set distpath=%distroot%\a2

set sevenpath=%source_path%\7zr
set sevenx=%sevenpath%\7zr.exe
set srcsfx=%source_path%\a2_installer.sfx.exe
set sfx=%distroot%\a2_installer.sfx.exe
set archive=%distroot%\archive.7z
set config=%distroot%\config.txt
set installerx=%distroot%\a2_installer.exe
set mtx=C:\Program Files (x86)\Windows Kits\8.1\bin\x86\mt.exe
set manifest=%distroot%\a2_installer_manifest.xml


echo ### building a2 installer packed executable ###
echo distroot: %distroot%

if not exist "%Ahk2Exe%" (
  echo Could not find Ahk2Exe.exe! [at: %Ahk2Exe%]
  pause
  exit
)

echo copying fresh sfx-file ...
copy "%srcsfx%" "%sfx%" 

if exist "%mtx%" (
  echo Adding new manifest %manifest% ...
  "%mtx%" -nologo -manifest "%manifest%" -outputresource:"%sfx%"
)

echo building installer script executable...
"%Ahk2Exe%" /in "%source_path%\a2_installer.ahk" /out "%distpath%\setup.exe" /icon %iconpath% /mpress 0

echo packing installer archive ...
"%sevenx%" a "%archive%" "%distpath%" -m0=BCJ2 -m1=LZMA:d25:fb255 -m2=LZMA:d19 -m3=LZMA:d19 -mb0:1 -mb0s1:2 -mb0s2:3 -mx

echo building installer executable ...
copy /b "%sfx%" + "%config%" + "%archive%" "%installerx%"

echo Build Installer Done!
