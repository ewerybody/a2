; a2test.ahk - AHK v2 unit test runner library
;
; Provides A2Test(name, fn) used by run_ahk_tests.py generated scripts.
; run_ahk_tests.py parses *.test.ahk source to discover test methods and
; generates explicit A2Test() calls — no AHK runtime reflection needed.
;
; Test convention (AHKUnit-compatible):
;   - Tests are methods in a class; throw Error = fail, return = pass.
;   - Methods starting with _ are skipped.
;
#Requires AutoHotkey v2.0

; Run a single named test (a zero-arg callable).
; Prints result to stdout. Returns 0 (pass) or 1 (fail).
A2Test(name, fn, indentation) {
    try {
        fn.Call()
        FileAppend(indentation "✅ PASS: " name "`n", "*", "UTF-8")
        return 0
    } catch Error as e {
        msg := indentation "❌ FAIL: " name "`n"
        msg .= indentation "   " e.Message "`n"
        msg .= indentation "   " e.File " (" e.Line ")`n"
        FileAppend(msg, "*", "UTF-8")
        return 1
    }
}

A2TestClass(name, indentation) {
    FileAppend(indentation "• " name "`n", "*", "UTF-8")
}

A2Results(fails, total) {
    FileAppend(" > Passed/Failed: " total - fails "/" fails " out of: " total "`n", "*", "UTF-8")
}

assertmsg(result) {
    if result
        return "✔️"
    return "❌"
}
