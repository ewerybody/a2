# adding a2 paths for imports
import time
import os
import io
import sys
import typing
import distlib
import zipfile
import subprocess
from os.path import join

THIS_PATH = os.path.dirname(__file__)
A2PATH = os.path.abspath(join(THIS_PATH, '..', '..', '..'))
UI_PATH = join(A2PATH, 'ui')
sys.path.append(UI_PATH)

A2 = 'a2'
NAME = A2 + '_installer'
PACKAGE_SUB_NAME = 'alpha'
MANIFEST_NAME = NAME + '_manifest.xml'
SRC_SFX = NAME + '.sfx.exe'
RCEDIT_EXE = 'rcedit-x64.exe'
SEVEN_ZIP_DIR = '7zr'
SEVEN_ZIP_EXE = '7zr.exe'

PYSIDE = 'PySide'
PYSIDE_VERSION = 6
QT_VERSION = 6
PYSIDE_NAME = f'{PYSIDE}{PYSIDE_VERSION}'
SHIBOKEN = 'shiboken'
SHIBOKEN_NAME = f'{SHIBOKEN}{PYSIDE_VERSION}'
TMP_NAME = A2 + '_temp_build_path'
SEVEN_FLAGS = '-m0=BCJ2 -m1=LZMA:d25:fb255 -m2=LZMA:d19 -m3=LZMA:d19 -mb0:1 -mb0s1:2 -mb0s2:3 -mx'.split()
AUTOHOTKEY = 'AutoHotkey'
PYTHON = 'Python'
PACKAGE_CFG_NAME = 'pyproject.toml'
# to gather versions in use:
VERSIONS = {PYSIDE: '', AUTOHOTKEY: '', PYTHON: ''}
CHK_MK = b'\xe2\x9c\x94'.decode()
EX_MRK = b'\xe2\x9c\x96'.decode()
I18N = 'i18n'

COMPANY = f'github.com/ewerybody/{A2}'
COPYRIGHT = f'GPLv3 ({COMPANY})'
EXE_NFO = {
    'FileVersion': '',
    'ProductVersion': '',
    'FileDescription': '',
    'ProductName': A2,
    'CompanyName': COMPANY,
    'LegalCopyright': COPYRIGHT,
}


def _get_versions(lib_dir, batches_path, ahk_path):
    """Get currently used versions."""
    pattern = 'get_%s_version.ahk'
    names = AUTOHOTKEY, PYSIDE, PYTHON
    scripts = (
        os.path.join(lib_dir, 'cmds', pattern % names[0]),
        os.path.join(batches_path, 'versions', pattern % names[1]),
        os.path.join(batches_path, 'versions', pattern % names[2]),
    )
    for name, script in zip(names, scripts):
        if not VERSIONS[name]:
            cwd = os.path.dirname(os.path.dirname(script))
            version_str = subprocess.check_output([ahk_path, script], cwd=cwd).decode()
            print(f'{name}: {version_str}')
            VERSIONS[name] = version_str
    return VERSIONS


class Paths:
    """Path holder object."""

    a2 = A2PATH
    lib = join(a2, 'lib')
    ui = UI_PATH
    i18n = join(a2, I18N)
    a2icon = join(ui, 'res', 'a2.ico')
    ahk2exe = join(lib, AUTOHOTKEY, 'Compiler', 'Ahk2Exe.exe')
    ahk_exe = join(lib, AUTOHOTKEY, AUTOHOTKEY + '.exe')

    package_config = join(a2, PACKAGE_CFG_NAME)

    source = join(lib, '_source')
    batches = join(lib, '_batches')
    # sfx_source_ui = join(source, SEVEN_ZIP_DIR, '7zS2.sfx')
    sfx_source_ui = join(source, SEVEN_ZIP_DIR, '7zSD.sfx')
    sfx_source_silent = join(source, SEVEN_ZIP_DIR, '7zS2con.sfx')
    seven_zip_exe = join(source, SEVEN_ZIP_DIR, SEVEN_ZIP_EXE)
    rcedit = join(source, RCEDIT_EXE)
    manifest = join(source, MANIFEST_NAME)
    manifest_tmp = join(source, 'manifest.xml.template')
    installer_script = join(source, NAME + '.ahk')
    installer_script_silent = join(source, NAME + '_silent.ahk')

    dist_root = join(a2, '_ package')
    sfx_target_ui = join(dist_root, '_ ' + SRC_SFX)
    sfx_target_silent = join(dist_root, '_ silent_' + SRC_SFX)
    manifest_target = join(dist_root, '_ ' + MANIFEST_NAME)
    archive_target = join(dist_root, '_ archive.7z')

    dist = join(dist_root, 'a2')
    distlib = join(dist, 'lib')
    dist_ui = join(dist, 'ui')
    distlib_test = join(distlib, AUTOHOTKEY, 'lib', 'test')
    dist_portable = join(dist_root, 'a2_portable')
    dist_i18n = join(dist, I18N)

    py_packs = join(a2, '_ py_packs')

    # Note: This points to the Python packages of the RUNNING python
    # Not necessarily the one that we ship a2 with!
    if sys.executable.endswith(os.path.join('.venv', 'Scripts', 'python.exe')):
        py_lib = os.path.join(os.path.dirname(os.path.dirname(sys.executable)), 'Lib')
    else:
        py_lib = os.path.join(os.path.dirname(sys.executable), 'Lib')
    py_site_packs = os.path.join(py_lib, 'site-packages')
    pyside = os.path.join(py_site_packs, PYSIDE_NAME)
    temp_build = os.path.join(os.environ['TEMP'], TMP_NAME)

    _get_versions(lib, batches, ahk_exe)
    qt_dir = os.path.join(temp_build, 'qt')
    qt_temp = os.path.join(qt_dir, VERSIONS[PYSIDE])

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


def make_ahk_exe(script_path, out_path, nfo=None, icon=None):
    if not os.path.isfile(script_path):
        raise RuntimeError('No such Script File!! (%s)' % script_path)

    print(f'Generating AHK executable "{os.path.basename(out_path)}" ...', end='')

    if os.path.isfile(out_path):
        print(
            f'There is already "{out_path}" ({time.time() - os.path.getctime(out_path)}s old)'
        )
        os.unlink(out_path)

    cmd = [
        Paths.ahk2exe,
        '/in',
        script_path,
        '/out',
        out_path,
        '/compress',
        '0',
        '/ahk',
        Paths.ahk_exe,
    ]
    if isinstance(icon, str) and os.path.isfile(icon):
        cmd.extend(['/icon', icon])

    subprocess.call(cmd, cwd=Paths.lib)
    if not os.path.isfile(out_path):
        print('cmd: %s' % cmd)
        print('Paths.lib: %s' % Paths.lib)
        raise RuntimeError('%s FAIL!: "%s" was not created!\n' % (EX_MRK, out_path))

    print(f'\b\b\b{CHK_MK}  ')

    if nfo is not None:
        if not nfo.get('OriginalFilename'):
            nfo['OriginalFilename'] = os.path.basename(out_path)
        set_rc_nfo(out_path, nfo)

    return out_path


def make_py_exe(
    script_path, out_path, nfo: dict[str, str], icon_path=None, console=False
):
    if not os.path.isfile(script_path):
        raise RuntimeError('No such Script File!! (%s)' % script_path)
    if os.path.isfile(out_path):
        file_age = time.time() - os.path.getctime(out_path)
        print(f'There is already "{out_path}" ({file_age:.1f}s old)')
        os.unlink(out_path)

    print(f'Generating Python executable "{os.path.basename(out_path)}" ...', end='')

    stub_version = ('w64.exe', 't64.exe')[console]
    py_exe_version = ('pythonw.exe', 'python.exe')[console]
    distlib_dir = os.path.dirname(distlib.__file__)
    stub_bytes = read_bytes(os.path.join(distlib_dir, stub_version))
    script_contents = read_text(script_path)

    archive_buffer = io.BytesIO()
    with zipfile.ZipFile(archive_buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('__main__.py', script_contents)

    out_dir = os.path.dirname(out_path)
    if os.path.isfile(os.path.join(out_dir, 'ui', py_exe_version)):
        py_path = os.path.join('ui', py_exe_version)
    else:
        py_path = sys.executable

    with open(out_path, 'wb') as file_obj:
        file_obj.write(stub_bytes)
    print(f'\b\b\b{CHK_MK}  ')

    if not nfo.get('OriginalFilename'):
        nfo['OriginalFilename'] = os.path.basename(out_path)
    set_rc_nfo(out_path, nfo)

    print('  Setting icon ...', end='')
    if icon_path is None or not os.path.isfile(icon_path):
        icon_path = Paths.a2icon
    subprocess.call([Paths.rcedit, out_path, '--set-icon', icon_path])
    print(f'\b\b\b{CHK_MK}  ')

    print('  Applying manifest ...', end='')
    base, ext = os.path.splitext(os.path.basename(script_path))
    manifest_tmp = read_text(Paths.manifest_tmp).format(
        name=base,
        version=make_4_numbers_version(nfo['FileVersion']),
        description=nfo['FileDescription'],
    )
    manifest_target = os.path.join(Paths.dist_root, f'_ {base}_manifest.xml')
    with open(manifest_target, 'w', encoding='utf8') as file_obj:
        file_obj.write(manifest_tmp)
    subprocess.call(
        [Paths.rcedit, out_path, '--application-manifest', Paths.manifest_target]
    )
    print(f'\b\b\b{CHK_MK}  ')

    # These always need to go last!!
    with open(out_path, 'ab') as file_obj:
        file_obj.write(f'#!{py_path}\r\n'.encode())
        file_obj.write(archive_buffer.getvalue())


def set_rc_nfo(target_path: str, nfo: dict[str, str]):
    print(f'Setting Details on "{os.path.basename(target_path)}" ...')
    for key, value in nfo.items():
        _set_rc_key(target_path, key, value)


def _set_rc_key(target_path, key, value_string):
    """
    --set-version-string <key> <value>         Set version string
    --get-version-string <key>                 Print version string
    --set-file-version <version>               Set FileVersion
    --set-product-version <version>            Set ProductVersion
    --set-icon <path-to-icon>                  Set file icon
    --set-requested-execution-level <level>    Pass nothing to see usage
    --application-manifest <path-to-file>      Set manifest file
    --set-resource-string <key> <value>        Set resource string
    --get-resource-string <key>                Get resource string

    For key names have a look at the `string-name` section under:
    https://docs.microsoft.com/en-us/windows/win32/menurc/versioninfo-resource#parameters
    FileDescription, ProductName, LegalCopyright, OriginalFilename, CompanyName
    """
    error, current = subprocess.getstatusoutput(
        [Paths.rcedit, target_path, '--get-version-string', key]
    )
    if error:
        current = ''

    if current == value_string:
        return

    print(f'  {key}: "{value_string}" ', end='')
    if key == 'FileVersion':
        subprocess.call([Paths.rcedit, target_path, '--set-file-version', value_string])
    elif key == 'ProductVersion':
        subprocess.call(
            [Paths.rcedit, target_path, '--set-product-version', value_string]
        )
    else:
        subprocess.call(
            [Paths.rcedit, target_path, '--set-version-string', key, value_string]
        )

    # check if things were changed correctly
    current = subprocess.check_output(
        [Paths.rcedit, target_path, '--get-version-string', key]
    ).decode()
    if current == value_string:
        print(f'{CHK_MK}')
    else:
        print(f'{EX_MRK} "{key}" is "{current}" NOT "{value_string}"!')


def get_package_cfg() -> dict[str, typing.Any]:
    import tomllib

    with open(Paths.package_config, 'rb') as file_obj:
        return tomllib.load(file_obj)


def read_bytes(file_path):
    with open(file_path, 'rb') as file_obj:
        return file_obj.read()


def read_text(file_path):
    with open(file_path, encoding='utf8') as file_obj:
        return file_obj.read()


def make_4_numbers_version(version):
    """Take a version string and make sure it's 3 dots between 4 numbers."""
    version_list = []
    for i, number in enumerate(version.split('.')):
        if not number.isdigit():
            print('ERROR:\n  Bad Nr in version string %i: %s' % (i, number))
            continue
        version_list.append(number)
    version_list.extend((4 - len(version_list)) * '0')
    version_string = '.'.join(version_list)
    return version_string
