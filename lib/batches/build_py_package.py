"""
a2 package build script.

Whow! Batch files are such a pain. Better keep them as short as possible.
"""
import os
import sys
import shutil
import codecs
from os.path import join


PACKAGE_SUB_NAME = 'alpha'
this_path = os.path.dirname(__file__)
DESKTOP_INI_FILE = 'ui/res/a2.ico'
DESKTOP_INI_CODE = ('[.ShellClassInfo]\nIconResource=%s\nIconIndex=0\n' %
                    DESKTOP_INI_FILE)
ROOT_FILES = ['package.json', 'a2 on github.com.URL', 'LICENSE']
LIB_EXCLUDES = ['batches', '_source', 'a2ui', 'a2ui dev', 'ahklib',
                'a2init_check', 'a2dev_find_py', 'a2init_check']
UI_FOLDERS = ['a2ctrl', 'a2widget', 'a2element', 'res', 'style']

INSTALLER_CFG = (
    ';!@Install@!UTF-8!\n'
    'RunProgram="a2\setup.exe"\n'
    ';!@InstallEnd@!')
MANIFEST_NAME = 'a2_installer_manifest.xml'

# adding a2 paths for imports
a2path = os.path.abspath(join(this_path, '..', '..'))
uipath = join(a2path, 'ui')
sys.path.append(uipath)
import a2ahk
import a2util


def main():
    package_cfg = a2util.json_read(join(a2path, 'package.json'))
    package_name = f'a2 {PACKAGE_SUB_NAME} {package_cfg["version"]}'
    print('package_name: %s' % package_name)

    distroot = join(a2path, '_ package')
    distpath = join(distroot, 'a2')
    if not os.path.isdir(distpath):
        raise FileNotFoundError('No Package found at "%s"!' % distpath)

    srcpath = join(a2path, 'lib', '_source')
    update_manifest(srcpath, package_cfg["version"], distroot)

    print('distpath: %s' % distpath)
    app_path = join(distpath, 'a2app')
    if not os.path.isdir(app_path):
        raise FileNotFoundError('App Path "%s" was not found!\n'
                                'Package already handled?' % app_path)

    distui = join(distpath, 'ui')
    os.rename(app_path, distui)
    print('distui: %s' % distui)

    print('copying root files ...')

    for item in os.scandir(a2path):
        if item.is_file() and item.name in ROOT_FILES:
            shutil.copy2(item.path, distpath)

    print('copying lib files ...')
    distlib = join(distpath, 'lib')
    a2lib = join(a2path, 'lib')
    os.mkdir(distlib)
    for item in os.scandir(a2lib):
        if item.name.startswith('_ '):
            continue

        base, ext = os.path.splitext(item.name)
        if base in LIB_EXCLUDES:
            continue

        if item.name == 'a2ui release.ahk':
            shutil.copy2(item.path, join(distlib, 'a2ui.ahk'))
            continue

        if item.is_file():
            if ext == '.ahk':
                shutil.copy2(item.path, distlib)
        else:
            shutil.copytree(item.path, join(distlib, item.name), ignore=_ignore_items)

    print('copying ui files ...')
    a2uipath = join(a2path, 'ui')

    for folder in UI_FOLDERS:
        shutil.copytree(join(a2uipath, folder),
                        join(distui, folder), ignore=_ignore_items)

    shutil.rmtree(join(distui, 'PySide', folder), ignore_errors=True)
    for item in os.scandir(distui):
        if item.name.startswith('libopenblas.') and item.name.endswith('.dll'):
            print('removing libopenblas ...')
            os.remove(item.path)
        if item.is_dir() and item.name in ['lib2to3', 'Include', 'numpy']:
            print(f'removing {item.name} ...')
            shutil.rmtree(item.path, ignore_errors=True)

    config_file = join(distlib, 'a2_config.ahk')
    a2ahk.set_variable(config_file, 'a2_title', package_name)

    with open(join(distpath, 'desktop.ini'), 'w') as file_obj:
        file_obj.write(DESKTOP_INI_CODE)

    with open(join(distroot, 'config.txt'), 'w') as file_obj:
        file_obj.write(INSTALLER_CFG)


def _ignore_items(path, items):
    result = []
    path_low = os.path.normpath(path.lower())
    for item in items:
        # ignore temp stuff
        if item.startswith('_ '):
            result.append(item)
            continue

        # ignore ahk lib tests
        if path_low.endswith('\\a2\\lib\\autohotkey\\lib\\test'):
            result.append(item)
            continue

        item_path = join(path, item)
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


def update_manifest(srcpath, version, distroot):
    manifest_path = join(srcpath, MANIFEST_NAME)
    if not os.path.isfile(manifest_path):
        print('ERROR: No manifest file: %s' % manifest_path)
        return

    versions = []
    for i, n in enumerate(version.split('.')):
        if not n.isdigit():
            print('ERROR:\n  Bad Nr in version string %i: %n' % (i, n))
            continue
        versions.append(n)
    versions.extend((4 - len(versions)) * '0')

    content = ''
    with codecs.open(manifest_path, encoding=a2util.UTF8_CODEC) as fobj:
        for line in fobj:
            line = line.strip()
            if not line:
                continue
            if line.startswith('<?xml version="'):
                continue
            if line.startswith('<!--'):
                continue

            if line.startswith('version="'):
                line = 'version="%s"' % '.'.join(versions)
                print(line)

            if not line.endswith('>'):
                line += ' '
            content += line

    manifest_trg = join(distroot, MANIFEST_NAME)
    a2util.write_utf8(manifest_trg, content)
    print('manifest written: %s' % manifest_trg)


if __name__ == '__main__':
    main()
