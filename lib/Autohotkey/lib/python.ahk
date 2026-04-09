; a2 Autohotkey python lib

; Run given python script with given arguments in first found Python executable and return its output.
python_get_output(py_file, args := "") {
    py_exe := python_get_console_path()
    cmd := '"' py_exe '" "' py_file '" ' args
    shell := ComObject("WScript.Shell")
    exec := shell.Exec(cmd)
    errors := exec.StdErr.ReadAll()
    if (errors) {
        msgbox_error(errors, "python_get_output-ERROR")
        return
    }

    result := exec.StdOut.ReadAll()
    return result
}

; Get path to the "python" console executable.
python_get_console_path() {
    exe_type := {filename: "python.exe", reg_name: "ExecutablePath"}
    return _py_get_path(exe_type)
}

; Get path to the "pythonw" executable for GUI without console.
python_get_path() {
    exe_type := {filename: "pythonw.exe", reg_name: "WindowedExecutablePath"}
    return _py_get_path(exe_type)
}

_py_get_path(exe_type) {
    out_dir := path_dirname(A_LineFile, 4)
    venv_path := path_join(out_dir, '.venv', 'Scripts', exe_type.filename)
    if FileExist(venv_path)
        return venv_path

    py_path := python_check_registry(exe_type)
    if (py_path != "")
        Return py_path

    MsgBox_error("Could not find a Python installation!`nSupported versions include: " string_join(PYTHON_SUPPORTED_VERSIONS)
        , "No Matching Python Version!")
}

; Loop over supported Python versions to find according registry entries.
; Return first valid entry under `InstallPath`
python_check_registry(exe_type) {
    for i, version in PYTHON_SUPPORTED_VERSIONS
    {
        py_key := "HKEY_CURRENT_USER\Software\Python\PythonCore\" version "\InstallPath"
        py_path := RegRead(py_key, exe_type.reg_name)

        if !string_endswith(py_path, exe_type.filename) {
            py_key := "HKEY_LOCAL_MACHINE\Software\Python\PythonCore\" version "\InstallPath"
            py_path := RegRead(py_key, exe_type.reg_name)
        }

        If FileExist(py_path) {
            global a2_PY_VERSION_SHORT := version
            Return py_path
        }
    }
}
