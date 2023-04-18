import traceback
from a2qt import QtWidgets

import a2uic
import a2ctrl
import a2ctrl.connect
from a2element import DrawCtrl, EditCtrl, button_edit_ui
from a2core import get_logger
from a2widget import local_script, a2error_dialog


log = get_logger(__name__)
BUTTON_SCRIPT_PREFIX = 'a2_button_script_'
BUTTON_SCRIPT_TEMPLATE = '''# a2 button script "{name}"

def main(a2, mod):
    """
    :param a2: Main A2 object instance.
    :param mod: Current a2 module instance.
    """
    print('calling button script "{name}" main() ...')
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
        script_name = self.cfg.get('script_name')
        file_name = local_script.build_file_name(script_name, BUTTON_SCRIPT_PREFIX)
        try:
            self.mod.call_python_script(file_name)
        except Exception as error:
            a2error_dialog.A2ErrorDialog(
                traceback.format_exc().strip(),
                f'There was an error trying to execute the script "{script_name}":',
                error,
                self
            )


class Edit(EditCtrl):
    """
    The background widget that sets up how the user can edit the element,
    visible when editing the module.
    """

    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        a2uic.check_module(button_edit_ui)
        self.ui = button_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

        self.menu = local_script.BrowseScriptsMenu(self, main)
        self.menu.file_prefix = BUTTON_SCRIPT_PREFIX
        self.menu.script_template = BUTTON_SCRIPT_TEMPLATE
        self.menu.config_typ = 'button'
        self.menu.dialog_title = 'New Button Script'
        self.menu.dialog_msg = 'Give a name for the new button script:'
        self.menu.script_selected.connect(self._on_script_selected)
        self.ui.script_selector.set_config(BUTTON_SCRIPT_PREFIX, cfg, main, self.menu)

    @staticmethod
    def element_name():
        return 'Button'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().button

    def _on_script_selected(self, file_name, name):
        self.cfg['script_name'] = name
        self.ui.script_selector.set_selection(file_name, name)


def get_settings(*args):
    pass
