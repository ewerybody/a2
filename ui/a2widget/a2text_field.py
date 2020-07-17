"""
Text field that automatically gets bigger the more lines you add.

@created: 01.11.2016
@author: eric
"""
import pprint
from PySide2 import QtGui, QtCore, QtWidgets

DEFAULT_MAX_LINES = 20
DEFAULT_MIN_LINES = 1
DEFAULT_FINISH_DELAY = 1500
BACKUP_LINE_HEIGHT = 16


class A2TextField(QtWidgets.QPlainTextEdit):
    """
    Can be set in QDesigner from PlainTextEdit. Has an editing_finished-signal
    similar to the one on the Line edit. The difference is: The trigger here
    is timed and on focus loss. Enter adds a new line as expected.
    """
    editing_finished = QtCore.Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super(A2TextField, self).__init__(parent, *args, **kwargs)
        self.finish_delay = DEFAULT_FINISH_DELAY

        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        qsize_pol = QtWidgets.QSizePolicy
        size_policy = qsize_pol(qsize_pol.Expanding, qsize_pol.Maximum)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        size_policy.setVerticalStretch(0)
        size_policy.setHorizontalStretch(0)
        self.setSizePolicy(size_policy)

        self.blockCountChanged.connect(self._set_height_to_block_count)
        self._cursor_height = None
        self._backup_height = BACKUP_LINE_HEIGHT
        self.maximum_blocks = DEFAULT_MAX_LINES
        self.minimum_blocks = DEFAULT_MIN_LINES

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
        return QtWidgets.QPlainTextEdit.showEvent(self, *args, **kwargs)

    def focusOutEvent(self, *args, **kwargs):
        self.finish_editing()
        return QtWidgets.QPlainTextEdit.focusOutEvent(self, *args, **kwargs)

    def text(self):
        return self.toPlainText()

    def setText(self, this):
        self.blockSignals(True)
        try:
            self.setPlainText(this)
        except TypeError:
            self.setPlainText(pprint.pformat(this))

        self._set_height_to_block_count()
        self.blockSignals(False)

    def _set_height_to_block_count(self, block_count=None):
        if block_count is None:
            block_count = self.blockCount()
        if self.maximum_blocks is not None:
            block_count = min(
                max(block_count, self.minimum_blocks),
                max(1, self.maximum_blocks))

        cursor_height = self.cursorRect().height()
        if cursor_height:
            self._cursor_height = cursor_height
        elif self._cursor_height is None:
            cursor_height = self._backup_height
        else:
            cursor_height = self._cursor_height

        magic_height = (cursor_height / 3) + 8
        height = (cursor_height * block_count) + magic_height

        self.setMinimumHeight(height)
        self.setMaximumHeight(height)

    def check_editing_finished(self):
        """Rewind the timer."""
        self._timer.start()

    def finish_editing(self):
        """Care for the timer being stopped and send editing_finished signal."""
        if self._timer.isActive():
            self._timer.stop()
        self.editing_finished.emit()


class A2CodeField(A2TextField):
    """
    Just subclassed to be identifiable via CSS to apply a monospaced font.
    """
    def __init__(self, parent=None, *args, **kwargs):
        A2TextField.__init__(self, parent, *args, **kwargs)
