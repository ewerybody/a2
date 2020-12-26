"""
a2element.nfo

@created: Sep 3, 2016
@author: eRiC
"""
from a2qt import QtWidgets

import a2core
import a2ctrl.connect
from a2element import nfo_edit_ui


class Draw(QtWidgets.QWidget):
    def __init__(self, *args):
        super(Draw, self).__init__()
        self.main_layout = QtWidgets.QVBoxLayout(self)

        text = args[1].get('description', '')
        if text:
            self.label = QtWidgets.QLabel(self)
            self.label.setText(text)
            self.label.setWordWrap(True)
            self.main_layout.addWidget(self.label)
        else:
            self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.is_expandable_widget = False


class Edit(QtWidgets.QGroupBox):
    def __init__(self, cfg, *_args):
        super(Edit, self).__init__()
        self.cfg = cfg
        self.typ = cfg['typ']
        self.setTitle('module information:')
        self.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        )
        self.boxlayout = QtWidgets.QVBoxLayout(self)
        self.boxlayout.setSpacing(5)
        self.boxlayout.setContentsMargins(5, 5, 5, 10)
        self.setLayout(self.boxlayout)
        self.main_widget = QtWidgets.QWidget(self)
        self.boxlayout.addWidget(self.main_widget)

        a2ctrl.check_ui_module(nfo_edit_ui)
        self.ui = nfo_edit_ui.Ui_edit()
        self.ui.setupUi(self.main_widget)
        self.ui.cfg_tags.set_available_tags(a2core.A2TAGS)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)
        self.is_expandable_widget = False


def get_settings(*args):
    raise NotImplementedError('Settings for nfo are never fetched!')
