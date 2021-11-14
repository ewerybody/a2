import a2uic
import a2ctrl
import a2ctrl.connect
import a2util

from a2qt import QtWidgets
from a2element import group_edit_ui, DrawCtrlMixin, EditCtrl


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
        self.clicked.connect(self.check)

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

    def check(self, state=None):
        if state is None:
            state = self.isChecked()
        self.set_user_value(state, 'enabled')
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
        self.cfg.setdefault('name', '')
        self.cfg.setdefault('children', [])
        self.config_list = self.cfg['children']
        self._child_elements = []

        a2uic.check_module(group_edit_ui)
        self.ui = group_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

        self._check_checkable()
        self.ui.cfg_disablable.clicked.connect(self._check_checkable)

    def fill_elements(self, elements: list):
        from a2element._edit import EditAddElem

        adder_widget = EditAddElem(self.main, self.config_list, 'Add Group Element')
        adder_widget.add_request.connect(self._add_element)
        elements.append(adder_widget)

        self._child_elements.clear()
        for element in elements:
            self.ui.edit_layout.addWidget(element)
            self._child_elements.append(element)

    def get_child_index(self, element):
        return self._child_elements.index(element)

    def _add_element(self, element_cfg):
        # type: (dict[str, bool | float | str | list[str]]) -> None
        self.config_list.append(element_cfg)
        self.changed.emit()

    def _check_checkable(self, checked=None):
        """If not checkable the group is automatically enabled!"""
        if checked is None:
            checked = self.cfg.get('disablable', True)

        if not checked:
            self.ui.cfg_enabled.setChecked(True)
            self.cfg['enabled'] = True
        self.ui.cfg_enabled.setVisible(checked)

    @property
    def max_index(self):
        """Give index of the last element config."""
        return len(self.config_list) - 1

    @property
    def top_index(self):
        return 0

    @staticmethod
    def element_name():
        return 'GroupBox'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().group


def get_settings(module_key, cfg, db_dict, _user_cfg):
    sub_cfg = cfg.get('children', [])
    a2ctrl.assemble_settings(module_key, sub_cfg, db_dict)
