"""
@created: 19.09.2016
@author: eric
"""
import os
import subprocess
from PySide import QtGui, QtCore

import a2core
import a2util
import a2ctrl.connect
from a2widget.a2input_dialog import A2InputDialog
import json
import importlib


LABEL_GLOBAL = 'Add globally as "a2element.%s"'
DISPLAY_ELEMENTS_LABEL = 'DISPLAY_ELEMENTS'
LABEL_LIST_CHECK = 'Enlist in %s' % DISPLAY_ELEMENTS_LABEL
LABEL_LOCAL = 'Add locally to module "%s"'
LABEL_NOLOCAL = 'There is no module selected!'


class NewElementDialog(A2InputDialog):
    cfg_changed = QtCore.Signal(bool)

    def __init__(self, main):
        self.main = main
        self.a2 = a2core.A2Obj.inst()
        self._current_elements = [os.path.splitext(f)[0] for f in os.listdir(self.main.a2.paths.elements)]
        super(NewElementDialog, self).__init__(
            self.main, 'New Element Dialog', msg='Name the new element:', text='name',
            ok_func=self.create_element,
            check_func=self.check_element_name)
        self.element_cfg = {'target': 'global', 'enlist': True}
        self.setup_ui()

    def setup_ui(self):
        self.ui.radio_global = QtGui.QRadioButton(LABEL_GLOBAL % self.text, self)
        self.ui.radio_global.setObjectName('target_global')
        self.ui.main_layout.insertWidget(0, self.ui.radio_global)

        self.ui.check_display_list = QtGui.QCheckBox(LABEL_LIST_CHECK, self)
        self.ui.check_display_list.setObjectName('enlist')
        hlayout = QtGui.QHBoxLayout()
        indent = QtGui.QLabel()
        indent.setMaximumWidth(self.main.css_values['margin_h'])
        indent.setMinimumWidth(self.main.css_values['margin_h'])
        hlayout.addWidget(indent)
        hlayout.addWidget(self.ui.check_display_list)
        self.ui.main_layout.insertLayout(1, hlayout)

        self.ui.radio_local = QtGui.QRadioButton(self)
        self.ui.radio_local.setObjectName('target_local')
        self.ui.main_layout.insertWidget(2, self.ui.radio_local)

        element_ctrls = [self.ui.radio_global, self.ui.radio_local, self.ui.check_display_list]
        self.element_cfg.update(self.a2.db.get('new_element_cfg') or self.element_cfg)
        a2ctrl.connect.control_list(element_ctrls, self.element_cfg, self.cfg_changed)
        self.cfg_changed.connect(self.on_cfg_changed)

        if self.main.mod is None:
            self.ui.radio_local.setText(LABEL_NOLOCAL)
            self.ui.radio_local.setEnabled(False)
            self.ui.radio_global.setChecked(True)
        else:
            self.ui.radio_local.setText(LABEL_LOCAL % self.main.mod.name)
            self.ui.radio_local.setEnabled(True)

    def on_cfg_changed(self, *args):
        self.ui.check_display_list.setEnabled(self.element_cfg['target'] == 'global')

    def check_element_name(self, name):
        # change radio button label to match the entered name when ctrl is available
        try:
            self.ui.radio_global.setText(LABEL_GLOBAL % name.lower())
        except Exception:
            pass

        return a2util.standard_name_check(name, self._current_elements)

    def create_element(self, NAME):
        name = NAME.lower()
        template = os.path.join(self.a2.paths._defaults, 'element.template.py')
        self.a2.db.set('new_element_cfg', self.element_cfg)
        with open(template) as fobj:
            new_element_code = fobj.read().format(
                description='Some element description ...',
                creation_date=a2util.get_date(),
                author_name=self.main.devset.author_name,
                element_name=name.title())

        if self.element_cfg['target'] == 'global':
            new_path = os.path.join(self.a2.paths.elements, name + '.py')

            if self.element_cfg['enlist']:
                a2element_init = os.path.join(self.a2.paths.elements, '__init__.py')
                with open(a2element_init) as fobj:
                    lines = fobj.read().split('\n')
                for i, line in enumerate(lines):
                    if line.startswith(DISPLAY_ELEMENTS_LABEL):
                        values = json.loads(line.split(' = ', 1)[1].replace("'", '"'))
                        values.append(name)
                        lines[i] = '%s = %s' % (DISPLAY_ELEMENTS_LABEL, str(sorted(values)).replace("u'", "'"))
                with open(a2element_init, 'w') as fobj:
                    fobj.write('\n'.join(lines))

                import a2element
                importlib.reload(a2element)
                a2element.get_list(force=True)
        else:
            new_path = os.path.join(self.main.mod.path, name + '.py')

        with open(new_path, 'w') as fobj:
            fobj.write(new_element_code)

        subprocess.Popen(['explorer.exe', '/select,', os.path.normpath(new_path)])


if __name__ == '__main__':
    pass
