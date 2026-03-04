import a2dl

SQLITE_URL = 'https://www.sqlite.org/'


def get_latest_version() -> tuple[tuple[int, ...], str, int]:
    download_page = a2dl.read(SQLITE_URL + 'download.html')
    pos = download_page.find('/sqlite-dll-win-x64-')
    if pos == -1:
        return ((), '')

    line_start = download_page.rfind('PRODUCT,', pos - 100, pos)
    line_end = download_page.find('\n', pos)
    line = download_page[line_start:line_end]
    try:
        latest_version, path, size, _checksum = line.split(',')[1:]
    except ValueError:
        return ((), '')

    return tuple(int(v) for v in latest_version.split('.')), f'{SQLITE_URL}{path}', int(size)


# def asdf():
#     sql_path = os.path.join(Paths.dist_ui, 'sqlite3.dll')

#     script = os.path.join(Paths.batches, 'versions', 'get_version.ahk')
#     script_wd = os.path.dirname(os.path.dirname(script))
#     if os.path.isfile(sql_path):
#         current_version = subprocess.check_output([Paths.ahk_exe, script, sql_path], cwd=script_wd).decode()
#         current = tuple(int(v) for v in current_version.split('.'))
#         if current >= latest:
#             print(f'  {CHK_MK} SQLite3 already up-to-date! ({current_version})')
#             return
#     else:
#         current_version = '?'

#     print(f'  Updating SQLite3 from {current} to latest: {latest} ...')
#     zip_path = os.path.join(Paths.py_packs, os.path.basename(path))
#     if not os.path.isfile(zip_path):
#         print('  Downloading ...')
#         new_sqlite_data = request.urlopen(SQLITE_URL + path).read()
#         # new_sqlite_data = qdl.read_raw(SQLITE_URL + path)
#         with open(zip_path, 'wb') as file_obj:
#             file_obj.write(new_sqlite_data)

#     with zipfile.ZipFile(zip_path) as tmp_zip:
#         for filename in tmp_zip.namelist():
#             if filename == 'sqlite3.dll':
#                 tmp_zip.extract(filename, Paths.dist_ui)
#                 break

#     current_version = subprocess.check_output([Paths.ahk_exe, script, sql_path], cwd=script_wd).decode()
#     current = tuple(int(v) for v in current_version.split('.'))
#     if current >= latest:
#         print(f'  {CHK_MK} SQLite3 Updated!')
#         return
#     print(f'  {EX_MRK} ERROR: SQLite3 Update failed! Current: {current_version}/Latest: {latest_version}')
