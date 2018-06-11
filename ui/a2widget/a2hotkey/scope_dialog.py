import a2core
import a2ctrl
from PySide import QtGui, QtCore

from . import scope_dialog_ui
from .hotkey_widget import Vars


log = a2core.get_logger(__name__)
SCOPE_ITEMS = ['titles', 'classes', 'processes']


class ScopeDialog(QtGui.QDialog):
    okayed = QtCore.Signal(dict)

    def __init__(self, parent, config):
        super(ScopeDialog, self).__init__(parent)
        a2ctrl.check_ui_module(scope_dialog_ui)
        self.ui = scope_dialog_ui.Ui_ScopeDialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Setup Scope')
        self.ui.scope_widget.set_config(config)
        self.ui.scope_widget.changed.connect(self.check)
        self.ui.display_only_label.setVisible(not config.get(Vars.scope_change, False))

        self.ui.a2ok_button.clicked.connect(self.ok)
        self.ui.a2cancel_button.clicked.connect(self.reject)

    def showEvent(self, *args, **kwargs):
        self.ui.scope_widget.setMinimumWidth(self.minimumSizeHint().height() * 3)
        return QtGui.QDialog.showEvent(self, *args, **kwargs)

    def check(self):
        cfg = self.ui.scope_widget.get_config()
        if not cfg[Vars.scope]:
            if cfg[Vars.scope_mode] == 1:
                self.ui.a2ok_button.setEnabled(False)
                self.ui.a2ok_button.setText('Include "nothing" Deativates the scope!')
                return
            elif cfg[Vars.scope_mode] == 2:
                self.ui.a2ok_button.setEnabled(False)
                self.ui.a2ok_button.setText('Exclude "nothing" makes it global!')
                return
        self.ui.a2ok_button.setText('OK')
        self.ui.a2ok_button.setEnabled(True)

    def ok(self):
        cfg = self.ui.scope_widget.get_config()
        self.okayed.emit(cfg)
        self.accept()
