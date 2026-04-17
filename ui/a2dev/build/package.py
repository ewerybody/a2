"""
a2 package assembly to prepare deployment without pyinstaller.
This now copies OUR code and Qt stuff separately.
To be able to zip OUR stuff ONTO a pre-packed Qt package this will leave the
new package dir UNFINISHED! It will need to be copied together afterwards to
create the portable zip package.
"""

import os
import shutil
import ctypes
import subprocess

import a2ahk
import a2core

import a2dev.build
from a2dev.build import A2, PYSIDE, PYSIDE_VERSION, QT_VERSION, PYSIDE_NAME, PACKAGE_CFG_NAME
from a2dev.build import CHK_MK, EX_MRK, SHIBOKEN, SHIBOKEN_NAME, VERSIONS, Paths

PACKAGE_SUB_NAME = 'alpha'
DESKTOP_ICO_FILE = 'theme/a2.ico'
DESKTOP_INI_CODE = (
    f'[.ShellClassInfo]\nIconResource={DESKTOP_ICO_FILE}\nIconIndex=0\n[ViewState]\nMode=\nVid=\nFolderType=Generic'
)
FILE_ATTR_HIDDEN = 0x02
ROOT_FILES = (PACKAGE_CFG_NAME, f'{A2} on github.com.URL', 'LICENSE', 'README.md')
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

# The Qt dlls we need!
QT_LIBS = 'Core', 'Widgets', 'Gui', 'Network', 'Svg'
QT_DLLS = QT_LIBS  # + ('Qml',)
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


def main():
    package_cfg = a2dev.build.get_package_cfg()
    version = package_cfg['project']['version']
    package_name = f'{A2} {version} {PACKAGE_SUB_NAME}'
    print('\n{0} Making package: {1} ... {0}'.format(8 * '#', package_name))
    a2 = a2core.get()

    prepare_package()
    get_py_package()
    patch_sqlite()
    copy_files()

    prepare_qt()
    update_readme()

    config_file = os.path.join(Paths.distlib, 'a2_config.ahk')
    a2ahk.set_variable(config_file, 'a2_title', package_name)

    make_desktop_ini()
    make_executables(version)

    print('{0} package: {1} finished! {0}\n'.format(8 * '#', package_name))


def prepare_package():
    if os.path.isdir(Paths.dist):
        print('Removing old package ...', end='')
        shutil.rmtree(Paths.dist)
        if os.path.isdir(Paths.dist):
            print(f'\b\b\b{EX_MRK}  ')
            raise RuntimeError(f'Old package still in place?\n  {Paths.dist}')
    else:
        print('Creating fresh package dir ...', end='')

    os.makedirs(Paths.dist)
    print(f'\b\b\b{CHK_MK}  ')


def update_readme():
    print('Checking Package versions ...')
    # get versions in readme:
    readme_path = os.path.join(Paths.a2, 'README.md')
    if not os.path.isfile(readme_path):
        raise RuntimeError('No "README.md" file!?!?!')
    if not os.path.getsize(readme_path):
        raise RuntimeError('"README.md" is empty?!!?!')

    lines = []
    linebreak = ''
    with open(readme_path, encoding='utf8') as fileobj:
        for line in fileobj:
            lines.append(line)

            if not linebreak:
                if line[-2:] == '\r\n':
                    linebreak = '\r\n'
                elif line[-1:] == '\n':
                    linebreak = '\n'

    if not linebreak:
        raise RuntimeError('Linebreak could not be determined from readme file!!!')

    versions = a2dev.build.VERSIONS
    for name, version_str in versions.items():
        print('* %s: %s' % (name, version_str))

    changed = False
    for i, line in enumerate(lines):
        for name in versions:
            if not line.startswith(f'* {name}: '):
                continue
            set_version = line.split(':')[1].strip()
            if set_version == versions[name]:
                continue
            lines[i] = f'* {name}: {versions[name]}{linebreak}'
            changed = True

    if changed:
        print(f'  Updating {readme_path}\n')
        with open(readme_path, 'w', encoding='utf8') as file_obj:
            file_obj.write(''.join(lines))
    else:
        print('  Versions unchanged!\n')


def copy_files():
    print('Copy root files ...', end='')

    for item in os.scandir(Paths.a2):
        if item.is_file() and item.name in ROOT_FILES:
            shutil.copy2(item.path, Paths.dist)

    print(f'\b\b\b{CHK_MK}  \b\b\nCopy lib files ...', end='')
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

    print(f'\b\b\b{CHK_MK}  \b\b\nCopy ui files ...', end='')
    shutil.copytree(Paths.ui, Paths.dist_ui, ignore=_ui_ignore, dirs_exist_ok=True)

    print(f'\b\b\b{CHK_MK}  \b\b\nCopy i18n files ...', end='')
    shutil.copytree(Paths.i18n, Paths.dist_i18n, ignore=_i18n_ignore, dirs_exist_ok=True)

    print(f'\b\b\b{CHK_MK}  \b\b\nCopy theme files ...', end='')
    shutil.copytree(Paths.theme, Paths.dist_theme, ignore=_theme_ignore, dirs_exist_ok=True)
    print(f'\b\b\b{CHK_MK}  \b\b')


def prepare_qt():
    """
    Instead of fixing PyInstallers greedy take-all, we copy ONLY
    the things we need to the target dir.

    * shiboken dll
    * selected Qt dlls
    * shiboken and PySide dirs
    * selected qt plugins
    Note: We're no longer copying the Qt stuff into the package!!!
    This makes the package unusable as is :/
    but we're skipping the huge re-compression part for all the Qt things!
    """
    print('Checking Qt files ...')
    _assemble_qt()
    _zip_qt()
    # shutil.copytree(tmp_qt, Paths.dist_ui)


def _assemble_qt():
    if os.path.isdir(Paths.qt_temp):
        print(f'  {CHK_MK} Qt for Python {VERSIONS[PYSIDE]} already assembled!\n  {Paths.qt_temp}')
        return

    include = [QT_DLL % (QT_VERSION, base) for base in QT_DLLS]
    include.append(f'{PYSIDE.lower()}{PYSIDE_VERSION}{ABI_DLL}')

    # qt_core_dll_path = os.path.join(Paths.pyside, include[0])

    for q_item in os.scandir(Paths.pyside):
        if q_item.is_dir():
            continue

        dst_path = os.path.join(Paths.qt_temp, q_item.name)
        if q_item.name in include:
            _copy(q_item.path, dst_path)
            continue
        if q_item.name.lower().startswith('msvcp') and q_item.name.endswith('.dll'):
            _copy(q_item.path, dst_path)
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
        print(f'  {CHK_MK} Qt for Python already zipped!\n  {zip_path}')
        return

    tmp_dirname = os.path.join(Paths.qt_dir, A2)
    if os.path.isdir(tmp_dirname):
        shutil.rmtree(tmp_dirname, ignore_errors=True)
    os.mkdir(tmp_dirname)
    tmp_ui = os.path.join(tmp_dirname, 'ui')
    os.rename(Paths.qt_temp, tmp_ui)

    from a2dev.dependency import seven_zip

    subprocess.call([Paths.seven_zip_exe, 'a', zip_path, tmp_dirname] + seven_zip.FLAGS)

    os.rename(tmp_ui, Paths.qt_temp)
    os.rmdir(tmp_dirname)


def _qt_ignore(path, items):
    this_base = os.path.basename(path)
    if this_base == 'imageformats':
        keep = [('q%s.dll' % n) for n in IMG_FORMATS]
        return [n for n in items if n not in keep]
    return []


def get_py_package():
    if os.path.isdir(Paths.dist_ui):
        print('Dist-path ui already exists! skipping `get_py_package` ...')
        return

    import a2dev.dependency.python_embed

    pack_path = a2dev.dependency.python_embed.check()

    print(f'  Copying fresh {os.path.basename(pack_path)} ...', end='')
    shutil.copytree(pack_path, Paths.dist_ui)
    print(f'\b\b\b{CHK_MK} ({Paths.dist_ui})')


def patch_sqlite():
    print('Checking for sqlite to be up-to-date in dist ui ...')
    import a2dev.dependency.sqlite

    latest_version, latest_url = a2dev.dependency.sqlite.get_latest_version()
    a2dev.dependency.sqlite.check(Paths.dist_ui, latest_version, latest_url)

    if not latest_version:
        print(f'  {EX_MRK} Error! Could not find version on sqlite website!')
        return


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


def make_desktop_ini():
    folder_icon_ini = os.path.join(Paths.dist, 'desktop.ini')
    if not os.path.isfile(folder_icon_ini):
        with open(folder_icon_ini, 'w') as file_obj:
            file_obj.write(DESKTOP_INI_CODE)
        ctypes.windll.kernel32.SetFileAttributesW(folder_icon_ini, FILE_ATTR_HIDDEN)


def make_executables(version):
    for name, source_name, description in (
        (A2, 'a2_starter', 'a2 Runtime Starter'),
        (f'{A2}ui', 'a2_ui_starter', 'a2 UI Starter'),
    ):
        nfo = a2dev.build.EXE_NFO.copy()
        nfo['FileVersion'] = version
        nfo['ProductVersion'] = version
        nfo['FileDescription'] = description
        a2dev.build.make_py_exe(
            os.path.join(Paths.source, f'{source_name}.py'),
            os.path.join(Paths.dist, f'{name}.exe'),
            nfo=nfo,
            console=False,
        )

    for name, source_name, icon in ((f'Uninstall {A2}', 'a2_uninstaller', 'a2x'),):
        a2dev.build.make_ahk_exe(
            os.path.join(Paths.source, f'{source_name}.ahk'),
            os.path.join(Paths.dist, f'{name}.exe'),
            icon=icon,
        )


def _lib_ignore(path, items):
    # we ignore ANY '_' starting dirs and files in lib
    result = [i for i in items if i.startswith('_') and i not in LIB_INCLUDES]
    this_base = os.path.basename(path)

    for item in [i for i in items if i not in result]:
        item_path = os.path.join(path, item)
        if not os.path.isdir(item_path):
            continue
        if item == 'test' and this_base == 'lib':
            result.append(item)
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
    return result


def _i18n_ignore(path, items):
    result = []
    # nah we can pass the i18n README to the package. COuld be useful to module devs.
    # if path == Paths.i18n and 'README.md' in items:
    #     result.append('README.md')
    return result


def _theme_ignore(path, items):
    result = []
    if path == Paths.theme and '_source' in items:
        result.append('_source')
    return result


if __name__ == '__main__':
    main()
