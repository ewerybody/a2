"""
Recompile All found .ui files in the repository.
"""

import os
import sys
import inspect
import subprocess
from pathlib import Path
from pprint import pprint
from importlib import import_module
from xml.etree import ElementTree

from _ensure_a2_path import A2_PATH, A2UI_PATH
import a2uic
import a2widget
from PySide6 import QtWidgets


def main():
    a2widget_path = Path(a2widget.__file__).parent
    if not A2UI_PATH.is_dir():
        raise NotADirectoryError(f'No such path: "{A2UI_PATH}"')

    a2widget_classes = _get_a2_widget_classes(a2widget_path)
    pprint(f'{a2widget_classes = }')

    curr_cwd = os.getcwd()
    os.chdir(A2_PATH)

    if QtWidgets.__package__ is None:
        raise RuntimeError('Cannot recompile with `QtWidgets.__package__` being `None`!')
    uic_path = Path(sys.modules[QtWidgets.__package__].__path__[0]) / 'uic.exe'

    for dir_path, _, files in A2UI_PATH.walk():
        for ui_file in [f for f in files if os.path.splitext(f)[1] == '.ui']:
            ui_path = os.path.join(dir_path, ui_file)
            _fixml(ui_path, a2widget_classes)

            ui_relative = os.path.relpath(ui_path, A2_PATH)
            base = os.path.splitext(ui_file)[0]
            py_file = base + '_ui.py'
            if py_file not in files:
                continue

            py_path = os.path.join(os.path.dirname(ui_path), py_file)
            try:
                # with open(os.path.join(dir_path, py_file), 'w') as pyf_obj:
                #     compileUi(ui_path, pyf_obj)
                subprocess.call([uic_path, '-g', 'python', ui_relative, '-o', py_path])

            except Exception as error:
                print('error: %s' % error)
                error
            a2uic.UIPatcher(ui_path, py_path)
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


def _get_a2_widget_classes(a2widget_path: Path) -> dict[str, str]:
    a2widget_classes = {}
    for dir_item, _, file_names in a2widget_path.walk():
        for name in file_names:
            item = dir_item / name
            if not item.suffix.lower() == '.py' or not item.stem.endswith('_ui'):
                continue
            if dir_item == a2widget_path:
                mod_name = f'{a2widget.__name__}.{item.stem}'
            else:
                parts = [dir_item.relative_to(a2widget_path).name]
                parent = dir_item.relative_to(a2widget_path).parent
                while parent != Path('.'):
                    parts.insert(0, parent.name)
                    parent = parent.parent
                mod_name = f'{a2widget.__name__}.{".".join(parts)}.{item.stem}'
            try:
                mod = import_module(mod_name, a2widget.__name__)
            except ImportError as error:
                # raise error
                print(f'Error importing "{mod_name}":\n {error = }\n {item}')
                continue

            for cls_name, cls in inspect.getmembers(mod, inspect.isclass):
                if not issubclass(cls, QtWidgets.QWidget):
                    continue
                if cls.__module__ != mod_name:
                    continue
                if cls_name in a2widget_classes:
                    raise RuntimeError(f'Class name {cls_name} already listed!!??!')

                a2widget_classes[cls_name] = mod_name

    return a2widget_classes


if __name__ == '__main__':
    main()
