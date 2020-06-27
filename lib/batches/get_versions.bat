@echo off

set here=%~dp0
set ahk_exe=%here%..\Autohotkey\Autohotkey.exe
set tmp_txt=_ sfdgsdfgsdfgsdfg.txt

rem get the version of our Autohotkey.exe
"%ahk_exe%" ..\cmds\get_AutoHotkey_version.ahk > "%tmp_txt%"
set /p ahk_version= < "%tmp_txt%"
del "%tmp_txt%"

echo ahk_version: %ahk_version%

"%ahk_exe%" versions\get_Python_version.ahk > "%tmp_txt%"
set /p python= < "%tmp_txt%"
del "%tmp_txt%"

echo python: %python%

"%ahk_exe%" versions\get_PySide2_version.ahk > "%tmp_txt%"
set /p pyside_version= < "%tmp_txt%"
del "%tmp_txt%"

echo pyside_version: %pyside_version%

pause
