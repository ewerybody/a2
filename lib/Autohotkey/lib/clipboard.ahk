; Uses the clipboard to get selected things.
;
; Basically stores current clipboard, fires Ctrl+C, gets variable from clipboard,
; restores clipboard and returns variable.
clipboard_get(clipWaitTime=0.5)
{
    SavedClipboard := ClipboardAll
    Clipboard =
    Sleep, 0

    ; also watch for the process-executable instead of just window title:
    WinGetClass, Class, A
    WinGet, this_process, ProcessName, ahk_class %Class%

    ; sending keystroke Ctrl+C in maya can cause a "scene clipboard save" which can be heavy
    ; to avoid this we go sure we are in the text editor window of maya
    if (this_process == "maya.exe")
    {
        WinGetTitle, this_title, A
        if (this_title != "Script Editor")
            Return ""
    }

    ;Send, {Blind}%resetModifiers%^c%restoreModifiers%
    if (this_process == "Photoshop.exe")
    {
        SetKeyDelay, 20, 20
        SendEvent, {Ctrl down}^c{Ctrl up}
    }
    Else If Class in PuTTY,ConsoleWindowClass,ytWindow
        Send, {ENTER}
    Else
        Send, {Ctrl down}^c{Ctrl up}

    If clipWaitTime <>
    {
        If copyAsText = 0
            ClipWait, %clipWaitTime%, 1
        Else
            ClipWait, %clipWaitTime%
    }
    Sleep,0

    Selection := Clipboard
    Clipboard := SavedClipboard

    Return Selection
}

; Uses the clipboard to paste given text.
clipboard_paste( byref inputString, sleepTime=50 ){
    SavedClipboard := ClipboardAll
    Clipboard =
    Sleep, %sleepTime%
    Clipboard := inputString
    ClipWait, 1
    Send, {Ctrl down}^v{Ctrl up}
    Clipboard := SavedClipboard
}


; Parses lines in clipboard, returns list of found existing file paths
clipboard_get_files() {
    files := []
    lines := StrSplit(Clipboard, "`r`n")
    for i, line in lines
        if FileExist(line)
            files.push(line)

    if (files.length())
        return files
}
