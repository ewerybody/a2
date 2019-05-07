@echo off
set here=%~dp0
set a2path=%here%..\..\..
set iconpath=%a2path%\ui\res\a2.ico
set source_path=%a2path%\lib\_source
set distroot=%a2path%\_ package
set distpath=%distroot%\a2
set sfx=%distroot%\a2_installer.sfx.exe
set archive=%distroot%\archive.7z
set config=%distroot%\config.txt
set installerx=%distroot%\a2_installer.exe
set pypath=C:\Python37

echo ### building a2 installer packed executable ###
echo distroot: %distroot%

echo running build assistant script ...
%pypath%\python.exe %here%build_installer.py

echo finishing installer executable ...
copy /b "%sfx%" + "%config%" + "%archive%" "%installerx%"

echo ########### Build Installer Done! ###########
