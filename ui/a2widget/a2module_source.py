import a2util
from PySide import QtGui, QtCore


class ModSourceWidget(QtGui.QWidget):
    toggled = QtCore.Signal()

    def __init__(self, mod_source, enabled_list):
        super(ModSourceWidget, self).__init__()
        self.mod_source = mod_source
        self.mainlayout = QtGui.QHBoxLayout(self)
        m = 1
        self.mainlayout.setContentsMargins(m, m, m, m)
        self.check = QtGui.QCheckBox(mod_source.name)
        self.check.setChecked(mod_source.name in enabled_list)
        self.mainlayout.addWidget(self.check)
        self.check.clicked[bool].connect(mod_source.toggle)
        self.check.clicked.connect(self.toggled.emit)

        self.mod_count = QtGui.QLabel('%i modules, %i enabled'
                                      % (mod_source.mod_count, mod_source.enabled_count,))
        self.mainlayout.addWidget(self.mod_count)

        self.button = QtGui.QPushButton('settings')
        self.mainlayout.setStretch(0, 1)
        self.mainlayout.setStretch(1, 1)
        self.mainlayout.addWidget(self.button)
        self.setLayout(self.mainlayout)

        self.menu = QtGui.QMenu(self)
        self.button.setMenu(self.menu)
        self.menu.aboutToShow.connect(self.build_menu)

    def build_menu(self):
        self.menu.clear()
        self.menu.addAction(QtGui.QAction('Details...', self, triggered=self.show_details))
        self.menu.addAction(QtGui.QAction('Explore to ...', self, triggered=self.explore_source))

    def show_details(self):
        raise NotImplementedError('Module Source Dialog tbd...')

    def explore_source(self):
        a2util.explore(self.mod_source.path)
