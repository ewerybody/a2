"""
@created: 20.09.2016
@author: eric
"""
import os

import a2core
from a2mod import MOD_SOURCE_NAME
from a2widget.a2input_dialog import A2InputDialog


log = a2core.get_logger(__name__)


class NewModuleSourceTool(A2InputDialog):
    def __init__(self, main):
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self.source_names = [m.lower() for m in self.a2.module_sources]
        super(NewModuleSourceTool, self).__init__(
            self.main, 'New Module Source', self.create_source, self.check_name,
            msg='Name the new module source:', text='my_module_source')

    def check_name(self, NAME):
        """
        Runs on keystroke when creating new module source
        to give way to okaying creation.
        """
        name = NAME.lower()
        if NAME == '':
            return 'Name cannot be empty!'
        if name == 'a2':
            return 'You just cannot name your module "a2"! Ok?'
        if name in self.source_names:
            return 'Module source name "%s" is in use!' % name
        if any([(l in a2core.string.whitespace) for l in name]):
            return 'Name cannot have whitespace! Use _ or - insead!'
        if not all([(l in a2core.ALLOWED_CHARS) for l in name]):
            return 'Name can only have letters, digits, _ and -'
        if name in a2core.ILLEGAL_NAMES:
            return 'Name cannot be reserved OS device name!'
        if not any([(l in a2core.string.ascii_letters) for l in name]):
            return 'Come one have at least 1 letter in the name!'
        return True

    def create_source(self, name):
        if not self.check_name(name):
            return
        if not os.access(self.a2.paths.modules, os.W_OK):
            log.error('A2 module directory not writable! %s' % self.a2.paths.modules)
            return

        source_path = os.path.join(self.a2.paths.modules, name)
        source_cfg = os.path.join(source_path, MOD_SOURCE_NAME)
        os.mkdir(source_path)
        a2core.json_write(source_cfg, {})
        self.a2.fetch_modules()
        self.main.ui.module_view.draw_mod()
