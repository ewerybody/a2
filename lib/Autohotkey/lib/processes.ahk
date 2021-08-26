
processes_list_ids(process_name="") {
    ; Gather list of PIDs from all running processes via COM.
    ; https://www.autohotkey.com/docs/commands/Process.htm#ListCom
    ; These COM objects have a multitude of interesting member variables:
    ; https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-process?redirectedfrom=MSDN
    ; Name, ProcessId ...
    pids := []
    for proc in ComObjGet("winmgmts:").ExecQuery("Select * from Win32_Process") {
        if (process_name and process_name != proc.name)
            Continue
        pids.Push(proc.ProcessID)
    }
    return pids
}
