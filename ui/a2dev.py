"""a2 Developer stuff."""
import os
from a2qt import QtWidgets, QtCore

import a2core
import a2util

from a2widget.a2input_dialog import A2ConfirmDialog

_TASK_MSG = 'browse for a %s executable'
_QUEST_MSG = 'Do you want to %s now?'
log = a2core.get_logger(__name__)
MSG_CFG_DIFF = (
    'The module configuration appears to have changed!\n'
    'Do you really want to exit and discard the changes?\n\n'
    'You can also have a look at the differences...'
)
MSG_CFG_NEW = (
    'The module configuration appears to be new!\n'
    'Do you really want to exit and discard the changes?'
)


class OkDiffDialog(A2ConfirmDialog):
    diff_requested = QtCore.Signal()

    def __init__(self, parent, title, msg, file_path1=None, file_path2=None):
        super(OkDiffDialog, self).__init__(
            parent,
            title,
            msg,
        )

        self.file_path1 = file_path1
        self.file_path2 = file_path2

        if self.file_path1 is not None:
            button = QtWidgets.QPushButton('Diff', self)
            button.setObjectName('a2ok_button')
            button.clicked.connect(self.diff_requested.emit)
            button.clicked.connect(self.diff)
            self.ui.horizontalLayout.insertWidget(1, button)
            self.ui.diff_button = button

    def diff(self):
        app_path = self.parent().devset.get_differ()
        if not app_path:
            return
        _res, _pid = a2util.start_process_detached(app_path, [self.file_path1, self.file_path2])

    def remove_temp_files(self):
        for file_path in self.file_path1, self.file_path2:
            if not file_path:
                continue
            dirpath, base = os.path.split(file_path)
            if os.path.normcase(dirpath) == os.path.normcase(os.getenv('TEMP')):
                log.info('Deleting temp file: %s', base)
                os.unlink(file_path)


class RollbackDiffDialog(OkDiffDialog):
    """Dialog to ask user for rollback confirmation and offer diffing."""

    def __init__(self, parent, title, file_path1, file_path2):
        title = 'Rollback to "%s"' % title
        msg = 'Press <b>OK</b> to can roll back directly or <b>Diff</b> it if you want:'
        super(RollbackDiffDialog, self).__init__(parent, title, msg, file_path1, file_path2)


# pylint: disable=too-many-instance-attributes
class DevSettings:
    """Developer settings holder."""

    def __init__(self, a2):
        self._enabled = False
        self.author_name = ''
        self.author_url = ''
        self.code_editor = ''
        self.diff_app = ''
        self.json_indent = 2
        self.loglevel_debug = False

        self._a2 = a2
        self._defaults = {
            'author_name': os.getenv('USERNAME'),
            'author_url': '',
            'code_editor': '',
            'diff_app': '',
            'json_indent': 2,
            'loglevel_debug': False,
        }
        self.get()

        log.info('loglevel_debug: %s', self.loglevel_debug)
        log.debug('loglevel_debug: %s', self.loglevel_debug)

    def _get_from_db(self):
        return self._a2.db.get_changes('dev_settings', self._defaults)

    def get(self):
        """Fetch developer settings from the database."""
        settings = self._get_from_db()
        self._set_attrs(settings)
        return settings

    def _set_attrs(self, settings):
        for key, value in settings.items():
            setattr(self, key, value)
        a2util.JSON_INDENT = self.json_indent

    def set(self, these):
        """Set given developer settings to the database."""
        self._a2.db.set_changes('dev_settings', these, self._defaults)
        self._set_attrs(these)

    def set_var(self, key, value):
        """Set a specific developer setting to the database."""
        settings = self._get_from_db()
        settings[key] = value
        self.set(settings)

    def get_editor(self):
        return self._get_app('code_editor', 'Code Editor')

    def get_differ(self):
        return self._get_app('diff_app', 'Diff Application')

    def _get_app(self, var_name, display_name):
        variable = getattr(self, var_name)
        if os.path.isfile(variable):
            return variable

        task_msg = _TASK_MSG % display_name
        question = _QUEST_MSG % task_msg
        parent = self._a2.win
        reply = QtWidgets.QMessageBox.question(
            parent,
            'No Valid %s Set!' % display_name,
            question,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
        )

        if reply == QtWidgets.QMessageBox.Yes:
            exepath, _ = QtWidgets.QFileDialog.getOpenFileName(
                parent, task_msg.title(), variable, 'Executable (*.exe)'
            )
            if exepath:
                self.set_var(var_name, exepath)
                return exepath

        return ''
