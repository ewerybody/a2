"""
a2app backend hosting only the QApplication.
Tries makes sure it's only visible once through the 'singlesiding' package
and enables sending messages to the main app instance.
"""
import os
import sys
import logging
import platform
import traceback
from ctypes import windll

from PySide2 import QtWidgets
from singlesiding import QSingleApplication


class A2Main(QSingleApplication):
    """The a2 app foundation object."""
    def __init__(self):
        super(A2Main, self).__init__(sys.argv)
        # self._app = None
        self._core = None
        self._win = None

        logging.basicConfig()
        self._log = logging.getLogger('a2app')
        self._log.setLevel(logging.DEBUG)

        # ensure_single will already exit() after sending the message
        if not sys.argv[1:]:
            self.ensure_single(['--show'])
        else:
            self.ensure_single()

        self.message_received.connect(self.app_msg_get)
        self.lastWindowClosed.connect(self.last_window_closed)

        # adding PySide plugin paths. e.g. to make all the imageformats available
        pyside_plugin_path = os.path.join(sys.modules['PySide2'].__path__[0], 'plugins')
        self.addLibraryPath(pyside_plugin_path)

        winfo = platform.uname()
        self.info('initialised!\n  python: %s\n  windows: %s', sys.version, str(winfo)[31:-1])

        # this is to set the actual taskbar icon
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('ewerybody.a2.0.1')

        self.init_a2_win()

    def last_window_closed(self):
        """Handle last window deletion."""
        self.info('a2 lastWindowClosed!')
        self.exit()

    def init_a2_win(self):
        """Load main a2 submodules and instantiate them."""
        this_dir = os.path.abspath(os.path.dirname(__file__))
        if os.getcwd() != this_dir:
            self.info('Bending cwd to "%s"', this_dir)
            os.chdir(this_dir)

        try:
            import a2core
            self._core = a2core.A2Obj.inst()
            self._core.start_up()

            import a2ui
            self._win = a2ui.A2Window(self)
            self._core.win = self._win
            self._core.app = self
            self._core.win.show_raise()

        except Exception as error:
            # TODO: provide more detailed startup error report
            # error_class, error_msg, trace_back = sys.exc_info()
            title = 'a2app: Error on "init_a2_win()"!'
            msg = ('Could not call A2Window! Error:\n%s\n'
                   'Traceback:%s' % (error, traceback.format_exc().strip()))

            QtWidgets.QMessageBox.critical(
                None, title, msg + '\n\nPress Ctrl+C to copy this message.')
            raise RuntimeError(msg)

    def app_msg_get(self, msg):
        """
        Handle received messeges with.
        """
        if '--close' in msg:
            self.exit()

        elif '--show' in msg:
            self.info('received show command ...')
            self._win.show_raise()

        elif '--reload' in msg:
            self.error('reload is deprecated!')

        else:
            self.error('received unhandled message: %s', ' '.join(msg))

    def info(self, *msg):
        """Log an info message"""
        self._log.info(*msg)

    def error(self, *msg):
        """Log an error message"""
        self._log.error(*msg)


def main():
    """The main entrypoint for the whole thing."""
    try:
        import a2output
        a2output.get_logwriter()
        app = A2Main()
        app.exec_()
    # Broad except is expected here!
    # pylint: disable=broad-except
    except Exception:
        error_msg = traceback.format_exc().strip()
        print(error_msg)
        this_dir = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(this_dir, '_ startup_error.log'), 'w') as fobj:
            fobj.write(error_msg)


if __name__ == '__main__':
    main()
