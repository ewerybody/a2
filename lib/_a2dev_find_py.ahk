a2dev_get_py()
{
    ; TODO: this needs to be a little bit more dynamic
    supported_versions := ["3.12", "3.11", "3.10", "3.9"]
    ; First: Try to read python path from registry in either CURRENT_USER or LOCAL_MACHINE domain
    pypath := check_registry(supported_versions)
    if (pypath != "")
        Return pypath

    title := "No Matching Python Version!"
    msg := "Could not find a Python installation!`nSupported versions include: " . string_join(supported_versions) . "!"
    MsgBox(msg, title, 16)
    ExitApp
}


check_registry(supported_versions) {
    ;exe_type := {filename: "python.exe", reg_name: "ExecutablePath"}
    exe_type := {filename: "pythonw.exe", reg_name: "WindowedExecutablePath"}
    reg_name := exe_type.reg_name

    Loop(supported_versions.Length)
    {
        this_version := supported_versions[A_Index]
        py_key := "HKEY_CURRENT_USER\Software\Python\PythonCore\" . this_version . "\InstallPath"
        pypath := RegRead(py_key, reg_name)

        if !string_endswith(pypath, exe_type.filename)
        {
            py_key := "HKEY_LOCAL_MACHINE\Software\Python\PythonCore\" . this_version . "\InstallPath"
            pypath := RegRead(py_key, reg_name)
        }

        If FileExist(pypath)
        {
            global a2_PY_VERSION_SHORT := this_version
            Return pypath
        }
    }
}
