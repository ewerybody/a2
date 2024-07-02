#Requires AutoHotkey v2.0

#Include %A_ScriptDir%\..\
#Include msgbox.ahk
#Include explorer.ahk
#Include string.ahk
#include path.ahk

selected_b4 := explorer_get_selected()

basenames := []
select_these := []
for path in explorer_get_all() {
    this_base := path_basename(path)
    basenames.push(this_base)
    if Random(0, 1)
        select_these.push(this_base)
}
msgbox_info("All " basenames.length " files here:`n" string_join(basenames) "`nSelecting Random " select_these.length ": ...")
explorer_select(select_these)
sleep 500
msgbox_info("Selecting Random Single ...")
explorer_select(basenames[Random(1, basenames.length)])