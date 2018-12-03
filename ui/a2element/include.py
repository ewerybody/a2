import a2ctrl
import a2core

from PySide2 import QtWidgets

from a2element import EditCtrl
from a2widget.local_script import ScriptSelector
from a2element.common import LocalAHKScriptsMenu


log = a2core.get_logger(__name__)


class Edit(EditCtrl):
    """
    User-invisible control that you only setup in edit-mode for
    unconditional autohotkey script include. If the parent element is
    enabled: it gets included in (enabled group or module).
    """
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        self.base_layout = QtWidgets.QHBoxLayout(self.mainWidget)
        self.mainWidget.setLayout(self.base_layout)
        # self.base_layout.setSpacing(5)
        self.label = QtWidgets.QLabel('script file:')
        # self.label.setAlignment(QtCore.Qt.AlignRight)
        self.base_layout.addWidget(self.label)

        self.script_selector = ScriptSelector(self, main)
        self.base_layout.addWidget(self.script_selector)
        self.script_selector.set_selection(self.cfg['file'])

        self.local_scripts_menu = LocalAHKScriptsMenu(self, main)
        self.local_scripts_menu.script_selected.connect(self._on_script_selected)
        self.script_selector.set_menu(self.local_scripts_menu)

#         self.button = QtWidgets.QPushButton(self.cfg['file'])
#         self.button_menu = BrowseScriptsMenu(self.main)
#         self.button_menu.script_selected.connect(self.set_script)
#         self.button.setMenu(self.button_menu)
#         self.base_layout.addWidget(self.button)
#
#         self.edit_button = QtWidgets.QPushButton('edit script')
#         self.edit_button.clicked.connect(self.edit_script)
#         self.edit_button.setIcon(a2ctrl.Icons.inst().edit)
#         self.base_layout.addWidget(self.edit_button)
#
#         self.base_layout.addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

    def _on_script_selected(self, args):
        _, file_name = args
        self.cfg['file'] = file_name
        self.script_selector.set_selection(file_name)

    @staticmethod
    def element_name():
        return 'Include'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().code


def get_settings(_module_key, cfg, db_dict, _user_cfg):
    file_name = cfg.get('file')
    if file_name:
        db_dict.setdefault('includes', []).append(file_name)
