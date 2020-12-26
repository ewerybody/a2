import a2ctrl

from a2qt import QtWidgets
from a2element import check_edit_ui, DrawCtrl, EditCtrl


class Draw(DrawCtrl):
    def __init__(self, *args):
        super(Draw, self).__init__(*args)
        self._setup_ui()

    def _setup_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.checkbox = QtWidgets.QCheckBox(self.cfg.get('label', ''), self)
        self.checkbox.setChecked(self.get_user_value(bool))
        self.checkbox.clicked[bool].connect(self.delayed_check)
        self.main_layout.addWidget(self.checkbox)
        self.setLayout(self.main_layout)

    def check(self, *args):
        self.set_user_value(args[0])
        self.change('variables')
        super(Draw, self).check()


class Edit(EditCtrl):
    """
    Checkbox to control boolean values for the a2 runtime.
    We might put them to the db and get and fetch from there or first: just write them into
    code directly and start with the variables include.
    """

    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        self.helpUrl = self.a2.urls.helpCheckbox

        self.ui = check_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        self.check_new_name()
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

    @staticmethod
    def element_name():
        return 'CheckBox'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().check


def get_settings(_module_key, cfg, db_dict, user_cfg):
    value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=bool, default=cfg.get('value', False))
    db_dict.setdefault('variables', {})[cfg['name']] = value
