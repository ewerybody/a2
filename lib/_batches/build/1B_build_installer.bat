rem Kick off calling the installer builder (Python).
@echo off
set here=%~dp0
set py_path=%here%..\..\..\.venv\Scripts
echo py_path: %py_path%

echo running build assistant script ...
%py_path%\python.exe %here%build_installer.py

echo ########### Build Installer Done! ###########
