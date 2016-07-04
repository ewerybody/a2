'''
nfo about Autohotkey that we might use across the modules

Created on Aug 7, 2015

@author: eRiC
'''
import time
import logging
import subprocess
from os.path import join


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def translateHotkey(displayString):
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


def call_cmd(cmd_name, *args):
    if not cmd_name.endswith('.ahk'):
        cmd_name += '.ahk'

    import a2core
    a2 = a2core.A2Obj.inst()
    cmd_path = join(a2.paths.lib, 'cmds', cmd_name)
    args = [a2.paths.autohotkey, cmd_path] + [str(a) for a in args]
    proc = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)

#        ahkProcess = QtCore.QProcess()
#        ahkProcess.startDetached(self.a2.paths.autohotkey, [self.a2.paths.a2_script], self.a2.paths.a2)

    cmd_result = str(proc.communicate()[0])
    proc.kill()

    cmd_result = cmd_result.strip()
    quote_char = cmd_result[-1]
    # cut away first & last quote char
    cmd_result = cmd_result[cmd_result.find(quote_char) + 1:cmd_result.rfind(quote_char)]

    return cmd_result


def killA2process():
    """
    finds and kills Autohotkey processes that run a2.ahk.
    takes a moment. so start it in a thread!
    TODO: make sure restart happens after this finishes?

    there is also:
    ctypes.windll.kernel32.TerminateProcess(handle, 0)
    """
    t1 = time.time()
    wmicall = 'wmic process where name="Autohotkey.exe" get ProcessID,CommandLine'
    wmicout = subprocess.check_output(wmicall)
    wmicout = str(wmicout).split('\\r\\r\\n')
    for line in wmicout[1:-1]:
        if 'autohotkey.exe' in line.lower():
            cmd, pid = line.rsplit(maxsplit=1)
            if cmd.endswith('a2.ahk') or cmd.endswith('a2.ahk"'):
                taskkill_proc = subprocess.Popen('taskkill /f /pid %s' % pid, shell=True,
                                                 stdout=subprocess.DEVNULL)
                taskkill_proc.wait()
                taskkill_proc.kill()
    log.debug('killA2process took: %fs' % (time.time() - t1))


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
