#include {lib_path}a2.ahk
#include {data_path}
#include includes\variables.ahk
#include includes\source_libs.ahk
#include {data_path}
#include includes\includes.ahk
#include {data_path}
#include includes\hotkeys.ahk
#include includes\init.ahk
if IsSet(a2_init_calls)
    a2_init_calls()
#include includes\exit.ahk