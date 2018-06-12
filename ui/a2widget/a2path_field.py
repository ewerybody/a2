"""
A universal file/folder path field with a browse button.
the field can be made writable or read-only to allow only browsed paths
it can be made browsing for folders or files

At files it can be set to save-mode where inexistent paths can be selected
and filtered file types can be set. See:
http://pyside.github.io/docs/pyside/PySide/QtGui/QFileDialog.html?highlight=qfiledialog#detailed-description

TODO: add recent paths?

@created: Jun 19, 2016
@author: eRiC
"""
import os
from PySide import QtGui, QtCore

import a2ctrl
import a2util


class BrowseType(object):
    folder = '0'
    file = '1'


class A2PathField(QtGui.QWidget):
    changed = QtCore.Signal(str)

    def __init__(self, parent, value='', file_types='', writable=True,
                 label_text=None, save_mode=False, changable=True):
        super(A2PathField, self).__init__(parent)
        self.main_layout = QtGui.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.line_field = QtGui.QLineEdit(self)
        self.line_field.setText(value)
        self.main_layout.addWidget(self.line_field)
        self.browse_button = QtGui.QPushButton('Browse...', self)
        self.browse_button.setIcon(a2ctrl.Icons.inst().folder2)
        self.browse_button.clicked.connect(self.browse)
        self.main_layout.addWidget(self.browse_button)

        self.options_menu = QtGui.QMenu()
        self.a2option_button = QtGui.QToolButton(self)
        self.a2option_button.setObjectName('a2option_button')
        self.a2option_button.setAutoRaise(True)
        self.a2option_button.setIcon(a2ctrl.Icons.inst().more)
        # self.a2option_button.setArrowType(QtCore.Qt.DownArrow)
        self.a2option_button.clicked.connect(self.show_options_menu)
        self.main_layout.addWidget(self.a2option_button)

        self._set_delay = 150
        self._field_set = False

        self._value = value
        self.file_types = file_types
        self.save_mode = save_mode
        self.browse_type = BrowseType.file
        self.label_text = label_text

        self._changable = None
        self.changable = changable
        self._writable = None
        self.writable = writable

    @property
    def writable(self):
        return self._writable

    @writable.setter
    def writable(self, state):
        if state == self._writable:
            return

        if state and not self.changable:
            raise RuntimeError('PathField cannot be set writable while not being changable at the same time!')

        self._writable = state
        self.line_field.setReadOnly(not state)
        if state:
            self.line_field.editingFinished.connect(self._delayed_set)
        else:
            try:
                self.line_field.editingFinished.disconnect(self._delayed_set)
            except Exception:
                pass

    @property
    def changable(self):
        return self._changable

    @changable.setter
    def changable(self, state):
        if state == self._changable:
            return

        if not state and self.writable:
            self.writable = False
        self._changable = state
        self.browse_button.setVisible(state)

    def browse(self):
        if self.browse_type == BrowseType.file:
            file_types = 'All Files (*)' if not self.file_types else self.file_types
            if self.save_mode:
                file_path, _ = QtGui.QFileDialog.getSaveFileName(self, self.label_text, self._value, file_types)
            else:
                file_path, _ = QtGui.QFileDialog.getOpenFileName(self, self.label_text, self._value, file_types)
        else:
            file_path = QtGui.QFileDialog.getExistingDirectory(self, caption=self.label_text, dir=self._value)

        if file_path:
            self.value = file_path

    def _delayed_set(self):
        if self._field_set:
            return
        QtCore.QTimer().singleShot(self._set_delay, self._set_field)

    def _set_field(self):
        self._value = self.line_field.text()
        self.changed.emit(self._value)

    def setText(self, this):
        """Just to be compatible with QDesigner setting text already"""
        self.value = this

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, this):
        self._field_set = True
        self._value = os.path.normpath(this)
        self.line_field.setText(self._value)
        self.changed.emit(self._value)
        self._field_set = False

    def show_options_menu(self):
        icons = a2ctrl.Icons.inst()
        self.options_menu.clear()
        self.options_menu.addAction(icons.copy, 'Copy Path', self.copy_path)
        self.options_menu.addAction(icons.folder, 'Explore Path', self.explore_path)
        self.options_menu.popup(QtGui.QCursor.pos())

    def explore_path(self):
        a2util.explore(self.value)

    def copy_path(self):
        QtGui.QApplication.clipboard().setText(self.value)
