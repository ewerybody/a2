from functools import partial
from a2widget import a2input_dialog
from a2widget import busy_icon
from a2qt import QtWidgets, QtCore

class AboutDialog(a2input_dialog.A2ConfirmDialog):
    def __init__(self, parent):
        msg = '...'
        super().__init__(parent, 'About a2', msg)

        self.setWindowFlags(a2input_dialog.FIXED_FLAGS)
        # dialog.okayed.connect(self.confirm_dialog_okayed)
        # dialog.canceled.connect(self.confirm_dialog_canceled)
        self.show()
        QtCore.QTimer(self).singleShot(500, self._add_text)

    def _add_text(self):
        current = self.ui.label.text()
        current += 'EXTRA_TEXTEXTRA_TEXTEXTRA_TEXTEXTRA_TEXTEXTRA_TEXTEXTRA_TEXT'

        button = QtWidgets.QPushButton('HHaaallo')
        button.setMinimumHeight(100)
        self.ui.main_layout.addWidget(button)
        self.ui.label.setText(current)
