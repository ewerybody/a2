#Requires AutoHotkey v2.0

#Include <jxon>
#Include <path>
#Include <windows>

/**
 * Get the theme to be used. In this order:
 * - user defined theme (if set and existing)
 * - system theme ("light" or "dark")
 * @returns {(String)} - Theme name as in "dark", "light", or whatever set
 */
theme_get() {
    user_theme := theme_get_user()
    if user_theme
        return user_theme
    return theme_get_system()
}

/**
 * Get user set theme from database if available or from global var `a2_theme` if set.
 * @returns {(String)}
 */
theme_get_user() {
    if IsSet(a2) {
        theme := a2.db.get("theme", "a2")
        if theme != "" && path_is_dir(path_join(a2.paths.resources, theme))
            return theme
    }
    if IsSet(a2_theme)
        return a2_theme
    return ""
}

/**
 * Get system "theme" name. As in: is set to "light" or "dark"?
 * @returns {(String)}
 */
theme_get_system() {
    if windows_is_dark()
        return "dark"
    return "light"
}

/**
 * Set the theme to be used.
 * @param {(String)} [theme_name] - Name of the theme to take.
 * Leave empty to return to system theme (Default)
 */
theme_set(theme_name := "") {
    if !theme_name {
        if IsSet(a2)
            a2.db.delete("theme", "a2")
        if IsSet(a2_theme) {
            global a2_theme
            a2_theme := ""
        }
        return
    }

    theme_path := theme_get_path(theme_name)
    if !path_is_dir(theme_path)
        throw Error("No such theme '" theme_name "'!")

    if IsSet(a2) {
        a2.db.set("theme", theme_name, "a2")
        return
    }
    a2tip('No global a2 object! Can only set theme temporarily for current runtime')
    global a2_theme
    a2_theme := theme_name
}

/**
 * Lookup set theme config for its 'is_dark' flag.
 * For things that we cannot set directly with colors but need Windows support like window title bars and menus.
 * @param {(String)} [theme_name] - Optional name of theme to get colors from. (Default: auto gets theme name).
 * @returns {(Boolean)}
 */
theme_is_dark(theme_name := "") {
    if theme_name == ""
        theme_name := theme_get()
    config := Jxon_Read(path_join(theme_get_path(theme_name), 'config.json'))
    return config['is_dark']
}

/**
 *
 * @param {(String)} [theme_name] - Optional name of theme to get colors from. (Default: auto gets theme name).
 * @returns {(Object)}
 */
theme_get_colors(theme_name := "") {
    if theme_name == ""
        theme_name := theme_get()
    color_map := Jxon_Read(path_join(theme_get_path(theme_name), 'colors.json'))
    color_obj := {}
    for key, value in color_map {
        color_obj.%key% := LTrim(value, "#")
    }
    return color_obj
}


theme_get_path(theme_name) {
    if IsSet(a2)
        return path_join(a2.paths.resources, theme_name)
    return path_join(path_dirname(A_LineFile, 4), 'theme', theme_name)
}
