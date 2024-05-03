#Include <WinClip>
#Include <WinClipAPI>


clipboard_get(clipWaitTime:=0.5) {
    ; Use the clipboard to get selected text.
    ;
    ; Basically stores current clipboard, fires Ctrl+C, gets variable
    ; from clipboard, restores clipboard and returns variable. Voila!

    wc := WinClip()
    wc.Copy(clipWaitTime)
    selection := wc.GetText()
    wc := 0
    return selection

    ; SavedClipboard := ClipboardAll
    ; clipboard_empty()
    ; Sleep, 0

    ; ; also watch for the process-executable instead of just window title:
    ; WinGetClass, Class, A
    ; WinGet, this_process, ProcessName, ahk_class %Class%

    ; ; Sending `Ctrl+C` in Maya may cause a "scene clipboard save" which can be heavy!
    ; ; To avoid this we make sure we're not on the main window of Maya.
    ; if (this_process == "maya.exe")
    ; {
    ;     WinGetTitle, this_title, A
    ;     if (string_startswith(this_title, "Autodesk Maya "))
    ;         Return ""
    ; }

    ; ;Send, {Blind}%resetModifiers%^c%restoreModifiers%
    ; if (this_process == "Photoshop.exe")
    ; {
    ;     SetKeyDelay, 20, 20
    ;     SendEvent, {Ctrl down}^c{Ctrl up}
    ; }
    ; Else If Class in PuTTY,ConsoleWindowClass,ytWindow
    ;     Send, {ENTER}
    ; Else
    ;     Send, {Ctrl down}^c{Ctrl up}

    ; If clipWaitTime <>
    ; {
    ;     If copyAsText = 0
    ;         ClipWait, %clipWaitTime%, 1
    ;     Else
    ;         ClipWait, %clipWaitTime%
    ; }
    ; Sleep,0

    ; Selection := Clipboard
    ; Clipboard := SavedClipboard

    ; Return Selection
}

clipboard_paste( inputString, sleepTime:=50 ) {
    wc := WinClip()
    wc.Paste(inputString)
    ; Use the clipboard to paste given text.
    ; SavedClipboard := ClipboardAll
    ; clipboard_empty()
    ; Clipboard := inputString
    ; ClipWait, 1
    ; Send, {Ctrl down}^v{Ctrl up}
    ; Sleep, 20
    ; Clipboard := SavedClipboard
}

clipboard_get_files() {
    ; Parse lines in clipboard, return list of existing file paths.
    files := []
    for i, line in StrSplit(A_Clipboard, "`r`n")
    {
        if string_startswith(line, "//")
            continue
        if FileExist(line)
            files.push(line)
    }
    if (files.length)
        return files
}

clipboard_empty() {
    ; make sure the clipboard is empty
    Loop 10
    {
        if (A_Clipboard == "")
            return
        A_Clipboard := ""
        Sleep 20
    }
    msgbox_error("Could not empty the clipboard after 10 tries :/ (clipboard: '" . A_Clipboard . "'')")
}
