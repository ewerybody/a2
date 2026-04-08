import winreg


def read_value(path, value_name: str = '', hkey: int = winreg.HKEY_CURRENT_USER):
    with winreg.OpenKey(hkey, path) as registry_key:
        return winreg.QueryValueEx(registry_key, value_name)[0]


def read_values(path: str, hkey: int = winreg.HKEY_CURRENT_USER):
    with winreg.OpenKey(hkey, path) as registry_key:
        return dict(winreg.EnumValue(registry_key, i)[:2] for i in range(winreg.QueryInfoKey(registry_key)[1]))


def read_keys(path, hkey: int = winreg.HKEY_CURRENT_USER):
    with winreg.OpenKey(hkey, path) as registry_key:
        return [winreg.EnumKey(registry_key, i) for i in range(winreg.QueryInfoKey(registry_key)[0])]
