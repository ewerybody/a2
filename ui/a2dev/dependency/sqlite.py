import os
import zipfile

import a2dl
import a2ahk

from a2dev.build import CHK_MK, EX_MRK, Paths, DownloadCB


NAME = 'sqlite'
DISPLAY = 'SQLite3'
SQLITE_URL = f'https://www.{NAME}.org/'
DLL = f'{NAME}3.dll'


def get_latest_version() -> tuple[tuple[int, ...], str, int]:
    download_page = a2dl.read(SQLITE_URL + 'download.html')
    pos = download_page.find('/sqlite-dll-win-x64-')
    if pos == -1:
        return ((), '', 0)

    line_start = download_page.rfind('PRODUCT,', pos - 100, pos)
    line_end = download_page.find('\n', pos)
    line = download_page[line_start:line_end]
    try:
        latest_version, path, size, _checksum = line.split(',')[1:]
    except ValueError:
        return ((), '', 0)

    return tuple(int(v) for v in latest_version.split('.')), f'{SQLITE_URL}{path}', int(size)


def check(dir_path=None, latest_version=None):
    print(f'  Looking up latest {DISPLAY} online ...')
    if dir_path is None:
        dir_path = Paths.lib
    if latest_version is None:
        latest_version, latest_url, download_size = get_latest_version()

    outdated = ''
    dll_path = os.path.join(dir_path, DLL)
    if os.path.isfile(dll_path):
        current_str = a2ahk.call_lib_cmd('get_version', dll_path)
        current_version = tuple(int(v) for v in current_str.split('.'))
        if current_version >= latest_version:
            print(f'  {CHK_MK} {DISPLAY} already up-to-date! ({current_version})')
            return
        outdated = os.path.join(dir_path, f'{DLL}.outdated')
        os.rename(dll_path, outdated)

    print(f'  Fetching {DISPLAY} {latest_version} ...')
    zip_path = os.path.join(Paths.py_packs, os.path.basename(latest_url))
    if not os.path.isfile(zip_path):
        a2dl.download(latest_url, zip_path, progress_callback=DownloadCB(NAME).callback)

    with zipfile.ZipFile(zip_path) as tmp_zip:
        for filename in tmp_zip.namelist():
            if filename == DLL:
                tmp_zip.extract(filename, dir_path)
                break

    if os.path.isfile(dll_path):
        print(f'  {CHK_MK} {DISPLAY} Updated {latest_version}!')
        return

    print(f'  {EX_MRK} {DISPLAY} NOT Updated! File not found in zip?')
    if outdated:
        os.rename(outdated, dll_path)
    return
