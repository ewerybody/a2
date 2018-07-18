; good ol getSelection function from ac'tivAid
; copyOnly=1 to actually fill the clipboard
aagetSelection( copyAsText=1, copyOnly=0, clipWaitTime=0.5 )
{
    global Selection, SavedClipboard, NoOnClipboardChange
    NoOnClipboardChange = 1

    ; also watch for the process-executable instead of just window title:
    WinGetClass, Class, A
    WinGet, this_process, ProcessName, ahk_class %Class%

    ; sending keystroke Ctrl+C in maya can cause a "scene clipboard save" which can be heavy
    ; to avoid this we go sure we are in the text editor window of maya
    if (this_process == "maya.exe")
    {
        WinGetTitle, this_title, A
        if (this_title != "Script Editor")
        {
            Selection := ""
            Return
        }
    }

    if (this_process == "Photoshop.exe")
    {
        SetKeyDelay, 20, 20
        SendEvent, {Ctrl down}^c{Ctrl up}
    }
    Else If Class in PuTTY,ConsoleWindowClass,ytWindow
        Send, {ENTER}
    Else
        Send, {Ctrl down}^c{Ctrl up}

    if (this_process == "Photoshop.exe")
    {
        Gui, 99:+ToolWindow
        Gui, 99:Show, x-1000 y-1000 w10 h10
    }

    If clipWaitTime <>
    {
        If copyAsText = 0
            ClipWait, %clipWaitTime%, 1
        Else
            ClipWait, %clipWaitTime%
    }
    Sleep, 0

    if (this_process == "Photoshop.exe")
    {
        Sleep,10
        Gui, 99:Destroy
    }

    If copyAsText = 1
        Selection := Clipboard
    ;Else If copyAsText in Unicode,UTF8,UTF-8
    ;{
    ;   Transform, Selection, Unicode
    ;   ;msgbox, % Ansi2UTF8(UTF82Ansi(Selection)) "`n" Selection
    ;   If (Ansi2UTF8(UTF82Ansi(Selection)) = Selection)
    ;       Selection := Clipboard
    ;}
    Else
        Selection := ClipboardAll

    If copyOnly = 0
    {
        Sleep, 20
        Clipboard := SavedClipboard
    }
    Sleep,0

    NoOnClipboardChange =

    If copyAsText = 1
        Return Selection
}


; to remove whitespace from strings start + end
; strtrim(string)
; {
;     start := 1
;     stringLen, end, string
;     loop, %end% ; fix the start
;     {
;         l := SubStr(string, A_Index, 1)
;         if (l != A_Space && l != A_Tab && l != "`n" && l != "`r")
;         {
;             start := A_Index
;             break
;         }
;     }
;     string := SubStr(string, start)
;     stringLen, end, string
;     loop, %end% ; fix the end
;     {
;         i := - A_Index + 1
;         l := SubStr(string, i, 1)
;         if (l != A_Space && l != A_Tab && l != "`n" && l != "`r")
;         {
;             end := A_Index - 1
;             break
;         }
;     }
;     StringTrimRight, string, string, %end%
;     return string
; }

is_whitespace(byref string) {
    if (string == A_Space OR string == A_Tab OR string == "`n" OR string == "`r")
        return true
    else
        return false
}

; Determines if a string starts with another string.
; NOTE: It's a bit faster to simply use InStr(string, startstr) = 1
strStartsWith(byref string, byref startstr)
{
    return InStr(string, startstr) = 1
}

; Determines if a string ends with another string
strEndsWith(byref string, byref end)
{
    return strlen(end) <= strlen(string) && Substr(string, -strlen(end) + 1) = end
}

strTrim(byref string, byref trim)
{
    return strTrimLeft(strTrimRight(string, trim), trim)
}

; Removes all occurences of trim at the beginning of string
; trim can be an array of strings that should be removed.
strTrimLeft(string, trim)
{
    if (!IsObject(trim))
        trim := [trim]
    for index, trimString in trim
    {
        len := strLen(trimString)
        while(InStr(string, trimString) = 1)
            StringTrimLeft, string, string, %len%
    }
    return string
}

; Removes all occurences of trim at the end of string
; trim can be an array of strings that should be removed.
strTrimRight(string, trim)
{
    if (!IsObject(trim))
        trim := [trim]
    for index, trimString in trim
    {
        len := strLen(trimString)
        while(strEndsWith(string, trimString))
            StringTrimRight, string, string, %len%
    }
    return string
}


; WIP: Which version do you like more?!?!
; strips whitespace from start and end of a string:
strip(byref inputString)
{
    ; if first char is space, tab or linefeed, remove it and look again:
    c := SubStr(inputString, 1, 1)
    if (c == A_Space OR c == A_Tab OR c == "`n" OR c == "`r")
    {
        StringTrimLeft, inputString, inputString, 1
        strip(inputString)
    }
    ; now last character:
    c := SubStr(inputString, 0)
    if (c == A_Space OR c == A_Tab OR c == "`n" OR c == "`r")
    {
        StringTrimRight, inputString, inputString, 1
        strip(inputString)
    }
    
    return inputString
}

; Remove quotes from a string if necessary
UnQuote(string)
{
    if (InStr(string, """") = 1 && strEndsWith(string, """"))
        return strTrim(string, """")
    return string
}

; Add quotes to a string only if necessary
Quote(string, once = 1)
{
    if (once)
    {
        if (InStr(string, """") != 1)
            string := """" string
        if (!strEndsWith(string, """"))
            string := string """"
        return string
    }
    return """" string """"
}
