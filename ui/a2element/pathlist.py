# -*- coding: utf-8 -*-
"""
Some element description ...

@created: 2017 11 1
@author: Eric Werner
"""
import a2ctrl
from PySide import QtGui
from a2element import pathlist_edit_ui, DrawCtrl, EditCtrl
from a2widget import A2PathField


class Draw(QtGui.QGroupBox, DrawCtrl):
    """
    The frontend widget visible to the user with options
    to change the default behavior of the element.
    """
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__()
        DrawCtrl.__init__(self, main, cfg, mod, _init_ctrl=False)
        self.setTitle(self.cfg.get('label', ''))
        self.setCheckable(False)

        self.a2_group_layout = QtGui.QVBoxLayout(self)

        self.path_widgets = []
        for i, path in enumerate(self.get_user_value(list)):
            self.path_widgets.append(self._make_path_widget(i, path))

    def add_path(self):
        path_widget = self._make_path_widget(self.a2_group_layout.count())
        self.path_widgets.append(path_widget)

    def remove_path(self):
        widget = self.path_widgets.pop(self.sender().path_index)
        widget.parent().deleteLater()
        self.check()

    def _make_path_widget(self, i, path=''):
        widget = QtGui.QWidget()
        layout = QtGui.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QtGui.QLabel(str(i + 1)))
        field = A2PathField(widget, path, writable=False)
        field.browse_type = self.cfg.get('browse_type', 0)
        field.changed.connect(self.check)
        layout.addWidget(field)
        button = QtGui.QToolButton(self)
        if i:
            button.path_index = i
            button.setIcon(a2ctrl.Icons.inst().clear)
            button.clicked.connect(self.remove_path)
        else:
            button.clicked.connect(self.add_path)
            button.setIcon(a2ctrl.Icons.inst().label_plus)
        layout.addWidget(button)
        self.a2_group_layout.addWidget(widget)
        return field

    def check(self):
        path_list = [w.value for w in self.path_widgets]
        self.set_user_value(path_list)
        self.change('variables')


class Edit(EditCtrl):
    """
    The background widget that sets up how the user can edit the element,
    visible when editing the module.
    """
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)

        a2ctrl.check_ui_module(pathlist_edit_ui)
        self.ui = pathlist_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

    @staticmethod
    def element_name():
        """The elements display name shown in UI"""
        return 'Pathlist'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().check


def get_settings(module_key, cfg, db_dict, user_cfg):
    """
    Called by the module on "change" to get an elements data thats
    eventually written into the runtime includes.

    Passed into is all you might need:
    :param str module_key: "module_source_name|module_name" combo used to identify module in db
    :param dict cfg: Standard element configuration dictionary.
    :param dict db_dict: Dictionary that's used to write the include data with "hotkeys", "variables" and "includes" keys
    :param dict user_cfg: This elements user edits saved in the db

    To make changes to the:
    * "variables" - a simple key, value dictionary in db_dict

    Get the current value via get_cfg_value() given the default cfg and user_cfg.
    If value name is found it takes the value from there, otherwise from cfg or given default.

        value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=bool, default=False)

    write the key and value to the "variables" dict:

        db_dict['variables'][cfg['name']] = value

    * "hotkeys" - a dictionary with scope identifiers

    * "includes" - a simple list with ahk script paths
    """
    db_dict.setdefault('variables', {})
    value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=list, default=[])
    db_dict['variables'][cfg['name']] = value
