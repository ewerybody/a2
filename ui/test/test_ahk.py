"""Test the a2ahk module"""
import os
import uuid
import pytest

import a2ahk

TEST_CONTENT = """; some random ahk comment
_a_string := "lorem ipsum... "
  anIndentedString = as2va3sd as5dfa4sd ad4fas1d
_a_bool := false
_a_number = 42133723
_a_float = 123.567
"""


def test_get_set_vars():
    test_file = _get_test_ahk_path()
    with open(test_file, 'w') as fob:
        fob.write(TEST_CONTENT)

    ahk_vars = a2ahk.get_variables(test_file)
    assert len(ahk_vars) == 4
    assert '_a_string' in ahk_vars
    assert ahk_vars['_a_string'] == 'lorem ipsum...'

    a2ahk.set_variable(test_file, '_a_bool', True)
    ahk_vars = a2ahk.get_variables(test_file)
    assert ahk_vars['_a_bool']
    with pytest.raises(KeyError):
        a2ahk.set_variable(test_file, 'MissingName', False)

    a2ahk.set_variable(test_file, '_a_number', 1)
    ahk_vars = a2ahk.get_variables(test_file)
    assert ahk_vars['_a_number'] == 1
    test_string = 'a rose is a rose...'
    a2ahk.set_variable(test_file, '_a_string', test_string)
    ahk_vars = a2ahk.get_variables(test_file)
    assert ahk_vars['_a_string'] == test_string

    with pytest.raises(KeyError):
        a2ahk.set_variable(test_file, 'bad name', 123)

    os.remove(test_file)
    assert not os.path.isfile(test_file)

def test_get_set_vars_new_file():
    test_file = _get_test_ahk_path()
    assert not os.path.isfile(test_file)
    for key, value in (('some_key', 'Monkeys'), ('another', 4815162342)):
        a2ahk.set_variable(test_file, key, value)
        assert os.path.isfile(test_file)
        vars = a2ahk.get_variables(test_file)
        assert key in vars
        assert vars[key] == value
        os.remove(test_file)
        assert not os.path.isfile(test_file)

def test_create_vars():
    """Test adding lines to files or re-using last empty line."""
    for content in TEST_CONTENT, TEST_CONTENT.strip():
        test_file = _get_test_ahk_path()
        with open(test_file, 'w') as fob:
            fob.write(content)

        key, value = str(uuid.uuid4()).replace('-', ''), str(uuid.uuid4())
        a2ahk.set_variable(test_file, key, value, create_key=True)
        ahk_vars = a2ahk.get_variables(test_file)
        assert ahk_vars[key] == value

def test_string_convert():
    result = a2ahk.convert_string_to_type('string')
    assert isinstance(result, str)
    assert 'string' == result
    assert a2ahk.convert_string_to_type('true')
    assert not a2ahk.convert_string_to_type('faLSe')
    result = a2ahk.convert_string_to_type('345243')
    assert isinstance(result, int)
    result = a2ahk.convert_string_to_type('345243.')
    assert isinstance(result, float)

def test_py_value_to_string():
    for item, result in [
        (True, 'true'),
        (False, 'false'),
        ('String', '"String"'),
        ('escaped "String"', "'escaped \"String\"'"),
        (0.333, '0.333'),
        (1337, '1337'),
        (['something', 42, 13.37], '["something", 42, 13.37]'),
        ({'abc': 123, 'def': 'poop'}, 'Map("abc", 123, "def", "poop")')
    ]:
        converted = a2ahk.py_value_to_ahk_string(item)
        assert converted == result

def test_ensure_ahk_ext():
    base = str(uuid.uuid4())
    name = a2ahk.ensure_ahk_ext(base)
    parts = os.path.splitext(name)
    assert parts[0] == base
    assert parts[1] == a2ahk.EXTENSION

def test_call_lib_cmd():
    win_startup_path = a2ahk.call_lib_cmd('get_win_startup_path')
    assert isinstance(win_startup_path, str)

def test_var_names():
    legal_names = ('a', 'ABC', 'snake_case', '_____lol', '1name')
    illegal_nms = ('1', 'sva-sdf', 'as2da.asd', '12342', 'with  space', ' ')
    for name in legal_names:
        assert not a2ahk.check_variable_name(name)
    for name in illegal_nms:
        assert a2ahk.check_variable_name(name)

def test_get_version():
    try:
        version = a2ahk.get_latest_version()
    except RuntimeError as error:
        pytest.skip(f'Problem getting version from homepage:\n{error}')

    assert isinstance(version, str)
    assert version.startswith(a2ahk.BASE_VERSION)


def _get_test_ahk_path():
    return os.path.join(os.getenv('temp', ''), str(uuid.uuid4()) + a2ahk.EXTENSION)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
