'''
Created on Dec 28, 2015

@author: eRiC
'''
import a2ctrl
from PySide import QtGui
from a2ctrl import group_edit_ui


class Draw(QtGui.QGroupBox, a2ctrl.DrawCtrl):
    """
    Group box to bundle multiple other controls or includes that can be
    enabled/disables all at once.
    """
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__()
        a2ctrl.DrawCtrl.__init__(self, main, cfg, mod, _init_ctrl=False)
        self.setTitle(self.cfg.get('label', ''))
        self.setCheckable(self.cfg.get('disablable', True))
        self.setChecked(self.get_user_value(bool, 'enabled'))
        self.clicked[bool].connect(self.check)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(a2ctrl.UIValues.spacing)
        for child in self.cfg.get('children', []):
            ctrl = a2ctrl.draw(self.main, child, self.mod)
            if ctrl:
                self.layout.addWidget(ctrl)

    def check(self, state):
        self.set_user_value(state, 'enabled')
        self.change()


class Edit(a2ctrl.EditCtrl):
    """
    Group box to bundle multiple other controls or includes that can be
    enabled/disables all at once.
    These also use the draw()/edit() functions to create the sub-controls.
    Each EditGroup has its own 'add...' button to create sub controls for itself
    but just without the option to create further groups within. (Although if
        properly implemented it would probably work very well, we will
        not go deeper than this to keep complexity under the lid)
    """
    def __init__(self, cfg, main, parentCfg):
        self.ctrlType = 'Groupbox'
        super(Edit, self).__init__(cfg, main, parentCfg, addLayout=False)
        if 'children' not in self.cfg:
            self.cfg['children'] = []

        self.ui = group_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        controls = []
        for child in self.cfg['children']:
            controls.append(a2ctrl.edit(child, self.main, self.cfg['children']))

        controls.append(a2ctrl.EditAddElem(self.main, self.cfg['children']))
        for ctrl in controls:
            self.ui.edit_layout.addWidget(ctrl)

        self.check_new_name()
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

    def paste(self):
        """
        Amends child list with cfgs from the main edit_clipboard
        and flushes it afterwards.
        """
        for cfg in self.main.edit_clipboard:
            self.cfg['children'].append(cfg)
        self.main.edit_clipboard = []
        self.main.edit_mod()


if __name__ == '__main__':
    import a2app
    a2app.main()
