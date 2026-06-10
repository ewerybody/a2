#Requires AutoHotkey v2.0

#Include %A_ScriptDir%\..\
#Include <a2dlg>
#Include <explorer>
#Include <string>
#include <path>

window := explorer_get_window()
if !window {
    a2dlg_error("Run this from the Windows File Explorer please!")
    ExitApp
}
selected_b4 := explorer_get_selected()

base_names := []
select_these := []
for i, path in explorer_get_all() {
    this_base := path_basename(path)
    base_names.push(this_base)
    if Random(0, 1)
        select_these.push(this_base)
}
a2dlg_info("All " base_names.length " files here:`n" string_join(base_names) "`nSelecting Random " select_these.length ": ...")
explorer_select(select_these)
sleep 500
if (base_names.length) {
    a2dlg_info("Selecting Random Single ...")
    explorer_select(base_names[Random(1, base_names.length)])
}
ExitApp