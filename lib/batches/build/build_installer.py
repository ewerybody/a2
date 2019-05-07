"""
a2 installer build script.
"""
import os
import time
import codecs
import subprocess
from os.path import join
from shutil import copy2

import _build_package_init
import a2util

A2PATH = _build_package_init.a2path
AHK2EXE = r'C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe'
A2UIPATH = _build_package_init.uipath
MANIFEST_NAME = 'a2_installer_manifest.xml'
PACKAGE_SUB_NAME = 'alpha'
SRC_SFX = 'a2_installer.sfx.exe'
RCEDIT_EXE = 'rcedit-x64.exe'
INSTALLER_CFG = (
    ';!@Install@!UTF-8!\n'
    'RunProgram="a2\setup.exe"\n'
    ';!@InstallEnd@!')
MANIFEST_NAME = 'a2_installer_manifest.xml'
SEVENZ_EXE = r'7zr\7zr.exe'
TMP_NAME = 'a2_temp_buildpath'


def main():
    package_cfg = a2util.json_read(join(A2PATH, 'package.json'))
    package_name = f'a2 {PACKAGE_SUB_NAME} {package_cfg["version"]}'
    print('\n{0} building installer: {1} ... {0}'.format(15 * '#', package_name))

    distroot = join(A2PATH, '_ package')
    distpath = join(distroot, 'a2')
    source_path = join(A2PATH, 'lib', '_source')

    sfx_path = join(source_path, SRC_SFX)
    if not os.path.isfile(sfx_path):
        raise FileNotFoundError('SFX file "%s" is missing!' % sfx_path)

    sfx_trg = join(distroot, SRC_SFX)
    if os.path.isfile(sfx_trg):
        os.unlink(sfx_trg)
    print('copying fresh sfx file ...')
    copy2(sfx_path, sfx_trg)

    rcedit = join(source_path, RCEDIT_EXE)
    if not os.path.isfile(rcedit):
        raise FileNotFoundError('rcedit "%s" is missing!' % rcedit)

    version_string = check_version(package_cfg['version'])
    version_label = (version_string if not PACKAGE_SUB_NAME else
                     version_string + ' ' + PACKAGE_SUB_NAME)

    manifest_trg = update_manifest(source_path, version_string, distroot)

    set_file_version(rcedit, sfx_trg, version_label)
    set_product_version(rcedit, sfx_trg, version_label)
    apply_manifest(rcedit, manifest_trg, sfx_trg)

    print('writing installer config file ...')
    with open(join(distroot, 'config.txt'), 'w') as file_obj:
        file_obj.write(INSTALLER_CFG)

    check_installer_script_executable(source_path, distpath)

    pack_installer_archive(source_path, distroot, distpath)


def set_file_version(rcedit, file_path, value_string):
    set_rc_key(rcedit, file_path, 'FileVersion', '--set-file-version', value_string)


def set_product_version(rcedit, file_path, value_string):
    set_rc_key(rcedit, file_path, 'ProductVersion', '--set-product-version', value_string)


def set_rc_key(rcedit, file_path, key, arg, value_string):
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
        [rcedit, file_path, '--get-version-string', key]).decode()

    if current != value_string:
        print('Changing "%s" on file "%s" ...' % (key, os.path.basename(file_path)))
        subprocess.call([rcedit, file_path, arg, value_string])
        current = subprocess.check_output(
            [rcedit, file_path, '--get-version-string', key]).decode()
        if current == value_string:
            print('  Success! "%s" is now "%s"!' % (key, value_string))
        else:
            print('  ERROR! "%s" is "%s" NOT "%s"!' % (key, current, value_string))


def check_version(version):
    version_list = []
    for i, n in enumerate(version.split('.')):
        if not n.isdigit():
            print('ERROR:\n  Bad Nr in version string %i: %s' % (i, n))
            continue
        version_list.append(n)
    version_list.extend((4 - len(version_list)) * '0')
    version_string = '.'.join(version_list)
    return version_string


def update_manifest(source_path, version_string, distroot):
    """
    Reads the template manifest, inserts the updated version, compacts and
    writes the new file to its target location.
    """
    manifest_path = join(source_path, MANIFEST_NAME)
    if not os.path.isfile(manifest_path):
        print('ERROR: No manifest file: %s' % manifest_path)
        return

    # write the manifest file
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
                line = 'version="%s"' % version_string
                print(line)

            if not line.endswith('>'):
                line += ' '
            content += line

    manifest_trg = join(distroot, MANIFEST_NAME)
    a2util.write_utf8(manifest_trg, content)
    print('manifest written: %s' % manifest_trg)
    return manifest_trg


def apply_manifest(rcedit, manifest_trg, file_path):
    subprocess.call([rcedit, file_path, '--application-manifest', manifest_trg])


def pack_installer_archive(source_path, distroot, distpath):
    # "%sevenx%" a "%archive%" "%distpath%" -m0=BCJ2 -m1=LZMA:d25:fb255 -m2=LZMA:d19 -m3=LZMA:d19 -mb0:1 -mb0s1:2 -mb0s2:3 -mx
    seven_zip_executable = os.path.join(source_path, SEVENZ_EXE)
    archive_path = os.path.join(distroot, 'archive.7z')
    if not os.path.isfile(seven_zip_executable):
        raise FileNotFoundError('Cannot zip package! %s not here!' % seven_zip_executable)

    if need_rezipping(archive_path, distpath):
        t0 = time.time()
        subprocess.call(
            [seven_zip_executable, 'a', archive_path, distpath,
             '-m0=BCJ2', '-m1=LZMA:d25:fb255', '-m2=LZMA:d19', '-m3=LZMA:d19',
             '-mb0:1', '-mb0s1:2', '-mb0s2:3', '-mx'])
        print('packing archive took: %.2fsec' % (time.time() - t0))


def need_rezipping(archive_path, distpath):
    """
    If there are any changes in the distpath: Return True
    """
    result = False
    if not os.path.isfile(archive_path):
        result = True

    digest_path = os.path.join(os.environ['TEMP'], TMP_NAME, 'archive_digest.json')
    if not diff_digest(distpath, digest_path):
        t0 = time.time()
        digest_map = create_digest(distpath)
        a2util.json_write(digest_path, digest_map)
        print('creating digest took: %.2fsec' % (time.time() - t0))
        result = True
    return result


def create_digest(distpath):
    digest_map = {}
    for dir_path, _, files in os.walk(distpath):
        if files:
            digest_map[dir_path] = {}
        for item in files:
            item_path = os.path.join(dir_path, item)
            digest_map[dir_path][item] = {'mtime': os.path.getmtime(item_path),
                                          'size': os.path.getsize(item_path)}
    return digest_map


def diff_digest(distpath, digest_path):
    """Return True if there is no difference"""
    if not os.path.isfile(digest_path):
        print('diff_digest: no digest yet!')
        return False

    current_map = a2util.json_read(digest_path)
    for dir_path, _, files in os.walk(distpath):
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


def check_installer_script_executable(source_path, distpath):
    script_path = os.path.join(source_path, 'a2_installer.ahk')
    if not os.path.isfile(script_path):
        raise FileNotFoundError('installer_script missing! %s' % script_path)

    json_path = os.path.join(os.environ['TEMP'], TMP_NAME, 'script_time.json')
    setup_exe = os.path.join(distpath, 'setup.exe')
    current_time = os.path.getmtime(script_path)

    if not os.path.isfile(setup_exe) or not os.path.isfile(json_path):
        print('check_installer_script_executable: Creating setup_exe!')
        _rebuild_installer_script_executable(script_path, setup_exe)
        a2util.json_write(json_path, current_time)
        return
    else:
        script_time = a2util.json_read(json_path)
        if script_time != current_time:
            print('check_installer_script_executable: Script Changed!')
            _rebuild_installer_script_executable(script_path, setup_exe)
            a2util.json_write(json_path, current_time)
            return
    print('check_installer_script_executable: Nice Nothing to-do!!')


def _rebuild_installer_script_executable(script_path, setup_exe):
    # "%Ahk2Exe%" /in "%source_path%\a2_installer.ahk" /out "%distpath%\setup.exe" /mpress 0
    cmds = [AHK2EXE, '/in', script_path, '/out', setup_exe, '/mpress', '0']
    subprocess.call(subprocess.list2cmdline(cmds))


if __name__ == '__main__':
    main()
