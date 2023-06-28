# adding a2 paths for imports
import os
import sys
from os.path import join

THIS_PATH = os.path.dirname(__file__)
A2PATH = os.path.abspath(join(THIS_PATH, '..', '..', '..'))
UIPATH = join(A2PATH, 'ui')
sys.path.append(UIPATH)

A2 = 'a2'
NAME = A2 + '_installer'
PACKAGE_SUB_NAME = 'alpha'
MANIFEST_NAME = NAME + '_manifest.xml'
SRC_SFX = NAME + '.sfx.exe'
RCEDIT_EXE = 'rcedit-x64.exe'
SEVENZ_DIR = '7zr'
SEVENZ_EXE = '7zr.exe'

PYSIDE = 'PySide'
PYSIDE_VERSION = 6
QT_VERSION = 6
PYSIDE_NAME = f'{PYSIDE}{PYSIDE_VERSION}'
SHIBOKEN = 'shiboken'
SHIBOKEN_NAME = f'{SHIBOKEN}{PYSIDE_VERSION}'
TMP_NAME = A2 + '_temp_buildpath'


class Paths:
    """Path holder object."""

    a2 = A2PATH
    lib = join(a2, 'lib')
    ui = UIPATH
    a2icon = join(ui, 'res', 'a2.ico')
    ahk2exe = join(lib, 'AutoHotkey', 'Compiler', 'Ahk2Exe.exe')
    ahkexe = join(lib, 'AutoHotkey', 'AutoHotkey.exe')

    package_config = join(a2, 'package.json')

    source = join(lib, '_source')
    batches = join(lib, '_batches')
    # sfx_source_ui = join(source, SEVENZ_DIR, '7zS2.sfx')
    sfx_source_ui = join(source, SEVENZ_DIR, '7zSD.sfx')
    sfx_source_silent = join(source, SEVENZ_DIR, '7zS2con.sfx')
    sevenz_exe = join(source, SEVENZ_DIR, SEVENZ_EXE)
    rcedit = join(source, RCEDIT_EXE)
    manifest = join(source, MANIFEST_NAME)
    installer_script = join(source, NAME + '.ahk')
    installer_script_silent = join(source, NAME + '_silent.ahk')

    distroot = join(a2, '_ package')
    sfx_target_ui = join(distroot, '_ ' + SRC_SFX)
    sfx_target_silent = join(distroot, '_ silent_' + SRC_SFX)
    manifest_target = join(distroot, '_ ' + MANIFEST_NAME)
    archive_target = join(distroot, '_ archive.7z')

    dist = join(distroot, 'a2')
    distlib = join(dist, 'lib')
    distui = join(dist, 'ui')
    distlib_test = join(distlib, 'AutoHotkey', 'lib', 'test')
    dist_portable = join(distroot, 'a2_portable')

    py_packs = join(a2, '_ py_packs')

    # Note: This points to the Python packages of the RUNNING python
    # Not necessarily the one that we ship a2 with!
    py_lib = os.path.join(os.path.dirname(sys.executable), 'Lib')
    py_site_packs = os.path.join(py_lib, 'site-packages')
    pyside = os.path.join(py_site_packs, PYSIDE_NAME)
    temp_build = os.path.join(os.environ['TEMP'], TMP_NAME)

    @classmethod
    def check(cls):
        """Test all the needed paths."""
        whats_missing = {}
        for name, path in cls.iter():
            if not os.path.exists(path):
                print(f'Does NOT exist: {path}!!!')
                whats_missing[name] = path

        if whats_missing:
            raise FileNotFoundError(
                'There are some paths missing!\n  %s\nPlease resolve before continuing!'
                % '\n  '.join(f'{k}: {p}' for k, p in whats_missing.items())
            )

        print("All paths checked! Nice! Let's go!")

    @staticmethod
    def _ignore_name(name):
        if name.startswith('_'):
            return True
        if name in ('check', 'iter'):
            return True
        if '_target' in name:
            return True
        if name.startswith('dist'):
            return True
        return False

    @classmethod
    def iter(cls):
        """Loop over the objs paths."""
        for name in cls.__dict__:
            if cls._ignore_name(name):
                continue
            yield name, cls.__dict__[name]
