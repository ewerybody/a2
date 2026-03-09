import os

import a2dl
import a2ahk
from a2dev.dependency import get_github_latest_release
from a2util import version_tuplify

NAME = 'rcedit'
EXE = f'{NAME}-x64.exe'
GITHUB_OWNER = 'electron'

def check():
    from a2dev.build import Paths, CHK_MK, EX_MRK, DownloadCB
    release = get_github_latest_release(GITHUB_OWNER, NAME)
    latest_version = version_tuplify(release.get('tag_name', ''))
    if os.path.isfile(Paths.rcedit):
        current_version = version_tuplify(a2ahk.call_lib_cmd('get_version', Paths.rcedit))
        if current_version >= latest_version:
            print(f'{CHK_MK} {EXE} already up-to-date!')
            return

    print(f'  Fetching {EXE} {latest_version} ...')
    asset = next((a for a in release['assets'] if a['name'] == EXE), None)
    if asset is None:
        raise RuntimeError(f'{EX_MRK} {EXE} not found in release assets!')

    rc_bytes = a2dl.read_raw(asset['browser_download_url'], progress_callback=DownloadCB(NAME).callback)
    os.makedirs(Paths.source, exist_ok=True)
    with open(Paths.rcedit, 'wb') as f:
        f.write(rc_bytes)
    print(f'  {CHK_MK} {EXE} Updated {latest_version}!')


if __name__ == '__main__':
    check()
