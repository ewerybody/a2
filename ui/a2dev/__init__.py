"""a2 Developer stuff."""

import os
import sys

import a2dl
import a2core
import a2util

_TASK_MSG = 'browse for a %s executable'
_QUEST_MSG = 'Do you want to %s now?'
log = a2core.get_logger(__name__)
MSG_CFG_DIFF = (
    'The module configuration appears to have changed!\n'
    'Do you really want to exit and discard the changes?\n\n'
    'You can also have a look at the differences...'
)
MSG_CFG_NEW = 'The module configuration appears to be new!\nDo you really want to exit and discard the changes?'


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

        from PySide6 import QtWidgets

        task_msg = _TASK_MSG % display_name
        question = _QUEST_MSG % task_msg
        parent = self._a2.win
        reply = QtWidgets.QMessageBox.question(
            parent,
            'No Valid %s Set!' % display_name,
            question,
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel,
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            exe_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                parent, task_msg.title(), variable, 'Executable (*.exe)'
            )
            if exe_path:
                self.set_var(var_name, exe_path)
                return exe_path

        return ''


def check_py_version():
    versions = []
    url = 'https://www.python.org/ftp/python/'
    for line in a2dl.read(url).split('\r\n'):
        if not line.startswith('<a href="') or not line[9].isdecimal():
            continue

        version_str = line[9 : line.find('/"', 9)]
        try:
            version = tuple(int(i) for i in version_str.split('.'))
        except ValueError:
            continue

        if version <= sys.version_info:
            continue

        if version[:2] > sys.version_info[:2]:
            # check for pre-release versions
            prefix = f'<a href="python-{version_str}'
            these_versions = [
                l[len(prefix) : l.find('">')]
                for l in a2dl.read(url + version_str).split('\r\n')
                if l.startswith(prefix)
            ]
            if any(v.startswith('-') for v in these_versions):
                # there is a version without attachment: that's a main release
                versions.append(version)
            else:
                # append the attachment to this one
                for v in set(v.split('-', 1)[0] for v in these_versions if '-' in v):
                    versions.append((*version, v))
        else:
            versions.append(version)
    return versions


def check_pyside_version():
    import a2qt

    url = 'https://pypi.org/pypi/PySide{}/json'.format(a2qt.QT_VERSION)
    data = a2dl.read_json(url)
    versions = []
    for version_str in data.get('releases', {}).keys():
        try:
            version = tuple(int(i) for i in version_str.split('.'))
        except ValueError:
            continue
        if version > a2qt.VERSION:
            versions.append(version)
    return versions


def check_dev_updates():
    import a2ahk
    import a2qt

    def str_ver(version):
        return '.'.join(str(i) for i in version)

    log.info('Checking %s version ...', a2ahk.NAME.title())
    current = a2ahk.get_current_version()
    try:
        latest = a2ahk.get_latest_version()

        if current != latest:
            log.info(f'New {a2ahk.NAME.title()} version online!\n Current: {current}\n Latest: {latest}')
            yield a2ahk.NAME, current, latest
        else:
            log.info('%s is up-to-date at %s', a2ahk.NAME.title(), current)
            yield a2ahk.NAME, current, None

    except RuntimeError as error:
        if str(error).startswith(a2ahk.LATEST_VERSION_ERROR):
            log.error(error)
        else:
            log.info('Could NOT check %s version online!\n%s', a2ahk.NAME.title(), error)
        yield a2ahk.NAME, current, 'ERROR'

    log.info('Checking Python version ...')
    new_version = None
    for version in check_py_version():
        if version[:2] == sys.version_info[:2]:
            new_version = str_ver(version)
            log.info('New patch for current Python version: %s', new_version)
        elif len(version) > 3:
            log.info(' new Python pre-release: %s', str_ver(version))
        else:
            new_version = str_ver(version)
            log.info('New Python version: %s', new_version)
    if new_version is None:
        log.info('Python is up-to-date at %s', str_ver(sys.version_info))
    yield 'python', str_ver(sys.version_info), new_version

    log.info('Checking PySide version ...')
    new_version = None
    for version in check_pyside_version():
        new_version = str_ver(version)
        log.info('New PySide version: %s', new_version)
    if new_version is None:
        log.info('PySide is up-to-date at %s', str_ver(a2qt.VERSION))
    yield 'pyside', str_ver(a2qt.VERSION), new_version


def build_package():
    a2 = a2core.get()
    batch_path = os.path.join(a2.paths.lib, '_batches')
    batch_name = '1_build_all.bat'
    _result, _pid = a2util.start_process_detached(
        os.getenv('COMSPEC'),
        ['/c', 'start %s' % batch_name],
        batch_path,
    )
