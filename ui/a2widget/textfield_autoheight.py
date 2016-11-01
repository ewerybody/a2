'''
Text field that automatically gets bigger the more lines you add.

@created: 01.11.2016
@author: eric
'''
from PySide import QtGui, QtCore


class TextField_AutoHeight(QtGui.QPlainTextEdit):
    def __init__(self, parent=None, *args, **kwargs):
        super(TextField_AutoHeight, self).__init__(parent, *args, **kwargs)

        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        size_policy.setVerticalStretch(0)
        size_policy.setHorizontalStretch(0)
        self.setSizePolicy(size_policy)

        self.blockCountChanged.connect(self._set_height_to_block_count)
        self._set_height_to_block_count(1)

    def _set_height_to_block_count(self, block_count):
        cursor_height = self.cursorRect().height()
        magic_height = (cursor_height / 3) + 5
        height = (cursor_height * block_count) + magic_height
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
