#include a2_settings.ahk
#include lib\_init_check.ahk

if (!a2_ahk) {
    _init_check_settings()
} else {
    Run, %a2_ahk% a2.ahk
}
