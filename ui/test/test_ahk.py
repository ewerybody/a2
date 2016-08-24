'''
Created on Aug 24, 2016

@author: eRiC
'''
import os
import uuid
import unittest
from os.path import exists

import ahk
from functools import partial


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
        ahkvars = ahk.get_variables(test_file)
        self.assertTrue(ahkvars['a_bool'])
        self.assertRaises(ValueError, partial(ahk.set_variable, test_file, 'MissingName', False))
        ahk.set_variable(test_file, 'a_number', 1)
        ahkvars = ahk.get_variables(test_file)
        self.assertEqual(ahkvars['a_number'], 1)
        test_string = 'a rose is a rose...'
        ahk.set_variable(test_file, 'a_string', test_string)
        ahkvars = ahk.get_variables(test_file)
        self.assertEqual(ahkvars['a_string'], test_string)

        os.remove(test_file)
        self.assertFalse(exists(test_file))

    def test_string_convert(self):
        result = ahk._convert_string_to_type('string')
        self.assertTrue(isinstance(result, str))
        self.assertEqual('string', result)
        result = ahk._convert_string_to_type('true')
        self.assertTrue(result)
        result = ahk._convert_string_to_type('faLSe')
        self.assertFalse(result)
        result = ahk._convert_string_to_type('345243')
        self.assertTrue(isinstance(result, int))
        result = ahk._convert_string_to_type('345243.')
        self.assertTrue(isinstance(result, float))


if __name__ == "__main__":
    unittest.main()
