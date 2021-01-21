@echo off
set here=%~dp0
echo here: %here%
set ahkbin=%here%..\..\AutoHotkey
set Ahk2Exe=%ahkbin%\Compiler\Ahk2Exe.exe
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
"%pypath%\python.exe" "%here%test_self_deleter.py"

@REM set this_path=%~dp0
@REM echo this_path: %this_path%
@REM set sourcedir=%this_path%
@REM set Ahk2Exe=%sourcedir%\..\AutoHotkey\Compiler\Ahk2Exe.exe
@REM set script=%this_path%\test_self_deleter.ahk
@REM set executable=%this_path%\test_self_deleter.exe
@REM set test_dir=%this_path%\_ self_deleter_test

@REM echo Ahk2Exe: %Ahk2Exe%

@REM if exist "%test_dir%" (
@REM     RMDIR /Q "%test_dir%"
@REM )
@REM MD "%test_dir%"

@REM echo creating executable %executable%...
@REM "%Ahk2Exe%" /in "%script%" /out "%executable%" /mpress 0

@REM echo copy executable to ...

@REM copy "%executable%" "%test_dir%\"
pause
