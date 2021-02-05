a2_exceptions_handle(exception) {
    ; Handle exceptions happening after load time.
    ; This will either open your code editor with the offending line
    ; selected of make the UI appear with the right module showing.
    ; command-line args for VS Code:
    ; https://code.visualstudio.com/docs/editor/command-line
    ; Maybe we could have a {executable: pattern} map for the different
    ; IDEs? like {
    ;    "Code.exe": "--reuse-window --goto \"{file}:{line}:{char}\"",
    ;    "nodepad++.exe": "\"{file}\" -n{line} -c{char}",
    ;    "subl.exe": "\"{file}:{line}:{char}\""
    ;    "": "\"{file}:{line}\"",
    ; }
    ;

    file_path := exception.File, line_nr := exception.Line
    FileReadLine, code_line, %file_path%, %line_nr%
    file_name := path_basename(file_path)

    msg := "There was an exception thrown:`n " exception.Message "`n"
    msg .= "command: """ exception.What """`n"
    msg .= "value: """ exception.Extra """`n"
    msg .= "file: " file_name ", Line: " line_nr "`n"
    msg .= ">>>" code_line
    title := "a2 Runtime Error: " exception.Message

    SetTimer, _a2ui_on_error_change_buttons, 50
    MsgBox, 19, %title%, %msg%
    IfMsgBox, Yes
    {
        editor := a2cfg.code_editor
        base := path_basename(editor)
        MsgBox editor: %editor%`nbase: %base%
        file_line := exception.File ":" exception.Line
        Run, "%editor%" --reuse-window --goto "%file_line%"
    }
    IfMsgBox, No
    a2ui()

    Reload

    _a2ui_on_error_change_buttons:
        IfWinNotExist, %title%
            return ; Keep waiting.
        SetTimer, _a2ui_on_error_change_buttons, Off
        WinActivate
        ControlSetText, Button1, Edit Code
        ControlSetText, Button2, Open UI
    Return
}
