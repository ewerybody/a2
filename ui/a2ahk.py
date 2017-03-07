"""
nfo about Autohotkey that we might use across the modules

Created on Aug 7, 2015

@author: eRiC
"""
import os
import codecs
import subprocess


def translate_hotkey(displayString):
    """
    Creates AHK readable string out of a human readable like:
    Win+Ctrl+M > #^m
    """
    tilde = ''
    if displayString.startswith('~'):
        tilde = '~'
        displayString = displayString[1:]
    parts = displayString.split('+')
    parts = [p.strip().lower() for p in parts]
    modifier = parts[:-1]
    ahkKey = tilde + ''.join([modifiers[m] for m in modifier]) + parts[-1]
    return ahkKey


def ensure_ahk_ext(filename):
    if not filename.lower().endswith('.ahk'):
        filename += '.ahk'
    return filename


def call_lib_cmd(cmd_name, *args):
    import a2core
    a2 = a2core.A2Obj.inst()
    cmd_name = ensure_ahk_ext(cmd_name)
    cmd_path = os.path.join(a2.paths.lib, 'cmds', cmd_name)
    return call_cmd(cmd_path, *args)


def call_cmd(cmd_path, *args, **kwargs):
    import a2core
    a2 = a2core.A2Obj.inst()

    args = [a2.paths.autohotkey, cmd_path] + [str(a) for a in args]
    if 'cwd' in kwargs:
        proc = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, cwd=kwargs['cwd'])
    else:
        proc = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)

    cmd_result = str(proc.communicate()[0])
    proc.kill()

    cmd_result = cmd_result.strip()
    quote_char = cmd_result[-1]
    # cut away first & last quote char
    cmd_result = cmd_result[cmd_result.find(quote_char) + 1:cmd_result.rfind(quote_char)]

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
        result[key] = _convert_string_to_type(value)
    return result


def set_variable(ahk_file, key, value):
    """
    Sets a single root variable in a Autohotkey script file.
    Raises ValueError if value was not found as root variable ie not indented.
    """
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
        curvalue = _convert_string_to_type(_value.strip('" '))
        if curvalue != value:
            write = True
            if isinstance(value, bool):
                lines[i] = '%s := %s' % (key, value)
            else:
                lines[i] = '%s = %s' % (key, value)
        break

    if not found:
        raise ValueError('There is no value "%s" to set in %s' % (key, ahk_file))

    if write:
        with open(ahk_file, 'w') as fobj:
            fobj.write('\n'.join(lines))


def _convert_string_to_type(string):
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except:
            lowstring = string.lower()
            if lowstring == 'true':
                return True
            elif lowstring == 'false':
                return False
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


def py_bool_to_ahk_string(py_bool):
    return str(py_bool).lower()


def py_string_to_ahk_string(py_str):
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


"""
http://www.autohotkey.com/docs/KeyList.htm
"""
modifiers = {'altgr': '<^>'}
for _key, _code in {'win': '#', 'shift': '+', 'alt': '!', 'ctrl': '^', 'control': '^'}.items():
    modifiers[_key] = _code
    modifiers['l' + _key] = '<' + _code
    modifiers['r' + _key] = '>' + _code


keys = (['lbutton', 'rbutton', 'mbutton', 'advanced', 'xbutton1', 'xbutton2', 'wheel',
         'wheeldown', 'wheelup', 'wheelleft', 'wheelright', 'capslock', 'space', 'tab',
         'enter', 'return', 'escape', 'esc', 'backspace', 'bs', 'scrolllock', 'delete',
         'del', 'insert', 'ins', 'home', 'end', 'pgup', 'pgdn', 'up', 'down', 'left',
         'right', 'numpad', 'numlock', 'numlock', 'numpad0', 'numpadins', 'numpad1',
         'numpadend', 'numpad2', 'numpaddown', 'numpad3', 'numpadpgdn', 'numpad4',
         'numpadleft', 'numpad5', 'numpadclear', 'numpad6', 'numpadright', 'numpad7',
         'numpadhome', 'numpad8', 'numpadup', 'numpad9', 'numpadpgup', 'numpaddot',
         'numpaddel', 'numpaddiv', 'numpaddiv', 'numpadmult', 'numpadmult', 'numpadadd',
         'numpadadd', 'numpadsub', 'numpadsub', 'numpadenter',
         'browser_back', 'browser_forward', 'browser_refresh', 'browser_stop',
         'browser_search', 'browser_favorites', 'browser_home', 'volume_mute',
         'volume_down', 'volume_up', 'media_next', 'media_prev', 'media_stop',
         'media_play_pause', 'launch_mail', 'launch_media', 'launch_app1',
         'launch_app2', 'special', 'appskey', 'printscreen', 'ctrlbreak', 'pause',
         'break', 'help', 'sleep'] +
        ['f%i' % _i for _i in range(1, 25)])
