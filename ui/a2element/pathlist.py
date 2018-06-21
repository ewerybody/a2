# -*- coding: utf-8 -*-
"""
Some element description ...

@created: 2017 11 1
@author: Eric Werner
"""
import a2ctrl
from PySide2 import QtCore, QtWidgets
from a2element import pathlist_edit_ui, DrawCtrl, EditCtrl
from a2widget import A2PathField


class Draw(QtWidgets.QGroupBox, DrawCtrl):
    """
    The frontend widget visible to the user with options
    to change the default behavior of the element.
    """
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main)
        DrawCtrl.__init__(self, main, cfg, mod, _init_ctrl=False)
        self.setTitle(self.cfg.get('label', ''))
        self.setCheckable(False)

        self.a2_group_layout = QtWidgets.QVBoxLayout(self)

        self.path_widgets = []
        for path in self.get_user_value(list, default=['']):
            self.add_path(path)

    def add_path(self, path=''):
        path_widget = PathEntry(self, self.a2_group_layout.count(),
                                self.cfg.get('browse_type', 0), path)
        path_widget.changed.connect(self.check)
        path_widget.add_path.connect(self.add_path)
        path_widget.delete_me.connect(self._path_removed)
        self.a2_group_layout.addWidget(path_widget)
        self.path_widgets.append(path_widget)

    def _path_removed(self, del_index):
        del_widget = self.path_widgets.pop(del_index)
        # fix index labels
        for i, widget in enumerate(self.path_widgets):
            widget.index = i

        # avoid check when path was empty
        if del_widget.path:
            self.check()

    def _make_path_widget(self, i, path=''):
        widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.label = QtWidgets.QLabel(str(i + 1))
        layout.addWidget(widget.label)
        field = A2PathField(widget, path, writable=False)
        field.browse_type = self.cfg.get('browse_type', 0)
        field.changed.connect(self.check)
        layout.addWidget(field)
        button = QtWidgets.QToolButton(self)
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

    def _check_indices(self):
        for i, widget in enumerate(self.path_widgets):
            print('widget.label.text() %i: %s' % (i, widget.label.text()))

    def check(self, *_args):
        path_list = [w.path for w in self.path_widgets if w.path]
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


class PathEntry(QtWidgets.QWidget):
    changed = QtCore.Signal(str)
    delete_me = QtCore.Signal(int)
    add_path = QtCore.Signal()

    def __init__(self, parent, index, browse_type, path=''):
        super(PathEntry, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._index = 0
        self._label = QtWidgets.QLabel()
        self.index = index
        layout.addWidget(self._label)
        self._field = A2PathField(self, path, writable=False)
        self._field.browse_type = browse_type
        self._field.changed.connect(self.changed.emit)
        layout.addWidget(self._field)

        button = QtWidgets.QToolButton(self)
        button.setAutoRaise(True)
        if index:
            button.setIcon(a2ctrl.Icons.inst().clear)
            button.clicked.connect(self.delete)
        else:
            button.setIcon(a2ctrl.Icons.inst().folder_add)
            button.clicked.connect(self.add_path.emit)
        layout.addWidget(button)

    @property
    def path(self):
        return self._field.value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
        self._label.setText(str(value + 1))

    def delete(self):
        self.deleteLater()
        self.delete_me.emit(self.index)

    def __repr__(self, *args, **kwargs):
        return '<PathEntry %i "%s" at %s>' % (self.index, self.path, id(self))


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
