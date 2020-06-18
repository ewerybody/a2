"""Test the a2ahk module"""
import uuid
import unittest
import os.path
from functools import partial

import a2ahk


class Test(unittest.TestCase):
    def test_get_set_vars(self):
        test_content = (
            '; some random ahk comment\n'
            'a_string := "lorem ipsum... " \n'
            ' anotherString = asvasd asdfasd asdfasd\n'
            'a_bool := false\n'
            'a_number = 42133723\n'
            'a_float = 123.567')

        test_file = os.path.join(os.getenv('temp'), str(uuid.uuid4()) + a2ahk.EXTENSION)
        with open(test_file, 'w') as fob:
            fob.write(test_content)
        ahkvars = a2ahk.get_variables(test_file)
        self.assertEqual(len(ahkvars), 4)
        self.assertTrue('a_string' in ahkvars)
        self.assertEqual(ahkvars['a_string'], 'lorem ipsum...')

        a2ahk.set_variable(test_file, 'a_bool', True)
        ahkvars = a2ahk.get_variables(test_file)
        self.assertTrue(ahkvars['a_bool'])
        self.assertRaises(ValueError, partial(a2ahk.set_variable, test_file, 'MissingName', False))
        a2ahk.set_variable(test_file, 'a_number', 1)
        ahkvars = a2ahk.get_variables(test_file)
        self.assertEqual(ahkvars['a_number'], 1)
        test_string = 'a rose is a rose...'
        a2ahk.set_variable(test_file, 'a_string', test_string)
        ahkvars = a2ahk.get_variables(test_file)
        self.assertEqual(ahkvars['a_string'], test_string)

        os.remove(test_file)
        self.assertFalse(os.path.isfile(test_file))

    def test_string_convert(self):
        result = a2ahk.convert_string_to_type('string')
        self.assertTrue(isinstance(result, str))
        self.assertEqual('string', result)
        result = a2ahk.convert_string_to_type('true')
        self.assertTrue(result)
        result = a2ahk.convert_string_to_type('faLSe')
        self.assertFalse(result)
        result = a2ahk.convert_string_to_type('345243')
        self.assertTrue(isinstance(result, int))
        result = a2ahk.convert_string_to_type('345243.')
        self.assertTrue(isinstance(result, float))

    def test_py_value_to_string(self):
        for item, result in [
                (True, 'true'), (False, 'false'),
                ('String', '"String"'),
                (0.333, '0.333'), (1337, '1337'),
                (['something', 42, 13.37], '["something", 42, 13.37]')]:
            converted = a2ahk.py_value_to_ahk_string(item)
            self.assertEqual(converted, result)


if __name__ == "__main__":
    unittest.main()
