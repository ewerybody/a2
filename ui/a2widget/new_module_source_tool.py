"""
@created: 20.09.2016
@author: eric
"""
import os

import a2core
import a2util
from a2mod import MOD_SOURCE_NAME
from a2widget.a2input_dialog import A2InputDialog


log = a2core.get_logger(__name__)


class NewModuleSourceTool(A2InputDialog):
    def __init__(self, main):
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self.source_names = [m.lower() for m in self.a2.module_sources]
        super(NewModuleSourceTool, self).__init__(
            self.main, 'New Module Source', self.check_name,
            msg='Name the new module source:', text='my_module_source')

    def check_name(self, name):
        """
        Runs on keystroke when creating new module source
        to give way to okaying creation.
        """
        return a2util.standard_name_check(
            name, self.source_names, 'The name "%s" is already in use!')
