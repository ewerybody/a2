import a2ctrl
import a2util

from PySide6 import QtWidgets
from a2element import group_edit_ui, DrawCtrlMixin, EditCtrl
from a2element.common import EditAddElem


class Draw(QtWidgets.QGroupBox, DrawCtrlMixin):
    """
    Group box to bundle multiple other controls or includes that can be
    enabled/disables all at once.
    """

    def __init__(self, main, cfg, mod, user_cfg):
        self.is_expandable_widget = False
        super(Draw, self).__init__(parent=main)
        DrawCtrlMixin.__init__(self, main, cfg, mod, user_cfg)

        self.setTitle(self.cfg.get('label', ''))
        self.setCheckable(self.cfg.get('disablable', True))
        self.setChecked(self.get_user_value(bool, 'enabled'))
        self.clicked[bool].connect(self.check)

        self.a2_group_layout = QtWidgets.QVBoxLayout(self)

        # for some reason items in this GroupBox are 0px close to the
        # group box title. It works in settings view tho. So far I'm unable
        # to fix this via CSS. Enlighten me!
        self.a2_group_marging_top = QtWidgets.QWidget()
        self.a2_group_marging_top.setMaximumHeight(self.main.style.get('margin_h'))
        self.a2_group_layout.addWidget(self.a2_group_marging_top)

        expandable = False
        module_user_cfg = self.mod.get_user_cfg()
        for child in self.cfg.get('children', []):
            name = a2util.get_cfg_default_name(child)
            ctrl = a2ctrl.draw(self.main, child, self.mod, module_user_cfg.get(name))
            if ctrl is None:
                continue
            try:
                expandable = ctrl.is_expandable_widget
            except AttributeError:
                pass

            self.a2_group_layout.addWidget(ctrl)
        if expandable:
            self.is_expandable_widget = True

    def check(self, *args):
        self.set_user_value(args[0], 'enabled')
        self.change()


class Edit(EditCtrl):
    """
    Group box to bundle multiple other controls or includes that can be
    enabled/disables all at once.
    These also use the draw()/edit() functions to create the sub-controls.
    Each EditGroup has its own 'add...' button to create sub controls for itself
    but just without the option to create further groups within. (Although if
        properly implemented it would probably work very well, we will
        not go deeper than this to keep complexity under the lid)
    """

    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        if 'children' not in self.cfg:
            self.cfg['children'] = []

        a2ctrl.check_ui_module(group_edit_ui)
        self.ui = group_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        controls = []
        for child in self.cfg['children']:
            controls.append(a2ctrl.edit(child, self.main, self.cfg['children']))

        controls.append(EditAddElem(self.main, self.cfg['children'], 'Add Group Element'))
        for ctrl in controls:
            self.ui.edit_layout.addWidget(ctrl)

        self.check_new_name()
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

        self._check_checkable()
        self.ui.cfg_disablable.clicked[bool].connect(self._check_checkable)

    def paste(self):
        """
        Amends child list with cfgs from the main edit_clipboard
        and flushes it afterwards.
        """
        for cfg in self.main.edit_clipboard:
            self.cfg['children'].append(cfg)
        self.main.edit_clipboard = []
        self.main.edit_mod()

    def _check_checkable(self, checked=None):
        """If not checkable the group is automatically enabled!"""
        if checked is None:
            checked = self.cfg.get('disablable', True)

        if not checked:
            self.ui.cfg_enabled.setChecked(True)
            self.cfg['enabled'] = True
        self.ui.cfg_enabled.setVisible(checked)

    @staticmethod
    def element_name():
        return 'GroupBox'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().group


def get_settings(module_key, cfg, db_dict, _user_cfg):
    sub_cfg = cfg.get('children', [])
    a2ctrl.assemble_settings(module_key, sub_cfg, db_dict)
