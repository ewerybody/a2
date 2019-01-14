import os
import a2core
import a2util
import importlib

DEFAULT = 'english_qwerty'
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
CFG_FILE = 'layouts.json'
DB_ATTR = 'keyboard_id'


def get_module(keyboard_id):
    # keyboard_module_name = __name__.rsplit('.', 1)[0] + '.' + keyboard_id
    keyboard_module_name = __name__ + '.' + keyboard_id
    return importlib.import_module(keyboard_module_name)


def iterate():
    for keyboard_id, label in a2util.json_read(os.path.join(THIS_DIR, CFG_FILE)).items():
        path = os.path.join(THIS_DIR, keyboard_id + '.py')
        if os.path.isfile(path):
            yield keyboard_id, label


def get_current():
    a2 = a2core.A2Obj.inst()
    return a2.db.get(DB_ATTR) or DEFAULT


def set_layout(keyboard_label):
    a2 = a2core.A2Obj.inst()
    for keyboard_id, label in iterate():
        if label == keyboard_label:
            a2.db.set(DB_ATTR, keyboard_id)
            return
    raise KeyError('Keyboard layout "%s" could not be found!' % keyboard_label)


if __name__ == '__main__':
    a2 = a2core.A2Obj.inst()
    keyboard_id = a2.db.get(DB_ATTR)
    print('keyboard_id: %s' % keyboard_id)
