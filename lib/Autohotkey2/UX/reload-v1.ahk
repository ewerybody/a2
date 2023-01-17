; This file is part of a trick for allowing a v2 script to relaunch itself with
; v2 when the user attempts to execute it with v1.  See inc\bounce-v1.ahk.

#NoTrayIcon

if (A_ScriptFullPath = A_LineFile)
{
    MsgBox 16,, This script is not meant to be executed.
    ExitApp 2
}

if (!A_Args.Length())
{
    Loop Files, %A_ScriptDir%\..\AutoHotkey32.exe, FR
    {
        Run "%A_LoopFileLongPath%" /force "%A_ScriptFullPath%"
        ExitApp
    }
}

MsgBox 16,, This script requires AutoHotkey v2, but was launched with v1.
ExitApp 2