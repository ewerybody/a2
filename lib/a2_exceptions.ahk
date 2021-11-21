a2_on_runtime_exception(exception) {
    ; Autohotkey already builds a convenient exception object at runtime.
    _a2_exceptions_handle("a2 Runtime Error", exception)
    Reload
}

a2_on_startup_exception(popup_text, root_script_path) {
    ; At startup we have to assemble the exception info from the different error popups.
    lines := StrSplit(popup_text, "`n")
    INCL_DIRECTIVE := "#include"
    INCL_FILE := INCL_DIRECTIVE " file"
    INCL_OPEN := " cannot be opened."
    IN_INCL := "in " INCL_FILE
    ERR := "Error"
    INCL_ERROR := ERR " " IN_INCL
    OTHER_ERRR := ERR " at line "

    exception := {}
    If string_startswith(lines[1], INCL_ERROR) {
        path := SubStr(lines[1], StrLen(INCL_ERROR) + 1)
        exception.File := string_unquote(string_trimRight(string_strip(path), ":"))
        exception.Message := string_strip(lines[2])
        _exception_search_lines(lines, exception)
    }
    else If string_startswith(lines[1], OTHER_ERRR) AND InStr(lines[1], IN_INCL) {
        len_mrk := StrLen(OTHER_ERRR) + 1
        nr_end := InStr(lines[1], IN_INCL,, len_mrk)
        exception.Line := string_strip(SubStr(lines[1], len_mrk, nr_end - len_mrk))
        file := string_strip(SubStr(lines[1], nr_end + StrLen(IN_INCL)))
        exception.File := string_unquote(string_trimRight(file, "."))

        for i, line in lines {
            if string_startswith(line, ERR ":")
                exception.Message := string_strip(SubStr(line, StrLen(ERR) + 2))
            if string_startswith(line, "Line Text:") {
                col_pos := InStr(line, ":") + 1
                exception.What := string_strip(SubStr(line, col_pos))
            }
        }
    }
    else if string_startswith(lines[1], ERR ":") {
        exception.Message := string_strip(SubStr(lines[1], 7))
        exception.File := root_script_path
        _exception_search_lines(lines, exception)
    }
    else if string_startswith(lines[1], OTHER_ERRR) {
        len_mrk := StrLen(OTHER_ERRR) + 1
        nr_end := InStr(lines[1], ".",, len_mrk)
        exception.Line := string_strip(SubStr(lines[1], len_mrk, nr_end - len_mrk))
        exception.File := root_script_path
        if string_startswith(lines[3], INCL_FILE) AND string_endswith(lines[3], INCL_OPEN) {
            exception.Message := INCL_FILE INCL_OPEN
            exception.What := INCL_DIRECTIVE
            incl_end := StrLen(INCL_FILE) + 3
            exception.Extra := SubStr(lines[3], incl_end, StrLen(lines[3]) - incl_end - StrLen(INCL_OPEN))
        }
    }

    else {
        for i, line in lines {
            msg .= i " " line "`n"
        }
        MsgBox % "Unhandled Startup Error:`n" msg
    }

    _a2_exceptions_handle("a2 Startup Error", exception)
}

_a2_exceptions_handle(title, exception) {
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
    code_lines := _get_neighbor_lines(exception.File, exception.Line, 3)

    msg := "There was an exception thrown:`n`n" A_Tab exception.Message "`n`n"
    if exception.Extra {
        msg .= "command: """ exception.What """`n"
        msg .= "value: """ exception.Extra """`n`n"
    }
    else
        msg .= "what: """ exception.What """`n`n"
    msg .= "file: " path_basename(exception.File) ", Line: " exception.Line ":`n`n"
    msg .= code_lines "`n`n"
    msg .= "file path: " exception.File
    title := title ": " exception.Message

    SetTimer, _a2ui_on_error_change_buttons, 50
    cursor_reset()
    MsgBox, 19, %title%, %msg%
    ; MsgBox, 16403, %title%, %msg%

    IfMsgBox, Yes
    {
        editor := a2.cfg.code_editor
        base := path_basename(editor)
        if !editor OR !base
            MsgBox editor: %editor%`nbase: %base%
        file_line := exception.File ":" exception.Line
        Run, "%editor%" --reuse-window --goto "%file_line%"
    }
    IfMsgBox, No
    {
        ui_func := "a2ui"
        if IsFunc(ui_func)
            %ui_func%()
    }

    _a2ui_on_error_change_buttons:
        IfWinNotExist, %title%
            return ; Keep waiting.
        SetTimer, _a2ui_on_error_change_buttons, Off
        WinActivate
        ControlSetText, Button1, Edit Code
        ControlSetText, Button2, Open UI
        ControlSetText, Button4, ...
    Return
}

_get_neighbor_lines(file_path, line_nr, num_neighbor_lines) {
    start_line := line_nr - num_neighbor_lines - 1
    Loop, % num_neighbor_lines * 2 + 1
    {
        this_nr := start_line + A_Index
        this_line := FileReadLine(file_path, this_nr)
        if !this_line
            Continue
        this_line := StringReplace(this_line, A_Tab, "    ")

        new_line := ""
        ; Optinal line number? But looks actually way better!
        new_line .= this_nr ": "

        if (this_nr == line_nr)
            new_line .= "-->"
        else
            new_line .= "     "
        new_line .= this_line "`n"

        max_len := 64
        if StrLen(new_line) > max_len
            new_line := SubStr(new_line, 1, max_len - 3) "...`n"

        code_lines .= new_line
    }

    return code_lines
}

_exception_search_lines(lines, exception) {
    CMD_MARKER := "Specifically:"
    LINE_MARKR := "--->"

    for i, line in lines {
        if string_startswith(line, CMD_MARKER) AND !exception.What {
            exception.What := string_unquote(string_strip(SubStr(line, StrLen(CMD_MARKER) + 1)))
        }
        if string_startswith(line, LINE_MARKR) {
            len_mrk := StrLen(LINE_MARKR) + 1
            len_sub := InStr(line, ":") - len_mrk
            exception.Line := string_strip(SubStr(line, len_mrk, len_sub))
            Return
        }
    }
}
