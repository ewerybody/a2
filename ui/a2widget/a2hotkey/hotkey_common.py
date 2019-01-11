"""
Common hotkey things.
"""


DISPLAY_MODIFIERS = {
    'ctrl': 'Ctrl',
    'lctrl': 'LCtrl',
    'rctrl': 'RCtrl',
    'win': 'Win',
    'lwin': 'LWin',
    'rwin': 'RWin',
    'alt': 'Alt',
    'lalt': 'LAlt',
    'ralt': 'RAlt',
    'altgr': 'AltGr',
    'shift': 'Shift',
    'lshift': 'LShift',
    'rshift': 'RShift'
}


class Vars(object):
    key_change = 'keyChange'

    scope = 'scope'
    scope_mode = 'scopeMode'
    scope_change = 'scopeChange'

    function_mode = 'functionMode'
    function_code = 'functionCode'
    function_url = 'functionURL'
    function_send = 'functionSend'

    dialog_style_setting = 'hotkey_dialog_style'


def get_keys_list(in_keys):
    """
    Returns a verified keys list given a string or list of shortcut+keys.

    :param (str, list) in_keys: String or list of shortcut+keys.
    :rtype: list
    """
    keys_list = []
    if in_keys is None:
        keys_list.append('')
    elif isinstance(in_keys, str):
        keys_list.append(in_keys)
    elif isinstance(in_keys, list):
        keys_list.extend(in_keys)
    else:
        raise TypeError(
            'Wrong Value Type for A2Hotkey.key: "%s" (%s)\n'
            'Need string or list of strings!' %
            (str(in_keys), type(in_keys)))

    for i, keys in enumerate(keys_list):
        fixed = sort_modifiers(keys)
        if keys != fixed:
            keys_list[i] = fixed

    return keys_list


def sort_modifiers(key_string):
    """
    Returns a sorted comparable verified keys list given a string or list of shortcut+keys.

    :param str key_string: String of a keyboard shortcut.
    :rtype: list
    """
    modifiers = key_string.lower().split('+')
    trigger_key = modifiers.pop(-1).title()
    if modifiers:
        new_mods = []
        for low_name, disp_name in DISPLAY_MODIFIERS.items():
            if low_name in modifiers:
                new_mods.append(disp_name)
        if len(new_mods) != len(modifiers):
            low_mods = map(str.lower, new_mods)
            raise ValueError('Some modifiers could not be identified!:\n  %s' %
                             set(modifiers).difference(low_mods))
        else:
            return '+'.join(new_mods + [trigger_key])
    else:
        return trigger_key


if __name__ == '__main__':
    # testing these things ...
    for k in ['f', 'numpadleft', 'alt+CTRL+f3', 'lShift+Altgr+y',
              'win+lbutton', 'ctrl+VSJKDBk+4', '']:
        try:
            print(' in: %s\nout: %s\n' % (k, sort_modifiers(k)))
        except ValueError as error:
            print(error, '\n')

    key_list = 'shift+Alt+d'
    new_list = get_keys_list(key_list)
    print(new_list)
    print(new_list == get_keys_list(new_list))
