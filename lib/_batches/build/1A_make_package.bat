rem Kick off a2 package creation
@echo off
set here=%~dp0
echo here: %here%
set py_path=%here%..\..\..\.venv\Scripts
echo py_path: %py_path%
echo running py build script ...
"%py_path%\python.exe" "%here%make_package.py"