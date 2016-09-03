"""
a2element.include

@created: Sep 3, 2016
@author: eRiC
"""
from a2element import EditCtrl
from PySide import QtGui, QtCore


class Edit(EditCtrl):
    """
    User-invisible control that you only see in edit-mode
    """
    def __init__(self, cfg, main, parentCfg):
        self.ctrlType = 'Include'
        super(Edit, self).__init__(cfg, main, parentCfg, addLayout=False)
        self.main = main
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setSpacing(5)
        self.labelCtrl = QtGui.QLabel('script file:')
        self.labelCtrl.setAlignment(QtCore.Qt.AlignRight)
        self.layout.addWidget(self.labelCtrl)
        self.button = QtGui.QPushButton(self.cfg['file'])
        self.buttonMenu = BrowseScriptsMenu(self.main, self.setScript)
        self.button.setMenu(self.buttonMenu)
        self.layout.addWidget(self.button)

        self.editButton = QtGui.QPushButton('edit script')
        self.editButton.pressed.connect(self.edit_script)
        self.layout.addWidget(self.editButton)

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout.addItem(spacerItem)
        self.mainWidget.setLayout(self.layout)

    def setScript(self, typ, name):
        self.cfg['file'] = name
        self.button.setText(name)

    def edit_script(self):
        if exists(self.main.devset.code_editor):
            subprocess.Popen([self.main.devset.code_editor,
                              os.path.join(self.main.mod.path, self.cfg['file'])])
        else:
            log.error('No code_editor found! Set it up in settings!')