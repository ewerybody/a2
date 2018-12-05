"""
package builder script

Whow! Batch files are such a pain. Petter keep them as short as possible.
"""
import os
import sys
import shutil
from os.path import join

this_path = os.path.dirname(__file__)


def main(package_name):
    a2path = os.path.abspath(join(this_path, '..', '..'))
    uipath = join(a2path, 'ui')
    sys.path.append(uipath)
    import a2ahk

    distpath = join(a2path, '_ package')
    print('distpath: %s' % distpath)
    distui = join(distpath, 'ui')
    os.rename(join(distpath, 'a2app'), distui)
    print('copying root files ...')

    for item in os.scandir(a2path):
        if item.is_file() and item.name in ['a2 on github.com.URL', 'LICENSE']:
            shutil.copy2(item.path, distpath)

    print('copying lib files ...')
    distlib = join(distpath, 'lib')
    a2lib = join(a2path, 'lib')
    os.mkdir(distlib)
    for item in os.scandir(a2lib):
        if item.name.startswith('_ '):
            continue

        base, ext = os.path.splitext(item.name)
        if base in ['batches', '_source', 'a2ui', 'a2ui dev', 'ahklib',
                    'a2init_check', 'a2dev_find_py', 'a2init_check']:
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

    for folder in ['a2ctrl', 'a2widget', 'a2element', 'res', 'style']:
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


def _ignore_items(path, items):
    result = []
    for item in items:
        if item.startswith('_ '):
            result.append(item)
            continue

        item_path = join(path, item)
        if os.path.isdir(item_path):
            if item in ['__pycache__']:
                result.append(item)
            elif item == 'demo' and os.path.basename(path) == 'a2widget':
                result.append(item)

        elif item.endswith('.ui'):
            result.append(item)

    if result:
        print('IGNORING: %s' % result)

    return result


def _get_package_name():
    with open(join(this_path, 'build_py_package.bat')) as file_obj:
        for line in file_obj:
            if line.startswith('set package_name'):
                return line.split('=')[1].strip()
    raise RuntimeError('package_name could not be fetched from batch file!')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append(_get_package_name())
    main(sys.argv[1])
