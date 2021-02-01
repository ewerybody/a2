path := A_ScriptDir
batch_path := create_deleter_batch(A_ScriptDir)
x := FileExist(batch_path)
msg = A_ScriptDir:%A_ScriptDir%`npath: %path%`nbatch_path: %batch_path%`nx:%x%
log_info(A_ScriptName, msg, 0.5)
logmsg(" calling installer deleter...")

Run, %batch_path%
sleep, 100
ExitApp

Return, ;-----------------------------------------------------------------------
#Include, %A_ScriptDir%\..
#Include, a2_uninstaller.ahk
;@Ahk2Exe-SetMainIcon ..\..\..\ui\res\a2x.ico
