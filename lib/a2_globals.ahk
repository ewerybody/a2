global a2 := new Ca2()
global Settings := {} ;empty object for setting to be injected into

global UIresources := a2.Path "\ui\res"

global WinVer := GetWindowsVersion()
global WIN_XP := 5.1
global WIN_XP64 := 5.2
global WIN_VISTA := 6.0
global WIN_7 := 6.1
global WIN_8 := 6.2
global WIN_10 := 10.0

global NotifyIcons := new CNotifyIcons()

global WEB_TLDS := ["html", "com", "de", "net", "org", "co.uk"]

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
