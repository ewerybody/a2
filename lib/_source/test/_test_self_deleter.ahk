#Warn Unreachable, Off
path := A_ScriptDir
batch_path := create_deleter_batch(A_ScriptDir)
logmsg(A_ScriptName "`n  A_ScriptDir: " A_ScriptDir "`n  path: " path "`n  batch_path: " batch_path "`n  FileExist: " FileExist(batch_path))
logmsg(" Calling installer deleter...")

Run(batch_path)
Sleep(100)
ExitApp

Return ;-----------------------------------------------------------------------
#Include %A_ScriptDir%\..
#Include a2_uninstaller.ahk
;@Ahk2Exe-SetMainIcon ..\..\..\ui\res\a2x.ico
