import a2ctrl

from PySide2 import QtWidgets

from a2widget import a2path_field
from a2element import path_edit_ui, DrawCtrl, EditCtrl


class Draw(DrawCtrl):
    def __init__(self, *args):
        super(Draw, self).__init__(*args)
        self.value = self.get_user_value(str)
        self._setup_ui()

    def _setup_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.label_text = self.cfg.get('label', '')
        self.label = QtWidgets.QLabel(self.label_text, self)
        self.value_ctrl = a2path_field.A2PathField(self, value=self.value)
        self.value_ctrl.changed.connect(self.check)
        self.value_ctrl.writable = self.cfg.get('writable', False)
        self.value_ctrl.file_types = self.cfg.get('file_types', '')
        self.value_ctrl.browse_type = self.cfg.get('browse_type', '1')
        self.value_ctrl.save_mode = self.cfg.get('save_mode', False)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.value_ctrl)

    def check(self, *args):
        if args:
            value = args[0]
        else:
            value = self.value_ctrl.text()

        # prevent being called double
        if self.value == value:
            return

        self.value = value
        self.set_user_value(value)
        self.change('variables')


class Edit(EditCtrl):
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        self.helpUrl = self.a2.urls.help_path

        a2ctrl.check_ui_module(path_edit_ui)
        self.ui = path_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        self.check_new_name()
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)
        self._adjust_path_field()
        for ctrl in [self.ui.cfg_writable, self.ui.cfg_browse_type_0, self.ui.cfg_browse_type_1,
                     self.ui.cfg_save_mode]:
            ctrl.clicked.connect(self._adjust_path_field)
        self.ui.cfg_file_types.editingFinished.connect(self._adjust_path_field)

    def _adjust_path_field(self):
        self.ui.cfg_value.writable = self.cfg.get('writable', False)
        self.ui.cfg_value.file_types = self.cfg.get('file_types', '')
        self.ui.cfg_value.save_mode = self.cfg.get('save_mode', False)
        browse_type = self.cfg.get('browse_type', a2path_field.BrowseType.file)
        self.ui.cfg_value.browse_type = browse_type

        file_ctrls_visible = browse_type == a2path_field.BrowseType.file
        self.ui.cfg_file_types.setVisible(file_ctrls_visible)
        self.ui.cfg_save_mode.setVisible(file_ctrls_visible)
        self.ui.file_types_label.setVisible(file_ctrls_visible)
        #
        self.ui.browse_type_layout.setStretch(2, file_ctrls_visible)
        self.ui.browse_type_layout.setStretch(1, not file_ctrls_visible)

    @staticmethod
    def element_name():
        return 'Path'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().folder


def get_settings(_module_key, cfg, db_dict, user_cfg):
    db_dict.setdefault('variables', {})
    value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=str, default='')
    db_dict['variables'][cfg['name']] = value
