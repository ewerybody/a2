#include %A_ScriptDir%\..\..\_a2dev_find_py.ahk
pydir := path_dirname(a2dev_get_py())
if (!pydir) {
    MsgBox 16, Could not get "pydir" from "path_dirname(a2dev_get_py())"
    ExitApp
}

; Lists all compatible versions, prefered verison top.
; Lets not use `FileGetVersion` on QtCore.dll since they skip the last bits.
; The whole version is in the shiboken-init script:
; files := ["PySide6\Qt6Core.dll", "PySide2\Qt5Core.dll"]
files := ["shiboken6\__init__.py", "shiboken2\__init__.py"]

for _, rel_path in files
{
    file_path := pydir . "\Lib\site-packages\" . rel_path
    if (!FileExist(file_path))
        Continue

    version := FileReadLine(file_path, 1)
    version_prefix := "__version__ = "
    if !string_startswith(version, version_prefix) {
        msgbox_error("Cannot get version from " rel_path "!`nExpected line: >" version_prefix "<`nFound: " version)
        ExitApp
    }

    version := SubStr(version, StringLen(version_prefix))
    version := string_trim(version, " """)

    if version
        Break
}

if (!version) {
    msg := "Unable to find any of those:`n  "
    msg .= string_join(files, "`n  ") . "`n"
    msg .= "Make sure at least one is installed!"
    MsgBox, 16, No PySide Found!, %msg%
} else
    FileAppend, %version%, *
