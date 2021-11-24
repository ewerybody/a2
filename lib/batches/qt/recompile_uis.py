"""
Recompile All found .ui files in the repository.
"""
import os
import sys
import inspect
import subprocess
from pprint import pprint
from importlib import import_module
from xml.etree import ElementTree

import _ensure_a2_path
import a2uic
import a2widget
from PySide6 import QtWidgets


def main():
    ui_path = _ensure_a2_path.A2UI_PATH
    a2widget_path = os.path.dirname(a2widget.__file__)
    if not os.path.isdir(ui_path):
        raise NotADirectoryError(f'No such path: "{ui_path}"')

    a2widget_classes = {}
    for item in [i for i in os.scandir(a2widget_path) if i.is_file()]:
        base, ext = os.path.splitext(item.name)
        if ext != '.py' or item.name.endswith('_ui.py'):
            continue
        modname = f'{a2widget.__name__}.{base}'
        mod = import_module(modname, a2widget.__name__)
        for cls_name, cls in inspect.getmembers(mod, inspect.isclass):
            if issubclass(cls, QtWidgets.QWidget):
                if cls.__module__ != modname:
                    continue
                if cls_name in a2widget_classes:
                    raise RuntimeError(f'clsname {cls_name} already listed!!??!')
                a2widget_classes[cls_name] = modname

    pprint(a2widget_classes)
    curr_cwd = os.getcwd()
    os.chdir(_ensure_a2_path.A2_PATH)
    uic_path = os.path.join(sys.modules[QtWidgets.__package__].__path__[0], 'uic.exe')

    for dir_path, _, files in os.walk(ui_path):
        for ui_file in [f for f in files if os.path.splitext(f)[1] == '.ui']:
            ui_path = os.path.join(dir_path, ui_file)
            _fixml(ui_path, a2widget_classes)

            ui_relative = os.path.relpath(ui_path, _ensure_a2_path.A2_PATH)
            base = os.path.splitext(ui_file)[0]
            py_file = base + '_ui.py'
            if py_file in files:
                py_path = os.path.join(os.path.dirname(ui_path), py_file)
                try:
                    # with open(os.path.join(dir_path, py_file), 'w') as pyfobj:
                    #     compileUi(ui_path, pyfobj)
                    subprocess.call([uic_path, '-g', 'python', ui_relative, '-o', py_path])

                except Exception as error:
                    print('error: %s' % error)
                    error
                a2uic.patch_ui(ui_path, py_path)
                print('py_file recompiled:', py_path)
    os.chdir(curr_cwd)


def _fixml(ui_path, a2widget_classes):
    changes = []
    xml = ElementTree.parse(ui_path)
    for widget_node in xml.iter('customwidget'):
        header_node = widget_node.find('header')
        if header_node is None:
            continue
        class_node = widget_node.find('class')
        if class_node is None:
            continue
        proposed_mod = a2widget_classes.get(class_node.text)
        if proposed_mod != header_node.text and header_node.text is not None:
            print('header: %s' % header_node.text)
            print('class: %s' % class_node.text)
            header_parts = header_node.text.split('.')
            if header_parts[0] == a2widget.__name__:
                if len(header_parts) == 1:
                    changes.append(f'{header_node.text} > {proposed_mod}')
                    header_node.text = proposed_mod
                else:
                    header_parts
    if not changes:
        print('seems alright: %s' % ui_path)
    else:
        print('changed ui_file: %s\n  %s' % (ui_path, '\n  '.join(changes)))
        xml.write(ui_path)


if __name__ == '__main__':
    main()
