@echo off

set a2path=%~dp0..\..\
echo a2path: %a2path%
set scriptpath=%a2path%ui\a2app.py
echo scriptpath: %scriptpath%
set pypath=C:\Python34\
set buildpath=%temp%
set distpath=%~dp0..\..\_ package
echo distpath: %distpath%

echo removing old package ...
rd "%distpath%" /Q /S

echo running pyinstaller ...
%pypath%Scripts\pyinstaller.exe --noconsole --noupx --onedir -y "%scriptpath%" --distpath="%distpath%" --workpath="%buildpath%" --specpath=%~dp0

echo running py build script ...
%pypath%python.exe build_py_package.py