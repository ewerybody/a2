global a2 := new Ca2()
global Settings := {} ;empty object for setting to be injected into

global UIresources := a2.Path "\ui\res"

global WinVer := windows_get_version()
global WIN_XP := 5.1
global WIN_XP64 := 5.2
global WIN_VISTA := 6.0
global WIN_7 := 6.1
global WIN_8 := 6.2
global WIN_10 := 10.0

global WEB_TLDS := ["html", "com", "de", "net", "org", "co.uk"]

; groups for explorer classes
GroupAdd, ExplorerGroup, ahk_class ExploreWClass
GroupAdd, ExplorerGroup, ahk_class CabinetWClass
GroupAdd, DesktopGroup, ahk_class WorkerW
GroupAdd, DesktopGroup, ahk_class Progman ;Progman for older windows versions <Vista
GroupAdd, TaskbarGroup, ahk_class Shell_TrayWnd
GroupAdd, TaskbarGroup, ahk_class BaseBar
GroupAdd, TaskbarGroup, ahk_class DV2ControlHost
GroupAdd, TaskbarDesktopGroup, ahk_group DesktopGroup
GroupAdd, TaskbarDesktopGroup, ahk_group TaskbarGroup

; mouse cursor image constants
global IDC_APPSTARTING := 32650
global IDC_HAND := 32649
global IDC_ARROW := 32512
global IDC_CROSS := 32515
global IDC_IBEAM := 32513
global IDC_ICON := 32641
global IDC_NO := 32648
global IDC_SIZE := 32640
global IDC_SIZEALL := 32646
global IDC_SIZENESW := 32643
global IDC_SIZENS := 32645
global IDC_SIZENWSE := 32642
global IDC_SIZEWE := 32644
global IDC_UPARROW := 32516
global IDC_WAIT := 32514
global IDC_HELP := 32651

;Invisible border size. Usually Autohotkey methods apply to the inner size
SysGet, WIN_FRAME_WIDTH, 32
SysGet, WIN_FRAME_HEIGHT, 33
global WIN_FRAME_WIDTH
global WIN_FRAME_HEIGHT
