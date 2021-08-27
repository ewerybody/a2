import typing
import a2core
import a2mod

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

    def __init__(self):
        self.mod: typing.Optional[a2mod.Mod] = None
        self.selected: list[a2mod.Mod] = []

    def _module_selected(self, module_list: list[a2mod.Mod]) -> None: ...
