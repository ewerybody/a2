import a2uic
import a2ctrl
from a2qt import QtWidgets, QtCore
from a2element import string_edit_ui, DrawCtrl, EditCtrl
from a2widget.a2text_field import A2TextField


class Draw(DrawCtrl):
    def __init__(self, *args):
        super(Draw, self).__init__(*args)
        self.value = self.get_user_value(str)
        self._setupUi()

    def _setupUi(self):
        self.label_text = self.cfg.get('label', '')
        self.label = QtWidgets.QLabel(self.label_text, self)

        if self.cfg.get('password_mode', False):
            self.value_ctrl = QtWidgets.QLineEdit(self)
            self.value_ctrl.setEchoMode(QtWidgets.QLineEdit.Password)
            self.value_ctrl.editingFinished.connect(self.delayed_check)
        else:
            self.value_ctrl = A2TextField(self)
            self.value_ctrl.editing_finished.connect(self.delayed_check)
        self.value_ctrl.setText(self.value)

        if self.cfg.get('label_over_field', False):
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(self.label)
        else:
            layout = QtWidgets.QHBoxLayout(self)
            layout.addWidget(self.label)
            self.label.setAlignment(
                QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
            )
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.value_ctrl)

    def get_ui_value(self):
        return self.value_ctrl.text()

    def check(self, *args):
        self.default_check(*args)


class Edit(EditCtrl):
    """
    Checkbox to control boolean values for the a2 runtime.
    We might put them to the db and get and fetch from there or first: just write them into
    code directly and start with the variables include.
    """

    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        self.cfg.setdefault('name', '')
        self.help_url = self.a2.urls.help_string

        a2uic.check_module(string_edit_ui)
        self.ui = string_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

    @staticmethod
    def element_name():
        return 'String'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().string


def get_settings(_module_key, cfg, db_dict, user_cfg):
    db_dict.setdefault('variables', {})
    value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=str, default='')
    db_dict['variables'][cfg['name']] = value
