"""
a2 installer build helper script.
Called AFTER the PyInstaller package was built via _build_py_package.bat
And after the package was handled by _finish_py_package.bat and finish_package.py.
"""
import os
import time
import codecs
import subprocess
from shutil import copy2

import _build_package_init
import a2util

Paths = _build_package_init.Paths
PACKAGE_SUB_NAME = _build_package_init.PACKAGE_SUB_NAME
TMP_NAME = 'a2_temp_buildpath'
INSTALLER_CFG = (
    ';!@Install@!UTF-8!\n'
    'RunProgram="a2\\setup.exe"\n'
    ';!@InstallEnd@!')
ERROR_NO_PACKAGE = 'No package? No need to build an installer :/ build a package first!'


def main():
    """Main process entrypoint."""
    Paths.check()
    if not os.path.isdir(Paths.distroot):
        raise FileNotFoundError(ERROR_NO_PACKAGE)

    package_cfg = a2util.json_read(Paths.package_config)
    package_name = f'a2 {PACKAGE_SUB_NAME} {package_cfg["version"]}'
    print('\n{0} building installer: {1} ... {0}'.format(15 * '#', package_name))

    os.makedirs(Paths.distroot, exist_ok=True)

    if os.path.isfile(Paths.sfx_target):
        os.unlink(Paths.sfx_target)
    print('copying fresh sfx file ...')
    copy2(Paths.sfx, Paths.sfx_target)

    version_string = _check_version(package_cfg['version'])
    version_label = (version_string if not PACKAGE_SUB_NAME else
                     version_string + ' ' + PACKAGE_SUB_NAME)

    _update_manifest(version_string)
    _set_rc_key('FileVersion', '--set-file-version', version_label)
    _set_rc_key('ProductVersion', '--set-product-version', version_label)
    _apply_manifest()

    print('writing installer config file ...')
    with open(os.path.join(Paths.config_target), 'w') as file_obj:
        file_obj.write(INSTALLER_CFG)

    _check_installer_script_executable()

    _pack_installer_archive()

    _copy_together_installer_binary(package_cfg["version"])


def _set_rc_key(key, arg, value_string):
    """
    --set-version-string <key> <value>         Set version string
    --get-version-string <key>                 Print version string
    --set-file-version <version>               Set FileVersion
    --set-product-version <version>            Set ProductVersion
    --set-icon <path-to-icon>                  Set file icon
    --set-requested-execution-level <level>    Pass nothing to see usage
    --application-manifest <path-to-file>      Set manifest file
    --set-resource-string <key> <value>        Set resource string
    --get-resource-string <key>                Get resource string
    """
    current = subprocess.check_output(
        [Paths.rcedit, Paths.sfx_target, '--get-version-string', key]).decode()

    if current != value_string:
        print('Changing "%s" on file "%s" ...' % (key, os.path.basename(Paths.sfx_target)))
        subprocess.call([Paths.rcedit, Paths.sfx_target, arg, value_string])
        # check if things were changed correctly
        current = subprocess.check_output(
            [Paths.rcedit, Paths.sfx_target, '--get-version-string', key]).decode()
        if current == value_string:
            print('  Success! "%s" is now "%s"!' % (key, value_string))
        else:
            print('  ERROR! "%s" is "%s" NOT "%s"!' % (key, current, value_string))


def _check_version(version):
    """Have a look at our version string if it works like semver style."""
    version_list = []
    for i, number in enumerate(version.split('.')):
        if not number.isdigit():
            print('ERROR:\n  Bad Nr in version string %i: %s' % (i, number))
            continue
        version_list.append(number)
    version_list.extend((4 - len(version_list)) * '0')
    version_string = '.'.join(version_list)
    return version_string


def _update_manifest(version_string):
    """
    Read template manifest, insert the updated version, compact and
    write new file to target location.
    """
    content = ''
    with codecs.open(Paths.manifest, encoding=a2util.UTF8_CODEC) as fobj:
        for line in fobj:
            line = line.strip()
            if not line:
                continue
            if line.startswith('<?xml version="'):
                continue
            if line.startswith('<!--'):
                continue

            if line.startswith('version="'):
                line = 'version="%s"' % version_string
                print(line)

            if not line.endswith('>'):
                line += ' '
            content += line

    a2util.write_utf8(Paths.manifest_target, content)
    print('manifest written: %s' % Paths.manifest_target)


def _apply_manifest():
    subprocess.call(
        [Paths.rcedit, Paths.sfx_target, '--application-manifest', Paths.manifest_target])


def _pack_installer_archive():
    # "%sevenx%" a "%archive%" "%distpath%" -m0=BCJ2 -m1=LZMA:d25:fb255 -m2=LZMA:d19
    # -m3=LZMA:d19 -mb0:1 -mb0s1:2 -mb0s2:3 -mx
    if _need_rezipping():
        t0 = time.time()
        subprocess.call(
            [Paths.sevenz_exe, 'a', Paths.archive_target, Paths.dist,
             '-m0=BCJ2', '-m1=LZMA:d25:fb255', '-m2=LZMA:d19', '-m3=LZMA:d19',
             '-mb0:1', '-mb0s1:2', '-mb0s2:3', '-mx'])
        print('packing archive took: %.2fsec' % (time.time() - t0))


def _need_rezipping():
    """
    If there are any changes in the distpath: Return True
    """
    result = False
    if not os.path.isfile(Paths.archive_target):
        result = True

    digest_path = os.path.join(os.environ['TEMP'], TMP_NAME, 'archive_digest.json')
    if not _diff_digest(digest_path):
        t0 = time.time()
        digest_map = _create_digest()
        a2util.json_write(digest_path, digest_map)
        print('creating digest took: %.2fsec' % (time.time() - t0))
        result = True
    return result


def _create_digest():
    digest_map = {}
    for dir_path, _, files in os.walk(Paths.dist):
        if files:
            digest_map[dir_path] = {}
        for item in files:
            item_path = os.path.join(dir_path, item)
            digest_map[dir_path][item] = {
                'mtime': os.path.getmtime(item_path),
                'size': os.path.getsize(item_path)}
    return digest_map


def _diff_digest(digest_path):
    """Return True if there is no difference in the digest."""
    if not os.path.isfile(digest_path):
        print('diff_digest: no digest yet!')
        return False

    current_map = a2util.json_read(digest_path)
    for dir_path, _, files in os.walk(Paths.dist):
        this_map = current_map.get(dir_path, ())
        if len(files) != len(this_map):
            print('diff_digest: num files diff: %s' % dir_path)
            return False

        for item in files:
            item_path = os.path.join(dir_path, item)
            if item not in this_map:
                print('diff_digest: new file! %s' % item_path)
                return False

            if this_map[item]['mtime'] != os.path.getmtime(item_path):
                print('diff_digest: mtime diff! %s' % item_path)
                return False
            if this_map[item]['size'] != os.path.getsize(item_path):
                print('diff_digest: size diff! %s' % item_path)
                return False
    print('diff_digest: No differences!!')
    return True


def _check_installer_script_executable():
    json_path = os.path.join(os.environ['TEMP'], TMP_NAME, 'script_time.json')
    setup_exe = os.path.join(Paths.dist, 'setup.exe')
    current_time = os.path.getmtime(Paths.installer_script)

    write_exe = False
    if os.path.isfile(setup_exe) and os.path.isfile(json_path):
        script_time = a2util.json_read(json_path)
        if script_time != current_time:
            print('check_installer_script_executable: Script Changed!')
            write_exe = True
    else:
        print('check_installer_script_executable: Creating setup_exe!')
        write_exe = True

    if not write_exe:
        print('check_installer_script_executable: Nice Nothing to-do!!')
        return

    _rebuild_installer_script_executable(setup_exe)
    a2util.json_write(json_path, current_time)


def _rebuild_installer_script_executable(setup_exe):
    # "%Ahk2Exe%" /in "%source_path%\a2_installer.ahk" /out "%distpath%\setup.exe" /mpress 0
    cmds = [Paths.ahk2exe, '/in', Paths.installer_script, '/out', setup_exe, '/mpress', '0']
    subprocess.call(subprocess.list2cmdline(cmds))


def _copy_together_installer_binary(version_label):
    """To Replace the batch copy stuff.
    Binary copy together works in Python like a charm too!
    The original batch script was::

        echo finishing installer executable ...
        set installerx=%distroot%\\a2_installer.exe
        copy /b "%sfx%" + "%config%" + "%archive%" "%installerx%"
    """
    installer_name = f'{_build_package_init.NAME}_{version_label}_{PACKAGE_SUB_NAME}.exe'
    installer_target = os.path.join(Paths.distroot, installer_name)
    print('installer_target: %s' % installer_target)
    if os.path.isfile(installer_target):
        os.unlink(installer_target)

    with open(installer_target, 'wb') as installer_file:
        for source in (Paths.sfx_target, Paths.config_target, Paths.archive_target):
            with open(source, 'rb') as source_file:
                installer_file.write(source_file.read())

    if os.path.isfile(installer_target):
        print('Success!: %s written!' % installer_name)
    else:
        raise FileNotFoundError('Installer "%s" was not written!' % installer_name)


if __name__ == '__main__':
    main()
