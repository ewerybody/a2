from PySide.QtGui import QAction
from PySide.QtCore import Signal, Slot, QObject

import siding
import functools

class Test(siding.plugins.IPlugin):
    def __init__(self, manager, name):
        super(Test, self).__init__(manager, name)

        self.windows = []

    def do_rot13(self, win):
        """ Run rot13 on the editor text. """
        win.editor.setPlainText(win.editor.toPlainText().encode('rot13'))

    @Slot(QObject)
    def new_window(self, win):
        self.windows.append(win)

        win.actions['rot-13'] = act = QAction("&rot-13", win,
            statusTip="Rot-13 the text.",
            triggered=functools.partial(self.do_rot13, win))

        tb = win._rot13tb = win.addToolBar('rot-13')
        tb.setObjectName('_rot13tb')
        tb.addAction(act)
    
    @Slot(QObject)
    def closed_window(self, win):
        if win in self.windows:
            self.windows.remove(win)
