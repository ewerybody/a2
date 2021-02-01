rem Test batch script to run the self deleter on its own.
rem literally just finds local Autohotkey.exe,
rem runs ahk script to find latest Python.
rem runs python test script. I'm sorry :/ but it works.
@echo off
set here=%~dp0
echo here: %here%
set ahkbin=%here%..\..\AutoHotkey
set ahk_exe=%ahkbin%\Autohotkey.exe

rem getting latest python path
set tmp_txt=_ sfdgsdfgsdfgsdfg.txt
"%ahk_exe%" "%here%..\..\batches\versions\get_Python_path.ahk" > "%tmp_txt%"
set /p pypath= < "%tmp_txt%"
del "%tmp_txt%"
if not exist %pypath% (
  echo ERROR: Could not find Python package: %pypath%!
  pause
  exit
)
echo pypath: %pypath%

echo running py build script ...
"%pypath%\python.exe" "%here%_test_self_deleter.py"
pause
