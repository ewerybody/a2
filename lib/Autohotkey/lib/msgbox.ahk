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
    MsgBox, 16, %title%, %msg%
}
