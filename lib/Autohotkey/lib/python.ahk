; a2 Autohotkey python lib

python_get_output(py_file, args := "") {
    py_exe := python_get_console_path()
    cmd := '"' py_exe '" "' py_file '" ' args
    shell := ComObject("WScript.Shell")
    exec := shell.Exec(cmd)
    errors := exec.StdErr.ReadAll()
    if (errors)
        msgbox_error(errors, "python_get_output-ERROR")
    else {
        result := exec.StdOut.ReadAll()
        return result
    }
}

python_get_console_path() {
    exe_type := {filename: "python.exe", reg_name: "ExecutablePath"}
    return _py_get_path(exe_type)
}

python_get_path() {
    exe_type := {filename: "pythonw.exe", reg_name: "WindowedExecutablePath"}
    return _py_get_path(exe_type)
}

_py_get_path(exe_type) {
    pypath := python_check_registry(exe_type)
    if (pypath != "")
        Return pypath

    MsgBox_error("Could not find a Python installation!`nSupported versions include: " string_join(python_supported_versions)
        , "No Matching Python Version!")
}


python_check_registry(exe_type) {
    for i, version in python_supported_versions
    {
        py_key := "HKEY_CURRENT_USER\Software\Python\PythonCore\" version "\InstallPath"
        pypath := RegRead(py_key, exe_type.reg_name)

        if !string_endswith(pypath, exe_type.filename)
        {
            py_key := "HKEY_LOCAL_MACHINE\Software\Python\PythonCore\" version "\InstallPath"
            pypath := RegRead(py_key, exe_type.reg_name)
        }

        If FileExist(pypath)
        {
            global a2_PY_VERSION_SHORT := version
            Return pypath
        }
    }
}
