import os
import shutil
import tempfile
import subprocess

import a2dl
import a2ahk
import a2path

from a2dev.dependency import get_github_latest_release

# Perform lazy import to avoid cyclic import problems
# from a2dev.build import Paths, CHK_MK, EX_MRK, DownloadCB
from a2util import version_tuplify

NAME = '7zr'
DISPLAY = '7zip'
EXE = f'{NAME}.exe'
SFX = f'{NAME}.sfx.exe'
FLAGS = '-m0=BCJ2 -m1=LZMA:d25:fb255 -m2=LZMA:d19 -m3=LZMA:d19 -mb0:1 -mb0s1:2 -mb0s2:3 -mx'.split()
SFX_UI = '7zSD.sfx'
SFX_CLI = '7zS2con.sfx'
SDK_NAME = 'lzma'
GITHUB_OWNER = 'ip7z'
FILES = (SFX_UI, SFX_CLI, 'lzma-sdk.txt')
EVERYTHING_OK = 'Everything is Ok'

def check():
    """Make sure 7-Zip tools needed for building the self extracting installer are available
    and up-to-date.
    """
    from a2dev.build import CHK_MK, EX_MRK, DownloadCB

    print(f'  Looking up latest {DISPLAY} online ...')
    release = get_github_latest_release(GITHUB_OWNER, DISPLAY)
    latest_version = version_tuplify(release.get('tag_name', ''))
    seven_zip_dir, seven_zip_exe = get_paths()
    if os.path.isfile(seven_zip_exe):
        current_version = version_tuplify(a2ahk.call_lib_cmd('get_version', seven_zip_exe))
        if current_version >= latest_version:
            print(f'{CHK_MK} {EXE} already up-to-date {current_version}!')
            return
        shutil

    print(f'  Fetching {DISPLAY} {latest_version} ...')
    asset = next((a for a in release['assets'] if a['name'] == EXE), None)
    if asset is None:
        raise RuntimeError(f'{EX_MRK} {EXE} not found in release assets!')
    os.makedirs(seven_zip_dir, exist_ok=True)
    a2dl.download(asset.get('browser_download_url', ''), seven_zip_exe, progress_callback=DownloadCB(EXE).callback)

    asset = next((a for a in release['assets'] if a['name'].startswith(SDK_NAME) and a['name'].endswith('.7z')), None)
    if asset is None:
        raise RuntimeError(f'{EX_MRK} {SDK_NAME} not found in release assets!')

    with tempfile.NamedTemporaryFile(suffix='.7z') as tmp:
        callback = DownloadCB(SDK_NAME).callback
        a2dl.download(asset['browser_download_url'], tmp.name, overwrite=True, progress_callback=callback)
        extracted_tmp = f'{tmp.name}_x'
        cmd = [seven_zip_exe, 'e', tmp.name, f'-o{extracted_tmp}', '-y']
        subprocess.call(cmd, stdout=subprocess.DEVNULL)

        for item in a2path.iter_files(extracted_tmp):
            if item.name not in FILES:
                continue
            os.rename(item.path, os.path.join(seven_zip_dir, item.name))

    print(f'  {CHK_MK} {DISPLAY} updated {latest_version}!')


def add_to_archive(source, destination_archive, indent=''):
    from a2dev.build import CHK_MK
    _, exe_path = get_paths()
    print(f'{indent}Adding to archive ...')
    args = [exe_path, 'a', destination_archive, source] + FLAGS
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert process.stdout is not None

    line_nr = 0
    for line in process.stdout:
        print(f'{indent}  7zip {line_nr}: {line}', end='')
        line_nr += 1
    process.wait()
    if line.strip() == EVERYTHING_OK:
        print(f'{indent}{CHK_MK} {EVERYTHING_OK}!')


def get_paths():
    from a2dev.build import Paths

    dir_path = os.path.join(Paths.source, NAME)
    exe_path = os.path.join(dir_path, EXE)
    return dir_path, exe_path


if __name__ == '__main__':
    check()
