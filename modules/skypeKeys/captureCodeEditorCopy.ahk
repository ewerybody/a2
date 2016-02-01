; skypeKeys - captureCodeEditorCopy.ahk
; author: eric
; created: 2015 7 27
; https://support.skype.com/en/faq/FA12139/sending-instant-messages-iphone
; "!! " at start for monospace formatting
; http://community.skype.com/t5/iOS-iPhone-and-iPad/Disable-Text-Changes-Bold-etc/td-p/3278672
; turn off wiki formatting:
; /setupkey *Lib/Conversation/EnableWiki 0

captureCodeEditorCopy() {
    global captureCodeEditorCopyFlag

	WinGet, thisID, ID, A
    WinGetTitle, thisTitle, ahk_id %thisID%
	WinGetClass, thisClass, ahk_id %thisID%
	WinGet, thisProcess, ProcessName, ahk_id %thisID%
    editors := {eclipse: {"class": "SWT_Window0", "title": "Eclipse"}, notepad: {"class": "Notepad++"}}
    
    For editor, data in editors {
        MsgBox editor: %editor%
        for attr, value in data
            if (attr == "class" && value != thisClass) {
                MsgBox thisClass: %thisClass% != %value%
                captureCodeEditorCopyFlag := 0
                break
            }
            else if (attr == "title" && InStr(thisTitle, value) == 0) {
                MsgBox thisTitle: %thisTitle% != %value%
                captureCodeEditorCopyFlag := 0
                break
            }
        captureCodeEditorCopyFlag := 1
    }
    
    MsgBox captureCodeEditorCopyFlag: %captureCodeEditorCopyFlag%
}
