'''
nfo about Autohotkey that we might use across the modules

Created on Aug 7, 2015

@author: eRiC
'''


# http://www.autohotkey.com/docs/KeyList.htm
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
