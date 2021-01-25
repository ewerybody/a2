import a2ctrl.connect

from a2qt import QtWidgets
from a2element import EditCtrl
from a2widget.a2text_field import A2CodeField


class Edit(EditCtrl):
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg)

        self.mainLayout.addWidget(
            QtWidgets.QLabel('Some code to be executed on a2 runtime shutdown:')
        )
        self.text_field = A2CodeField()
        self.mainLayout.addWidget(self.text_field)
        a2ctrl.connect.control(self.text_field, 'code', self.cfg)

    @staticmethod
    def element_name():
        """The elements display name shown in UI"""
        return 'Exit Call'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().code


def get_settings(_module_key, cfg, db_dict, _user_cfg):
    db_dict.setdefault('exit_calls', []).append(cfg['code'])
