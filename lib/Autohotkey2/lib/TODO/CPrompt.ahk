/**
 * Object to Prompt the user for input
 *
 * Usage:
 *     prompt := new Prompt()           ; Ensure a new - unsused - instance of Prompt is being used
 *     Prompt.Cancel := true            ; Add "Cancel" button to UI
 *     Prompt.Placeholder := ""         ; Set a placeholder in the text area
 *     Prompt.DataType := "Text"        ; Set input type. Can be: Text (default), Path, File, Number, Time, Selection
 *     Prompt.Validation := true        ; Validate field before allow user to click "OK"
 *     Prompt.Title := "Select file"    ; Title of the Prompt window
 *     Prompt.Text := "choose you file" ; Text to display in the Prompt window
 *     Prompt.Width := 200              ; Width of the Prompt window
 *     Prompt.Rows := 1                 ; Rows the Prompt windows shoud have in height
 *     Prompt.prompt()                  ; Execute the Prompt
 */
 global Prompt := new CPrompt()
class CPrompt
{
    static Cancel := false
    static Placeholder := "Input"
    static DataType := "Text"
    static Validate := true
    static Selection := "Default Selection"
    static Text := ""
    static Title := ""
    static Width := 200
    static Rows := 1
    response := false

    /**
     * entry point:
     *     This method calls the UI and waits for the response
     */
    prompt()
    {
        this.response := false
        this.DisplayDialog()

        While (!this.response)
            sleep 50
        return this.response
    }

    /**
     * Build UI to show to the user
     */
    DisplayDialog()
    {
        Title := this.Title
        Text  := this.Text
        GuiNum:=GetFreeGUINum(1, "InputBox")
        this.tmpGuiNum := GuiNum
        StringReplace, Text, Text, ``n, `n
        Gui,%GuiNum%:Destroy
        Gui,%GuiNum%:Add,Text,y10,%Text%

        if (this.DataType = "Text" || this.DataType = "Path" || this.DataType = "File")
        {
            Gui,%GuiNum%:Add, Edit, % "x+10 yp-4 w" this.Width " hwndEdit gAction_Input_Edit" (this.Rows > 1 ? " R" this.Rows " Multi" : "")
            this.tmpEdit := Edit
            if (this.DataType = "Path" || this.DataType = "File")
            {
                Gui,%GuiNum%:Add, Button, x+10 w80 hwndButton gInputBox_Browse, Browse
                this.tmpButton := Button
            }
        }
        else if (this.DataType = "Number")
        {
            Gui,%GuiNum%:Add, Edit, x+10 yp-4 w200 hwndEdit Number
            this.tmpEdit := Edit
        }
        else if (this.DataType = "Time")
        {
            Gui, %GuiNum%:Add, Edit, x+2 yp-4 w30 hwndHours Number, 00
            Gui, %GuiNum%:Add, Text, x+2 yp+4, :
            Gui, %GuiNum%:Add, Edit, x+2 yp-4 w30 hwndMinutes Number, 10
            Gui, %GuiNum%:Add, Text, x+2 yp+4, :
            Gui, %GuiNum%:Add, Edit, x+2 yp-4 w30 hwndSeconds Number, 00
            this.tmpHours := Hours
            this.tmpHours := Minutes
            this.tmpSeconds := Seconds
        }
        else if (this.DataType = "Selection")
        {
            Selection := this.Selection
            Loop, Parse, Selection, |
            {
                Gui, %GuiNum%:Add, Radio, % "hwndRadio" (A_Index = 1 ? " Checked" : ""), %A_LoopField%
                this["tmpRadio" A_Index] := Radio
            }
        }
        ; ~ Gui, %GuiNum%:Add, Text, x+-80 y+10 hwndTest, test
        ; ~ ControlGetPos, PosX, PosY,,,,ahk_id %Test%
        ; ~ WinKill, ahk_id %Test%

        Gui, %GuiNum%:Show, Autosize Hide
        Gui, %GuiNum%:+LastFound
        x := max(window_get_geometry(WinExist()).w - (this.Cancel ? 180 : 90), 10)
        Gui, %GuiNum%:Add, Button, % "Default x" x " y+10 w80 hwndhOK gInputBox_OK " (this.Validate && (this.DataType = "Text" || this.DataType = "Path" || this.DataType = "File") ? "Disabled" : ""), OK
        if (this.Cancel)
            Gui, %GuiNum%:Add, Button, x+10 w80 gInputBox_Cancel, Cancel
        Gui,%GuiNum%:-MinimizeBox -MaximizeBox +LabelInputbox
        Gui,%GuiNum%:Show,Autosize,%Title%

        return
    }

    /**
     * Callback function for when the user clicks on "Browse"
     */
    InputBoxBrowse()
    {
        if (this.DataType = "Path")
        {
            FileSelectFolder, result,, 3, Select Folder
            if (!Errorlevel)
                ControlSetText, Edit1, %result%, A
        }
        else if (this.DataType = "File")
        {
            FileSelectFile, result,,, Select File
            if (!Errorlevel)
                ControlSetText, Edit1, %result%, A
        }
    }

    /**
     * Callback function for when the user uses a Text field
     */
    InputBoxEdit()
    {
        if (this.Validate)
        {
            ControlGetText, input, Edit1
            if (this.DataType = "Text")
            {
                if (input = "")
                    Control, Disable,, Button1
                else
                    Control, Enable,, Button1
            }
            else if (this.DataType = "File" || this.DataType = "Path")
            {
                if (FileExist(input))
                    Control, Enable,, Button2
                else
                    Control, Disable,, Button2
            }
        }
    }

    /**
     * Callback function to close Prompt GUI
     */
    InputBoxCancel()
    {
        if (!this.Cancel)
            return
        Gui, Destroy

        this.response := -1

        return
    }

    /**
     * Callback function for when the user clicks on "OK"
     */
    InputBoxOK()
    {
        if (this.DataType = "Text" || this.DataType = "Number" || this.DataType = "Path" || this.DataType = "File")
            ControlGetText, input, Edit1
        else if (this.DataType = "Time")
        {
            ControlGetText, Hours, Edit1
            ControlGetText, Minutes, Edit2
            ControlGetText, Seconds, Edit3
            input := (SubStr("00" Hours, -1) ":" SubStr("00" Minutes, -1) ":" SubStr("00" Seconds, -1))
        }
        else if (this.DataType = "Selection")
        {
            Loop
            {
                ControlGet, Selected, Checked, , , % "ahk_id " this["tmpRadio" A_Index]
                if (Errorlevel)
                    break
                if (Selected)
                {
                    ControlGetText, input, , % "ahk_id " this["tmpRadio" A_Index]
                    break
                }
            }
        }
        Gui, Destroy

        this.response := input
        return
    }
}

Action_Input_Edit:
    Prompt.InputBoxEdit()
return
InputBox_Browse:
    Prompt.InputBoxBrowse()
return
InputboxClose:
InputboxEscape:
InputBox_Cancel:
    Prompt.InputBoxCancel()
return
InputBox_OK:
    Prompt.InputBoxOK()
return
