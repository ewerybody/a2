; AUTO-GENERATED! Do not edit! Run: poe build-theme
#Include <path>
#Include <theme>
#Include <windows>

class A2Icons {
    static _cache := Map()
    static _base := path_dirname(A_LineFile, 4) "\theme\"
    static _last_theme := ""

    static __Get(name, params) {
        theme_name := theme_get()
        if A2Icons._last_theme != theme_name {
            A2Icons._cache := Map()
            A2Icons._last_theme := theme_name
        }
        if A2Icons._cache.Has(name)
            return A2Icons._cache[name]

        path := A2Icons._base name ".ico"
        if !FileExist(path) {
            path := A2Icons._base theme_name "\" name ".ico"
            if !FileExist(path)
                path := A2Icons._base "a2.ico"
        }
        A2Icons._cache[name] := path
        return path
    }

    static a2 => A2Icons.__Get("a2", 0)
    static a2help => A2Icons.__Get("a2help", 0)
    static a2reload => A2Icons.__Get("a2reload", 0)
    static a2tinted => A2Icons.__Get("a2tinted", 0)
    static a2x => A2Icons.__Get("a2x", 0)
    static autohotkey => A2Icons.__Get("autohotkey", 0)
    static github => A2Icons.__Get("github", 0)
    static gitter => A2Icons.__Get("gitter", 0)
    static telegram => A2Icons.__Get("telegram", 0)

    static arrow_left => A2Icons.__Get("arrow_left", 0)
    static arrow_right => A2Icons.__Get("arrow_right", 0)
    static check => A2Icons.__Get("check", 0)
    static checkbox_hover => A2Icons.__Get("checkbox_hover", 0)
    static checkbox_off => A2Icons.__Get("checkbox_off", 0)
    static checkbox_on => A2Icons.__Get("checkbox_on", 0)
    static clear => A2Icons.__Get("clear", 0)
    static copy => A2Icons.__Get("copy", 0)
    static folder => A2Icons.__Get("folder", 0)
    static paste => A2Icons.__Get("paste", 0)
    static switch => A2Icons.__Get("switch", 0)
    static to_clipboard => A2Icons.__Get("to_clipboard", 0)
    static trash => A2Icons.__Get("trash", 0)
    static volume_down => A2Icons.__Get("volume_down", 0)
    static volume_up => A2Icons.__Get("volume_up", 0)
}