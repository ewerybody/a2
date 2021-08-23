# import logging
import typing
import a2core
import a2mod

from a2widget import a2module_view
from a2qt import QtGui, QtCore, QtWidgets
from singlesiding import QSingleApplication

A2DEFAULT_HOTKEY: str
EDIT_DISCLAIMER: str

class A2Window(QtWidgets.QMainWindow):
    a2: a2core.A2Obj
    app: QSingleApplication
    temp_config: typing.Dict[str, typing.Dict]
    mod: typing.Optional[a2mod.Mod] = None
    module_view: a2module_view.A2ModuleView
