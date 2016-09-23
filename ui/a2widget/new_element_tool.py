"""
@created: 19.09.2016
@author: eric
"""
import os

from a2widget.a2input_dialog import A2InputDialog
import a2core
import subprocess


class NewElementDialog(A2InputDialog):
    def __init__(self, main):
        self.main = main
        super(NewElementDialog, self).__init__(
            self.main, 'New Element Dialog', msg='Name the new element:', text='name',
            okFunc=self.create_element,
            checkFunc=self.check_element_name)
        self._current_elements = [os.path.splitext(f)[0] for f in os.listdir(self.main.a2.paths.elements)]

    def check_element_name(self, name):
        return a2core.standard_name_check(name, self._current_elements)

    def create_element(self, name):
        template = os.path.join(self.main.a2.paths._defaults, 'element.template.py')
        with open(template) as fobj:
            new_element_code = fobj.read().format(
                description='Some element description ...',
                creation_date=a2core.get_date(),
                author_name=self.main.devset.author_name,
                element_name=name.title())

        new_path = os.path.join(self.main.a2.paths.elements, name + '.py')
        with open(new_path, 'w') as fobj:
            fobj.write(new_element_code)

        subprocess.Popen(['explorer.exe', '/select,', os.path.normpath(new_path)])


if __name__ == '__main__':
    pass
