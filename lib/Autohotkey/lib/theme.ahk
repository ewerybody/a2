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

theme_get_system() {
    if windows_is_dark()
        return "dark"
    return "light"
}

/**
 * Set the theme to be used.
 * @param {(String)} theme_name - Name of the theme to take.
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

    theme_path := IsSet(a2) ? path_join(a2.paths.resources, theme_name) : path_join(path_dirname(A_LineFile, 4), 'theme', theme_name)
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

theme_is_dark() {
    theme_name := theme_get()
    theme_path := IsSet(a2) ? path_join(a2.paths.resources, theme_name) : path_join(path_dirname(A_LineFile, 4), 'theme', theme_name)
    config := Jxon_Read(path_join(theme_path, 'config.json'))
    return config['is_dark']
}