import a2ui
import a2modsource
from a2qt import QtWidgets

class A2ModuleView(QtWidgets.QWidget):
    mod_source: a2modsource.ModSource
    def __init__(self, parent: a2ui.A2Window) -> A2ModuleView: ...
