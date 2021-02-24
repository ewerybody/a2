from a2qt import QtWidgets, QtCore

import a2uic
import a2core
import a2ctrl.connect


class Draw(QtWidgets.QWidget):
    def __init__(self, *args):
        super(Draw, self).__init__()
        self.main_layout = QtWidgets.QVBoxLayout(self)

        text = args[1].get('description', '')
        if text:
            self.label = QtWidgets.QLabel(self)
            self.label.setOpenExternalLinks(True)
            self.label.setTextFormat(QtCore.Qt.RichText)
            text = text.replace('\n', '<br>')
            self.label.setText(text)
            self.label.setWordWrap(True)
            self.main_layout.addWidget(self.label)
        else:
            self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.is_expandable_widget = False


class Edit(QtWidgets.QGroupBox):
    def __init__(self, cfg, main, *args):
        super(Edit, self).__init__()
        self.cfg = cfg
        self.typ = cfg['typ']
        self.setTitle('module information:')
        QSizePolicy = QtWidgets.QSizePolicy
        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))
        self.boxlayout = QtWidgets.QVBoxLayout(self)
        self.boxlayout.setSpacing(5)
        self.boxlayout.setContentsMargins(5, 5, 5, 10)
        self.setLayout(self.boxlayout)
        self.main_widget = QtWidgets.QWidget(self)
        self.boxlayout.addWidget(self.main_widget)

        from a2element import nfo_edit_ui

        a2uic.check_module(nfo_edit_ui)
        self.ui = nfo_edit_ui.Ui_edit()
        self.ui.setupUi(self.main_widget)

        self.ui.cfg_tags.set_available_tags(a2core.A2TAGS)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)
        self.is_expandable_widget = False

        self.ui.cfg_display_name.setPlaceholderText(main.mod.name)


def get_settings(*args):
    raise NotImplementedError('Settings for nfo are never fetched!')
