"""
a2ctrl.module_list
"""
from PySide import QtGui

import a2ctrl
from a2ctrl import module_list_ui

class ModuleList(QtGui.QWidget):

    def __init__(self, parent):
        super(ModuleList, self).__init__(parent)
        a2ctrl.check_ui_module(module_list_ui)
#        uifile = r'C:\Users\eRiC\io\code\a2\ui\a2ctrl\module_list.ui'
#        pyfile = r'C:\Users\eRiC\io\code\a2\ui\a2ctrl\module_list_ui.py'
#        with open(pyfile, 'w') as pyfobj:
#            compileUi(uifile, pyfobj)
        self.setup_ui()

    def setup_ui(self):
        self.ui = module_list_ui.Ui_ModuleList()
        self.ui.setupUi(self)

        self.setLayout(self.ui.module_list_layout)
