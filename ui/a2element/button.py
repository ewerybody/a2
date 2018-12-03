# -*- coding: utf-8 -*-
import a2ctrl
from PySide2 import QtWidgets, QtCore
from a2element import DrawCtrl, EditCtrl, button_edit_ui
from a2core import get_logger
from a2widget import local_script
import os


log = get_logger(__name__)
BUTTON_SCRIPT_PREFIX = 'a2_button_script_'
BUTTON_SCRIPT_TEMPLATE = '''# a2 button script "{name}"

def main(a2, mod):
    """
    :param a2: Main A2 object instance.
    :param mod: Current a2 module instance.
    """
    print('calling {name} ...')
'''


class Draw(DrawCtrl):
    """
    The frontend widget visible to the user with options
    to change the default behavior of the element.
    """
    def __init__(self, *args):
        super(Draw, self).__init__(*args)

        self.button_layout = QtWidgets.QHBoxLayout(self)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        labeltext = self.cfg.get('labeltext', '')
        if labeltext:
            label = QtWidgets.QLabel(labeltext)
            self.button_layout.addWidget(label)

        self.button = QtWidgets.QPushButton(self.cfg.get('buttontext', ''))
        self.button.clicked.connect(self.call_code)
        self.button_layout.addWidget(self.button)

    def call_code(self):
        file_name = build_script_file_name(self.cfg.get('script_name'))
        self.mod.call_python_script(file_name)


class Edit(EditCtrl):
    """
    The background widget that sets up how the user can edit the element,
    visible when editing the module.
    """
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        self.helpUrl = 'https://github.com/ewerybody/a2/wiki/Button-element'
        a2ctrl.check_ui_module(button_edit_ui)
        self.ui = button_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

        self.menu = ButtonScriptMenu(self, main)
        self.menu.script_selected.connect(self._on_script_selected)

        self.ui.script_selector.set_selection(
            build_script_file_name(cfg.get('script_name')), cfg.get('script_name'))
        self.ui.script_selector.set_main(main)
        self.ui.script_selector.set_menu(self.menu)

    @staticmethod
    def element_name():
        """The elements display name shown in UI"""
        return 'Button'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().button

    def _on_script_selected(self, name):
        file_name = build_script_file_name(name)
        self.ui.script_selector.set_selection(file_name, name)
        self.cfg['script_name'] = name

        path = os.path.join(self.main.mod.path, file_name)
        if not os.path.isfile(path):
            with open(path, 'w') as file_object:
                file_object.write(BUTTON_SCRIPT_TEMPLATE.format(name=name))


def build_script_file_name(name):
    if name is None:
        return None
    else:
        return BUTTON_SCRIPT_PREFIX + name + '.py'


class ButtonScriptMenu(local_script.BrowseScriptsMenu):
    script_selected = QtCore.Signal(str)

    def __init__(self, parent, main):
        super(ButtonScriptMenu, self).__init__(parent, main)
        self.extension = '.py'
        self.file_prefix = BUTTON_SCRIPT_PREFIX
        self.config_typ = 'button'

    def _on_script_selected(self):
        self.script_selected.emit(self.sender().data())

    def _on_create_script(self):
        from a2widget.a2input_dialog import A2InputDialog
        dialog = A2InputDialog(
            self.main, 'New Button Script',
            self._name_check,
            text='awesome_script',
            msg='Give a name for the new button script:')

        dialog.exec_()
        if not dialog.output:
            return

        self.script_selected.emit(dialog.output)


def get_settings(*args):
    pass
