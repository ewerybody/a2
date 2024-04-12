; msgbox library to have plaintext access to the different icons, combinations,
; buttons and eventually styles. WIP...
; 0 - OK
; 1 - OK/Cancel
; 16 - Hand (stop/error)
; 32 - Question
; 48 - Exclamation
; 64 - Info
; ... who wants to remember these!?!

msgbox_error(msg, title := "ERROR") {
    MsgBox(msg, title, 16) ; Iconx
}

msgbox_info(msg, title := "INFO") {
    MsgBox(msg, title, 64) ; Iconi
}

msgbox_yesnocancel(msg, title) {
    return MsgBox(msg, title, 19)
}

msgbox_accepted(msg, title) {
    result := msgbox(msg, title, 33)
    return result == "OK"
}