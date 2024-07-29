a2dev_get_py()
{
    ; TODO: this needs to be a little bit more dynamic
    supported_versions := ["3.12", "3.11", "3.10", "3.9"]
    ; First: Try to read python path from registry in either CURRENT_USER or LOCAL_MACHINE domain
    found_versions := check_registry(supported_versions)
    if found_versions.length
        return found_versions[1].path

    title := "No Matching Python Version!"
    msg := "Could not find a Python installation!`nSupported versions include: " . string_join(supported_versions) . "!"
    MsgBox(msg, title, 16)
    ExitApp
}

; Give Array of found python versions as objects with `path` and `version` properties.
check_registry(supported_versions) {
    ;exe_type := {filename: "python.exe", reg_name: "ExecutablePath"}
    exe_type := {filename: "pythonw.exe", reg_name: "WindowedExecutablePath"}
    reg_name := exe_type.reg_name

    found_versions := []
    for this_version in supported_versions
    {
        py_key := "HKEY_CURRENT_USER\Software\Python\PythonCore\" . this_version . "\InstallPath"
        pypath := RegRead(py_key, reg_name, "")

        if !string_endswith(pypath, exe_type.filename)
        {
            py_key := "HKEY_LOCAL_MACHINE\Software\Python\PythonCore\" . this_version . "\InstallPath"
            pypath := RegRead(py_key, reg_name, "")
        }

        If FileExist(pypath)
        {
            py_obj := {version: this_version, path: pypath}
            found_versions.push(py_obj)
        }
    }
    return found_versions
}
