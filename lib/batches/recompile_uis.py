"""
Script to pyside2uic-recompile All found .ui files in the repository.
"""
import os

from pyside2uic import compileUi


def main():
    ui_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'ui'))
    for dir_path, folders, files in os.walk(ui_path):
        for ui_file in [f for f in files if os.path.splitext(f)[1] == '.ui']:
            base, ext = os.path.splitext(ui_file)
            py_file = base + '_ui.py'
            if py_file in files:
                with open(os.path.join(dir_path, py_file), 'w') as pyfobj:
                    compileUi(os.path.join(dir_path, ui_file), pyfobj)
                print('py_file recompiled:', py_file)


if __name__ == '__main__':
    main()
