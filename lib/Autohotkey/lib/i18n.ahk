#Include <jxon>

/**
 * Get locale dictionary for the calling module.
 *
 * ⚠️ Always use A_LineFile (not A_ScriptDir or A_WorkingDir) to reference
 * paths relative to the current file! A_ScriptDir points to the main
 * entry script, which may be a temp file or a different location entirely.
 * @param {(String)} caller_file
 * Script path from `A_LineFile` variable to find localization files.
 * that should be right next in `i18n` folder.
 * @param {(String)} [_language]
 * For **testing purposed** only! Force a language to be used.
 * @returns {(Map)}
 */
i18n_locale(caller_file, _language := "") {
    SplitPath(caller_file, , &module_dir)
    i18n_dir := module_dir "\i18n"
    if !DirExist(i18n_dir)
        throw Error('No "i18n" directory at "' i18n_dir '"!')

    _language := i18n_get_language(_language)
    return _i18n_load(
        i18n_dir "\en.json",
        i18n_dir "\" _language ".json",
        "locale at '" module_dir "'"
    )
}

/**
 * Get locale dictionary for given domain of calling module.
 * @param {(String)} domain
 * Topic of the translations to get.
 * @param {(String)} [caller_file]
 * Optionally pass `A_LineFile` to get translation from local "i18n\en\domain.json".
 * @param {(String)} [_language]
 * For **testing purposed** only! Force a language to be used.
 * @returns {(Map)}
 */
i18n_domain(domain, caller_file := "", _language := "") {
    i18n_dir := _i18n_domain_dir(caller_file)
    if !DirExist(i18n_dir)
        throw Error('No "i18n" directory at "' i18n_dir '"!')

    _language := i18n_get_language(_language)
    return _i18n_load(
        i18n_dir "\en\" domain ".json",
        i18n_dir "\" _language "\" domain ".json",
        "domain '" domain "'"
    )
}

/**
 * Get the language to use.
 * * passed right away
 * * set by the user
 * * from system settings (default fallback)
 * @param {(String)} [language]
 * Optional language id string like "en-US" to force a language to be used.
 * @returns {(String)}
 * Resulting language id string.
 */
i18n_get_language(language := "") {
    if language != ""
        return language

    language := i18n_get_user_language()
    if language != ""
        return language

    language := i18n_get_system_language()
    return language
}

/**
 * Get the language from user settings is set.
 * @returns {(String)}
 * Resulting language id string.
 */
i18n_get_user_language() {
    if IsSet(a2) {
        language := a2.db.get("language", "a2")
        if language != ""
            return language
    }
    return ""
}

/**
 * Get the language from system settings.
 * @returns {(String)}
 * Resulting language id string.
 */
i18n_get_system_language() {
    buf := Buffer(16, 0)
    DllCall("GetUserDefaultLocaleName", "Ptr", buf, "Int", 16)
    return SubStr(StrGet(buf), 1, 2)
}

_i18n_load(en_path, lang_path, error_context) {
    if !FileExist(en_path)
        throw Error('No english i18n-file at "' en_path '"! We ALWAYS need a basic english file!')

    en_obj := Jxon_Read(en_path)

    ; If language is "en" the two paths are the same, already handled by caller
    if !FileExist(lang_path)
        return en_obj

    obj := Jxon_Read(lang_path)
    _i18n_patch_object(&en_obj, &obj)
    if obj is Map
        return obj

    throw Error("i18n: could not load " error_context)
}

_i18n_patch_object(&obj1, &obj2) {
    for key, value in obj1 {
        if (!obj2.has(key)) {
            obj2[key] := value
        } else if (obj2[key] == "") {
            obj2[key] := value
        }
    }
}

_i18n_domain_dir(caller_file) {
    if caller_file != "" {
        SplitPath(caller_file, , &module_dir)
        return module_dir "\i18n"
    }
    if IsSet(a2)
        return a2.paths.a2 "\i18n"
    SplitPath(A_LineFile, , &dir_path)
    SplitPath(dir_path, , &dir_path)
    SplitPath(dir_path, , &dir_path)
    SplitPath(dir_path, , &dir_path)
    return dir_path "\i18n"
}
