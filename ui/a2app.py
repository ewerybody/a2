"""
a2app — Qt application entry point.

Ensures only one instance runs at a time (Windows mutex + QLocalServer),
and enables sending messages to an already-running instance.
"""

import os
import sys
import json
import uuid
import struct
import logging
import platform
import traceback
import ctypes
import ctypes.wintypes
from ctypes import windll
from functools import partial

from PySide6 import QtWidgets, QtCore, QtNetwork


def main():
    """The main entrypoint for the whole thing."""
    try:
        import a2output

        a2output.get_logwriter()

        # Make sure the Qt platform plugin can be found.
        _qt_path = sys.modules[QtCore.Qt.__module__].__file__
        if _qt_path is not None:
            os.environ['QT_PLUGIN_PATH'] = os.path.abspath(
                os.path.join(_qt_path, '..', 'plugins')
            )

        # TODO: make a dedicated dark theme
        sys.argv.extend(('-platform', 'windows:darkmode=0'))

        app = A2App()
        app.exec()
    # Broad except is expected here!
    # pylint: disable=broad-except
    except Exception:
        error_msg = traceback.format_exc().strip()
        print(error_msg)
        this_dir = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(this_dir, '_ startup_error.log'), 'w') as file_obj:
            file_obj.write(error_msg)


ERROR_ALREADY_EXISTS = 0xB7


def _get_sid(pid: int) -> int:
    """Return the Windows session ID for the given process ID."""
    sid = ctypes.wintypes.DWORD()
    result = windll.kernel32.ProcessIdToSessionId(
        ctypes.wintypes.DWORD(pid), ctypes.byref(sid)
    )
    if not result:
        raise OSError(3, 'No such process')
    return sid.value


class QSingleApplication(QtWidgets.QApplication):
    """
    QApplication subclass that enforces a single running instance.
    A second launch sends a message to the first instance then exits.
    Windows-only (mutex-based locking via kernel32).
    """

    message_received = QtCore.Signal(list)

    session = None
    app_id = None

    _app_id = None
    _mutex = None
    _server = None
    _already = None

    def __init__(self, *args, **kwargs):
        if not args:
            args = (sys.argv,)
        QtWidgets.QApplication.__init__(self, *args, **kwargs)
        # Capture CloseHandle while globals are still alive (used in __del__).
        self._close_lock = self._close_mutex

    def __del__(self):
        self._close_mutex()
        self._close_server()

    @property
    def already_running(self):
        if self._already is None:
            self._acquire_lock()
        return self._already

    def ensure_single(self, message=None):
        """If another instance is running, send it a message and exit."""
        if self.already_running:
            if message is None:
                message = sys.argv[1:]
            if message:
                self.send_message(message)
            sys.exit()

    def _acquire_lock(self):
        if not self._app_id:
            self._build_app_id()
        result = self._create_mutex()
        if result:
            self._create_server()
        self._already = not result

    def _build_app_id(self):
        if self.app_id is None:
            path, binary = os.path.split(os.path.abspath(sys.argv[0]))
            self.app_id = 'q-single-app-%s-%s' % (binary, path)
        if self.session is None:
            try:
                sid = '%X' % _get_sid(os.getpid())
            except OSError:
                sid = os.getenv('USERNAME', '')
            self.session = sid
        self._app_id = str(uuid.uuid5(uuid.NAMESPACE_OID, self.app_id + self.session))

    def _close_mutex(self, CloseHandle=windll.kernel32.CloseHandle):
        if self._mutex:
            CloseHandle(self._mutex)
            self._mutex = None

    def _create_mutex(self):
        if self._app_id is None:
            return False
        mutex_name = ctypes.c_wchar_p(self._app_id[: ctypes.wintypes.MAX_PATH])
        handle = windll.kernel32.CreateMutexW(None, ctypes.c_bool(False), mutex_name)
        self._mutex = handle
        return not (not handle or ctypes.GetLastError() == ERROR_ALREADY_EXISTS)

    def _create_server(self, try_remove=True):
        if not self._server:
            self._server = QtNetwork.QLocalServer(self)
            self._server.newConnection.connect(self._new_connection)
        if self._server.isListening():
            return True
        assert self._app_id is not None
        if try_remove:
            QtNetwork.QLocalServer.removeServer(self._app_id)
        return self._server.listen(self._app_id)

    def _close_server(self):
        if self._server:
            try:
                if self._server.isListening():
                    self._server.close()
            except RuntimeError:
                pass
            self._server = None

    def _read_length(self, sock):
        if sock.bytesAvailable() < 4:
            return
        length = struct.unpack('!I', sock.read(4).data())[0]
        if not length:
            sock.close()
            return
        if sock.bytesAvailable() == length:
            self._read_message(sock, length)
        else:
            sock.readyRead.disconnect()
            sock.readyRead.connect(partial(self._read_message, sock, length))

    def _read_message(self, sock, length):
        if sock.bytesAvailable() < length:
            return
        message = json.loads(sock.readAll().data())
        sock.close()
        self.message_received.emit(message)

    def _new_connection(self):
        if self._server is None:
            return
        sock = self._server.nextPendingConnection()
        if not sock:
            return
        sock.readyRead.connect(partial(self._read_length, sock))

    def send_message(self, message, callback=None):
        """Send a message to the already-running instance."""
        assert self._app_id is not None
        encoded = json.dumps(message).encode()
        data = struct.pack('!I', len(encoded)) + encoded

        sock = QtNetwork.QLocalSocket(self)

        def on_error(*_args):
            if callback is not None:
                callback(False)

        def on_connected():
            sock.writeData(data, len(data))

        def on_bytes_written(*_args):
            if not sock.bytesToWrite() and callback is not None:
                sock.close()
                callback(True)

        if callback:
            sock.errorOccurred.connect(on_error)
            sock.connected.connect(on_connected)
            sock.bytesWritten.connect(on_bytes_written)

        sock.connectToServer(self._app_id)

        if not callback:
            if not sock.waitForConnected(5000):
                return False
            sock.writeData(data, len(data))
            while sock.bytesToWrite():
                if not sock.waitForBytesWritten(5000):
                    sock.close()
                    return False
            sock.close()
            return True


class A2App(QSingleApplication):
    """The a2 app foundation object."""

    def __init__(self):
        super().__init__(sys.argv)
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

        # adding PySide plugin paths. e.g. to make all the image formats available
        # pyside_plugin_path = os.path.join(QT_PATH, 'plugins')
        # self.addLibraryPath(pyside_plugin_path)

        self.info(
            f'initialized!\n  Python: {sys.version}\n  Windows: {str(platform.uname())[31:-1]}\n'
            f'  Qt: {QtCore.qVersion()}',
        )

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

            self._core = a2core.get()
            self._core.start_up()

            import a2ui

            self._win = a2ui.A2Window(self)
            self._core.win = self._win
            self._core.app = self
            self._core.win.show_raise()

        except Exception as error:
            title = 'a2app: Error on "init_a2_win()"!'
            msg = 'Could not call A2Window! Error:\n%s\nTraceback:%s' % (
                error,
                traceback.format_exc().strip(),
            )
            QtWidgets.QMessageBox.critical(
                None, title, msg + '\n\nPress Ctrl+C to copy this message.'
            )
            raise RuntimeError(msg)

    def app_msg_get(self, msg: str):
        """Handle received messages."""
        if '--close' in msg:
            self.exit()
        elif '--show' in msg:
            if self._win is None:
                return
            self.info('received show command ...')
            self._win.show_raise()
        elif '--reload' in msg:
            self.error('reload is deprecated!')
        else:
            self.error('received unhandled message: %s', ' '.join(msg))

    def info(self, *msg):
        """Log an info message."""
        self._log.info(*msg)

    def error(self, *msg):
        """Log an error message."""
        self._log.error(*msg)


if __name__ == '__main__':
    main()
