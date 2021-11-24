import os
import time
from functools import partial

import a2mod
import a2util
from a2ctrl import Icons
from a2qt import QtGui, QtCore, QtWidgets


MSG_DEFAULT = 'Appears everything is on "factory settings"!'
MSG_USER_CHANGES = 'This will throw away any user changes!\n'
MSG_JSON_ERROR = 'There was a problem loading data from the json file!\n\n'
_MSG_NEEDS = (
    'We need a dictionary with non-empty string keys!\nPlease make sure this is valid data!'
)
MSG_IMPORT_ERROR = (
    'Could not get valid data from the given file!\n' + _MSG_NEEDS
)


class ModuleConfig(QtCore.QObject):
    reload_requested = QtCore.Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.main = parent

    @property
    def mod(self) -> a2mod.Mod:
        mod = self.main.mod
        if mod is None:
            raise RuntimeError('There is no single module selected!')
        return mod

    @property
    def a2(self):
        return self.main.a2

    def export(self):
        user_cfg = self.mod.get_user_cfg()
        if not user_cfg:
            from a2widget.a2input_dialog import A2ConfirmDialog

            dialog = A2ConfirmDialog(self, 'Nothing to Export!', msg=MSG_DEFAULT)
            dialog.show()
            return

        name = f'{self.mod.name}_settings.json'
        path = os.path.join(self.a2.paths.a2, name)
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.main, 'Export Module Settings', path, 'JSON (*.json)'
        )
        if not file_path:
            return

        a2util.json_write(file_path, user_cfg)

    def load(self):
        from a2widget.a2input_dialog import A2ConfirmDialog

        current_cfg = self.mod.get_user_cfg()
        if current_cfg:
            msg = 'Are you sure you want to do this?\n' + MSG_USER_CHANGES + _MSG_NEEDS
            dialog = A2ConfirmDialog(self.main, 'Import User Settings', msg=msg)
            dialog.okayed.connect(self._on_import)
            dialog.show()

    def _on_import(self):
        name = f'{self.mod.name}_settings.json'
        path = os.path.join(self.a2.paths.a2, name)
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.main, 'Import Module Settings', path, 'JSON (*.json)'
        )
        if not file_path:
            return

        import json
        import traceback
        from a2widget.a2input_dialog import A2ConfirmDialog

        try:
            user_cfg = a2util.json_read(file_path)
        except json.JSONDecodeError:
            report = traceback.format_exc().strip()
            dialog = A2ConfirmDialog(self, 'JSONDecodeError!', msg=MSG_JSON_ERROR + report)
            dialog.show()
            return

        if not user_cfg or not isinstance(user_cfg, dict) or any(not key for key in user_cfg):
            dialog = A2ConfirmDialog(self, 'Error!', msg=MSG_IMPORT_ERROR)
            dialog.show()
            return

        self.mod.set_user_cfg(user_cfg)
        self.reload_requested.emit()

    def revert(self):
        from a2widget.a2input_dialog import A2ConfirmDialog

        module_user_cfg = self.mod.get_user_cfg()
        if module_user_cfg:
            dialog = A2ConfirmDialog(self.main, 'Revert User Settings', msg=MSG_USER_CHANGES)
            dialog.okayed.connect(self._on_revert)
            dialog.show()
        else:
            dialog = A2ConfirmDialog(self.main, 'Nothing to Revert!', msg=MSG_DEFAULT)
            dialog.show()

    def _on_revert(self):
        self.mod.clear_user_cfg()
        self.reload_requested.emit()

    def build_rollback_menu(self):
        menu = self.main.ui.menuRollback_Changes
        menu.clear()
        backups_sorted = self.mod.get_config_backups()
        if not backups_sorted:
            action = menu.addAction('Nothing to roll back to!')
            action.setEnabled(False)
        else:
            now = time.time()
            for this_time, backup_name in backups_sorted[:15]:
                try:
                    label = a2util.unroll_seconds(now - this_time, 2)
                    label = 'version %s - %s ago' % (
                        int(backup_name[-1]),
                        label,
                    )
                except ValueError:
                    continue
                action = menu.addAction(Icons.rollback, label, self.module_rollback_to)
                action.setData(backup_name)
            menu.addSeparator()
            menu.addAction(Icons.delete, 'Clear Backups', self.mod.clear_backups)

    def module_rollback_to(self):
        action = self.sender()
        if not isinstance(action, QtGui.QAction):
            return
        title = action.text()
        file_name = action.data()
        file_path = os.path.join(self.mod.backup_path, file_name)

        from a2dev import RollbackDiffDialog

        dialog = RollbackDiffDialog(self.main, title, self.mod.config_file, file_path)
        dialog.okayed.connect(partial(self.on_rollback, file_name))
        dialog.show()

    def on_rollback(self, file_name):
        self.mod.rollback(file_name)
        self.reload_requested.emit()
