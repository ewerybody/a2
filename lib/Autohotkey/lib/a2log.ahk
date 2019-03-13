/*
 * WIP logging functions.
 * 
 */

a2log_debug(title, input_object = "", module = "", delay = 0, Delimiter = "`n")
{
    _a2log(title, input_object, "debug", module, delay, delimiter)
}

a2log_info(title, input_object = "", module = "", delay = 0, delimiter = "`n")
{
    _a2log(title, input_object, "info", module, delay, delimiter)
}

a2log_error(title, input_object = "", module = "", delay = 0, delimiter = "`n")
{
    _a2log(title, input_object, "error", module, delay, delimiter)
}


_a2log(title, input_object = "", level = "info", module = "", delay = 0, delimiter = "`n")
{
    _prefix := level ? "[" level "] " : ""
    _module := module ? "[" module "] " : ""
    _time   := "[" FormatTime(A_Now, "HH:mm:ss") "] "

    if (Settings.Debug.Enabled)
    {
        sleep, %delay%
        FileAppend % _time _prefix _module title "`n", *
        if (input_object)
        {
            Loop, Parse, input_object, %delimiter%
                _a2log("    " A_LoopField, "", level, module, delay)
        }
    }
}