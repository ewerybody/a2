import time
import subprocess

import a2core


log = a2core.get_logger(__name__)


class HotkeyManager(object):
    def __init__(self):
        pass


def kill_a2_process():
    """
    finds and kills Autohotkey processes that run a2.ahk.
    takes a moment. so start it in a thread!
    TODO: make sure restart happens after this finishes?

    there is also:
    ctypes.windll.kernel32.TerminateProcess(handle, 0)
    """
    t1 = time.time()
    startup_nfo = subprocess.STARTUPINFO()
    startup_nfo.wShowWindow = subprocess.SW_HIDE
    startup_nfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    wmicall = 'wmic process where name="Autohotkey.exe" get ProcessID,CommandLine'
    wmicout = subprocess.check_output(wmicall, startupinfo=startup_nfo)
    wmicout = str(wmicout).split('\\r\\r\\n')
    for line in wmicout[1:-1]:
        if 'autohotkey.exe' in line.lower():
            cmd, pid = line.rsplit(maxsplit=1)
            if cmd.endswith('a2.ahk') or cmd.endswith('a2.ahk"'):
                taskkill_proc = subprocess.Popen('taskkill /f /pid %s' % pid, shell=True, startupinfo=startup_nfo)
                taskkill_proc.wait()
                taskkill_proc.kill()
    log.debug('killA2process took: %fs' % (time.time() - t1))
