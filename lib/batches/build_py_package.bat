@echo off

set a2path=%~dp0..\..\
set scriptpath=%a2path%ui\a2app.py
set pypath=C:\Python34\
set pyinstaller=%pypath%Scripts\pyinstaller.exe
set buildpath=%temp%\a2_temp_buildpath
set distpath=%~dp0..\..\_ package

if not exist %pypath% (
  echo ERROR: Could not find Python34 package: %pypath%!
  pause
  exit
)

if not exist %pyinstaller% (
  echo ERROR: PyInstaller not found! Install it via `pip install PyInstaller`.
  pause
  exit
)

if not exist %buildpath% (
    echo "buildpath" not in temp yet!
    echo    This may take a minute or two ...
)

echo removing old package ...
rd "%distpath%" /Q /S

echo running pyinstaller ...
"%pyinstaller%" --noconsole --noupx --onedir -y "%scriptpath%" --distpath="%distpath%" --workpath="%buildpath%" --specpath=%~dp0

echo running py build script ...
%pypath%python.exe build_py_package.py

echo Done!
pause
