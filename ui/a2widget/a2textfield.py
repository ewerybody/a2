"""
Text field that automatically gets bigger the more lines you add.

@created: 01.11.2016
@author: eric
"""
from PySide import QtGui, QtCore


class a2TextField(QtGui.QPlainTextEdit):
    """
    Can be set in QDesigner from PlainTextEdit.
    Has an editing_finished-signal similar to the one on the Line edit. The difference is:
    The trigger here is timed and on focus loss. Enter adds a new line as expected.
    """
    editing_finished = QtCore.Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super(a2TextField, self).__init__(parent, *args, **kwargs)

        self.finish_delay = 1500

        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        size_policy.setVerticalStretch(0)
        size_policy.setHorizontalStretch(0)
        self.setSizePolicy(size_policy)

        self.blockCountChanged.connect(self._set_height_to_block_count)
        self._cursor_height = None
        self._backup_height = 16

        self._timer = QtCore.QTimer()
        self._timer.setInterval(self.finish_delay)
        self._timer.timeout.connect(self.finish_editing)
        self.textChanged.connect(self.check_editing_finished)

    def showEvent(self, *args, **kwargs):
        """
        Final fix to calculate the correct height of the field on init.
        The field always gets wrong cursor heights before this event it triggered.
        """
        self._set_height_to_block_count()
        return QtGui.QPlainTextEdit.showEvent(self, *args, **kwargs)

    def focusOutEvent(self, *args, **kwargs):
        self.finish_editing()
        return QtGui.QPlainTextEdit.focusOutEvent(self, *args, **kwargs)

    def setText(self, this):
        self.setPlainText(this)
        self._set_height_to_block_count()

    def _set_height_to_block_count(self, block_count=None):
        if block_count is None:
            block_count = self.blockCount()

        cursor_height = self.cursorRect().height()
        if cursor_height:
            self._cursor_height = cursor_height
        elif self._cursor_height is None:
            cursor_height = self._backup_height
        else:
            cursor_height = self._cursor_height

        magic_height = (cursor_height / 3) + 5
        height = (cursor_height * block_count) + magic_height

        self.setMinimumHeight(height)
        self.setMaximumHeight(height)

    def check_editing_finished(self):
        # rewinds the timer
        self._timer.start()

    def finish_editing(self):
        if self._timer.isActive():
            self._timer.stop()
        self.editing_finished.emit()


class a2CodeField(a2TextField):
    """
    Just subclassed to be identifyable via CSS to apply a monospace font.
    """
    def __init__(self, parent=None, *args, **kwargs):
        a2TextField.__init__(self, parent, *args, **kwargs)
