@echo off

set package_name=a2 - alpha preview 0.1
set a2path=%~dp0..\..
set scriptpath=%a2path%\ui\a2app.py
set iconpath=%a2path%\ui\res\a2.ico
set pypath=C:\Python37\
set pyinstaller=%pypath%Scripts\pyinstaller.exe
set buildpath=%temp%\a2_temp_buildpath
set distpath=%a2path%\_ package

echo ### building a2 package "%package_name%" ###
echo distpath: %distpath%
echo ...


if not exist %pypath% (
  echo ERROR: Could not find Python37 package: %pypath%!
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

if exist "%distpath%" (
  echo removing old package ...
  rd "%distpath%" /Q /S
  
  if exist "%distpath%" (
    echo ERROR: distpath: "%distpath%" could not be removed!
    pause
    exit
  )
)

echo running pyinstaller ...
"%pyinstaller%" --noconsole --noupx --onedir -y "%scriptpath%" --distpath="%distpath%" --workpath="%buildpath%" --specpath=%~dp0 --icon "%iconpath%"

echo running py build script ...
%pypath%python.exe %~dp0build_py_package.py "%package_name%"

echo Done!
pause
