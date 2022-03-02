"""a2 Developer stuff."""
import os
import traceback
from a2qt import QtWidgets, QtCore

import a2ahk
import a2core
import a2util

from a2widget import a2input_dialog

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
            if os.path.normcase(dirpath) == os.path.normcase(os.getenv('TEMP', '')):
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
        self.mini_ns_tag = '{urn:schemas-microsoft-com:asm.v1}assemblyIdentity'
        self.error = 'ERROR'

        self._file_package = os.path.join(a2.paths.a2, 'package.json')
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
        self._file_manifest = os.path.join(source_dir, 'a2_installer_manifest.xml')

        self._all_set = False
        try:
            msg = self.get_versions()

            semver = '<a href="https://semver.org">semver.org-style</a>'
            msg = f'<div style="margin: 20px">{msg}</div>'
            msg = f'Currently set versions:{msg}Set another {semver} version:'
        except Exception:
            msg = traceback.format_exc().strip()
            self._orig_ver = self.error

        super().__init__(
            parent, self.__class__.__name__, self._check, self._orig_ver, msg, self.set_versions
        )

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

        from xml.etree import ElementTree

        xml = ElementTree.parse(self._file_manifest)
        id_node = xml.find(self.mini_ns_tag)
        mani_ver = self.nothing if id_node is None else id_node.get('version', self.nothing)
        if not mani_ver.startswith(self._orig_ver):
            self._all_set = False
        msgs.append(self.tmpl8 % (os.path.basename(self._file_manifest), mani_ver))

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

        # WHAT the XML namespace crap!? I'm out of ideas here.
        # Lets just parse and set text like in the olden days ... m()
        # from xml.etree import ElementTree
        # xml = ElementTree.parse(self._file_manifest)
        # id_node = xml.find(self.mini_ns_tag)
        # id_node.set('version', self.output + '.0')
        # xml.write(self._file_manifest)
        lines = a2util.load_utf8(self._file_manifest).split('\n')
        for i, line in enumerate(lines):
            if '<assemblyIdentity' not in line:
                continue
            nextline = lines[i + 1]
            marker = 'version="'
            if marker not in nextline:
                break
            pre, ver = nextline.split(marker, 1)
            parts = ver.split('.',3)
            current = '.'.join(parts[:3])
            if current == self.output:
                break
            lines[i + 1] = f'{pre}{marker}{self.output}.{parts[-1]}'
            log.info(f'Setting manifest version from:{current} to:{self.output}')
            a2util.write_utf8(self._file_manifest, '\n'.join(lines))
            break

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
        if not '.' in text:
            return 'No x.y.z semver style!'
        nrs = text.split('.')
        if not len(nrs) == 3 or not all(p.isnumeric() for p in nrs):
            return 'No x.y.z semver style!'
        return ''
