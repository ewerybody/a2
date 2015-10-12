; CalculAid - calculAid.ahk
; author: eRiC
; created: 2015 10 10
;
; nice :/ on win10 although you call calc.exe the calculator process executable will be:
; "ApplicationFrameHost.exe" and the class: "ApplicationFrameWindow". Thanks MS! This can be
; ANYTHING!!! OK the title is still "Calculator" but only on an english system.
; So basically we need logic for all of that because nothing
; is for sure. Furthermore that also means that the Close-hetkeys we wanna setup in a2ui will need
; win-version and language specific scope identifyers. In the end such a function will be quite
; nice to have in a2 anyway.

calculAid_open() {
    sel := getSelection()
    RegExMatch(sel, "[0-9.,+/*=-]+", numbers)
    tt(numbers)
    
    Run, calc.exe,, UseErrorLevel, calcPID
}

test() {
    fsdsdfesf := true
    if fsdsdfesf
        MsgBox YES
    else
        MsgBox NO
}