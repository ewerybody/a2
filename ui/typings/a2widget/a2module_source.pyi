import a2ui
import a2modsource
from a2qt import QtWidgets

class ModSourceWidget(QtWidgets.QWidget):
    mod_source: a2modsource.ModSource
    def __init__(
        self, main: a2ui.A2Window, mod_source: a2modsource.ModSource, show_enabled: bool
    ) -> ModSourceWidget: ...
