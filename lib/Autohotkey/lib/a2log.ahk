a2log_info(msg, module="") {
    _a2log("INFO", module, msg)
}

a2log_debug(msg, module="") {
    _a2log("DEBUG", module, msg)
}

a2log_warn(msg, module="") {
    _a2log("WARN", module, msg)
}

a2log_error(msg, module="") {
    _a2log("ERROR", module, msg)
}

_a2log(level, module, msg) {
    static last_logged
    now := time_unix()
    if (last_logged != now) {
        last_logged := now
        line := "@time " now "`n"
    }

    log_path := path_join(a2.paths.data, "a2.log")
    line .= level ":" module ": " msg
    FileAppend %line%`n, %log_path%
}
