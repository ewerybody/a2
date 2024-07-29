#include <path>
#include _a2dev_find_py.ahk

ahk_executable_path := path_join(A_ScriptDir, "Autohotkey", "Autohotkey.exe")
py_executable_path := a2dev_get_py()
root_path := path_dirname(A_ScriptDir)
icon_path := path_join(root_path, "ui", "res", "a2.ico")
; msgbox("icon_path: " . icon_path " exists: " FileExist(icon_path))
; iconsize := 32  ; Ideal size for alt-tab varies between systems and OS versions.
; hIcon := LoadPicture(icon_path, "Icon1 w" iconsize " h" iconsize, &imgtype)
TraySetIcon(icon_path)

A2DevUI := Gui("+DPIScale +Resize +MinSize640x180")
; SendMessage(0x0080, 1, hIcon, A2DevUI)

start_a2btn := A2DevUI.AddButton("xm Section", "Create A2`nstart shortcut")
start_a2btn.OnEvent("Click", start_a2)
A2DevUI.AddText("ys w75", "Autohotkey.exe:")
ahk_path_field := A2DevUI.AddEdit("ys +ReadOnly", ahk_executable_path)
A2DevUI.AddEdit("ys +ReadOnly", FileGetVersion(ahk_executable_path))

start_uibtn := A2DevUI.AddButton("xm Section", "Create A2UI`n shortcut")
start_uibtn.OnEvent("Click", start_ui)
A2DevUI.AddText("ys w75", "Python.exe:")
python_path_field := A2DevUI.AddEdit("ys +ReadOnly", py_executable_path)
A2DevUI.AddEdit("ys +ReadOnly", FileGetVersion(py_executable_path))
; A2DevUI.Add("GroupBox",, "Geographic Criteria")
; A2DevUI.Add("CheckBox",, "Build a2 & a2ui links.")

A2DevUI.show()


start_a2(*) {
    link_path := path_join(root_path, "a2.lnk")
    desc := "Start the a2 runtime with the built-in Autohotkey"
    FileCreateShortcut ahk_executable_path, link_path, root_path, "lib\a2.ahk", desc, icon_path
}

start_ui(*) {
    msgbox("ui...")
}