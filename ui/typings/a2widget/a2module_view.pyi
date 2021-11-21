import a2ui
import a2modsource
import a2module_editor
from a2qt import QtWidgets, QtCore
from a2widget import a2module_view_ui

class A2ModuleView(QtWidgets.QWidget):
    mod_source: a2modsource.ModSource
    okayed: QtCore.Signal
    reload_requested: QtCore.Signal
    enable_request: QtCore.Signal
    edit_mode: QtCore.Signal
    ui: a2module_view_ui.Ui_A2ModuleView
    editing: bool
    editor: a2module_editor.EditView
    menu_items: list


    def __init__(self, parent: QtWidgets.QWidget) -> None: ...
    def draw_mod(self): ...
    def edit_mod(self): ...
    def get_cfg_copy(self) -> list: ...
    def help(self): ...
    def setup_ui(self, parent: QtWidgets.QWidget) -> None: ...
    def update_header(self, author: str = '', version: str = '') -> None: ...
    def cfg_different(self) -> bool: ...
    def user_cancels(self) -> bool: ...
    def check_element(self, name: str) -> None: ...
