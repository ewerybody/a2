; a2 installer version to enforce silent mode

;@Ahk2Exe-ConsoleApp
;@Ahk2Exe-SetMainIcon ..\..\ui\res\a2x.ico
;@Ahk2Exe-SetCompanyName a2
;@Ahk2Exe-SetCopyright GPLv3
;@Ahk2Exe-SetDescription a2 install script silent
;@Ahk2Exe-SetOrigFilename setup.exe
;@Ahk2Exe-SetProductName a2
;@Ahk2Exe-SetVersion 0.4.2

complain_if_uncompiled()
check_execution_dir()

A2DIR := get_a2dir()
A2STUFF := ["lib", "ui", "a2.exe", "a2ui.exe"]
install_ver := read_version(A2DIR)
backup_dir_name := "_ a2 upgrade.bak"
install_script := "setup.exe"
A_Args.Push("--silent")
run_silent := true
PACKAGE_DIR := A_ScriptDir . "\a2"

intro()
check_running()
backup()
install()

logmsg("Starting a2 ...")
Run, a2.exe, %A2DIR%

; --------------------------------------------------------
Return
#include, a2_installer.ahk
