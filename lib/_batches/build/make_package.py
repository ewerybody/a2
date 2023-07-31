"""
a2 package assembly to prepare deployment without pyinstaller.
This now copies OUR code and Qt stuff separately.
To be able to zip OUR stuff ONTO a pre-packed Qt package this will leave the
new package dir UNFINISHED! It will need to be copied together afterwards to
create the portable zip package.
"""
import os
import sys
import time
import shutil
import ctypes
import codecs
import zipfile
import subprocess
from urllib import request

import _build_common
import a2ahk
import a2util

Paths = _build_common.Paths
from _build_common import (
    PYSIDE, PYSIDE_VERSION, QT_VERSION, PYSIDE_NAME, SHIBOKEN, SHIBOKEN_NAME
)

PACKAGE_SUB_NAME = 'alpha'
DESKTOP_ICO_FILE = 'ui/res/a2.ico'
DESKTOP_INI_CODE = (
    f'[.ShellClassInfo]\nIconResource={DESKTOP_ICO_FILE}\nIconIndex=0\n'
    '[ViewState]\nMode=\nVid=\nFolderType=Generic'
)
FILE_ATTR_HIDDEN = 0x02
ROOT_FILES = ('package.json', 'a2 on github.com.URL', 'LICENSE', 'README.md')
LIB_IGNORES = (('Autohotkey', 'Compiler'),)
# Lets keep lib/test for implementation examples in release!
LIB_INCLUDES = ('_Struct.ahk',)
UI_IGNORES = (
    ('a2widget', 'demo'),
    ('res', 'work'),
    ('a2hotkey', 'test'),
    ('ui', 'typings'),
    ('ui', 'test'),
)

# The Qt dlls we need! For some reason Qml is indispensable :/
QT_LIBS = 'Core', 'Widgets', 'Gui', 'Network', 'Svg'
QT_DLLS = QT_LIBS # + ('Qml',)
QT_DLL = 'Qt%i%s.dll'
QT_PYD = 'Qt%s.pyd'
IMG_FORMATS = ('jpeg', 'ico', 'svg')
ABI_DLL = '.abi3.dll'
# fmt: off
QT_PLUGIN_DIRS = (
    'iconengines', 'imageformats', 'networkinformation',
    'platforminputcontexts', 'platforms', 'styles', 'tls',
)
# fmt: on
SQLITE_URL = 'https://www.sqlite.org/'


def main():
    package_cfg = a2util.json_read(os.path.join(Paths.a2, 'package.json'))
    package_name = f'a2 {package_cfg["version"]} {PACKAGE_SUB_NAME}'
    print('\n{0} making package: {1} ... {0}'.format(8 * '#', package_name))

    get_py_package()
    patch_sqlite()
    copy_files()

    prepare_qt()
    update_readme()

    config_file = os.path.join(Paths.distlib, 'a2_config.ahk')
    a2ahk.set_variable(config_file, 'a2_title', package_name)

    make_desktop_ini()

    print('{0} {1} finished! {0}\n'.format(8 * '#', package_name))



def update_readme():
    # get versions in readme:
    readme_path = os.path.join(Paths.a2, 'README.md')
    lines = []
    linebreak = ''
    with codecs.open(readme_path, encoding='utf8') as fileobj:
        for line in fileobj:
            lines.append(line)

            if not linebreak:
                if line[-2:] == '\r\n':
                    linebreak = '\r\n'
                elif line[-1:] == '\n':
                    linebreak = '\n'

    if not linebreak:
        raise RuntimeError('Linebreak could not be determined from readme file!!!')

    versions = _build_common.VERSIONS
    print('Versions:\n')
    for name, version_str in versions.items():
        print('* %s: %s' % (name, version_str))
    print('')

    changed = False
    for i, line in enumerate(lines):
        for name in versions:
            if line.startswith(f'* {name}: '):
                set_version = line.split(':')[1].strip()
                if set_version != versions[name]:
                    lines[i] = f'* {name}: {versions[name]}{linebreak}'
                    changed = True

    if changed:
        print('Updating %s' % readme_path)
        with open(readme_path, 'wb') as fileobj:
            fileobj.write(''.join(lines).encode('utf8'))
    else:
        print('Versions unchanged!')


def copy_files():
    print('copying root files ...')

    for item in os.scandir(Paths.a2):
        if item.is_file() and item.name in ROOT_FILES:
            shutil.copy2(item.path, Paths.dist)

    print('copying lib files ...')
    os.makedirs(Paths.distlib, exist_ok=True)

    for item in os.scandir(Paths.lib):
        if item.name.startswith('_'):
            continue

        if item.is_file():
            if os.path.splitext(item.name)[1] == a2ahk.EXTENSION:
                shutil.copy2(item.path, Paths.distlib)
        else:
            this_dest = os.path.join(Paths.distlib, item.name)
            if not os.path.isdir(this_dest):
                shutil.copytree(item.path, this_dest, ignore=_lib_ignore)

    print('copying ui files ...')
    shutil.copytree(Paths.ui, Paths.distui, ignore=_ui_ignore, dirs_exist_ok=True)


def _lib_ignore(path, items):
    # we ignore ANY '_' starting dirs and files in lib
    result = [i for i in items if i.startswith('_') and i not in LIB_INCLUDES]
    this_base = os.path.basename(path)

    for item in [i for i in items if i not in result]:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            for base, name in LIB_IGNORES:
                if this_base == base and item == name:
                    result.append(item)
    # if result:
    #     print('IGNORING lib items: %s' % result)
    return result


def _ui_ignore(path, items):
    # Can't ignore all '_' because Python has __stuff. Look for '_ ' instead
    result = [i for i in items if i == '__pycache__' or i.startswith('_ ')]
    this_base = os.path.basename(path)

    for item in [i for i in items if i not in result]:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            for base, name in UI_IGNORES:
                if this_base == base and item == name:
                    result.append(item)

        elif item.endswith('.ui'):
            # TODO: handle ui files
            result.append(item)

    # if result:
    #     print('IGNORING ui items: %s' % result)

    return result


def prepare_qt():
    """
    Instead of fixing pyinstallers greedy take-all, we copy ONLY
    the things we need to the target dir.

    * shiboken dll
    * selected Qt dlls
    * shiboken and PySide dirs
    * selected qt plugins
    """
    print('copying Qt files ...')
    _assemble_qt()
    _zip_qt()
    # shutil.copytree(tmp_qt, Paths.distui)


def _assemble_qt():
    if os.path.isdir(Paths.qt_temp):
        print(f'Qt for Python already assembled!\n  {Paths.qt_temp}')
        return

    include = [QT_DLL % (QT_VERSION, base) for base in QT_DLLS]
    include.append(f'{PYSIDE.lower()}{PYSIDE_VERSION}{ABI_DLL}')

    # qtcore_dll_path = os.path.join(Paths.pyside, include[0])

    for qitem in os.scandir(Paths.pyside):
        if qitem.is_dir():
            continue

        dst_path = os.path.join(Paths.qt_temp, qitem.name)
        if qitem.name in include:
            _copy(qitem.path, dst_path)
            continue
        if qitem.name.lower().startswith('msvcp') and qitem.name.endswith('.dll'):
            _copy(qitem.path, dst_path)
            continue

    # copy shiboken files
    for name in f'{SHIBOKEN.title()}.pyd', '__init__.py':
        src = os.path.join(Paths.py_site_packs, SHIBOKEN_NAME, name)
        dst = os.path.join(Paths.qt_temp, SHIBOKEN_NAME, name)
        _copy(src, dst)

    # Pyinstaller copied this one into the root.. *shrug*
    abi = f'{SHIBOKEN_NAME}{ABI_DLL}'
    src = os.path.join(Paths.py_site_packs, SHIBOKEN_NAME, abi)
    dst = os.path.join(Paths.qt_temp, abi)
    _copy(src, dst)

    pyside_dst_dir = os.path.join(Paths.qt_temp, PYSIDE_NAME)
    for name in QT_LIBS:
        src = os.path.join(Paths.pyside, QT_PYD % name)
        dst = os.path.join(pyside_dst_dir, QT_PYD % name)
        _copy(src, dst)

    for dirname in QT_PLUGIN_DIRS:
        dst = os.path.join(pyside_dst_dir, 'plugins', dirname)
        if os.path.isdir(dst):
            continue
        src = os.path.join(Paths.pyside, 'plugins', dirname)
        shutil.copytree(src, dst, ignore=_qt_ignore)


def _zip_qt():
    zip_path = Paths.qt_temp + '.7z'
    if os.path.isfile(zip_path):
        print(f'Qt for Python already zipped!\n  {zip_path}')
        return

    tmp_dirname = os.path.join(Paths.qt_dir, _build_common.A2)
    os.mkdir(tmp_dirname)
    tmp_ui = os.path.join(tmp_dirname, 'ui')
    os.rename(Paths.qt_temp, tmp_ui)

    subprocess.call([Paths.sevenz_exe, 'a', zip_path, tmp_dirname] + _build_common.SEVEN_FLAGS)

    os.rename(tmp_ui, Paths.qt_temp)
    os.rmdir(tmp_dirname)


def _qt_ignore(path, items):
    this_base = os.path.basename(path)
    if this_base == 'imageformats':
        keep = [('q%s.dll' % n) for n in IMG_FORMATS]
        return [n for n in items if n not in keep]
    return []


def get_py_package():
    if os.path.isdir(Paths.distui):
        print('Dist-path ui already exists! skipping `get_py_package` ...')
        return

    py_ver = '.'.join(str(i) for i in sys.version_info[:3])
    pack_name = f'python-{py_ver}-embed-amd64'
    pack_path = os.path.join(Paths.py_packs, pack_name)

    if not os.path.isdir(pack_path):
        print(f'Getting py package "{pack_name}" ...')
        os.makedirs(Paths.py_packs, exist_ok=True)
        pack_zip = pack_name + '.zip'
        pack_zip_path = os.path.join(Paths.py_packs, pack_zip)

        if not os.path.isfile(pack_zip_path):
            pack_url = f'https://www.python.org/ftp/python/{py_ver}/{pack_zip}'
            df = _DownloadFeedback(pack_name)
            request.FancyURLopener().retrieve(pack_url, pack_zip_path, df.callback)
            print('done!')

        print(f'  Unzipping "{pack_name}" ...')
        with zipfile.ZipFile(pack_zip_path) as tmp_zip:
            for filename in tmp_zip.namelist():
                tmp_zip.extract(filename, pack_path)

    print(f'  Copying ...')
    shutil.copytree(pack_path, Paths.distui)
    print(f'  Ready! ({Paths.distui})')


def patch_sqlite():
    print('Checking for latest sqlite ...')
    import qdl

    download_page = qdl.read(SQLITE_URL + 'download.html')
    pos = download_page.find('/sqlite-dll-win64-x64-')
    if pos == -1:
        print('  Error! Could not find version on sqlite website!')
        return

    line_start = download_page.rfind('PRODUCT,', pos - 100, pos)
    line_end = download_page.find('\n', pos)
    line = download_page[line_start:line_end]
    try:
        latest_version, path, size, checksum = line.split(',')[1:]
    except ValueError:
        print(f'  Error! Could not read line from sqlite website:\n"{line}"')
        return

    latest = tuple(int(v) for v in latest_version.split('.'))
    sqlpath = os.path.join(Paths.distui, 'sqlite3.dll')

    script = os.path.join(Paths.batches, 'versions', 'get_version.ahk')
    script_wd = os.path.dirname(os.path.dirname(script))
    if os.path.isfile(sqlpath):
        current_version = subprocess.check_output(
            [Paths.ahkexe, script, sqlpath], cwd=script_wd
        ).decode()
        current = tuple(int(v) for v in current_version.split('.'))
        if current >= latest:
            print(f'  SQLite3 already up-to-date! ({current_version})')
            return
    else:
        current_version = '?'

    print(f'  Updating SQLite3 to latest: {latest} ...')
    zip_path = os.path.join(Paths.py_packs, os.path.basename(path))
    if not os.path.isfile(zip_path):
        print(f'  Downloading ...')
        new_sqlite_data = qdl.read_raw(SQLITE_URL + path)
        with open(zip_path, 'wb') as file_obj:
            file_obj.write(new_sqlite_data)

    with zipfile.ZipFile(zip_path) as tmp_zip:
        for filename in tmp_zip.namelist():
            if filename == 'sqlite3.dll':
                tmp_zip.extract(filename, Paths.distui)
                break

    current_version = subprocess.check_output(
        [Paths.ahkexe, script, sqlpath], cwd=script_wd
    ).decode()
    current = tuple(int(v) for v in current_version.split('.'))
    if current >= latest:
        print('  SQLite3 Updated!')
        return
    print(f'  ERROR: SQLite3 Update failed! Current: {current_version}/Latest: {latest_version}')


class _DownloadFeedback:
    def __init__(self, name):
        self._bytes_received = 0
        self._last_posted = 0
        self._name = name
        self._size = None
        self._width = 0
        self.channel = sys.stdout

    def callback(self, blocknum, blocksize, fullsize):
        self._bytes_received += blocksize
        if self._size is None:
            self._size = f'{round(fullsize / (1024 * 1024), 2)}MB'

        now = time.time()
        if now - self._last_posted > 0.1:
            pct = round(100 * self._bytes_received / fullsize, 2)
            msg = f'downloading "{self._name}" {pct}% of {self._size} ...'

            if self._width:
                backup = '\b' * self._width
                self.channel.write(backup + ' ' * self._width + backup)

            self.channel.write(msg)
            self.channel.flush()
            self._width = len(msg)
            self._last_posted = now


def _copy(src, dst):
    if not os.path.isfile(src):
        raise FileNotFoundError(src)

    if os.path.isfile(dst):
        return

    dir_path = os.path.dirname(dst)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    shutil.copy2(src, dst)
    print(f'  copied {os.path.basename(dst)}')


def _get_versions():
    """Get currently used versions."""
    pattern = 'get_%s_version.ahk'
    names = 'AutoHotkey', PYSIDE, 'Python'
    scripts = (
        os.path.join(Paths.lib, 'cmds', pattern % names[0]),
        os.path.join(Paths.batches, 'versions', pattern % names[1]),
        os.path.join(Paths.batches, 'versions', pattern % names[2]),
    )
    versions = {}
    for name, script in zip(names, scripts):
        cwd = os.path.dirname(os.path.dirname(script))
        version_str = subprocess.check_output([Paths.ahkexe, script], cwd=cwd).decode()
        versions[name] = version_str
    return versions


def make_desktop_ini():
    folder_icon_ini = os.path.join(Paths.dist, 'desktop.ini')
    if not os.path.isfile(folder_icon_ini):
        with open(folder_icon_ini, 'w') as file_obj:
            file_obj.write(DESKTOP_INI_CODE)
        ctypes.windll.kernel32.SetFileAttributesW(folder_icon_ini, FILE_ATTR_HIDDEN)


if __name__ == '__main__':
    main()
