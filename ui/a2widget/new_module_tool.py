import os

from PySide2 import QtWidgets

import a2mod
import a2core
import a2util
import a2ctrl.connect
from a2widget.a2input_dialog import A2InputDialog


class NewModulueTool(A2InputDialog):
    def __init__(self, main, module_source=None):
        self.a2 = a2core.A2Obj.inst()
        self.main = main

        if not self.a2.module_sources:
            title = 'No Module Source!'
            msg = ('There is no <b>module source</b> to create a module in!\n'
                   'Would you like to create a local one?')
            reply = QtWidgets.QMessageBox.question(None, title, msg, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            if reply is QtWidgets.QMessageBox.Yes:
                self.main.create_local_source()
            return

        self.source_dict = self._init_source_dict(module_source)

        super(NewModulueTool, self).__init__(
            self.main, 'New Module', check_func=self.check_name,
            msg='Name the new module:', text='my_module')

        self.okayed.connect(self.create_module)
        self.ui.main_layout.insertWidget(0, QtWidgets.QLabel('Module Source:'))

        self.source_index = QtWidgets.QComboBox(self)
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
        module = self.a2.get_module_obj(source_name, name)
        self.main.module_list.draw_modules([module])

    def check_name(self, name):
        """
        Runs on keystroke when creating new module source
        to give way to okaying creation.
        """
        source = self.source_dict['sources'][self.source_dict['source_index']]
        # fetch folders in module source as deactivated sources were not listed before
        if source not in self.source_dict['names']:
            names = a2mod.get_folders(self.a2.module_sources[source].path)
            self.source_dict['names'][source] = list(map(str.lower, names))

        self._module_list = self.source_dict['names'][source]
        return a2util.standard_name_check(name, self._module_list, 'Module name "%s" is in use!')

    def _init_source_dict(self, module_source):
        sources = [s.name for s in self.a2.module_sources.values() if s.enabled]
        source_dict = {'sources': sources, 'names': {}}
        if module_source is None:
            last_source = self.a2.db.get('last_module_create_source')
            if last_source and last_source in source_dict['sources']:
                module_source = last_source
            else:
                module_source = source_dict['sources'][0]

        source_dict['selected_source'] = module_source
        source_dict['source_index'] = source_dict['sources'].index(module_source)
        return source_dict
