import io
import os
import zipfile

import a2dl
import a2ahk
from a2dev.build import Paths, CHK_MK, EX_MRK, DownloadCB
from a2dev.dependency import get_github_latest_release
from a2util import version_tuplify

NAME = 'Autohotkey'
EXE = f'{NAME}.exe'
BASE_VERSION = '2.0'
HOMEPAGE = f'https://www.{NAME}.com'
DOWNLOADS_URL = f'{HOMEPAGE}/download/{BASE_VERSION}'
LATEST_VERSION_URL = f'{DOWNLOADS_URL}/version.txt'
LATEST_VERSION_ERROR = f'Error checking latest {NAME} {BASE_VERSION} version online! '
AHK2EXE = 'Ahk2Exe'


def check():
    """Make sure AutoHotkey v2 executable and compiler are present and up-to-date."""
    check_autohotkey_exe()
    check_autohotkey_compiler()


def check_autohotkey_exe():
    print(f'  Looking up latest {EXE} {BASE_VERSION} online ...')
    release = get_github_latest_release(NAME)
    latest_version = version_tuplify(release.get('tag_name', ''))

    outdated = ''
    if os.path.isfile(Paths.ahk_exe):
        current_version = version_tuplify(a2ahk.call_lib_cmd('get_AutoHotkey_version'))
        if current_version >= latest_version:
            print(f'{CHK_MK} {NAME} is already up-to-date! {current_version}')
            return
        outdated = os.path.join(Paths.ahk_dir, f'{EXE}.outdated')
        os.rename(Paths.ahk_exe, outdated)

    print(f'  Fetching {NAME} {latest_version} ...')
    zip_asset = next((a for a in release['assets'] if a['name'].lower().endswith('.zip')), None)
    if zip_asset is None:
        os.rename(outdated, Paths.ahk_exe)
        raise RuntimeError(f'{EX_MRK} No zip asset found in latest AutoHotkey release!')

    zip_bytes = a2dl.read_raw(zip_asset['browser_download_url'], progress_callback=DownloadCB(AHK2EXE).callback)

    print('  Extracting ...')
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        names = zf.namelist()
        # Prefer explicit x64 build; fall back to AutoHotkey.exe
        src_name = next((n for n in ('AutoHotkey64.exe', 'AutoHotkey.exe') if n in names), None)
        if src_name is None:
            os.rename(outdated, Paths.ahk_exe)
            RuntimeError(f'{EX_MRK} Could not find AutoHotkey exe in zip. Contents: {names}')

        with zf.open(src_name) as src, open(Paths.ahk_exe, 'wb') as dst:
            dst.write(src.read())

        license = 'license.txt'
        if license in names:
            with zf.open(license) as src, open(os.path.join(Paths.ahk_dir, license), 'wb') as dst:
                dst.write(src.read())

    print(f'  {CHK_MK} {NAME} Updated {latest_version}!')


def check_autohotkey_compiler():
    print(f'  Looking up latest {AHK2EXE} online ...')
    release = get_github_latest_release(NAME, 'Ahk2Exe')
    latest_version = version_tuplify(release.get('tag_name', '').strip(AHK2EXE))
    if os.path.isfile(Paths.ahk2exe):
        current_version = version_tuplify(a2ahk.call_lib_cmd('get_version', Paths.ahk2exe))
        if current_version >= latest_version:
            print(f'  {CHK_MK} {AHK2EXE} is already up-to-date! {current_version}')
            return

    zip_asset = next((a for a in release['assets'] if a['name'].endswith('.zip')), None)
    if zip_asset is None:
        raise RuntimeError(f'{EX_MRK} No zip asset found in {AHK2EXE} release!')

    os.makedirs(os.path.dirname(Paths.ahk2exe), exist_ok=True)
    zip_bytes = a2dl.read_raw(zip_asset['browser_download_url'], progress_callback=DownloadCB(AHK2EXE).callback)
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        for name in zf.namelist():
            if name.endswith('/'):
                continue
            with zf.open(name) as src, open(Paths.ahk2exe, 'wb') as dst:
                dst.write(src.read())
    print(f'  {CHK_MK} {AHK2EXE} updated {latest_version}!')


def get_latest_version():
    version = a2dl.read(LATEST_VERSION_URL, size=32).strip()
    # Validate if there are dots and some numbers.
    # (there could also be letters (v for version, b for beta))
    if '.' in version and sum(c.isdecimal() for c in version) > 3:
        return version

    if version.startswith('<'):
        # cloudflare puts some 'aRe YOu huMaN?' test page in front of this m(
        # let's back up with github:
        info = get_github_latest_release(NAME)
        if 'tag_name' in info:
            return info.get('tag_name', '').lstrip('v')

        version = version.replace('\n', ' ')
        raise RuntimeError(
            f'{LATEST_VERSION_ERROR}\n'
            f'There is some HTML code inside? "{version} ..."\n'
            f'Please check in browser:\n  {LATEST_VERSION_URL}'
        )

    raise RuntimeError(f'{LATEST_VERSION_ERROR}\n  {LATEST_VERSION_URL}')


if __name__ == '__main__':
    check()
