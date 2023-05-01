#SingleInstance, Force
SendMode, Input
SetWorkingDir, %A_ScriptDir%

#Include a2test.ahk
#Include %A_ScriptDir%\..\
#Include move.ahk
#Include string.ahk
#Include path.ahk
#Include msgbox.ahk


test_dir := path_join(A_Temp, "_a2_move_test_1234")
if FileExist(test_dir) {
    FileRemoveDir, %test_dir%
    if FileExist(test_dir) {
        msgbox_error("Cannot remove test dir! Aborting ...")
        ExitApp
    }
}

FileCreateDir, %test_dir%
test_dir2 := test_dir "5"

result := secure_move(test_dir, test_dir2)
report := "simple move dir: " assertmsg(result == 1 AND !FileExist(test_dir) AND FileExist(test_dir2)) "`n"

result := secure_move(test_dir, test_dir2)
report .= "fail when already exists: " assertmsg(result == 0)
FileRemoveDir, %test_dir2%



MsgBox report: %report%