rem This actually ONLY calls the Python installer builder!
@echo off
set here=%~dp0
set a2path=%here%..\..\..
set distroot=%a2path%\_ package

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
