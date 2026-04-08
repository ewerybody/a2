import os
import winreg
from pathlib import Path

import a2ahk
import a2path
import a2toolbox.reg
from a2util import version_tuplify

INKSCAPE = 'inkscape'
EXE_PATH = os.path.join('bin', f'{INKSCAPE}.exe')
THIS_DIR = Path(__file__).parent.resolve()
PATH_FILE_NAME = f'_ {INKSCAPE}_path.txt'
PATH_FILE = THIS_DIR / PATH_FILE_NAME


def get_path() -> Path:
    """Find InkScape executable or take a user defined one.
    For exporting highest quality pixels from SVG files we NEED InkScape.
    """
    path: str = get_user_path()
    if path:
        return Path(path)

    paths = []
    for item in a2path.iter_dirs(os.getenv('PROGRAMFILES', '')):
        if not item.name.lower().startswith(INKSCAPE):
            continue
        this_exe = item.join(EXE_PATH)
        if not os.path.isfile(this_exe):
            continue
        paths.append(this_exe)

    try:
        svg_handler = a2toolbox.reg.read_value('.svg', hkey=winreg.HKEY_CLASSES_ROOT)
        keys = a2toolbox.reg.read_keys(svg_handler, hkey=winreg.HKEY_CLASSES_ROOT)
        if 'DefaultIcon' in keys:
            path = a2toolbox.reg.read_value(
                os.path.join(svg_handler, 'DefaultIcon'), hkey=winreg.HKEY_CLASSES_ROOT
            ).strip('"')
            if is_inkscape_exe(path) and not any(a2path.is_same(p, path) for p in paths):
                paths.append(path)
    except FileNotFoundError:
        pass

    if not paths:
        return Path()

    versions = {}
    for path in paths:
        this_version = version_tuplify(a2ahk.call_lib_cmd('get_version', path))
        if this_version in versions:
            print(f'Warning! Version "{this_version}" already collected!')
        versions[version_tuplify(a2ahk.call_lib_cmd('get_version', path))] = path

    version = sorted(versions)[-1]
    found = Path(versions[version])
    print(f'Found Inkscape ({version}): {found}')
    return found


def get_user_path() -> str:
    if not PATH_FILE.is_file():
        print(f'Warning! No "{PATH_FILE_NAME}"! Set one to skip searching for {INKSCAPE}.')
        return ''
    contents = PATH_FILE.read_text().strip()
    if is_inkscape_exe(contents):
        return contents
    return ''


def set_user_path(path: str | Path) -> None:
    inkscape_path = Path(path)
    if not inkscape_path.is_file():
        raise FileNotFoundError(f'No InkScape here!: {inkscape_path}')
    PATH_FILE.write_text(str(inkscape_path))


def is_inkscape_exe(path: str) -> bool:
    return path.lower().endswith(EXE_PATH) and os.path.isfile(path)


if __name__ == '__main__':
    path = get_path()
    print(f'get_path(): {path}')
    path
