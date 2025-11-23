#Include <WinClip>
#Include <WinClipAPI>

; Use the clipboard to get selected text.
; Basically stores current clipboard, fires Ctrl+C, gets variable
; from clipboard, restores clipboard and returns variable. Voila!
clipboard_get(clipWaitTime:=0.5) {
    ; wc := WinClip()
    ; wc.Copy(clipWaitTime)
    ; selection := wc.GetText()
    ; wc := 0
    ; return selection

    saved_clipboard := ClipboardAll()
    clipboard_empty()

    ; ; also watch for the process-executable instead of just window title:
    ; WinGetClass, Class, A
    ; WinGet, this_process, ProcessName, ahk_class %Class%

    ; Send{Blind}%resetModifiers%^c%restoreModifiers%
    ; if (this_process == "Photoshop.exe")
    ; {
    ;     SetKeyDelay, 20, 20
    ;     SendEvent, {Ctrl down}^c{Ctrl up}
    ; }
    ; Else If Class in PuTTY,ConsoleWindowClass,ytWindow
    ;     Send, {ENTER}
    ; Else
    Send("{Ctrl down}^c{Ctrl up}")

    If clipWaitTime
    {
        ClipWait(clipWaitTime)
    }
    Sleep(0)

    Selection := A_Clipboard
    A_Clipboard := saved_clipboard

    Return Selection
}


; Use the clipboard to paste given text.
clipboard_paste(input_string) {
    clipbackup := ClipboardAll()
    ; Set new data to clipboard
    A_Clipboard := input_string
    ; Send the default paste command
    Send('^v')
    ; Check repeatedly to see if the clipboard is still open
    Loop
        ; If more than 20 tries
        if (A_Index > 20)
            ; Stop trying and notify of failure
            return TrayTip(A_ThisFunc ' failed to restore clipboard contents.')
        ; Otherwise, wait another 100ms
        else Sleep(100)
    ; Stop when clipboard window isn't in use
    Until !DllCall('GetOpenClipboardWindow', 'Ptr')
    ; Restore original clipboard contents
    A_Clipboard := clipbackup

    ; wc := WinClip()
    ; wc.Paste(inputString)
    ; saved_clipboard := ClipboardAll()
    ; clipboard_empty()
    ; clip_now := A_Clipboard
    ; a2tip("A_Clipboard: " . clip_now . "`nsaved: " . saved_clipboard.)
    ; Sleep(400)
    ; A_Clipboard := input_string
    ; ClipWait(1)
    ; Send("{Ctrl down}{Insert}{Ctrl up}")

    ; Sleep(20)
    ; A_Clipboard := saved_clipboard
}

; Parse lines in clipboard, return list of existing file paths.
clipboard_get_files() {
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

; make sure the clipboard is empty
clipboard_empty() {
    Loop 10
    {
        if (A_Clipboard == "")
            return
        A_Clipboard := ""
        Sleep 20
    }
    msgbox_error("Could not empty the clipboard after 10 tries :/ (clipboard: '" . A_Clipboard . "'')")
}
