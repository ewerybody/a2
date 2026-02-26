#include %A_ScriptDir%\..\..\_a2dev_find_py.ahk
#include %A_ScriptDir%\..\..\a2_globals.ahk
#include <string>
#include <path>
#include <msgbox>

py_dir := path_dirname(a2dev_get_py())
if (!py_dir) {
    msgbox_error('Could not get "py_dir" from "path_dirname(a2dev_get_py())"')
    ExitApp
}

; Lists all compatible versions, preferred version top.
; Lets not use `FileGetVersion` on QtCore.dll since they skip the last bits.
; The whole version is in the shiboken-init script:
; files := ["PySide6\Qt6Core.dll", "PySide2\Qt5Core.dll"]
files := ["shiboken6\__init__.py", "shiboken2\__init__.py"]

for _, rel_path in files
{
    file_path := py_dir . "\Lib\site-packages\" . rel_path
    if (!FileExist(file_path))
        Continue

    FileObj := FileOpen(file_path, "r")
    version := FileObj.ReadLine()

    version_prefix := "__version__ = "
    if !string_startswith(version, version_prefix) {
        msgbox_error("Cannot get version from " rel_path "!`nExpected line: >" version_prefix "<`nFound: " version)
        ExitApp
    }

    version := SubStr(version, StrLen(version_prefix))
    version := string_strip(version, ' "')

    if version
        Break
}

if (!version) {
    msg := "Unable to find any of those:`n  "
    msg .= string_join(files, "`n  ") . "`n"
    msg .= "Make sure at least one is installed!"
    msgbox_error(msg, 'No PySide Found!')
} else
    FileAppend version, "*"
