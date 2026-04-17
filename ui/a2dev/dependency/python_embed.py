import sys
import os
import zipfile

import a2dl
import a2ahk

from a2dev.build import CHK_MK, EX_MRK, Paths, DownloadCB

PACK_NAME = 'python-{py_ver}-embed-amd64'
PY_PACK_URL = 'https://www.python.org/ftp/python/{}/{}'

def check():
    py_ver = '.'.join(str(i) for i in sys.version_info[:3])
    pack_name = PACK_NAME.format(py_ver=py_ver)
    pack_path = os.path.join(Paths.py_packs, pack_name)

    if os.path.isdir(pack_path):
        return pack_path

    print(f'Getting py package "{pack_name}" ...')
    os.makedirs(Paths.py_packs, exist_ok=True)
    pack_zip = pack_name + '.zip'
    pack_zip_path = os.path.join(Paths.py_packs, pack_zip)

    if not os.path.isfile(pack_zip_path):
        a2dl.download(PY_PACK_URL.format(py_ver, pack_zip), pack_zip_path, progress_callback=DownloadCB(PACK_NAME).callback)

    print(f'  Unzipping "{pack_name}" ...', end='')
    with zipfile.ZipFile(pack_zip_path) as tmp_zip:
        for filename in tmp_zip.namelist():
            tmp_zip.extract(filename, pack_path)
    print(f'\b\b\b{CHK_MK} done!')
    return pack_path
