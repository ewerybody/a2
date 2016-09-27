"""
a2element.nfo

@created: Sep 3, 2016
@author: eRiC
"""
from PySide import QtGui

import a2ctrl
from a2element import nfo_edit_ui


class Draw(QtGui.QWidget):
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__()
        self.layout = QtGui.QVBoxLayout(self)
        self.label = QtGui.QLabel(self)
        self.label.setText(cfg.get('description') or '')
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)


class Edit(QtGui.QGroupBox):
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__()
        self.cfg = cfg
        self.typ = cfg['typ']
        self.setTitle('module information:')
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                             QtGui.QSizePolicy.Maximum))
        self.boxlayout = QtGui.QVBoxLayout(self)
        self.boxlayout.setSpacing(5)
        self.boxlayout.setContentsMargins(5, 5, 5, 10)
        self.setLayout(self.boxlayout)
        self.main_widget = QtGui.QWidget(self)
        self.boxlayout.addWidget(self.main_widget)

        a2ctrl.check_ui_module(nfo_edit_ui)
        self.ui = nfo_edit_ui.Ui_edit()
        self.ui.setupUi(self.main_widget)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)


def get_settings(*args):
    raise NotImplementedError('Settings for nfo are never fetched!')
