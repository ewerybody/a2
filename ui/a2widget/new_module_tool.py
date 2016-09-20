"""
@created: 20.09.2016
@author: eric
"""
import os

from PySide import QtGui

import a2core
import a2ctrl
from a2mod import get_folders
from a2widget.a2input_dialog import A2InputDialog


class NewModulueTool(A2InputDialog):
    def __init__(self, main, module_source=None):
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self.source_dict = {'sources': list(self.a2.module_sources.keys()), 'names': {}}
        if module_source is None:
            module_source = self.a2.db.get('last_module_create_source') or self.source_dict['sources'][0]
        self.source_dict['seleceted_source'] = module_source
        self.source_dict['source_index'] = self.source_dict['sources'].index(module_source)

        super(NewModulueTool, self).__init__(
            self.main, 'New Module', self.create_module, self.check_name,
            msg='Name the new module:', text='my_module')

        self.ui.main_layout.insertWidget(0, QtGui.QLabel('Module Source:'))

        self.source_index = QtGui.QComboBox(self)
        self.source_index.addItems(self.source_dict['sources'])
        a2ctrl.connect.control(self.source_index, 'source_index', self.source_dict)
        self.source_index.currentIndexChanged.connect(self.check_on_source_change)
        self.ui.main_layout.insertWidget(1, self.source_index)

    def check_on_source_change(self, _int):
        self.check()

    def create_module(self, name):
        """
        Creates path to the new module, makes the dir
        refreshes modules and selects the new one in the list
        TODO: workaround creating for disables sources, works but lacks feedback.
        """
        source_name = self.source_dict['sources'][self.source_dict['source_index']]
        self.a2.db.set('last_module_create_source', source_name)
        source = self.a2.module_sources[source_name]

        module_path = os.path.join(source.path, name)
        os.mkdir(module_path)
        self.a2.fetch_modules()
        self.main.module_list.draw_modules('%s|%s' % (source.name, name))

    def check_name(self, NAME):
        """
        Runs on keystroke when creating new module source
        to give way to okaying creation.
        """
        source = self.source_dict['sources'][self.source_dict['source_index']]
        # fetch folders in module source as deactivated sources were not listed before
        if source not in self.source_dict['names']:
            names = get_folders(self.a2.module_sources[source].path)
            self.source_dict['names'][source] = list(map(str.lower, names))

        name = NAME.lower()
        if NAME == '':
            return 'Name cannot be empty!'
        if name == 'a2':
            return 'You cannot take the name "a2"! Ok?'
        if name in self.source_dict['names'][source]:
            return 'Module name "%s" is in use!' % name
        if any([(l in a2core.string.whitespace) for l in name]):
            return 'No whitespace! Use _ or - insead!'
        if not all([(l in a2core.ALLOWED_CHARS) for l in name]):
            return 'Name can only have letters, digits, _-'
        if name in a2core.ILLEGAL_NAMES:
            return 'Name is reserved OS device name!'
        if not any([(l in a2core.string.ascii_letters) for l in name]):
            return 'Have at least 1 letter in the name!'
        return True
