; Use the clipboard to get selected text.
; Basically stores current clipboard, fires Ctrl+C, gets variable
; from clipboard, restores clipboard and returns variable. Voila!
clipboard_get(clipWaitTime:=0.5) {
        backup := ClipboardAll()
        A_Clipboard := ''
        Send('^c')

        ClipWait(clipWaitTime, clipWaitTime)
        ; if !ClipWait(clipWaitTime, clipWaitTime) {
        ;     return (A_Clipboard := backup)
        ; }

        txt := A_Clipboard
        A_Clipboard := backup
        return txt
}


; Use the clipboard to paste given text.
clipboard_paste(input_string) {
    clip_backup := ClipboardAll()
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
    A_Clipboard := clip_backup
}

clipboard_paste_and_select(input_string) {
    clipboard_paste(input_string)
    Send("+{Left " StrLen(input_string) "}")
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
