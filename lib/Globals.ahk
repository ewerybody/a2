ifNotExist, %a2_ahk%
    a2_ahk = %A_ScriptDir%\Autohotkey\Autohotkey.exe
global a2 := {Title: "a2", Path: A_ScriptDir "\..", Modules: a2_modules, Exe: a2_ahk}
global Settings := RichObject() ;empty object for setting to be injected into
global Triggers := RichObject() ; empty object where modules can register for external triggers

global UIresources := a2.Path "\ui\res"
global libs := a2.Path "\lib\ahklib"

global WinVer := GetWindowsVersion()
global WIN_XP := 5.1
global WIN_XP64 := 5.2
global WIN_VISTA := 6.0
global WIN_7 := 6.1
global WIN_8 := 6.2
global WIN_10 := 10.0

global NotifyIcons := new CNotifyIcons()
global Prompt := new CPrompt()

; Groups for explorer classes
GroupAdd, ExplorerGroup, ahk_class ExploreWClass
GroupAdd, ExplorerGroup, ahk_class CabinetWClass
GroupAdd, DesktopGroup, ahk_class WorkerW
GroupAdd, DesktopGroup, ahk_class Progman ;Progman for older windows versions <Vista
GroupAdd, TaskbarGroup, ahk_class Shell_TrayWnd
GroupAdd, TaskbarGroup, ahk_class BaseBar
GroupAdd, TaskbarGroup, ahk_class DV2ControlHost
GroupAdd, TaskbarDesktopGroup, ahk_group DesktopGroup
GroupAdd, TaskbarDesktopGroup, ahk_group TaskbarGroup
