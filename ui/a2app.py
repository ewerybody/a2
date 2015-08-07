'''
New a2app backend hosting the actual a2ui window.
Makes sure its only wisible once through the 'siding' package
and enables sending messages to the main app instance.

Created on Aug 7, 2015

@author: eRiC
'''
import importlib
import sys

from siding import QSingleApplication
import a2ui

import logging
logging.basicConfig()
log = logging.getLogger('a2app')
log.setLevel(logging.DEBUG)

#global a2win

def app_msg_get(msg):
    global a2win
    if '--close' in msg:
        app.exit()
    elif '--show' in msg:
        a2win.showRaise()
    elif '--reload' in msg:
        log.info('attempting reload ...')
        a2win.close()
        importlib.reload(a2ui)
        for module in a2ui.a2PyModules:
            log.debug('reloading module: %s' % module.__name__)
            importlib.reload(module)
        for module in a2ui.a2ctrl.uiModules:
            log.debug('reloading module: %s' % module.__name__)
            importlib.reload(module)
        a2win = a2ui.A2Window(app=app)
        a2win.showRaise()
    else:
        log.info('received unhandled message: %s' % ' '.join(msg))


if __name__ == '__main__':
    app = QSingleApplication(sys.argv)
    # ensure_single will already exit() after sending the message
    if not sys.argv[1:]:
        #app.ensure_single(['--show'])
        app.ensure_single(['--reload'])
    else:
        app.ensure_single()

    log.info('initialised! (running on python %s)' % sys.version)
    #app.setStyle(QtGui.QStyleFactory.create("Plastique"))
    a2win = a2ui.A2Window(app=app)
    a2win.show()
    app.messageReceived.connect(app_msg_get)
    exit(app.exec_())
