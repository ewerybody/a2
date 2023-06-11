"""
a2 installer build helper script.
Called AFTER the PyInstaller package was built via _build_py_package.bat
And after the package was handled by _finish_py_package.bat and finish_package.py.
"""
import os
import sys
import time
import shutil
import codecs
import subprocess

import _build_package_init
import a2core
import a2util

Paths = _build_package_init.Paths
PACKAGE_SUB_NAME = _build_package_init.PACKAGE_SUB_NAME
TMP_NAME = a2core.NAME + '_temp_buildpath'
NFO_DESCRIPTION = a2core.NAME + ' self-extracting installation package.'
SETUP_EXE = 'setup.exe'
INSTALLER_CFG = f';!@Install@!UTF-8!\nRunProgram="{SETUP_EXE}"\n;!@InstallEnd@!'
ERROR_NO_PACKAGE = 'No package? No need to build an installer :/ build a package first!'
SEVEN_FLAGS = (
    '-m0=BCJ2 -m1=LZMA:d25:fb255 -m2=LZMA:d19 -m3=LZMA:d19 -mb0:1 -mb0s1:2 -mb0s2:3 -mx'.split()
)
COMPANY = 'github.com/ewerybody/a2'
COPYRIGHT = f'GPLv3 ({COMPANY})'
EXE_NFO = {
    'FileVersion': '',
    'ProductVersion': '',
    'FileDescription': '',
    'ProductName': a2core.NAME,
    'CompanyName': COMPANY,
    'LegalCopyright': COPYRIGHT,
}
CHKMK = b'\xe2\x9c\x94'.decode()
EXMRK = b'\xe2\x9c\x96'.decode()
_prnt = sys.stdout.write
_TIMINGS = {}


def main():
    """Main process entrypoint."""
    t00 = time.time()
    Paths.check()
    if not os.path.isdir(Paths.distroot):
        raise FileNotFoundError(ERROR_NO_PACKAGE)

    package_cfg = a2util.json_read(Paths.package_config)
    package_name = f'{a2core.NAME} {PACKAGE_SUB_NAME} {package_cfg["version"]}'
    print('\n{0} building installer: {1} ... {0}'.format(15 * '#', package_name))

    version_string = _check_version(package_cfg['version'])
    version_label = (
        version_string if not PACKAGE_SUB_NAME else version_string + ' ' + PACKAGE_SUB_NAME
    )
    t_mainchecks = time.time() - t00

    t0 = time.time()
    _create_fresh_sfx_files()
    t_create_fresh_sfx_files = time.time() - t0

    t0 = time.time()
    _update_manifest(version_string)
    t_update_manifest = time.time() - t0

    t0 = time.time()
    _pack_installer_archive()
    t_pack_installer_archive = time.time() - t0

    t0 = time.time()
    _copy_together_installer_binary(package_cfg['version'])
    t_copy_together_installer_binary = time.time() - t0

    t0 = time.time()
    _make_portable()
    t_make_portable = time.time() - t0

    print('%s took %.3fs' % ('main checks', time.time() - t0))
    print('t_mainchecks: %s' % t_mainchecks)
    print('t_create_fresh_sfx_files: %s' % t_create_fresh_sfx_files)
    print('t_update_manifest: %s' % t_update_manifest)
    print('t_pack_installer_archive: %s' % t_pack_installer_archive)
    print('t_copy_together_installer_binary: %s' % t_copy_together_installer_binary)
    print('t_make_portable: %s' % t_make_portable)
    print('t_all_in_all: %s' % (time.time() - t00))


def _set_rc_nfo(target_path: str, nfo: dict[str, str]):
    for key, value in nfo.items():
        _set_rc_key(target_path, key, value)


def _set_rc_key(target_path, key, value_string):
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

    For key names have a look at the `string-name` section under:
    https://docs.microsoft.com/en-us/windows/win32/menurc/versioninfo-resource#parameters
    FileDescription, ProductName, LegalCopyright, OriginalFilename, CompanyName
    """
    try:
        current = subprocess.check_output(
            [Paths.rcedit, target_path, '--get-version-string', key]
        ).decode()
    except subprocess.CalledProcessError:
        current = ''

    if current == value_string:
        return

    _prnt('Set "%s" on "%s"...' % (key, os.path.basename(target_path)))
    if key == 'FileVersion':
        subprocess.call([Paths.rcedit, target_path, '--set-file-version', value_string])
    elif key == 'ProductVersion':
        subprocess.call([Paths.rcedit, target_path, '--set-product-version', value_string])
    else:
        subprocess.call([Paths.rcedit, target_path, '--set-version-string', key, value_string])

    # check if things were changed correctly
    current = subprocess.check_output(
        [Paths.rcedit, target_path, '--get-version-string', key]
    ).decode()
    if current == value_string:
        print(' %s %s' % (CHKMK, value_string))
    else:
        print(' %s "%s" is "%s" NOT "%s"!' % (EXMRK, key, current, value_string))


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
                line = f'version="{version_string}"'

            if not line.endswith('>'):
                line += ' '
            content += line

    a2util.write_utf8(Paths.manifest_target, content)
    print('manifest written: %s' % Paths.manifest_target)


def _apply_manifest(sfx_target):
    subprocess.call([Paths.rcedit, sfx_target, '--application-manifest', Paths.manifest_target])


def _pack_installer_archive():
    # "%sevenx%" a "%archive%" "%distpath%" -m0=BCJ2 -m1=LZMA:d25:fb255 -m2=LZMA:d19
    # -m3=LZMA:d19 -mb0:1 -mb0s1:2 -mb0s2:3 -mx
    if _need_rezipping():
        t0 = time.time()
        subprocess.call([Paths.sevenz_exe, 'a', Paths.archive_target, Paths.dist] + SEVEN_FLAGS)
        print('packing archive took: %.2fsec' % (time.time() - t0))


def _need_rezipping():
    """
    If there are any changes in the distpath: Return True
    """
    result = False
    if not os.path.isfile(Paths.archive_target):
        print('Re-zip: TRUE :: No Archive yet!')
        result = True

    tmp_dir = os.path.join(os.environ['TEMP'], TMP_NAME)
    if not os.path.isdir(tmp_dir):
        os.makedirs(tmp_dir)
    digest_path = os.path.join(tmp_dir, 'archive_digest.json')
    if _diff_digest(digest_path):
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
                'size': os.path.getsize(item_path),
            }
    return digest_map


def _diff_digest(digest_path):
    """Return True if there is no difference in the digest."""
    if not os.path.isfile(digest_path):
        print('Re-zip: TRUE :: No digest yet!')
        return True

    current_map = a2util.json_read(digest_path)
    for dir_path, _, files in os.walk(Paths.dist):
        this_map = current_map.get(dir_path, ())
        if len(files) != len(this_map):
            print('Re-zip: TRUE :: num files diff: %s' % dir_path)
            return True

        for item in files:
            item_path = os.path.join(dir_path, item)
            if item not in this_map:
                print('Re-zip: TRUE :: new file! %s' % item_path)
                return True

            if this_map[item]['mtime'] != os.path.getmtime(item_path):
                print('Re-zip: TRUE :: Modified item: %s' % item_path)
                return True
            if this_map[item]['size'] != os.path.getsize(item_path):
                print('Re-zip: TRUE :: Size diff: %s' % item_path)
                return True
    print('_diff_digest :: No differences.')
    return False


def _copy_together_installer_binary(version_label):
    """To Replace the batch copy stuff.
    Binary copy together works in Python like a charm too!
    The original batch script was::

        echo finishing installer executable ...
        set installerx=%distroot%\\a2_installer.exe
        copy /b "%sfx%" + "%config%" + "%archive%" "%installerx%"
    """
    name = f'{_build_package_init.NAME}_{version_label}_{PACKAGE_SUB_NAME}'
    name_ui = name + '.exe'
    name_silent = name + '_silent.exe'

    target_cfg = os.path.join(Paths.distroot, '_ config.cfg')
    with open(os.path.join(target_cfg), 'w') as file_obj:
        file_obj.write(INSTALLER_CFG)

    vnfo = EXE_NFO.copy()
    vnfo['FileVersion'] = version_label
    vnfo['ProductVersion'] = version_label

    for target_name, target_sfx, script in (
        (name_ui, Paths.sfx_target_ui, Paths.installer_script),
        (name_silent, Paths.sfx_target_silent, Paths.installer_script_silent),
    ):
        nfo = vnfo.copy()
        nfo['FileDescription'] = NFO_DESCRIPTION
        nfo['OriginalFilename'] = target_name
        _set_rc_nfo(target_sfx, nfo)
        _apply_manifest(target_sfx)

        target_path = os.path.join(Paths.distroot, target_name)
        if os.path.isfile(target_path):
            os.unlink(target_path)

        # copy archive
        this_archive = os.path.join(Paths.distroot, f'_ {target_name}.7z')
        shutil.copyfile(Paths.archive_target, this_archive)

        # add setup executable to archive
        exe_path = make_ahkexe(script, os.path.join(Paths.distroot, SETUP_EXE), nfo)
        subprocess.call([Paths.sevenz_exe, 'a', this_archive, exe_path] + SEVEN_FLAGS)
        os.unlink(exe_path)

        # copy together
        with open(target_path, 'wb') as trg_file:
            for source in (target_sfx, target_cfg, this_archive):
                with open(source, 'rb') as source_file:
                    trg_file.write(source_file.read())

        if os.path.isfile(target_path):
            print('\n%s Success!: "%s" written!\n' % (CHKMK, target_name))
        else:
            raise FileNotFoundError('%s Installer "%s" was not written!' % (EXMRK, target_name))


def _create_fresh_sfx_files():
    for src, trg in (
        (Paths.sfx_source_ui, Paths.sfx_target_ui),
        (Paths.sfx_source_silent, Paths.sfx_target_silent),
    ):
        if os.path.isfile(trg):
            os.unlink(trg)
        print(f'copy fresh sfx {os.path.basename(Paths.sfx_target_ui)} ...')
        shutil.copyfile(src, trg)
        subprocess.call([Paths.rcedit, trg, '--set-icon', Paths.a2icon])


def _make_portable():
    """
    a2 is now portable by default! This is just preparing a zip without a
    setup executable. That's all. Voila!
    """
    print('Making portable package ...')
    _prnt('  copying ... ')
    if os.path.exists(Paths.dist_portable):
        print(f'{CHKMK} Already done')
        # shutil.rmtree(Paths.dist_portable, ignore_errors=True)
    else:
        shutil.copytree(Paths.dist, Paths.dist_portable, copy_function=shutil.copyfile)
        print(f'{CHKMK} done')

    # remove unwanted files if present
    for name in 'setup',:
        path = os.path.join(Paths.dist_portable, name + '.exe')
        if os.path.isfile(path):
            os.unlink(path)

    _prnt('  zipping ... ')
    name = os.path.basename(Paths.dist_portable)
    package_cfg = a2util.json_read(Paths.package_config)
    portable_name = f'{name}_{package_cfg["version"]}_{PACKAGE_SUB_NAME}.zip'
    portable_path = os.path.join(Paths.distroot, portable_name)
    if os.path.isfile(portable_path):
        print(f'{CHKMK} Already done')
    else:
        tar = os.path.join(os.getenv('WINDIR', ''), 'System32', 'tar.exe')
        subprocess.call([tar, '-a', '-c', '-f', portable_path, '*'], cwd=Paths.dist_portable)
        print(f'{CHKMK} done')


def make_ahkexe(script, outpath, nfo=None):
    if not os.path.isfile(script):
        raise RuntimeError('No such Script File!! (%s)' % script)

    cmd = [Paths.ahk2exe, '/in', script, '/out', outpath, '/compress', '0', '/ahk', Paths.ahkexe]
    subprocess.call(cmd, cwd=Paths.lib)
    if not os.path.isfile(outpath):
        print('cmd: %s' % cmd)
        print('Paths.lib: %s' % Paths.lib)
        raise RuntimeError('%s FAIL!: "%s" was not created!\n' % (EXMRK, outpath))

    if nfo is not None:
        if not nfo.get('OriginalFilename'):
            nfo['OriginalFilename'] = os.path.basename(outpath)
        _set_rc_nfo(outpath, nfo)

    return outpath


if __name__ == '__main__':
    main()
