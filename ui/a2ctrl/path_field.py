"""
A universal file/folder path field with a browse button.
the field can be made writable or read-only to allow only browsed paths
it can be made browsing for folders or files
at files it can be set to save-mode where inexistent paths can be selected
and filtered file types can be set. See:
http://pyside.github.io/docs/pyside/PySide/QtGui/QFileDialog.html?highlight=qfiledialog#detailed-description

TODO: add recent paths, copy path, explore to path on the button

@created: Jun 19, 2016
@author: eRiC
"""
from PySide import QtGui, QtCore


class BrowseType(object):
    folder = '0'
    file = '1'


class PathField(QtGui.QWidget):
    changed = QtCore.Signal(str)

    def __init__(self, parent, value='', file_types='', writable=True, label_text=None, save_mode=False):
        super(PathField, self).__init__(parent)
        self.main_layout = QtGui.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.line_field = QtGui.QLineEdit(self)
        self.line_field.setText(value)
        self.main_layout.addWidget(self.line_field)
        self.browse_button = QtGui.QPushButton('Browse...', self)
        self.browse_button.clicked.connect(self.browse)
        self.main_layout.addWidget(self.browse_button)
        self._set_delay = 150
        self._field_set = False

        self._value = value
        self.file_types = file_types
        self.save_mode = save_mode
        self.browse_type = BrowseType.file
        self.label_text = label_text
        self._writable = writable

        self.writable = self._writable

    @property
    def writable(self):
        return self._writable

    @writable.setter
    def writable(self, state):
        if state == self._writable:
            return
        print('state: %s' % state)
        self._writable = state
        self.line_field.setReadOnly(not state)
        if state:
            self.line_field.editingFinished.connect(self._delayed_set)
        else:
            try:
                self.line_field.editingFinished.disconnect(self._delayed_set)
            except:
                pass

    def browse(self):
        if self.browse_type == BrowseType.file:
            file_types = 'All Files (*)' if not self.file_types else self.file_types
            if self.save_mode:
                filepath, _ = QtGui.QFileDialog.getSaveFileName(self, self.label_text, self._value, file_types)
            else:
                filepath, _ = QtGui.QFileDialog.getOpenFileName(self, self.label_text, self._value, file_types)
        else:
            filepath = QtGui.QFileDialog.getExistingDirectory(self, caption=self.label_text, dir=self._value)

        if filepath:
            self.value = filepath

    def _delayed_set(self):
        if self._field_set:
            return
        QtCore.QTimer().singleShot(self._set_delay, self._set_field)

    def _set_field(self):
        self._value = self.line_field.text()
        self.changed.emit(self._value)

    def setText(self, this):
        self.value = this

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, this):
        self._field_set = True
        self._value = this
        self.line_field.setText(this)
        self.changed.emit(this)
        self._field_set = False
