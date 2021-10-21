import typing
import a2core
import a2mod
import a2app
import a2style

import a2widget.a2module_list
import a2widget.a2module_view
from a2qt import QtGui, QtCore, QtWidgets
from singlesiding import QSingleApplication

A2DEFAULT_HOTKEY: str
EDIT_DISCLAIMER: str

class A2Window(QtWidgets.QMainWindow):
    a2: a2core.A2Obj
    app: QSingleApplication
    temp_config: typing.Dict[str, typing.Dict]
    style: a2style.A2StyleBuilder | None

    def __init__(self, app: a2app.A2App):
        self.mod: typing.Optional[a2mod.Mod] = None
        self.selected: list[a2mod.Mod] = []

    def _module_selected(self, module_list: list[a2mod.Mod]) -> None: ...

    def show_raise(self) -> None: ...