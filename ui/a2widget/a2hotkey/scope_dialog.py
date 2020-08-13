"""
Home of the Scope Dialog ui.
"""
from PySide2 import QtCore, QtWidgets

import a2core
import a2ctrl

from . import scope_dialog_ui
from .hotkey_widget import Vars



log = a2core.get_logger(__name__)
INCLUDE_MSG = 'Include "nothing" Deactivates the scope!'
EXCLUDE_MSG = 'Exclude "nothing" makes it global!'


class ScopeDialog(QtWidgets.QDialog):
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
        return QtWidgets.QDialog.showEvent(self, *args, **kwargs)

    def check(self):
        cfg = self.ui.scope_widget.get_config()
        if not cfg.get(Vars.scope):
            if cfg[Vars.scope_mode] == 1:
                self.ui.a2ok_button.setEnabled(False)
                self.ui.a2ok_button.setText(INCLUDE_MSG)
                return
            if cfg[Vars.scope_mode] == 2:
                self.ui.a2ok_button.setEnabled(False)
                self.ui.a2ok_button.setText(EXCLUDE_MSG)
                return
        self.ui.a2ok_button.setText('OK')
        self.ui.a2ok_button.setEnabled(True)

    def ok(self):
        cfg = self.ui.scope_widget.get_config()
        self.okayed.emit(cfg)
        self.accept()


def get_changable_no_global(parent, cfg=None):
    if cfg is None:
        cfg = {Vars.scope_change: True}
    elif isinstance(cfg, dict):
        cfg[Vars.scope_change] = True
    else:
        raise TypeError('Unusable config type "%s"' % type(cfg))

    dialog = ScopeDialog(parent, cfg)
    dialog.ui.scope_widget.hide_global_button()
    return dialog
