a2dev_get_py()
{
    ; TODO: this needs to be a little bit more dynamic
    supported_versions := ["3.10", "3.9", "3.8", "3.7", "3.6"]
    ;exe_type := {filename: "python.exe", reg_name: "ExecutablePath"}
    exe_type := {filename: "pythonw.exe", reg_name: "WindowedExecutablePath"}

    ; First: Try to read python path from registry in either CURRENT_USER or LOCAL_MACHINE domain
    pypath := check_registry(supported_versions, exe_type)
    if (pypath != "")
        Return pypath

    versions_string := string_join(supported_versions)

    MsgBox, 16, No Matching Python Version!, Could not find a Python installation!`nSupported versions include: %versions_string%!
    ExitApp
}


check_registry(supported_versions, exe_type) {
    reg_name := exe_type["reg_name"]
    Loop, % supported_versions.MaxIndex()
    {
        this_version := supported_versions[A_Index]

        py_key = HKEY_CURRENT_USER\Software\Python\PythonCore\%this_version%\InstallPath
        RegRead, pypath, %py_key%, %reg_name%

        if !string_endswith(pypath, exe_type.filename)
        {
            py_key = HKEY_LOCAL_MACHINE\Software\Python\PythonCore\%this_version%\InstallPath
            RegRead, pypath, %py_key%, %reg_name%
        }

        IfExist, %pypath%
        {
            global a2_PY_VERSION_SHORT := this_version
            Return, pypath
        }
    }
}
