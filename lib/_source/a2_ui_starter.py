# This is the new Python script that becomes the a2ui.exe in root!
import os
import sys
import runpy


def main():
    root_path = os.path.join(os.getcwd(), 'ui')
    if not os.path.isdir(root_path):
        error_msg(f'There is no "ui" directory here!?\n{root_path}')
        return

    sys.path.insert(0, root_path)
    app_script_path = os.path.join(root_path, 'a2app.py')
    if not os.path.isfile(app_script_path):
        error_msg(f'There is no entry point script file here!?\n{app_script_path}')
        return

    try:
        runpy.run_path(app_script_path, run_name='__main__')
    except Exception as error:
        error_msg(str(error))


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
