@echo off
set here=%~dp0
set a2path=%here%..\..\..
set scriptpath=%a2path%\ui\a2app.py
set iconpath=%a2path%\ui\res\a2.ico
set buildpath=%temp%\a2_temp_buildpath
set distpath=%a2path%\_ package\a2

rem getting latest python path
set ahk_exe=%here%..\..\Autohotkey\Autohotkey.exe
set tmp_txt=_ sfdgsdfgsdfgsdfg.txt

"%ahk_exe%" %here%..\versions\get_Python_path.ahk > "%tmp_txt%"
set /p pypath= < "%tmp_txt%"
del "%tmp_txt%"

echo pypath: %pypath%
set pyinstaller=%pypath%\Scripts\pyinstaller.exe


echo ### building a2 package ###
echo distpath: %distpath%
echo ...


if not exist %pypath% (
  echo ERROR: Could not find Python package: %pypath%!
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
rem "%pyinstaller%" --noupx --onedir -y "%scriptpath%" --distpath="%distpath%" --workpath="%buildpath%" --specpath=%here% --icon "%iconpath%"
"%pyinstaller%" --noconsole --noupx --onedir -y "%scriptpath%" --distpath="%distpath%" --workpath="%buildpath%" --specpath=%here% --icon "%iconpath%"

echo ######## Build Py Package Done! ########
