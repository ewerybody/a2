'''
New a2app backend hosting the actual a2ui window.
Makes sure its only wisible once through the 'siding' package
and enables sending messages to the main app instance.

Created on Aug 7, 2015

@author: eRiC
'''
import sys
import platform
from importlib import reload
from ctypes import windll
from PySide import QtGui
from siding import QSingleApplication
import a2ui
import logging


logging.basicConfig()
log = logging.getLogger('a2app')
log.setLevel(logging.DEBUG)


def app_msg_get(msg):
    global app, a2win
    if '--close' in msg:
        app.exit()
    elif '--show' in msg:
        a2win.showRaise()
    elif '--reload' in msg:
        log.info('attempting reload ...')
        a2win.close()
        reload(a2ui)
        for module in a2ui.a2PyModules:
            log.debug('reloading module: %s' % module.__name__)
            reload(module)
        for module in a2ui.a2ctrl.uiModules + a2ui.a2ctrl.reModules:
            log.debug('reloading module: %s' % module.__name__)
            reload(module)
        a2win = a2ui.A2Window(app=app)
        a2win.showRaise()
    else:
        log.info('received unhandled message: %s' % ' '.join(msg))


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
    if winfo:
        style = QtGui.QStyleFactory.create("Plastique")
        app.setStyle(style)
        # some palette playing around...
        #QtGui.QApplication.palette()
        #style.standardPalette()
        #originalPalette = QtGui.QApplication.palette()
        #QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
        #app.setPalette(QtGui.QApplication.palette())
        #app.setPalette(QtGui.QApplication.style().standardPalette())
    
    # this is to set the actual taskbar icon
    windll.shell32.SetCurrentProcessExplicitAppUserModelID('ewerybody.a2.0.1')
    a2win = a2ui.A2Window(app=app)
    a2win.show()
    app.messageReceived.connect(app_msg_get)
    exit(app.exec_())


if __name__ == '__main__':
    main()
