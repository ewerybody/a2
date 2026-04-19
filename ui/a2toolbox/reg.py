import winreg


HKCU = winreg.HKEY_CURRENT_USER
HKCC = winreg.HKEY_CURRENT_CONFIG
HKLM = winreg.HKEY_LOCAL_MACHINE
HKCR = winreg.HKEY_CLASSES_ROOT
HKEYS = {
    'CU': winreg.HKEY_CURRENT_USER,
    'CC': winreg.HKEY_CURRENT_CONFIG,
    'LM': winreg.HKEY_LOCAL_MACHINE,
    'CR': winreg.HKEY_CLASSES_ROOT,
}
HKEY_TYPE_ERROR = 'HKEY identifier needs to be integer or string!'
DEFAULT_ICON = 'DefaultIcon'

def read_value(path, value_name: str = '', hkey: int | str = winreg.HKEY_CURRENT_USER) -> str:
    with winreg.OpenKey(resolve_hkey(hkey), path) as registry_key:
        return winreg.QueryValueEx(registry_key, value_name)[0]


def read_values(path: str, hkey: int | str = winreg.HKEY_CURRENT_USER) -> dict[str, str]:
    with winreg.OpenKey(resolve_hkey(hkey), path) as registry_key:
        return dict(winreg.EnumValue(registry_key, i)[:2] for i in range(winreg.QueryInfoKey(registry_key)[1]))


def read_keys(path, hkey: int | str = winreg.HKEY_CURRENT_USER) -> list[str]:
    with winreg.OpenKey(resolve_hkey(hkey), path) as registry_key:
        return [winreg.EnumKey(registry_key, i) for i in range(winreg.QueryInfoKey(registry_key)[0])]


def resolve_hkey(hkey: int | str) -> int:
    if isinstance(hkey, int) and hkey in HKEYS.values():
        return hkey
    if not isinstance(hkey, str):
        raise TypeError(HKEY_TYPE_ERROR)

    if hkey in HKEYS:
        return HKEYS[hkey]
    hkey = hkey.upper()
    for k, value in HKEYS.items():
        if k.endswith(hkey):
            return value
    raise TypeError(HKEY_TYPE_ERROR)
