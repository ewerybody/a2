'''
Created on Dec 28, 2015

@author: eRiC
'''
from PySide import QtCore, QtGui
import a2ctrl
import logging


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Draw(QtGui.QWidget):
    """
    Group box to bundle multiple other controls or includes that can be
    enabled/disables all at once.
    """
    def __init__(self, cfg, mod):
        super(Draw, self).__init__()


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
    def __init__(self, cfg, main):
        self.ctrlType = 'Groupbox'
        super(Edit, self).__init__(cfg, main)
        print('EditGroup cfg: %s' % self.cfg)
        for child in self.cfg.get('children', []):
            print('child: %s' % child)
            a2ctrl.edit(cfg, self.mod, self)
                    
        #a2ctrl.EditAddElem(self.mod, self.tempConfig, self.editMod)
