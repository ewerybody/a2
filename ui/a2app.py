# -*- coding: utf-8 -*-
"""
New a2app backend hosting the actual a2ui window.
Makes sure its only visible once through the 'siding' package
and enables sending messages to the main app instance.

Created on Aug 7, 2015

@author: eRiC
"""
import os
import sys
import logging
import platform
import traceback
from ctypes import windll
from importlib import reload

from siding import QSingleApplication
from PySide import QtGui

# first basicConfic. No need for more.
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
        # app.ensure_single(['--show'])
        app.ensure_single(['--show'])
    else:
        app.ensure_single()

    # adding PySide plugin paths. e.g. to make all the imageformats available
    pyside_plugin_path = os.path.join(sys.modules['PySide'].__path__[0], 'plugins')
    QtGui.QApplication.addLibraryPath(pyside_plugin_path)

    winfo = platform.uname()
    log.info('initialised!\n  python: %s\n  windows: %s' % (sys.version, str(winfo)[31:-1]))
    app.messageReceived.connect(app_msg_get)
    # this is to set the actual taskbar icon
    windll.shell32.SetCurrentProcessExplicitAppUserModelID('ewerybody.a2.0.1')

    a2win = init_a2_win(app)

    app.exec_()


def init_a2_win(app):
    global a2win
    try:
        import a2core
        a2 = a2core.A2Obj.inst()
        # TODO: remove this:
        a2core._dbCleanup()
        a2.start_up()

        import a2ui
        a2win = a2ui.A2Window(app=app)
        a2.win = a2win
        a2.app = app
        a2win.showRaise()
    except Exception as error:
        title = 'a2app: Error on "init_a2_win()"!'
        msg = ('Could not call A2Window! Error:\n%s\n'
               'Traceback:%s\n\nPress Ctrl+C to copy this message.'
               % (error, traceback.format_exc().strip()))
        from PySide import QtGui
        QtGui.QMessageBox.critical(None, title, msg)
        raise RuntimeError(msg)
    return a2win


def app_msg_get(msg):
    global app, a2win
    if '--close' in msg:
        app.exit()
    elif '--show' in msg:
        log.info('received show command ...')
        a2win.showRaise()
    elif '--reload' in msg:
        log.info('attempting reload ...')
        import a2ui
        import a2core
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
