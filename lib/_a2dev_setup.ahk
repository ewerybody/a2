#include <path>
ahk_executable_path := path_join(A_ScriptDir, "Autohotkey", "Autohotkey.exe")
root_path := path_dirname(A_ScriptDir)
icon_path := path_join(root_path, "ui", "res", "a2.ico")
; msgbox("icon_path: " . icon_path " exists: " FileExist(icon_path))
; iconsize := 32  ; Ideal size for alt-tab varies between systems and OS versions.
; hIcon := LoadPicture(icon_path, "Icon1 w" iconsize " h" iconsize, &imgtype)
TraySetIcon(icon_path)

A2DevUI := Gui("+DPIScale +Resize +MinSize640x180")
; SendMessage(0x0080, 1, hIcon, A2DevUI)

A2DevUI.AddText("Section", "Autohotkey.exe:")
ahk_path_field := A2DevUI.AddEdit("ys +ReadOnly", ahk_executable_path)
A2DevUI.AddEdit("ys +ReadOnly", FileGetVersion(ahk_executable_path))

; A2DevUI.Add("GroupBox",, "Geographic Criteria")
; A2DevUI.Add("CheckBox",, "Build a2 & a2ui links.")
start_a2btn := A2DevUI.AddButton("xm", "Create A2 start shortcut")
start_a2btn.OnEvent("Click", start_a2)
A2DevUI.show()


start_a2(*) {
    link_path := path_join(root_path, "a2.lnk")
    desc := "Start the a2 runtime with the built-in Autohotkey"
    FileCreateShortcut ahk_executable_path, link_path, root_path, "lib\a2.ahk", desc, icon_path
}
