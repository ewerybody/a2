# -*- coding: utf-8 -*-
"""
New a2app backend hosting the actual a2ui window.
Makes sure its only visible once through the 'singlesiding' package
and enables sending messages to the main app instance.
"""
import os
import sys
import logging
import platform
import traceback
from ctypes import windll

from singlesiding import QSingleApplication
from PySide2 import QtWidgets

logging.basicConfig()
log = logging.getLogger('a2app')
log.setLevel(logging.DEBUG)


app = None
a2win = None


def main():
    global app, a2win
    app = QSingleApplication(sys.argv)

    # ensure_single will already exit() after sending the message
    if not sys.argv[1:]:
        app.ensure_single(['--show'])
    else:
        app.ensure_single()
    app.message_received.connect(app_msg_get)
    app.lastWindowClosed.connect(last_window_closed)

    # adding PySide plugin paths. e.g. to make all the imageformats available
    pyside_plugin_path = os.path.join(sys.modules['PySide2'].__path__[0], 'plugins')
    app.addLibraryPath(pyside_plugin_path)

    winfo = platform.uname()
    log.info('initialised!\n  python: %s\n  windows: %s'
             % (sys.version, str(winfo)[31:-1]))

    # this is to set the actual taskbar icon
    windll.shell32.SetCurrentProcessExplicitAppUserModelID('ewerybody.a2.0.1')

    a2win = init_a2_win(app)
    app.exec_()


def last_window_closed():
    print('a2 lastWindowClosed!')
    app.exit()
    print('still here ...')


def init_a2_win(app):
    try:
        import a2core
        a2 = a2core.A2Obj.inst()
        # TODO: remove this:
        # a2core._dbCleanup()
        a2.start_up()

        import a2ui
        a2.win = a2ui.A2Window(app)
        a2.app = app
        a2.win.showRaise()

    except Exception as error:
        # TODO: provide more detailed startup error report
        # error_class, error_msg, trace_back = sys.exc_info()
        title = 'a2app: Error on "init_a2_win()"!'
        msg = ('Could not call A2Window! Error:\n%s\n'
               'Traceback:%s\n\nPress Ctrl+C to copy this message.'
               % (error, traceback.format_exc().strip()))
        QtWidgets.QMessageBox.critical(None, title, msg)
        raise RuntimeError(msg)
    return a2.win


def app_msg_get(msg):
    global app, a2win
    if '--close' in msg:
        app.exit()
    elif '--show' in msg:
        log.info('received show command ...')
        a2win.showRaise()
    elif '--reload' in msg:
        log.error('reload is deprecated!')

    else:
        log.info('received unhandled message: %s' % ' '.join(msg))


if __name__ == '__main__':
    main()
