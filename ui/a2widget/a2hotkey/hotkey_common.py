"""
Common hotkey things.
"""

SEND_MODES = ('Send', 'SendRaw', 'SendInput', 'SendPlay', 'SendEvent')
MOD_KEYS = ('! - Alt', '^ - Control', '+ - Shift', '# - Win')
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
    'rshift': 'RShift',
}


class Vars:
    """Stub for these hotkey strings."""

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
    Return a verified keys list given a string or list of shortcut+keys.

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
            'Need string or list of strings!' % (str(in_keys), type(in_keys))
        )

    for i, keys in enumerate(keys_list):
        fixed = sort_modifiers(keys)
        if keys != fixed:
            keys_list[i] = fixed

    return keys_list


def get_parts_from_list(key_list):
    """
    Disassemble modifier and trigger keys and format them nicely.
    """
    trigger_key = key_list.pop(-1).strip()
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
            raise ValueError(
                'Some modifiers could not be identified!:\n  %s'
                % set(modifiers).difference(low_mods)
            )
        mod_string = '+'.join(new_mods)
        return mod_string, trigger_key

    return '', trigger_key


def get_sorted_parts(key_string):
    """
    From key string find proper formatted modifier string and trigger key tuple.
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
    """Put together modifier and trigger keys via + if needed."""
    if modifier_string:
        return modifier_string + '+' + trigger_key
    return trigger_key


def parent_modifier_string(modifier_string):
    """
    Gets the modifier string without the side variant l/r.

    As a hotkey like "LWin+Shift+J" would still collide with "Win+Shift+J".
    This turns a given string like 'LWin+Shift' to 'Win+Shift'.

    :param str modifier_string: Hotkey modifier string with Ls or Rs.
    :rtype: str
    """
    if not modifier_string:
        return []

    modifiers = modifier_string.split('+')
    for i, part in enumerate(modifiers):
        if part[0].lower() in 'lr':
            modifiers[i] = part[1:]
    return '+'.join(modifiers)


def strip_mode(code, modes):
    """Find and remove `mode` from a Hotkey code snippet.
    Return stripped code and found mode in tuple."""
    _code = code.lower()
    for mode in modes:
        _mode = mode.lower()
        if _code.startswith(f'{_mode} '):
            return code[len(mode) :].strip('" '), mode
        if _code.startswith(f'{_mode},'):
            return code[len(mode) + 1:].strip('" '), mode
    return code, modes[0]


if __name__ == '__main__':
    import unittest
    from a2widget.a2hotkey.test import test_common

    unittest.main(test_common, verbosity=2)
