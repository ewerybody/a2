#SingleInstance, Force
SendMode, Input
SetWorkingDir, %A_ScriptDir%

#Include a2test.ahk
#Include %A_ScriptDir%\..\
#Include move.ahk
#Include string.ahk
#Include path.ahk
#Include msgbox.ahk

; report := test_move_secure()
report .= test_move_catched()
MsgBox report: %report%


Return ; --------------------------------------------

test_move_secure() {
    test_dir := _make_test_dir()
    test_dir2 := test_dir "5"

    result := move_secure(test_dir, test_dir2)
    report := "simple move dir: " assertmsg(result == 1 AND !FileExist(test_dir) AND FileExist(test_dir2)) "`n"

    result := move_secure(test_dir, test_dir2)
    report .= "fail when already exists: " assertmsg(result == 0) "`n"
    FileRemoveDir, %test_dir2%

    return report
}


test_move_catched() {
    ; create a bunch of files and dirs
    test_dir := _make_test_dir()
    DIR_NAME := "blocked_dir"
    blocked_dir := path_join(test_dir, DIR_NAME)
    FileCreateDir, %blocked_dir%
    FILE1 := "_file1.txt"
    test_file1 := path_join(test_dir, FILE1)
    FileAppend, Text, %test_file1%
    FILE2 := "XJHVDSJHV.md"
    test_file2 := path_join(test_dir, FILE2)
    FileAppend, # Text, %test_file2%
    target_dir := test_dir . "5"
    FileCreateDir, %target_dir%

    file_list1 := _listdir(test_dir)
    ; BLOCK a directory with a process, NOT by file attributes
    Run, %ComSpec% , %blocked_dir%, hide, OutputVarPID
    result := move_catched(test_dir, target_dir, file_list1)

    report := "dir blocked/rolled back: " . assertmsg(result == false)
    file_list2 := _listdir(test_dir)
    report .= assertmsg(string_join(file_list1) == string_join(file_list2)) . "`n"

    Process, Close , %OutputVarPID%
    result := move_catched(test_dir, target_dir, file_list1)
    report .= "unblocked/retry: " . assertmsg(result == true)
    file_list2 := _listdir(target_dir)
    report .= assertmsg(string_join(file_list1) == string_join(file_list2))
    report .= assertmsg(path_is_empty(test_dir)) "`n"

    ; try blocking by opening a file/setting it read-only:
    locked_file := path_join(target_dir, FILE1)
    file := FileOpen(locked_file, "w")
    file.Write("Some new string ...")

    result := move_catched(target_dir, test_dir, file_list1)
    report .= "opened file does not block: " . assertmsg(result == true)
    file.Close()
    report .= assertmsg(path_is_empty(target_dir)) . assertmsg(!path_is_file(locked_file)) "`n"

    locked_file := path_join(test_dir, FILE2)
    path_set_readonly(locked_file)
    result := move_catched(test_dir, target_dir, file_list1)
    report .= "locked file does not block: " . assertmsg(result == true)

    FileRemoveDir, %test_dir%, 1
    FileRemoveDir, %target_dir%, 1

    return "test_move_catched ...`n" . report
}


_listdir(dir_path) {
    item_list := []
    Loop, %dir_path%\*, 1
        item_list.Push(A_LoopFileName)
    return item_list
}


_make_test_dir(name := "_a2_move_test_1234") {
    test_dir := path_join(A_Temp, name)
    if FileExist(test_dir) {
        FileRemoveDir, %test_dir%, 1
        if FileExist(test_dir) {
            msgbox_error("Cannot remove test dir! Aborting ...")
            ExitApp
        }
    }

    FileCreateDir, %test_dir%
    return test_dir
}