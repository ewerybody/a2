import typing
import a2core
import a2mod
import a2app
import a2style

import a2widget.a2module_list
import a2widget.a2module_view
from a2qt import QtGui, QtCore, QtWidgets


A2DEFAULT_HOTKEY: str
EDIT_DISCLAIMER: str

class A2Window(QtWidgets.QMainWindow):
    a2: a2core.A2Obj
    app: a2app.A2App
    temp_config: typing.Dict[str, typing.Dict]
    style: a2style.A2StyleBuilder | None
    mod: typing.Optional[a2mod.Mod] = None
    selected: list[a2mod.Mod] = []

    def __init__(self, app: a2app.A2App): ...
    def _module_selected(self, module_list: list[a2mod.Mod]) -> None: ...
    def show_raise(self) -> None: ...
    def load_runtime_and_ui(self) -> None: ...


class RuntimeCallThread(QtCore.QThread): ...
class RuntimeWatcher(QtCore.QThread): ...
