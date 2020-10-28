"""
a2 package assembly script to prepare deployment.

Whow! Batch files are such a pain!
Better keep them as short as possible.
"""
import os
import shutil
import codecs
import subprocess

import _build_package_init
import a2ahk
import a2util

Paths = _build_package_init.Paths
PACKAGE_SUB_NAME = 'alpha'
DESKTOP_ICO_FILE = 'ui/res/a2.ico'
DESKTOP_INI_CODE = ('[.ShellClassInfo]\nIconResource=%s\nIconIndex=0\n' %
                    DESKTOP_ICO_FILE)
ROOT_FILES = 'package.json', 'a2 on github.com.URL', 'LICENSE'
LIB_EXCLUDES = (
    'batches', '_source', 'a2ui', 'a2ui dev', 'ahklib', 'a2init_check',
    'a2dev_find_py', 'a2init_check', '_a2_portable', 'a2_portable',
)
UI_FOLDERS = 'a2ctrl', 'a2widget', 'a2element', 'res', 'style'
UI_REMOVE_FILES = (
    'd3dcompiler_47.dll', 'Qt5VirtualKeyboard.dll', 'libGLESv2.dll', 'Qt5Quick.dll',
    'opengl32sw.dll', 'Qt5QmlModels.dll', 'Qt5DBus.dll', 'Qt5Pdf.dll',
    r'PySide2\plugins\platforms\qwebgl.dll', r'PySide2\plugins\imageformats\qtiff.dll',
    r'PySide2\plugins\imageformats\qpdf.dll', r'PySide2\plugins\imageformats\qtga.dll'
)
UI_REMOVE_DIRS = 'lib2to3', 'Include', 'numpy', r'PySide2\translations'


def main():
    package_cfg = a2util.json_read(os.path.join(Paths.a2, 'package.json'))
    package_name = f'a2 {PACKAGE_SUB_NAME} {package_cfg["version"]}'
    print('\n{0} finishing: {1} ... {0}'.format(15 * '#', package_name))

    if not os.path.isdir(Paths.dist):
        raise FileNotFoundError('No Package found at "%s"!' % Paths.dist)

    update_readme()

    copy_files()
    cleanup()

    config_file = os.path.join(Paths.distlib, 'a2_config.ahk')
    a2ahk.set_variable(config_file, 'a2_title', package_name)

    with open(os.path.join(Paths.dist, 'desktop.ini'), 'w') as file_obj:
        file_obj.write(DESKTOP_INI_CODE)

    make_portable()

    print('{0} {1} finished! {0}\n'.format(18 * '#', package_name))


def update_readme():
    # get currently used versions
    ahk_exe = os.path.join(Paths.lib, 'Autohotkey', 'Autohotkey.exe')
    batches_dir = os.path.join(Paths.lib, 'batches')
    pattern = 'get_%s_version.ahk'
    names = 'AutoHotkey', 'PySide2', 'Python'
    scripts = (os.path.join(Paths.lib, 'cmds', pattern % names[0]),
               os.path.join(batches_dir, 'versions', pattern % names[1]),
               os.path.join(batches_dir, 'versions', pattern % names[2]))
    versions = {}
    for name, script in zip(names, scripts):
        cwd = os.path.dirname(os.path.dirname(script))
        version_str = subprocess.check_output([ahk_exe, script], cwd=cwd).decode()
        versions[name] = version_str

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
    app_path = os.path.join(Paths.dist, 'a2app')
    if not os.path.isdir(app_path):
        # raise FileNotFoundError(
        print(
            f'App Path was not found!\n  {app_path}\n'
            'Package already handled?')
    else:
        os.rename(app_path, Paths.distui)
    print('distui: %s' % Paths.distui)

    print('copying root files ...')

    for item in os.scandir(Paths.a2):
        if item.is_file() and item.name in ROOT_FILES:
            shutil.copy2(item.path, Paths.dist)

    print('copying lib files ...')
    if not os.path.isdir(Paths.distlib):
        os.mkdir(Paths.distlib)

    for item in os.scandir(Paths.lib):
        if item.name.startswith('_ '):
            continue

        base, ext = os.path.splitext(item.name)
        if base in LIB_EXCLUDES:
            continue

        if item.name == 'a2ui release.ahk':
            shutil.copy2(item.path, os.path.join(Paths.distlib, 'a2ui.ahk'))
            continue

        if item.is_file():
            if ext == a2ahk.EXTENSION:
                shutil.copy2(item.path, Paths.distlib)
        else:
            this_dest = os.path.join(Paths.distlib, item.name)
            if os.path.isdir(this_dest):
                print(f'  dir already copied: {this_dest}')
            else:
                shutil.copytree(item.path, this_dest, ignore=_ignore_items)

    print('copying ui files ...')
    for folder in UI_FOLDERS:
        this_dest = os.path.join(Paths.distui, folder)
        if os.path.isdir(this_dest):
            print(f'  dir already copied: {this_dest}')
            continue
        shutil.copytree(
            os.path.join(Paths.ui, folder),
            this_dest,
            ignore=_ignore_items,
            copy_function=shutil.copyfile
        )


def cleanup():
    print('cleaning up package ...')
    for dirname in UI_REMOVE_DIRS:
        path = os.path.join(Paths.distui, dirname)
        shutil.rmtree(path, ignore_errors=True)
    for filename in UI_REMOVE_FILES:
        path = os.path.join(Paths.distui, filename)
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


def make_portable():
    print('making portable package ...')
    if os.path.exists(Paths.dist_portable):
        shutil.rmtree(Paths.dist_portable, ignore_errors=True)

    print('  copying ...')
    shutil.copytree(Paths.dist, Paths.dist_portable, copy_function=shutil.copyfile)

    shutil.copyfile(
        os.path.join(Paths.lib, '_a2_portable.ahk'),
        os.path.join(Paths.dist_portable, 'lib', 'a2_portable.ahk')
    )
    # remove unwanted files if present
    for name in 'setup', 'Uninstall a2':
        path = os.path.join(Paths.dist_portable, name + '.exe')
        if os.path.isfile(path):
            os.unlink(path)

    print('  zipping ...')
    name = 'a2_portable'
    package_cfg = a2util.json_read(Paths.package_config)
    portable_name = f'{name}_{package_cfg["version"]}_{_build_package_init.PACKAGE_SUB_NAME}.zip'
    tar = os.path.join(os.getenv('WINDIR'), 'System32', 'tar.exe')
    subprocess.call(
        [tar, '-a', '-c', '-f',
         os.path.join(Paths.distroot, portable_name),
         '*'], cwd=Paths.dist_portable,
    )


if __name__ == '__main__':
    main()
