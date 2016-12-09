; a2 - modular Autohotkey script envirionment
; main file! This basically gathers all resources
#SingleInstance Off
#Persistent
#NoTrayIcon
#MaxHotkeysPerInterval 1000 ;Required for mouse wheel
#NoEnv ;Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input ;Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%\.. ;Ensures a consistent starting directory.
DetectHiddenWindows, On
OnExit("ReleaseInstance")

; Depending on the command line parameters supplied, this instance might send event triggers to another instance which is already running.
ProcessCommandLineParameters() ;Possible exit point

FileCreateDir %A_Temp%\a2
; Hwnd.txt is written to allow other processes to find the main window of a2
FileDelete, %A_Temp%\a2\hwnd.txt
FileAppend, %A_ScriptHwnd%, %A_Temp%\a2\hwnd.txt

#include settings\a2_settings.ahk
#include lib\Globals.ahk
#include lib\InstanceHandler.ahk
#include lib\_defaults\a2_urls.ahk

Menu, Tray, Icon, %UIresources%\a2.ico, , 1
Menu, Tray, Icon
Gui, 1:Destroy

Menu, Tray, NoStandard
Menu, Tray, DeleteAll
Menu, Tray, Tip, %a2_title%
Menu, Tray, Click, %a2_tray_click_button% ;makes the menu act on standard "left" click
Menu, Tray, add, open a2 user interface, a2ui
Menu, Tray, icon, open a2 user interface, %UIresources%\a2.ico
Menu, Tray, default, open a2 user interface
Menu, Tray, add, reload a2, a2ui_reload
Menu, Tray, icon, reload a2, %UIresources%\a2reload.ico
Menu, Tray, add, help on a2, a2ui_help
Menu, Tray, icon, help on a2, %UIresources%\a2help.ico
Menu, Tray, add, quit a2, a2ui_exit
Menu, Tray, icon, quit a2, %UIresources%\a2x.ico

if a2_startup_tool_tips
    tt(a2_title, 1)

; Setup the message handler for receiving triggers from other instances of 7plus (and possibly other programs) and from the Shell extension.
OnMessage(55555, "TriggerFromOtherInstance")
; Make sure that non-elevated processes can send this messages to the elevated 7plus process.
; Keyword: UIPI
DllCall("ChangeWindowMessageFilter", "UInt", 55555, "UInt", 1)
DllCall("ChangeWindowMessageFilter", "UInt", 55556, "UInt", 1)

#include %A_ScriptDir%\..\settings\a2_init.ahk
Return ; -----------------------------------------------------------------------------

a2UI:
    a2UI()
Return
a2ui() {
    Run, % a2.Exe " " A_ScriptDir "\a2ui.ahk", %A_ScriptDir%
}

a2ui_help:
    Run, %a2_help%
Return

reload()
{
    msgbox % "howdy"
}

a2ui_reload:
    Reload
Return

a2ui_exit:
    deleteHwnd := true
ExitApp
