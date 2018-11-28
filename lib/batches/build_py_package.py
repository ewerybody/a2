"""
package builder script

Whow! Batch files are such a pain. Petter keep them as short as possible.
"""
import os
import sys
import shutil
from os.path import join


def main(package_name):
    this_path = os.path.dirname(__file__)
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
        if item.name in ['a2_init.ahk', 'a2_settings.ahk']:
            continue

        if item.is_file():
            if item.name.endswith('.ahk') or item.name in ['LICENSE']:
                shutil.copy2(item.path, distpath)

    print('copying lib files ...')
    distlib = join(distpath, 'lib')
    a2lib = join(a2path, 'lib')
    os.mkdir(distlib)
    for item in os.scandir(a2lib):
        base, ext = os.path.splitext(item.name)
        if base in ['batches', '_source', 'a2ui', 'a2ui dev',
                    'a2init_check', 'a2dev_find_py', 'a2init_check']:
            continue
        if base.startswith('_ '):
            continue

        if item.name == 'a2ui release.ahk':
            shutil.copy2(item.path, join(distlib, 'a2ui.ahk'))
            continue

        if item.is_file():
            if ext == '.ahk':
                shutil.copy2(item.path, distlib)
        else:
            shutil.copytree(item.path, join(distlib, item.name))

    print('copying ui files ...')
    a2uipath = join(a2path, 'ui')

    def ui_ignore(path, items):
        return [f for f in items if f.endswith('.ui')] + ['__pycache__', 'demo', 'work']

    for folder in ['a2ctrl', 'a2widget', 'a2element', 'res', 'style']:
        shutil.copytree(join(a2uipath, folder),
                        join(distui, folder), ignore=ui_ignore)

    shutil.rmtree(join(distui, 'PySide', folder), ignore_errors=True)
    for item in os.scandir(distui):
        if item.name.startswith('libopenblas.') and item.name.endswith('.dll'):
            print('removing libopenblas ...')
            os.remove(item.path)
            break

    numpy_path = join(distui, 'numpy')
    if os.path.isdir(numpy_path):
        print('removing numpy ...')
        shutil.rmtree(numpy_path, ignore_errors=True)

    github_link_name = 'a2 on github.com.URL'
    shutil.copy(join(a2path, github_link_name),
                join(distpath, github_link_name))

    config_file = join(distlib, 'a2_config.ahk')
    a2ahk.set_variable(config_file, 'a2_title', package_name)


if __name__ == '__main__':
    main(sys.argv[1])
