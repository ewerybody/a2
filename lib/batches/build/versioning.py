"""
a2 package build script for versioning
"""
import os
import _build_package_init
import a2ahk
import a2util
from os.path import join
from shutil import copy2
import subprocess
import codecs

A2PATH = _build_package_init.a2path
A2UIPATH = _build_package_init.uipath
MANIFEST_NAME = 'a2_installer_manifest.xml'
PACKAGE_SUB_NAME = 'alpha'
SRC_SFX = 'a2_installer.sfx.exe'
RCEDIT_EXE = 'rcedit-x64.exe'


def main():
    package_cfg = a2util.json_read(join(A2PATH, 'package.json'))
    package_name = f'a2 {PACKAGE_SUB_NAME} {package_cfg["version"]}'
    print('package_name: %s' % package_name)

    distroot = join(A2PATH, '_ package')
    # distpath = join(distroot, 'a2')
    srcpath = join(A2PATH, 'lib', '_source')

    sfx_path = join(srcpath, SRC_SFX)
    if not os.path.isfile(sfx_path):
        raise FileNotFoundError('SFX file "%s" is missing!' % sfx_path)

    sfx_trg = join(distroot, SRC_SFX)
    if os.path.isfile(sfx_trg):
        os.unlink(sfx_trg)
    copy2(sfx_path, sfx_trg)

    rcedit = join(srcpath, RCEDIT_EXE)
    if not os.path.isfile(rcedit):
        raise FileNotFoundError('rcedit "%s" is missing!' % rcedit)

    version_string = check_version(package_cfg['version'])
    version_label = (version_string if not PACKAGE_SUB_NAME else
                     version_string + ' ' + PACKAGE_SUB_NAME)

    set_file_version(rcedit, sfx_trg, version_label)
    set_product_version(rcedit, sfx_trg, version_label)


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


def prepare_versioning_files(srcpath, version_string, distroot):
    manifest_path = join(srcpath, MANIFEST_NAME)
    if not os.path.isfile(manifest_path):
        print('ERROR: No manifest file: %s' % manifest_path)
        return

    # write some simple text files to get version strings from
    with open(join(distroot, 'version.txt'), 'w') as file_object:
        file_object.write(version_string)
    with open(join(distroot, 'version_string.txt'), 'w') as file_object:
        if PACKAGE_SUB_NAME:
            file_object.write(version_string + ' ' + PACKAGE_SUB_NAME)
        else:
            file_object.write(version_string)

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


if __name__ == '__main__':
    main()
