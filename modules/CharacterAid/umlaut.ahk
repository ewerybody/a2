charAid_umlaut() {
    ; trying to avoid modifier key to trigger while listening to Input
    Hotkey, # UP, charAid_umlaut_dummy
    tt("umlaut...")
    Input, thiskey, L1, {LControl}{RControl}{LAlt}{RAlt}{LWin}{RWin}{AppsKey}{F1}{F2}{F3}{F4}{F5}{F6}{F7}{F8}{F9}{F10}{F11}{F12}{Left}{Right}{Up}{Down}{Home}{End}{PgUp}{PgDn}{Del}{Ins}{BS}{Capslock}{Numlock}{PrintScreen}{Pause}
    Hotkey, # UP, Off
    
    letters := ["o", "O", "a", "A", "u", "U", "e", "E", "s"]
    umlauts := ["ö", "Ö", "ä", "Ä", "ü", "Ü", "ë", "Ë", "ß"]
    idx := inArray(thiskey, letters)
    if (idx != 0) {
        umlaut := umlauts[idx]
        Send, %umlaut%
        tt("Sending " umlaut, 0.5)
    }
    else
        tt("...", 0.6)
}

charAid_umlaut_dummy:
Return