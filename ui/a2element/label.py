# -*- coding: utf-8 -*-
"""
Some element description ...

@created: 2016 11 10
@author: Eric Werner
"""
import a2ctrl
from PySide import QtGui
from a2element import DrawCtrl, EditCtrl
from a2widget import A2TextField


class Draw(DrawCtrl):
    """
    The frontend widget visible to the user with options
    to change the default behavior of the element.
    """
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)

        self.layout = QtGui.QVBoxLayout(self)
        text = self.cfg.get('text', 'Nothing yet').replace('\n', '<br>')

        # TODO: This might be used in other places. Make it a DrawCtrl method?
        if '%module_path%' in text:
            text = text.replace('%module_path%', self.mod.path)

        self.label = QtGui.QLabel(text, self)
        self.label.setOpenExternalLinks(True)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


class Edit(EditCtrl):
    """
    The background widget that sets up how the user can edit the element,
    visible when editing the module.
    """
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg)

        self.mainLayout.addWidget(QtGui.QLabel('Some text to show in the module frontend:'))
        self.text_field = A2TextField()
        self.mainLayout.addWidget(self.text_field)
        a2ctrl.connect.control(self.text_field, 'text', self.cfg)

    @staticmethod
    def element_name():
        """The elements display name shown in UI"""
        return 'Label'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().text


def get_settings(module_key, cfg, db_dict, user_cfg):
    pass
