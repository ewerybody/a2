"""
a2 installer build helper script.
Called AFTER the package was built via build/package.py
"""

import os
import time
import shutil
import subprocess

import a2dev.build
import a2core
import a2util
from a2dev.build import PACKAGE_SUB_NAME, CHK_MK, EX_MRK
from a2dev.build import Paths, make_ahk_exe, EXE_NFO, make_4_numbers_version
from a2dev.dependency import seven_zip

NFO_DESCRIPTION = a2core.NAME + ' self-extracting installation package.'
SETUP_EXE = 'setup.exe'
INSTALLER_CFG = f';!@Install@!UTF-8!\nRunProgram="{SETUP_EXE}"\n;!@InstallEnd@!'
ERROR_NO_PACKAGE = 'No package? No need to build an installer :/ build a package first!'
USE_PRE_ZIPPED_QT = True
_DATA = {}


def main():
    """Main installer build entrypoint."""
    t00 = time.perf_counter()
    timings = {}
    for function in (
        _main_checks,
        _create_fresh_sfx_files,
        _update_manifest,
        _pack_installer_archive,
        _copy_together_installer_binaries,
        _make_portable,
    ):
        this_t = time.perf_counter()
        function()
        timings[function.__name__] = time.perf_counter() - this_t

    t_all = time.perf_counter() - t00
    print(f'\nBuild Done! {CHK_MK} took {t_all:.3f}s')
    for name, time_taken in timings.items():
        print(f'  {name}: {time_taken:.3f}s')


def _main_checks():
    Paths.check()
    if not os.path.isdir(Paths.dist_root):
        raise FileNotFoundError(ERROR_NO_PACKAGE)

    package_cfg = a2dev.build.get_package_cfg()
    version = package_cfg['project']['version']
    package_name = f'{a2core.NAME} {PACKAGE_SUB_NAME} {version}'

    print('\n{0} building installer: {1} ... {0}'.format(15 * '#', package_name))

    _DATA['version'] = version
    _DATA['package_name'] = package_name
    _DATA['version_string'] = make_4_numbers_version(version)


def _create_fresh_sfx_files():
    print('Creating fresh sfx files ...')
    for sfx, trg in (
        (seven_zip.SFX_UI, Paths.sfx_target_ui),
        (seven_zip.SFX_CLI, Paths.sfx_target_silent),
    ):
        if os.path.isfile(trg):
            os.unlink(trg)
        print(f'  {sfx} ...', end='')
        src = os.path.join(Paths.source, seven_zip.NAME, sfx)
        shutil.copyfile(src, trg)
        subprocess.call([Paths.rcedit, trg, '--set-icon', Paths.a2icon])
        print(f'\b\b\b{CHK_MK}  ')


def _update_manifest():
    """
    Read template manifest, insert the updated version, compact and
    write new file to target location.
    """
    print('Updating manifest ...', end='')
    version_string = _DATA['version_string']
    with open(os.path.join(Paths.manifest_tmp), encoding='utf8') as file_obj:
        content = file_obj.read().format(
            version=version_string,
            name=a2dev.build.NAME,
            description=a2dev.build.NAME,
        )

    with open(Paths.manifest_target, 'w', encoding='utf8') as file_obj:
        file_obj.write(content)
    print(f'\b\b\b{CHK_MK} {os.path.relpath(Paths.manifest_target, Paths.a2)}')


def _apply_manifest(sfx_target):
    subprocess.call([Paths.rcedit, sfx_target, '--application-manifest', Paths.manifest_target])


def _pack_installer_archive():
    print('Packing installer archive ...', end='')
    if not _need_re_zipping():
        print(f'\b\b\b{CHK_MK} already done!')
        return

    if os.path.isfile(Paths.archive_target):
        os.unlink(Paths.archive_target)

    t0 = time.time()
    if USE_PRE_ZIPPED_QT:
        shutil.copyfile(Paths.qt_temp + '.7z', Paths.archive_target)
    else:
        shutil.copytree(Paths.qt_temp, Paths.dist_ui, dirs_exist_ok=True)

    seven_zip.add_to_archive(Paths.dist, Paths.archive_target)
    print(f'  packing archive took: {time.time() - t0:.2f}sec')


def _need_re_zipping():
    """
    If there are any changes in the dist-path: Return True
    """
    result = False
    if not os.path.isfile(Paths.archive_target):
        print('  Re-zip: TRUE :: No Archive yet!')
        result = True

    if not os.path.isdir(Paths.temp_build):
        os.makedirs(Paths.temp_build)
    digest_path = os.path.join(Paths.temp_build, 'archive_digest.json')
    if _diff_digest(digest_path):
        t0 = time.time()
        digest_map = _create_digest()
        a2util.json_write(digest_path, digest_map)
        print(f'  creating digest took: {time.time() - t0:.2f}sec')
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
        print('  Re-zip: TRUE :: No digest yet!')
        return True

    current_map = a2util.json_read(digest_path)
    for dir_path, _, files in os.walk(Paths.dist):
        this_map = current_map.get(dir_path, ())
        if len(files) != len(this_map):
            print('  Re-zip: TRUE :: num files diff: %s' % dir_path)
            return True

        for item in files:
            item_path = os.path.join(dir_path, item)
            if item not in this_map:
                print('  Re-zip: TRUE :: new file! %s' % item_path)
                return True

            if this_map[item]['mtime'] != os.path.getmtime(item_path):
                print('  Re-zip: TRUE :: Modified item: %s' % item_path)
                return True
            if this_map[item]['size'] != os.path.getsize(item_path):
                print('  Re-zip: TRUE :: Size diff: %s' % item_path)
                return True
    return False


def _copy_together_installer_binaries():
    """To Replace the batch copy stuff.
    Binary copy together works in Python like a charm too!
    The original batch script was::

        echo finishing installer executable ...
        set installer=%dist_root%\\a2_installer.exe
        copy /b "%sfx%" + "%config%" + "%archive%" "%installer%"
    """
    print('Copying together installer binaries ...')
    version = _DATA['version']
    version_label = _DATA['version_string']
    name = f'{a2dev.build.NAME}_{version}_{PACKAGE_SUB_NAME}'

    target_cfg = os.path.join(Paths.dist_root, '_ config.cfg')
    with open(os.path.join(target_cfg), 'w') as file_obj:
        file_obj.write(INSTALLER_CFG)

    version_nfo = EXE_NFO.copy()
    version_nfo['FileVersion'] = version_label
    version_nfo['ProductVersion'] = version_label

    for target_name, target_sfx, script_path in (
        (name + '.exe', Paths.sfx_target_ui, Paths.installer_script),
        (name + '_silent.exe', Paths.sfx_target_silent, Paths.installer_script_silent),
    ):
        print(f'  {target_name}:')
        nfo = version_nfo.copy()
        nfo['FileDescription'] = NFO_DESCRIPTION
        nfo['OriginalFilename'] = target_name
        a2dev.build.set_rc_nfo(target_sfx, nfo, '    ')
        _apply_manifest(target_sfx)

        target_path = os.path.join(Paths.dist_root, target_name)
        if os.path.isfile(target_path):
            os.unlink(target_path)

        # copy archive
        this_archive = os.path.join(Paths.dist_root, f'_ {target_name}.7z')
        shutil.copyfile(Paths.archive_target, this_archive)

        # add setup executable to archive
        exe_path = make_ahk_exe(script_path, os.path.join(Paths.dist_root, SETUP_EXE), nfo, indent='    ')
        seven_zip.add_to_archive(exe_path, this_archive, '    ')
        os.unlink(exe_path)

        # copy together
        with open(target_path, 'wb') as trg_file:
            for source in (target_sfx, target_cfg, this_archive):
                with open(source, 'rb') as source_file:
                    trg_file.write(source_file.read())

        if os.path.isfile(target_path):
            print('\n  %s Success!: "%s" written!\n' % (CHK_MK, target_name))
        else:
            raise FileNotFoundError('%s Installer "%s" was not written!' % (EX_MRK, target_name))


def _make_portable():
    """
    a2 is now portable by default! This is just preparing a zip without a
    setup executable. That's all. Voila!
    """
    print('Making portable package ...\n  copying ...', end='')
    for item in os.scandir(Paths.qt_temp):
        trg_path = os.path.join(Paths.dist_ui, item.name)
        if item.is_dir() and not os.path.isdir(trg_path):
            shutil.copytree(item.path, trg_path)
        elif item.is_file() and not os.path.isfile(trg_path):
            shutil.copyfile(item.path, trg_path)

    # remove unwanted files if present
    for name in ('setup',):
        path = os.path.join(Paths.dist, name + '.exe')
        if os.path.isfile(path):
            os.unlink(path)

    print(f'\b\b\b{CHK_MK}  \n  zipping ...', end='')
    name = os.path.basename(Paths.dist)
    package_cfg = a2dev.build.get_package_cfg()
    portable_name = f'{name}_{package_cfg["project"]["version"]}_{PACKAGE_SUB_NAME}.zip'
    portable_path = os.path.join(Paths.dist_root, portable_name)
    if os.path.isfile(portable_path):
        os.unlink(portable_path)

    tar = os.path.join(os.getenv('WINDIR', ''), 'System32', 'tar.exe')
    subprocess.call([tar, '-a', '-c', '-f', portable_path, '*'], cwd=Paths.dist)
    print(f'\b\b\b{CHK_MK} Done!')

    if os.path.isfile(portable_path):
        print(f'\n  {CHK_MK} Success!: "{portable_name}" written!\n')
    else:
        raise FileNotFoundError(f'{EX_MRK} Installer "{portable_path}" was not written!')


if __name__ == '__main__':
    main()
