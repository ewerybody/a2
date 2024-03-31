#SingleInstance Force
#Warn All, StdOut
FileEncoding("UTF-8")

global ahu := AutoHotUnitManager(AutoHotUnitCLIReporter())

class AutoHotUnitSuite {
    assert := AutoHotUnitAsserter()

    ; Executed once before any tests execute
    beforeAll() {
    }

    ; Executed once before each test is executed
    beforeEach() {
    }

    ; Executed once after each test is executed
    afterEach() {
    }

    ; Executed once after all tests have executed
    afterAll() {
    }
}

class AutoHotUnitManager {
    Suite := AutoHotUnitSuite
    suites := []

    __New(reporter) {
        this.reporter := reporter
    }

    RegisterSuite(SuiteSubclasses*)
    {
        for i, subclass in SuiteSubclasses {
            this.suites.push(subclass)
        }
    }

    RunSuites() {
        this.reporter.onRunStart()
        for i, suiteClass in this.suites {
            suiteInstance := suiteClass()
            suiteName := suiteInstance.__Class
            this.reporter.onSuiteStart(suiteName)
            
            testNames := []
            for propertyName in suiteInstance.base.OwnProps() {
                ; If the property name starts with an underscore, skip it
                underScoreIndex := InStr(propertyName, "_")
                if (underScoreIndex == 1) {
                    continue
                }

                ; If the property name is one of the Suite base class methods, skip it
                if (propertyName == "beforeAll" || propertyName == "beforeEach" || propertyName == "afterEach" || propertyName == "afterAll") {
                    continue
                }

                if (GetMethod(suiteInstance, propertyName) is Func) {
                    testNames.push(propertyName)
                }
            }



            try {
                suiteInstance.beforeAll()
            } catch Error as e {
                this.reporter.onTestResult("beforeAll", "failed", "", e)
                continue
            }

            for j, testName in testNames {
                try {
                    suiteInstance.beforeEach()
                } catch Error as e {
                    this.reporter.onTestResult(testName, "failed", "beforeEach", e)
                    continue
                }

                try {
                    local method := GetMethod(suiteInstance, testName)
                    
                    method(suiteInstance)
                } catch Error as e {
                    this.reporter.onTestResult(testName, "failed", "test", e)
                    continue
                }

                try {
                    suiteInstance.afterEach()
                } catch Error as e {
                    this.reporter.onTestResult(testName, "failed", "afterEach", e)
                    continue
                }

                this.reporter.onTestResult(testName, "passed", "", "")
            }

            try {
                suiteInstance.afterAll()
            } catch Error as e {
                this.reporter.onTestResult("afterAll", "failed", "", e)
                continue
            }

            this.reporter.onSuiteEnd(suiteName)
        }
        this.reporter.onRunComplete()
    }
}

class AutoHotUnitCLIReporter {
    currentSuiteName := ""
    failures := []
    red := "[31m"
    green := "[32m"
    reset := "[0m"

    printLine(str) {
        FileAppend(str, "*", "UTF-8")
        FileAppend("`r`n", "*")
    }

    onRunStart() {
        this.printLine("Starting test run`r`n")
    }

    onSuiteStart(suiteName) {
        this.printLine(suiteName ":")
        this.currentSuiteName := suiteName
    }
    
    onTestStart(testName) {
    }

    onTestResult(testName, status, where, error) {
        if (status != "passed" && status != "failed") {
            throw Error("Invalid status: " . status)
        }

        prefix := this.green . "."
        if (status == "failed") {
            prefix := this.red . "x"
        }

        this.printLine("  " prefix " " testName " " status this.reset)
        if (status == "failed") {
            this.printLine(this.red "      " error.Message this.reset)
            this.failures.push(this.currentSuiteName "." testName " " where " failed:`r`n  " error.Message)
        }
    }

    onSuiteEnd(suiteName) {
    }

    onRunComplete() {
        this.printLine("")
        postfix := "All tests passed." 
        if (this.failures.Length > 0) {
            postfix := this.failures.Length . " test(s) failed."
        }
        this.printLine("Test run complete. " postfix)

        if (this.failures.Length > 0) {
            this.printLine("")
        }

        for i, failure in this.failures {
            this.printLine(this.red failure this.reset)
        }

        Exit(this.failures.Length)
    }
}

class AutoHotUnitAsserter {
    static deepEqual(actual, expected) {
        if (actual is Array && expected is Array) {
            if (actual.Length != expected.Length) {
                return false
            }

            for i, actualItem in actual {
                if (!this.deepEqual(actualItem, expected[i])) {
                    return false
                }
            }

            return true
        }

        return actual == expected
    }

    static getPrintableValue(value) {
        if (value is Array) {
            str := "["
            for i, item in value {
                if (i > 1) {
                    str .= ", "
                }
                str .= this.getPrintableValue(item)
            }
            str .= "]"
            return str
        }

        return value
    }

    equal(actual, expected) {
        if (!AutoHotUnitAsserter.deepEqual(actual, expected)) {
            throw Error("Assertion failed: " . AutoHotUnitAsserter.getPrintableValue(actual) . " != " . AutoHotUnitAsserter.getPrintableValue(expected))
        }
    }

    notEqual(actual, expected) {
        if (actual == expected) {
            throw Error("Assertion failed: " . actual . " == " . expected)
        }
    }

    isTrue(actual) {
        if (actual != true) {
            throw Error("Assertion failed: " . actual . " is not true")
        }
    }

    isFalse(actual) {
        if (actual == true) {
            throw Error("Assertion failed: " . actual . " is not false")
        }
    }

    isEmpty(actual) {
        if (actual != "") {
            throw Error("Assertion failed: " . actual . " is not empty")
        }
    }

    notEmpty(actual) {
        if (actual == "") {
            throw Error("Assertion failed: " . actual . " is empty")
        }
    }

    fail(message) {
        throw Error("Assertion failed: " . message)
    }
    
    isAbove(actual, expected) {
        if (actual <= expected) {
            throw Error("Assertion failed: " . actual . " is not above " . expected)
        }
    }

    isAtLeast(actual, expected) {
        if (actual < expected) {
            throw Error("Assertion failed: " . actual . " is not at least " . expected)
        }
    }

    isBelow(actual, expected) {
        if (actual >= expected) {
            throw Error("Assertion failed: " . actual . " is not below " . expected)
        }
    }

    isAtMost(actual, expected) {
        if (actual > expected) {
            throw Error("Assertion failed: " . actual . " is not at most " . expected)
        }
    }
}