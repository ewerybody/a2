@echo off

set here=%~dp0
set ahk_exe=%here%..\Autohotkey\Autohotkey.exe
set tmp_txt=_ sfdgsdfgsdfgsdfg.txt

"%ahk_exe%" versions\get_Python_path.ahk > "%tmp_txt%"
set /p python= < "%tmp_txt%"
del "%tmp_txt%"

echo python: %python%
pause
