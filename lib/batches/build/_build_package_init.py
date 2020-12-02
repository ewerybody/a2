# adding a2 paths for imports
import os
import sys
from os.path import join

THIS_PATH = os.path.dirname(__file__)
A2PATH = os.path.abspath(join(THIS_PATH, '..', '..', '..'))
UIPATH = join(A2PATH, 'ui')
sys.path.append(UIPATH)

NAME = 'a2_installer'
PACKAGE_SUB_NAME = 'alpha'
MANIFEST_NAME = NAME + '_manifest.xml'
SRC_SFX = NAME + '.sfx.exe'
RCEDIT_EXE = 'rcedit-x64.exe'
SEVENZ_EXE = '7zr\\7zr.exe'


class Paths:
    """Path holder object."""
    a2 = A2PATH
    lib = join(a2, 'lib')
    ui = UIPATH
    ahk2exe = join(os.environ['PROGRAMFILES'], 'AutoHotkey', 'Compiler', 'Ahk2Exe.exe')
    package_config = join(a2, 'package.json')

    source = join(lib, '_source')
    sfx = join(source, SRC_SFX)
    rcedit = join(source, RCEDIT_EXE)
    manifest = join(source, MANIFEST_NAME)
    sevenz_exe = join(source, SEVENZ_EXE)
    installer_script = join(source, NAME + '.ahk')

    distroot = join(a2, '_ package')
    sfx_target = join(distroot, SRC_SFX)
    manifest_target = join(distroot, MANIFEST_NAME)
    archive_target = join(distroot, 'archive.7z')
    config_target = join(distroot, 'config.txt')

    dist = join(distroot, 'a2')
    dist_portable = join(distroot, 'a2_portable')
    distlib = join(dist, 'lib')
    distui = join(dist, 'ui')
    distlib_test = join(distlib, 'AutoHotkey', 'lib', 'test')

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
                'There are some paths missing!\n  %s\nPlease resolve before continuing!' %
                '\n  '.join(f'{k}: {p}' for k, p in whats_missing.items()))

        print('All paths checked! Nice! Let\'s go!')

    @staticmethod
    def _ignore_name(name):
        if name.startswith('_'):
            return True
        if name in ('check', 'iter'):
            return True
        if name.endswith('_target'):
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
