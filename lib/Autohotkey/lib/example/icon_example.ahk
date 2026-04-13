#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon

#Include <a2dlg>
#Include <path>
#Include <string>
#Include <icon>

dlg := A2Dialog("A2 Icon Library", {w: 500})
c := dlg.c

dlg.header("A2 Icon Library Demo")
dlg.sep()

; Resolves the registered default icon path for a file extension via HKCR.
dlg.heading("icon_from_type")
for ext in ["py", "ahk", "txt", "pdf", "zip"] {
    pth := icon_from_type(ext)
    p := icon_path_split(pth)
    dlg.pic_row(p.file, p.opt, "." ext " => " pth)
}

dlg.space(6)
dlg.sep()

; icon_get_count returns the total; icon_extract returns an HICON handle.
dlg.heading("icon_extract  /  icon_get_count")

dll := "C:\Windows\System32\imageres.dll"
count := icon_get_count(dll)
dlg.text(dll "  ·  icon_get_count => " count)
dlg.space(6)
icons := []
loop count
    icons.Push({file: dll, opt: "Icon" A_Index})
shown := dlg.pic_strip(icons)
dlg.text("(showing first " shown " of " icons.Length " icons)")

; icon_extract returns an HICON handle — useful for set_icon, overlays, etc.
dlg.space(4)
win_ico := icon_extract(dll, 4)
dlg.text("icon_extract(dll, 4) => hIcon: " win_ico "  (set as window icon below)")

dlg.space(8)
dlg.sep()

dlg.btn_row_right([
    {label: "Pick Dialog Icon", func: pick_dialog_icon},
    {label: "Close", func: (*) => dlg.destroy()}
], )
dlg.show()

if win_ico
    dlg.set_icon(win_ico)

dlg.exit_on_close()
dlg.esc_to_close()


pick_dialog_icon(*) {
    result := icon_pick(dlg.hwnd)
    dlg.set_icon(result.file, result.idx)
}
