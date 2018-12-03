'''
Created on 11.07.2018

@author: eric
'''
import os

import a2core
import a2util

from a2widget.a2input_dialog import A2ConfirmDialog
from PySide2 import QtWidgets, QtCore


log = a2core.get_logger(__name__)


class RollbackDiffDialog(A2ConfirmDialog):
    diff = QtCore.Signal()

    def __init__(self, parent, title):
        title = 'Rollback to "%s"' % title
        msg = 'Press <b>OK</b> to can roll back directly or <b>Diff</b> it if you want:'
        super(RollbackDiffDialog, self).__init__(parent, title, msg)

        self.ui.diff_button = QtWidgets.QPushButton('Diff', self)
        self.ui.diff_button.setObjectName("a2ok_button")
        self.ui.horizontalLayout.insertWidget(1, self.ui.diff_button)
        self.ui.diff_button.clicked.connect(self.diff.emit)


class DevSettings(object):
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
            'loglevel_debug': False}
        self.get()

        log.info('loglevel_debug: %s' % self.loglevel_debug)
        log.debug('loglevel_debug: %s' % self.loglevel_debug)

    def _get_from_db(self):
        return self._a2.db.get_changes('dev_settings', self._defaults)

    def get(self):
        settings = self._get_from_db()
        self._set_attrs(settings)
        return settings

    def _set_attrs(self, settings):
        for key, value in settings.items():
            setattr(self, key, value)
        a2util.JSON_INDENT = self.json_indent

    def set(self, these):
        self._a2.db.set_changes('dev_settings', these, self._defaults)
        self._set_attrs(these)

    def set_var(self, key, value):
        settings = self._get_from_db()
        settings[key] = value
        self.set(settings)