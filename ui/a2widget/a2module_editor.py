from copy import deepcopy

import a2mod
import a2util
import a2ctrl
import a2element.common
import a2element._edit

from a2qt import QtCore, QtWidgets, QtGui


class EditView(QtWidgets.QWidget):
    def __init__(self, parent, config_list):
        super(EditView, self).__init__(parent)
        self.controls = []
        self.config_list = config_list
        self.main = parent

        if not config_list:
            new_cfg = a2mod.NEW_MODULE_CFG.copy()
            new_cfg['description'] = a2mod.NEW_MODULE_DESC % self.main.mod.name
            new_cfg['date'] = a2util.get_date(),
            new_cfg['author'] = self.main.devset.author_name
            config_list.insert(0, new_cfg)

        self.edit_layout = QtWidgets.QVBoxLayout(self)
        self._draw()

    def _draw(self):
        for ctrl in self.controls:
            ctrl.deleteLater()
        self.controls.clear()

        for cfg in self.config_list:
            ctrl = a2ctrl.edit(cfg, self.main, self.config_list)
            if ctrl is None:
                continue

            self.edit_layout.addWidget(ctrl)

            if isinstance(ctrl, a2element.common.EditCtrl):
                ctrl.delete_requested.connect(self.delete_element)
                ctrl.move_abs_requested.connect(self.move_absolute)
                ctrl.move_rel_requested.connect(self.move_relative)
                ctrl.changed.connect(self._draw)

            self.controls.append(ctrl)

        edit_select = a2element._edit.EditAddElem(self.main, self.config_list)
        edit_select.add_request.connect(self.add_element)
        self.controls.append(edit_select)
        self.edit_layout.addWidget(edit_select)

        # amend a spacer
        policy = QtWidgets.QSizePolicy
        spacer = QtWidgets.QSpacerItem(10, 10, policy.Minimum, policy.Minimum)
        self.edit_layout.addItem(spacer)

        self.setSizePolicy(policy(policy.Preferred, policy.Maximum))


    def get_cfg_copy(self) -> list:
        return deepcopy(self.config_list)

    def delete_element(self):
        ctrl = self.sender()
        if ctrl.cfg in self.config_list:
            self.config_list.remove(ctrl.cfg)
            self._draw()

    def move_relative(self, value):
        sender = self.sender()
        print('move_relative', sender, value)

    def move_absolute(self, value):
        sender = self.sender()
        print('move_absolute', sender, value)

    def on_menu_button_clicked(self):
        button = self.sender()
        pass

    def add_element(self, element):
        self.config_list.append(element)
        self._draw()
