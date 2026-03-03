import os
import traceback

from PySide6 import QtWidgets, QtCore

import a2ahk
import a2core
import a2util
from a2widget import a2input_dialog

SEMVER_URL = 'https://semver.org'
log = a2core.get_logger(__name__)


class OkDiffDialog(a2input_dialog.A2ConfirmDialog):
    diff_requested = QtCore.Signal()

    def __init__(self, parent, title, msg, file_path1=None, file_path2=None):
        super().__init__(parent, title, msg)

        self.file_path1 = file_path1
        self.file_path2 = file_path2

        if self.file_path1 is not None:
            button = QtWidgets.QPushButton('Diff', self)
            button.setObjectName('a2ok_button')
            button.clicked.connect(self.diff_requested.emit)
            button.clicked.connect(self.diff)
            self.ui.horizontalLayout.insertWidget(1, button)
            # self.ui.diff_button = button

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
            if os.path.normcase(dirpath) == os.path.normcase(os.getenv('TEMP', '')):
                log.info('Deleting temp file: %s', base)
                os.unlink(file_path)


class RollbackDiffDialog(OkDiffDialog):
    """Dialog to ask user for rollback confirmation and offer diffing."""

    def __init__(self, parent, title, file_path1, file_path2):
        title = 'Rollback to "%s"' % title
        msg = 'Press <b>OK</b> to can roll back directly or <b>Diff</b> it if you want:'
        super(RollbackDiffDialog, self).__init__(parent, title, msg, file_path1, file_path2)


class VersionBumpDialog(a2input_dialog.A2InputDialog):
    """
    To have overview and control of the version numbers put in different places.
    Usually after release we'd bump the development version
    """

    def __init__(self, parent):
        a2 = a2core.get()

        self.tmpl8 = '%s <b>%s</b>'
        self.nothing = 'NOTHING FOUND!'
        self.ahk_setver = ';@Ahk2Exe-SetVersion'
        self.error = 'ERROR'

        self._file_package = a2.paths.package_cfg
        self._file_config = a2.paths.a2_config
        source_dir = os.path.join(a2.paths.lib, '_source')
        self._files_source = (
            os.path.join(source_dir, 'a2_starter.ahk'),
            os.path.join(source_dir, 'a2ui_dev.ahk'),
            os.path.join(source_dir, 'a2ui_release.ahk'),
            os.path.join(source_dir, 'a2_installer.ahk'),
            os.path.join(source_dir, 'a2_installer_silent.ahk'),
            os.path.join(source_dir, 'a2_uninstaller.ahk'),
        )

        self._all_set = False
        try:
            msg = self.get_versions()

            semver = f'<a href="{SEMVER_URL}">semver.org-style</a>'
            msg = f'<div style="margin: 20px">{msg}</div>'
            msg = f'Currently set versions:{msg}Set another {semver} version:'
        except Exception:
            msg = traceback.format_exc().strip()
            self._orig_ver = self.error

        super().__init__(parent, self.__class__.__name__, self._check, self._orig_ver, msg, self.set_versions)

    def get_versions(self):
        self._all_set = True
        msgs = []
        self._orig_ver = a2util.json_read(self._file_package).get('version')
        msgs.append(self.tmpl8 % (os.path.basename(self._file_package), self._orig_ver))

        a2_title = a2ahk.get_variables(self._file_config).get('a2_title', '')
        cfg_ver = a2_title.rsplit(' ', 1)[1]
        if cfg_ver != self._orig_ver:
            self._all_set = False
        msgs.append(self.tmpl8 % (os.path.basename(self._file_config), cfg_ver))

        for pth in self._files_source:
            msgs.append(self._text_file_get(pth, self.ahk_setver))
        return '<br>'.join(msgs)

    def set_versions(self, *arg):
        package_data = a2util.json_read(self._file_package)
        package_data['version'] = self.output
        a2util.json_write(self._file_package, package_data)

        a2_title = a2ahk.get_variables(self._file_config).get('a2_title', '')
        prefix = a2_title.rsplit(' ', 1)[0]
        new_value = f'{prefix} {self.output}'
        if new_value != a2_title:
            log.info(f'Setting config version: {new_value}')
            a2ahk.set_variable(self._file_config, 'a2_title', new_value)

        for pth in self._files_source:
            self._text_file_set(pth, self.ahk_setver)

    def _text_file_get(self, file_path, startswith):
        base = os.path.basename(file_path)
        with open(file_path) as file_obj:
            for _line in file_obj:
                line = _line.strip()
                if ' ' in line and line.startswith(startswith):
                    this_version = line.rsplit(' ', 1)[1]
                    if this_version != self._orig_ver:
                        self._all_set = False
                    return self.tmpl8 % (base, this_version)

        return self.tmpl8 % (base, self.nothing)

    def _text_file_set(self, file_path, startswith):
        lines = []
        with open(file_path) as file_obj:
            for _line in file_obj:
                line = _line.strip()
                if ' ' in line and line.startswith(startswith):
                    prefix, old = _line.rstrip().rsplit(' ', 1)
                    if old == self._orig_ver:
                        # no need to change!
                        return
                    log.info(f'Setting {os.path.basename(file_path)} version: {self._orig_ver}')
                    lines.append(f'{prefix} {self.output}\n')
                else:
                    lines.append(_line)

        with open(file_path, 'w') as file_obj:
            file_obj.write(''.join(lines))

    def _check(self, _text):
        if self._orig_ver == self.error:
            return self.error
        text = _text.strip()
        if not text:
            return 'Enter something'
        if text == self._orig_ver and self._all_set:
            return 'No change'
        if '.' not in text:
            return 'No x.y.z semver style!'
        nrs = text.split('.')
        if not len(nrs) == 3 or not all(p.isnumeric() for p in nrs):
            return 'No x.y.z semver style!'
        return ''


def call_version_bump_dialog(parent):
    dialog = VersionBumpDialog(parent)
    dialog.exec()
