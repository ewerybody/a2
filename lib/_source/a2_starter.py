# This is the new Python script that becomes the a2.exe in root!
import os
import sys
import subprocess


def main():
    root_path = os.getcwd()
    lib_path = os.path.join(root_path, 'lib')
    if not os.path.isdir(lib_path):
        error_msg(f'There is no lib directory here!?\n{lib_path}')
        return

    # portable vs installed mode detection
    data_path = os.path.join(root_path, 'data')
    if not os.path.isdir(data_path):
        data_path = os.path.join(os.environ['LOCALAPPDATA'], 'a2', 'data')

    entry_path = os.path.join(data_path, 'a2_entry.ahk')
    ahk_exe_path = os.path.join(lib_path, 'Autohotkey', 'Autohotkey.exe')

    if os.path.isfile(entry_path):
        subprocess.Popen([ahk_exe_path, entry_path], cwd=root_path)
        return

    subprocess.Popen([os.path.join(root_path, 'a2ui.exe')])


def error_msg(msg):
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.WinDLL('user32')
    msgbox = user32.MessageBoxW
    msgbox.argtypes = wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT
    msgbox.restype = ctypes.c_int

    title = 'A2UI STARTUP ERROR'
    u_type = 0x10  # MB_OK
    return msgbox(None, msg, title, u_type)


if __name__ == '__main__':
    main()
    sys.exit(0)
