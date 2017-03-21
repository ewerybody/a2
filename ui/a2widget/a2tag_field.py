from PySide import QtCore, QtGui

import a2ctrl
from a2widget.flowlayout import FlowLayout


class A2TagField(QtGui.QWidget):
    changed = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(A2TagField, self).__init__(parent=parent)
        self.main_layout = FlowLayout(self)

        self.plus_button = QtGui.QToolButton()
        #self.plus_button.setIcon(a2ctrl.Icons().)
        self.plus_button.setText('+')
        self.main_layout.addWidget(self.plus_button)

        self._tags = []
        self._tag_widgets = []

    def set_tags(self, these):
        """
        Replaces the saved tags with given ones.

        :param these: Tags to put.
        """
        if isinstance(these, str):
            these = [these]
        elif not isinstance(these, (tuple, list, set)):
            raise RuntimeError('Tag Field needs an iterable as tags')

        self._tags

    def clear(self):
        for widget in self._tag_widgets:
            widget.deleteLater()
        self._tags = []
        # TODO: emit only if it wasn't empty before

    @property
    def value(self):
        return self._tags

    @value.setter
    def value(self, these):
        self.set_tags(these)



if __name__ == '__main__':
    pass
