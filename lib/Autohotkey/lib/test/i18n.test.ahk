#Requires AutoHotkey v2.0
#NoTrayIcon
#Include <i18n>

class I18nTests {
    class Locale {
        load_locale_en() {
            t := i18n_locale(A_LineFile, "en")
            expect := "Welcome to the i18n test!"
            result := Format(t["welcome"], "the i18n test")
            if (result != expect)
                throw Error("Got: '" result "' expected: '" expect "'!")
        }
        load_locale_de() {
            t := i18n_locale(A_LineFile, "de")
            expect := "Willkommen beim i18n test!"
            result := Format(t["welcome"], "i18n test")
            if (result != expect)
                throw Error("Got: '" result "' expected: '" expect "'!")

            if !t.has("only_english")
                throw Error('German dictionary should have missing keys replaced!!')

            t_en := i18n_locale(A_LineFile, "en")
            if (t["only_english"] != t_en["only_english"])
                throw Error('German dictionary should have same replaced missing keys!!')

            if t['umlauts'] != "Ümläüts Ök?"
                throw Error('Error reading umlauts!!')
        }

        no_english_file_throws() {
            try
                i18n_locale("C:\nonexistent\path\file.ahk", "en")
            catch Error
                return
            throw Error("Missing i18n dir should throw!")
        }

        empty_string_key_gets_patched() {
            t := i18n_locale(A_LineFile, "de")
            t_en := i18n_locale(A_LineFile, "en")
            if (t["empty_in_german"] != t_en["empty_in_german"])
                throw Error("Empty string key should fall back to English value!")
        }
    }

    class Domain {
        load_correct_string() {
            t := i18n_domain("i18n",, _language := "en")
            expect := "translation"
            if (t["translation"] != expect)
                throw Error('Expected "' expect '", got: "' t["translation"] '"')
        }

        fall_back_to_english() {
            ; assuming language "xx" doesn't exist
            t := i18n_domain("test", A_LineFile, _language := "xx")
            if (!t.Has("english_fallback"))
                throw Error("Fallback to English failed")
        }

        no_such_domain() {
            try
                t := i18n_domain("sdfglvks")
            catch Error
                return
            throw Error("Looking up inexistent domain should break!")
        }
    }

    class Language {
        explicit_overrides_system() {
            lang := i18n_get_language("fr")
            if (lang != "fr")
                throw Error("Explicit language should take priority!")
        }

        system_language_is_two_chars() {
            lang := i18n_get_system_language()
            if (StrLen(lang) != 2)
                throw Error("System language should be 2 chars, got: '" lang "'")
        }

        unknown_language_falls_back_to_english() {
            t := i18n_locale(A_LineFile, "xx")
            t_en := i18n_locale(A_LineFile, "en")
            if (t["welcome"] != t_en["welcome"])
                throw Error("Unknown language should silently fall back to English!")
        }
    }
}
