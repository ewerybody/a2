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


def get_parts_from_list(key_list):
    """
    """
    trigger_key = key_list.pop(-1)
    modifiers = key_list

    # try to title-case the trigger_key:
    _title_cased = trigger_key.title()
    # to avoid malforming keys like german umlaut 's' to 'Ss'
    if len(_title_cased) == len(trigger_key):
        trigger_key = _title_cased

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
            mod_string = '+'.join(new_mods)
            return mod_string, trigger_key
    else:
        return '', trigger_key


def get_sorted_parts(key_string):
    """
    """
    key_list = key_string.lower().split('+')
    mod_string, trigger_key = get_parts_from_list(key_list)
    return mod_string, trigger_key


def sort_modifiers(key_string):
    """
    Returns a sorted comparable verified hotkey string.

    :param str key_string: String of a keyboard shortcut.
    :return: Cleaned up, sorted hotkey string.
    :rtype: str
    """
    modifier_string, trigger_key = get_sorted_parts(key_string)
    return build_string(modifier_string, trigger_key)


def build_string(modifier_string, trigger_key):
    if modifier_string:
        return modifier_string + '+' + trigger_key
    else:
        return trigger_key


def parent_modifier_string(modifier_string):
    """
    Gets the modifier string without the side variant l/r.

    A hotkey with the modifier LWin+J would collide with Win+J.
    """
    modifiers = modifier_string.split('+')
    for i, part in enumerate(modifiers):
        if part[0].lower() in 'lr':
            modifiers[i] = part[1:]
    return '+'.join(modifiers)


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
