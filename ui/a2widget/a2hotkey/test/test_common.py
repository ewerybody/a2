from functools import partial
import unittest
from a2widget.a2hotkey import hotkey_common


class Test(unittest.TestCase):
    def test_sortmods(self):
        # testing these things ...
        for k in [
            'f',
            'numpadleft',
            'alt+CTRL+f3',
            'lShift+Altgr+ y',
            'win+lbutton',
            '',
        ]:
            try:
                print(' in: %s\nout: %s\n' % (k, hotkey_common.sort_modifiers(k)))
            except ValueError as error:
                print(error, '\n')

        self.assertRaises(ValueError, partial(hotkey_common.sort_modifiers, 'ctrl+VSJKDBk+4'))

    def test_key_list(self):
        _key_list = 'shift+Alt+d'
        _new_list = hotkey_common.get_keys_list(_key_list)
        print(_new_list)
        print(_new_list == hotkey_common.get_keys_list(_new_list))


if __name__ == '__main__':
    unittest.main()
