"""
Autohotkey stuff to be used across the modules.
"""
import os
import codecs
import subprocess


EXECUTABLE_NAME = 'autohotkey.exe'
EXTENSION = '.ahk'
_LOW_BOOLS = {'true': True, 'false': False}


def translate_hotkey(display_string):
    """
    Create AHK readable string out of a human readable like:
    Win+Ctrl+M > #^m
    """
    # Strip and reattach tilde if given.
    tilde = ''
    if display_string.startswith('~'):
        tilde = '~'
        display_string = display_string[1:]

    # split by "plus", lower and make sure to remove empties ''
    parts = [p.strip() for p in display_string.lower().split('+')]
    parts = [p for p in parts if p]

    if len(parts) == 1 and parts[0] in MODIFIERS:
        # make sure single modifiers are forwarded by full name
        result = tilde + parts[0]
    else:
        modifier = parts[:-1]
        result = tilde + ''.join([MODIFIERS[m] for m in modifier]) + parts[-1]
    return result


def ensure_ahk_ext(file_name):
    """Make sure the given file_name ends with proper Autohotkey extension."""
    if not file_name.lower().endswith(EXTENSION):
        file_name += EXTENSION
    return file_name


def call_lib_cmd(cmd_name, *args, **kwargs):
    """
    Calls built-in Autohotkey with given script name from commands lib.

    :param str cmd_name: Name of the script to run.
    :rtype: str
    """
    import a2core
    a2 = a2core.A2Obj.inst()
    cmd_name = ensure_ahk_ext(cmd_name)
    cmd_path = os.path.join(a2.paths.lib, 'cmds', cmd_name)
    if not os.path.isfile(cmd_path):
        raise RuntimeError('Cannot find command script "%s" in lib!' % cmd_name)
    return call_cmd(cmd_path, cwd=a2.paths.a2, *args, **kwargs)


def call_cmd(cmd_path, *args, **kwargs):
    """
    Calls built-in Autohotkey with given script file + args returns result.

    :param str cmd_path: Path to the Autohotkey script file to run.
    :rtype: str
    """
    if not os.path.isfile(cmd_path):
        raise RuntimeError(
            'Cannot call command script! No such file!\n  %s' % cmd_path)

    import a2core
    a2 = a2core.A2Obj.inst()

    args = [a2.paths.autohotkey, cmd_path] + [str(a) for a in args]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=kwargs.get('cwd'))

    cmd_result = proc.communicate()[0]
    try:
        cmd_result = cmd_result.decode()
    except UnicodeDecodeError:
        cmd_result = cmd_result.decode('latin1')
    proc.kill()

    # cut away quote characters if any
    cmd_result = cmd_result.strip(' \'"')
    return cmd_result


def get_variables(ahk_file):
    """
    Parses an Autohotkey file to get root variables to Python.
    Ignores any indented ones.
    Returns a dict with the variables.
    """
    with codecs.open(ahk_file, encoding='utf-8-sig') as fobj:
        lines = [l.split('=', 1) for l in fobj.read().split('\n') if l]
    lines = [(l[0], l[1].strip('" \r')) for l in lines if len(l) == 2]
    result = {}
    for key, value in lines:
        _key = key.strip(': ')
        # skip lines with indentation
        if key[0] != _key[0]:
            continue
        key = _key
        result[key] = convert_string_to_type(value)
    return result


def set_variable(ahk_file, key, value):
    """
    Set a single root variable in an Autohotkey script file.

    Root variable means ignore scoped or indented entries.
    If wile does not exist: Create new file with entry.
    Otherwise raise KeyError if value was not found.
    """
    try:
        with open(ahk_file) as fobj:
            lines = [l for l in fobj.read().split('\n')]

        found = False
        write = False
        for i, line in enumerate(lines):
            parts = line.split('=', 1)
            if not len(parts) == 2:
                continue
            _key, _value = parts
            curkey = _key.strip(': ')
            # skip lines with indentation
            if curkey[0] != _key[0]:
                continue
            # skip if its not the key we're looking for
            if key != curkey:
                continue
            found = True
            curvalue = convert_string_to_type(_value.strip('" '))
            if curvalue != value:
                write = True
                write_line_nr = i
            break

        if not found:
            raise KeyError('There is no key "%s" to set in %s' % (key, ahk_file))

    except FileNotFoundError:
        lines = ['']
        write_line_nr = 0
        write = True

    if not write:
        return

    if isinstance(value, bool):
        lines[write_line_nr] = '%s := %s' % (key, value)
    else:
        lines[write_line_nr] = '%s := "%s"' % (key, value)

    with open(ahk_file, 'w') as file_obj:
        file_obj.write('\n'.join(lines))


def convert_string_to_type(string):
    """
    Find proper type for string input.

    Examples:
        '1' -> 1
        '2.3' -> 2.3
        'true' -> True
        'something' -> 'something'
    """
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            try:
                return _LOW_BOOLS[string.lower()]
            except KeyError:
                return string


def py_value_to_ahk_string(py_obj):
    if isinstance(py_obj, bool):
        return py_bool_to_ahk_string(py_obj)
    elif isinstance(py_obj, str):
        return py_string_to_ahk_string(py_obj)
    elif isinstance(py_obj, float):
        return py_float_to_ahk_string(py_obj)
    elif isinstance(py_obj, int):
        return py_int_to_ahk_string(py_obj)
    elif isinstance(py_obj, list):
        return py_list_to_ahk_string(py_obj)
    elif isinstance(py_obj, dict):
        return py_dict_to_ahk_string(py_obj)


def py_bool_to_ahk_string(py_bool):
    return str(py_bool).lower()


def py_string_to_ahk_string(py_str):
    py_str = py_str.replace('\n', '`n')
    return '"%s"' % py_str


def py_float_to_ahk_string(py_float, decimals=None):
    template = '%f'
    if decimals is not None:
        template = '%.' + str(decimals) + 'f'
    return (template % py_float).rstrip('0')


def py_int_to_ahk_string(py_int):
    return '%i' % py_int


def py_list_to_ahk_string(list_obj):
    result = '['
    for item in list_obj:
        result += py_value_to_ahk_string(item) + ', '

    if result.endswith(', '):
        result = result[:-2]
    return result + ']'


def py_dict_to_ahk_string(dict_obj):
    result = '{'
    for key, value in dict_obj.items():
        result += '"%s": ' % key + py_value_to_ahk_string(value) + ', '

    if result.endswith(', '):
        result = result[:-2]
    return result + '}'


# : http://www.autohotkey.com/docs/KeyList.htm
MODIFIERS = {'altgr': '<^>'}
for _key, _code in {'win': '#', 'shift': '+', 'alt': '!', 'ctrl': '^', 'control': '^'}.items():
    MODIFIERS[_key] = _code
    MODIFIERS['l' + _key] = '<' + _code
    MODIFIERS['r' + _key] = '>' + _code

MOUSE_KEYS = ['lbutton', 'rbutton', 'mbutton', 'xbutton1', 'xbutton2',
              'wheeldown', 'wheelup', 'wheelleft', 'wheelright']
NUMPAD_KEYS = ['numlock', 'numpadins', 'numpadend', 'numpadpgup', 'numpadpgdn',
               'numpaddown', 'numpadleft', 'numpadright', 'numpadclear', 'numpadhome',
               'numpadup', 'numpaddot', 'numpaddel', 'numpad0', 'numpad1', 'numpad2',
               'numpad3', 'numpad4', 'numpad5', 'numpad6', 'numpad7', 'numpad8',
               'numpad9', 'numpaddiv', 'numpadmult', 'numpadadd', 'numpadsub', 'numpadenter', ]
KEYS = (['capslock', 'space', 'tab', 'enter', 'return', 'escape', 'esc', 'backspace',
         'bs', 'scrolllock', 'delete', 'del', 'insert', 'ins', 'home', 'end',
         'pgup', 'pgdn', 'up', 'down', 'left', 'right',
         'browser_back', 'browser_forward', 'browser_refresh', 'browser_stop',
         'browser_search', 'browser_favorites', 'browser_home', 'volume_mute',
         'volume_down', 'volume_up', 'media_next', 'media_prev', 'media_stop',
         'media_play_pause', 'launch_mail', 'launch_media', 'launch_app1',
         'launch_app2', 'special', 'appskey', 'printscreen', 'ctrlbreak', 'pause',
         'break', 'help', 'sleep'] + MOUSE_KEYS + NUMPAD_KEYS +
        ['f%i' % _i for _i in range(1, 25)])


if __name__ == '__main__':
    import unittest
    import test.test_ahk
    unittest.main(test.test_ahk, verbosity=2)
