#Requires AutoHotkey v2.0

#Include %A_ScriptDir%\..\
#Include <msgbox>
#Include <explorer>
#Include <string>
#include <path>

selected_b4 := explorer_get_selected()

base_names := []
select_these := []
for i, path in explorer_get_all() {
    this_base := path_basename(path)
    base_names.push(this_base)
    if Random(0, 1)
        select_these.push(this_base)
}
msgbox_info("All " base_names.length " files here:`n" string_join(base_names) "`nSelecting Random " select_these.length ": ...")
explorer_select(select_these)
sleep 500
if (base_names.length) {
    msgbox_info("Selecting Random Single ...")
    explorer_select(base_names[Random(1, base_names.length)])
}
