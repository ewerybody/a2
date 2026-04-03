import random
import os

from PySide6 import QtWidgets, QtGui
import a2ctrl

import a2path
from a2toolbox import shell_open

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_ITEMS = [i.path for i in a2path.iter_types(THIS_DIR, ['.py'])]
THAT_DIR = os.path.abspath(os.path.dirname(a2path.__file__))
TEST_ITEMS2 = [i.path for i in a2path.iter_types(THAT_DIR, ['.py'])]


class TestWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QtWidgets.QWidget()
        widget.setMinimumWidth(300)
        self.setCentralWidget(widget)
        self.setWindowIcon(a2ctrl.Icons.a2)
        self.setWindowTitle('`shell_open` Demo')

        layout = QtWidgets.QFormLayout(widget)
        font = QtGui.QFont()
        font.setPointSize(20)
        button = QtWidgets.QPushButton('Random Select')
        button.clicked.connect(self._single)
        layout.addRow('Single File:', button)

        button = QtWidgets.QPushButton('Random Select')
        button.clicked.connect(self._multi)
        layout.addRow('Multiple Files:', button)

        button = QtWidgets.QPushButton('Random Select')
        button.clicked.connect(self._multi_dirs)
        layout.addRow('Files in Multiple Dirs:', button)

        button = QtWidgets.QPushButton('Random Open')
        button.clicked.connect(self._dir_only)
        layout.addRow('Directory Only:', button)

    def _single(self):
        print(f'selecting 1 item in {THIS_DIR} ...')
        shell_open.main(random.choice(TEST_ITEMS))

    def _multi(self):
        items = random.sample(TEST_ITEMS, min(5, random.randint(1, len(TEST_ITEMS))))
        print(f'selecting {len(items)} item in {THIS_DIR} ...')
        shell_open.main(items)

    def _multi_dirs(self):
        items = random.sample(TEST_ITEMS2, min(3, random.randint(1, len(TEST_ITEMS2))))
        print(f'selecting {len(items)} item in {THAT_DIR} and')
        more_items = (random.sample(TEST_ITEMS, min(3, random.randint(1, len(TEST_ITEMS)))))
        print(f'  {len(more_items)} item in {THIS_DIR} ...')
        shell_open.main(items + more_items)

    def _dir_only(self):
        folder = random.choice([THIS_DIR, THAT_DIR, os.path.dirname(os.__file__)])
        print(f'opening up just {folder} ...')
        shell_open.main(folder)


def show():
    app = QtWidgets.QApplication([])
    win = TestWindow()
    win.show()
    app.exec()


if __name__ == '__main__':
    show()
