rem This actually ONLY calls the Python installer builder!
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


rem getting latest python path
set ahk_exe=%here%..\..\Autohotkey\Autohotkey.exe
set tmp_txt=_ sfdgsdfgsdfgsdfg.txt

"%ahk_exe%" %here%..\versions\get_Python_path.ahk > "%tmp_txt%"
set /p pypath= < "%tmp_txt%"
del "%tmp_txt%"
echo pypath: %pypath%

echo ### building a2 installer packed executable ###
echo distroot: %distroot%

echo running build assistant script ...
%pypath%\python.exe %here%build_installer.py

echo ########### Build Installer Done! ###########
