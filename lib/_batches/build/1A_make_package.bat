@echo off
set here=%~dp0
set a2path=%here%..\..\..
set source_path=%a2path%\lib\_source
set distroot=%a2path%\_ package
set distpath=%distroot%\a2

set ahkbin=%here%..\..\AutoHotkey
set Ahk2Exe=%ahkbin%\Compiler\Ahk2Exe.exe
set ahk_exe=%ahkbin%\Autohotkey.exe

if exist "%distpath%" (
  echo removing old package ...
  rd "%distpath%" /Q /S

  if exist "%distpath%" (
    echo ERROR: distpath: "%distpath%" could not be removed!
    pause
    exit
  )
)

rem getting latest python path
set tmp_txt=_ sfdgsdfgsdfgsdfg.txt
"%ahk_exe%" %here%..\versions\get_Python_path.ahk > "%tmp_txt%"
set /p pypath= < "%tmp_txt%"
del "%tmp_txt%"
echo pypath: %pypath%

md "%distpath%"

echo building root a2 executable ...
"%Ahk2Exe%" /in "%source_path%\a2_starter.ahk" /out "%distpath%\a2.exe" /compress 0 /ahk "%ahk_exe%"

echo building root a2ui executable ...
"%Ahk2Exe%" /in "%source_path%\a2ui_release.ahk" /out "%distpath%\a2ui.exe" /compress 0 /ahk "%ahk_exe%"

echo building root a2 Uninstaller executable ...
"%Ahk2Exe%" /in "%source_path%\a2_uninstaller.ahk" /out "%distpath%\Uninstall a2.exe" /compress 0 /ahk "%ahk_exe%"


echo running py build script ...
"%pypath%\python.exe" "%here%make_package.py"

echo ######## Make Package Done! ########
