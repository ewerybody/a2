"""
a2 package assembly script to prepare deployment.

Whow! Batch files are such a pain!
Better keep them as short as possible.
"""
import os
import shutil
import codecs

import _build_package_init
import a2ahk
import a2util
import subprocess

A2PATH = _build_package_init.a2path
A2UIPATH = _build_package_init.uipath
PACKAGE_SUB_NAME = 'alpha'
DESKTOP_ICO_FILE = 'ui/res/a2.ico'
DESKTOP_INI_CODE = ('[.ShellClassInfo]\nIconResource=%s\nIconIndex=0\n' %
                    DESKTOP_ICO_FILE)
ROOT_FILES = 'package.json', 'a2 on github.com.URL', 'LICENSE'
LIB_EXCLUDES = ('batches', '_source', 'a2ui', 'a2ui dev', 'ahklib',
                'a2init_check', 'a2dev_find_py', 'a2init_check')
UI_FOLDERS = 'a2ctrl', 'a2widget', 'a2element', 'res', 'style'
UI_REMOVE_FILES = ('d3dcompiler_47.dll', 'Qt5VirtualKeyboard.dll', 'libGLESv2.dll',
                   'Qt5Quick.dll', 'opengl32sw.dll', 'Qt5QmlModels.dll', 'Qt5DBus.dll',
                   r'PySide2\plugins\platforms\qwebgl.dll')
UI_REMOVE_DIRS = 'lib2to3', 'Include', 'numpy', r'PySide2\translations'


def main():
    package_cfg = a2util.json_read(os.path.join(A2PATH, 'package.json'))
    package_name = f'a2 {PACKAGE_SUB_NAME} {package_cfg["version"]}'
    print('\n{0} finishing: {1} ... {0}'.format(15 * '#', package_name))

    distroot = os.path.join(A2PATH, '_ package')
    distpath = os.path.join(distroot, 'a2')
    distlib = os.path.join(distpath, 'lib')
    distui = os.path.join(distpath, 'ui')
    a2lib = os.path.join(A2PATH, 'lib')

    if not os.path.isdir(distpath):
        raise FileNotFoundError('No Package found at "%s"!' % distpath)

    update_readme(a2lib)

    copy_files(distpath, distlib, a2lib, distui)
    cleanup(distui)

    config_file = os.path.join(distlib, 'a2_config.ahk')
    a2ahk.set_variable(config_file, 'a2_title', package_name)

    with open(os.path.join(distpath, 'desktop.ini'), 'w') as file_obj:
        file_obj.write(DESKTOP_INI_CODE)

    print('{0} {1} finished! {0}\n'.format(18 * '#', package_name))


def update_readme(a2lib):
    # get currently used versions
    AHKEXE = os.path.join(a2lib, 'Autohotkey', 'Autohotkey.exe')
    batches_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    version_scripts_dir = os.path.join(batches_dir, 'versions')

    versions = {}
    for script in os.scandir(version_scripts_dir):
        name = script.name
        if script.is_dir() or not name.startswith('get_') or not name.endswith(a2ahk.EXTENSION):
            continue
        version_str = subprocess.check_output(
            [AHKEXE, script.path], cwd=batches_dir).decode()
        # cut off "get_" and "_version.ahk"
        versions[name[4:-12]] = version_str

    # get versions in readme:
    readme_path = os.path.join(A2PATH, 'README.md')
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


def copy_files(distpath, distlib, a2lib, distui):
    print('distpath: %s' % distpath)
    app_path = os.path.join(distpath, 'a2app')
    if not os.path.isdir(app_path):
        # raise FileNotFoundError(
        print(
            f'App Path was not found!\n  {app_path}\n'
            'Package already handled?')
    else:
        os.rename(app_path, distui)
    print('distui: %s' % distui)

    print('copying root files ...')

    for item in os.scandir(A2PATH):
        if item.is_file() and item.name in ROOT_FILES:
            shutil.copy2(item.path, distpath)

    print('copying lib files ...')
    if not os.path.isdir(distlib):
        os.mkdir(distlib)

    for item in os.scandir(a2lib):
        if item.name.startswith('_ '):
            continue

        base, ext = os.path.splitext(item.name)
        if base in LIB_EXCLUDES:
            continue

        if item.name == 'a2ui release.ahk':
            shutil.copy2(item.path, os.path.join(distlib, 'a2ui.ahk'))
            continue

        if item.is_file():
            if ext == a2ahk.EXTENSION:
                shutil.copy2(item.path, distlib)
        else:
            this_dest = os.path.join(distlib, item.name)
            if os.path.isdir(this_dest):
                print(f'  dir already copied: {this_dest}')
            else:
                shutil.copytree(item.path, this_dest, ignore=_ignore_items)

    print('copying ui files ...')
    for folder in UI_FOLDERS:
        this_dest = os.path.join(distui, folder)
        if os.path.isdir(this_dest):
            print(f'  dir already copied: {this_dest}')
            continue
        shutil.copytree(os.path.join(A2UIPATH, folder), this_dest, ignore=_ignore_items)


def cleanup(distui):
    print('cleaning up package ...')
    for dirname in UI_REMOVE_DIRS:
        path = os.path.join(distui, dirname)
        shutil.rmtree(path, ignore_errors=True)
    for filename in UI_REMOVE_FILES:
        path = os.path.join(distui, filename)
        if os.path.isfile(path):
            os.remove(path)


def _ignore_items(path, items):
    result = []
    path_low = os.path.normcase(path)
    for item in items:
        # ignore temp stuff
        if item.startswith('_ '):
            result.append(item)
            continue

        # ignore ahk lib tests
        if path_low.endswith('\\a2\\lib\\autohotkey\\lib\\test'):
            result.append(item)
            continue

        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            # ignore autmatically build python 3 cache files
            if item in ['__pycache__']:
                result.append(item)
            # ignore a2 dev build stuff
            elif item == 'demo' and os.path.basename(path) == 'a2widget':
                result.append(item)
            elif item == 'work' and os.path.basename(path) == 'res':
                result.append(item)

        # ignore uncompiled ui files
        elif item.endswith('.ui'):
            result.append(item)

    if result:
        print('IGNORING: %s' % result)

    return result


if __name__ == '__main__':
    main()
