'''
New a2app backend hosting the actual a2ui window.
Makes sure its only visible once through the 'siding' package
and enables sending messages to the main app instance.

Created on Aug 7, 2015

@author: eRiC
'''
import sys
import a2ui
import a2core
import logging
import platform
from ctypes import windll
from importlib import reload
from siding import QSingleApplication

logging.basicConfig()
log = logging.getLogger('a2app')
log.setLevel(logging.DEBUG)


def main():
    global app, a2win
    app = QSingleApplication(sys.argv)
    # ensure_single will already exit() after sending the message
    if not sys.argv[1:]:
        #app.ensure_single(['--show'])
        app.ensure_single(['--reload'])
    else:
        app.ensure_single()

    winfo = platform.uname()
    log.info('initialised!\n  python: %s\n  windows: %s' % (sys.version, str(winfo)[31:-1]))
    app.messageReceived.connect(app_msg_get)
    # this is to set the actual taskbar icon
    windll.shell32.SetCurrentProcessExplicitAppUserModelID('ewerybody.a2.0.1')

    a2win = init_a2_win(app)
    #TODO: remove this:
    a2core._dbCleanup()

    exit(app.exec_())


def init_a2_win(app):
    a2 = a2core.A2Obj.inst()
    a2.start_up()

    a2win = a2ui.A2Window(app=app)
    a2.win = a2win
    a2.app = app
    a2win.showRaise()
    return a2win


def app_msg_get(msg):
    global app, a2win
    if '--close' in msg:
        app.exit()
    elif '--show' in msg:
        a2win.showRaise()
    elif '--reload' in msg:
        log.info('attempting reload ...')
        a2win.close()
        reload(a2core)
        reload(a2ui)

        for main_mod in [a2core, a2ui, a2ui.a2ctrl]:
            for module in main_mod.reload_modules:
                log.debug('reloading module: %s' % module.__name__)
                reload(module)

        a2win = init_a2_win(app)

    else:
        log.info('received unhandled message: %s' % ' '.join(msg))


if __name__ == '__main__':
    main()
