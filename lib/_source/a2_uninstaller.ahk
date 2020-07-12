; a2 uninstaller
; * remove Desktop link
; * remove autostart link
; * remove Start Menu links
; * shut down running a2 processes
; * ask user for user data deletion
; * delete things in a2 data dir
; * write uninstall deleter batch file
; * run uninstall deleter batch
; * exit

; complain_if_uncompiled()

A2DIR := get_a2dir()
batch_path := create_deleter_batch()
bx := FileExist(batch_path)

MsgBox, A2DIR: %A2DIR%`nbatch_path: %batch_path% - (%bx%)`nA_ScriptFullPath: %A_ScriptFullPath%
Run, %batch_path%
ExitApp

; --------------------------------------------------------
Return
#Include, _installib.ahk
#Include ..\Autohotkey\lib\path.ahk


create_deleter_batch() {
    batch_path := path_join(A_Temp, ["_ a2_uninstaller_deleter.bat"])
    If (A_IsCompiled)
        content := "DEL " . A_ScriptFullPath
    content .= "`nSLEEP 1`n"
    content = %content%(goto) 2>nul & del `"`%~f0`"
    FileDelete %batch_path%
    FileAppend, %content%, %batch_path%
    Return %batch_path%
}
