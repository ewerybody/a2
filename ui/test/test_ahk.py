'''
Created on Aug 24, 2016

@author: eRiC
'''
import os
import uuid
import unittest
from os.path import exists

import ahk


class Test(unittest.TestCase):
    def test_get_set_vars(self):
        test_content = (
            '; some random ahk comment\n'
            'a_string := "lorem ipsum... " \n'
            ' anotherString = asvasd asdfasd asdfasd\n'
            'a_bool := false\n'
            'a_number = 42133723\n'
            'a_float = 123.567')

        test_file = os.path.join(os.getenv('temp'), str(uuid.uuid4()) + '.ahk')
        with open(test_file, 'w') as fob:
            fob.write(test_content)
        ahkvars = ahk.get_variables(test_file)
        self.assertEqual(len(ahkvars), 4)
        self.assertTrue('a_string' in ahkvars)
        self.assertEqual(ahkvars['a_string'], 'lorem ipsum...')

        ahk.set_variable(test_file, 'a_bool', True)
        with open(test_file) as fob:
            new_content = fob.read()
        self.assertEqual(test_content, new_content)

        os.remove(test_file)
        self.assertFalse(exists(test_file))


if __name__ == "__main__":
    unittest.main()
