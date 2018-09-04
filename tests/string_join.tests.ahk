#include %A_ScriptDir%\..\lib\Autohotkey\lib\string_join.ahk

new StringJoinTestSuite()
return

class StringJoinTestSuite extends AhkUnit {
    beforeEach() {
        this.things := ["a", "b", "c"]
    }

    Test_NoSeparatorArgument() {
        d := this.describe("without argument for Separator")

        string := string_join(this.things)

        d.it("string should be 'a, b, c'").expect(string).toBe("a,b,c")
    }

    Test_CustomSeparatorArgument() {
        d := this.describe("with argument for Separator")

        string := string_join(this.things, "||")

        d.it("string should be 'a||b||c'").expect(string).toBe("a||b||c")
    }
}
