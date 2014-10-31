;don't bother editing - file is generated automatically
#IfWinActive,
#!c::a2UI()
#r::winr()
^+w::getWinfo()
^!B::BBCodeMenu()

#IfWinActive, ahk_class #32770
#o::pasteColor()
#IfWinActive, ahk_class TConversationForm
F4::skypeSnapshotKey()
#IfWinActive, ahk_class CabinetWClass
!v::ftpExplorerCopy()