"""
@created: 19.09.2016
@author: eric
"""
import os

from a2widget.a2input_dialog import A2InputDialog


class NewElementDialog(A2InputDialog):
    def __init__(self, main):
        self.main = main
        super(NewElementDialog, self).__init__(self.main, 'New Element Dialog')
        template = os.path.join(self.main.a2.paths._defaults, 'element.template.py')
        print('template: %s' % template)



if __name__ == '__main__':
    pass
