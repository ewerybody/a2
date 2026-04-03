"""
Open up maybe already existing Windows Explorer windows with multiple items selected.

Finally a little library to pull that off. I saw Perforce View doing that and VS Code
as well and thought: That something I want to have for a2! :D here we are!

This tries to make use of the `SHOpenFolderAndSelectItems` API from `ctypes.windll.shell32`.

"""

import os
from pathlib import Path
import ctypes

import a2path

shell32 = ctypes.windll.shell32
ole32 = ctypes.windll.ole32


ole32.CoInitialize.restype = ctypes.HRESULT
ole32.CoInitialize.argtypes = [ctypes.c_void_p]
shell32.ILCreateFromPathW.restype = ctypes.c_void_p
shell32.ILCreateFromPathW.argtypes = [ctypes.c_wchar_p]
shell32.ILClone.restype = ctypes.c_void_p
shell32.ILClone.argtypes = [ctypes.c_void_p]
shell32.ILRemoveLastID.restype = ctypes.c_bool
shell32.ILRemoveLastID.argtypes = [ctypes.c_void_p]
shell32.ILFindLastID.restype = ctypes.c_void_p
shell32.ILFindLastID.argtypes = [ctypes.c_void_p]
shell32.ILFree.restype = None
shell32.ILFree.argtypes = [ctypes.c_void_p]
shell32.SHOpenFolderAndSelectItems.restype = ctypes.HRESULT
shell32.SHOpenFolderAndSelectItems.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint,
    ctypes.c_void_p,
    ctypes.c_ulong,
]

PathArg = str | Path | list[str | Path] | tuple[str | Path, ...]


def main(paths: PathArg) -> None:
    """Pop Explorer window with given items selected."""
    for folder_path, items in a2path.build_dir_map(paths).items():
        shell_open_folder(str(folder_path), items)


def shell_open_folder(folder_path: str, item_names: list[str]) -> None:
    if not item_names:
        shell_exec_open(folder_path)
        return

    hr_init: int = ole32.CoInitialize(None)
    p_id_lists: list[int] = []
    try:
        folder_p_id_list: int = shell32.ILCreateFromPathW(folder_path)
        for name in item_names:
            p_id_list: int = shell32.ILCreateFromPathW(os.path.join(folder_path, name))
            if not p_id_list:
                raise ctypes.WinError()
            p_id_lists.append(p_id_list)

        # build C array of pointers
        c_array = (ctypes.c_void_p * len(p_id_lists))(*p_id_lists) if p_id_lists else None
        h_result: int = shell32.SHOpenFolderAndSelectItems(folder_p_id_list, len(p_id_lists), c_array, 0)
        if h_result:
            raise ctypes.WinError(h_result)

    finally:
        for p_id_list in p_id_lists:
            shell32.ILFree(p_id_list)
        if folder_p_id_list:
            shell32.ILFree(folder_p_id_list)
        if hr_init == 0:
            ole32.CoUninitialize()


def shell_exec_open(folder_path: str) -> None:
    """Call open to a folder or directory path to open it up.
    Might also reuse existing Explorers! Not guaranteed tho.
    """
    ctypes.windll.shell32.ShellExecuteW(None, 'open', folder_path, None, None, 1)


if __name__ == '__main__':
    from a2widget.demo import shell_open_demo

    shell_open_demo.show()
