import os
import sys

import a2path
from a2dev.build import Paths, make_py_exe, get_package_cfg, A2, EXE_NFO


def main():
    if not os.path.isfile(Paths.dev_python) or not a2path.is_same(
        sys.executable, Paths.dev_python
    ):
        print('WARNING!')
        raise RuntimeError(
            f'Cannot make dev executables without .venv python!\n ({Paths.dev_python})'
        )
    package_cfg = get_package_cfg()
    version = package_cfg['project']['version']
    for name, source_name, description in (
        (A2, 'a2_starter', 'a2 Runtime Starter'),
        (f'{A2}ui', 'a2_ui_starter', 'a2 UI Starter'),
    ):
        nfo = EXE_NFO.copy()
        nfo['FileVersion'] = version
        nfo['ProductVersion'] = version
        nfo['FileDescription'] = description
        make_py_exe(
            os.path.join(Paths.source, f'{source_name}.py'),
            os.path.join(Paths.a2, f'{name}.exe'),
            nfo=nfo,
            console=False,
        )

if __name__ == '__main__':
    main()
