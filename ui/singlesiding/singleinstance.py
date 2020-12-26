"""
A cross-platform implementation of a :class:`PySide.QtWidgets.QApplication`
subclass with the ability to determine if it's the only running instance of
an application, and if not, send a message to the previous instance before
closing.
"""
import os
import sys
import json
import uuid
import struct
from functools import partial

try:
    from PySide6 import QtCore, QtWidgets, QtNetwork
except ImportError:
    from PySide2 import QtCore, QtWidgets, QtNetwork

if os.name == 'nt':
    import ctypes.wintypes
else:
    import errno
    import fcntl

ERROR_ALREADY_EXISTS = 0xB7
WM_DWMCOMPOSITIONCHANGED = 0x31E

# Session ID for Windows
if os.name == 'nt':

    def getsid(pid):
        """ Returns the session ID for the process with the given ID. """
        sid = ctypes.wintypes.DWORD()
        result = ctypes.windll.kernel32.ProcessIdToSessionId(
            ctypes.wintypes.DWORD(pid), ctypes.byref(sid)
        )
        if not result:
            raise OSError(3, 'No such process')
        return sid.value


else:
    getsid = os.getsid


class QSingleApplication(QtWidgets.QApplication):
    """
    This subclass of :class:`~.QtWidgets.QApplication` ensures that only a
    single instance of an application will be run simultaneously, and provides
    a mechanism for new instances to send commands to the previously existing
    instance before the new instance closes.

    When running on Windows, QSingleApplication also listens for the
    ``WM_DWMCOMPOSITIONCHANGED`` message to allow styles utilizing Aero Glass
    to properly enable or disable Aero Glass on widgets when composition is
    enabled or disabled on a system-wide level.

    The application ID used to verify that the application is not already
    running can be customized by setting the ``app_id`` and ``session``
    variables of the QSingleApplication instance to the desired strings before
    using :attr:`already_running` or calling :func:`ensure_single` or
    :func:`send_message`.

    .. note::

        ``app_id`` and ``session`` will undergo additional processing and be
        converted into a :func:`UUID <uuid.uuid5>` before being utilized. If
        you *really* wish to use your own string, set ``_app_id``.
    """

    message_received = QtCore.Signal([dict], [list], [bool], [int], [float])
    composition_changed = QtCore.Signal()

    # Public Variables
    session = None
    app_id = None

    # Lock State Variables
    _app_id = None
    _mutex = None
    _lockfile = None
    _server = None
    _already = None

    def __init__(self, *args, **kwargs):
        if not args:
            args = (sys.argv,)

        QtWidgets.QApplication.__init__(self, *args, **kwargs)

        # During shutdown, we can't rely on globals like os being still available.
        if os.name == 'nt':
            self._close_lock = self._close_mutex
        else:
            self._close_lock = self._close_lockfile

    def __del__(self):
        """
        Close the handle of our mutex if we have one, destroy any existing lock
        file, any gracefully close the QLocalServer.
        """

        self._close_lock()
        self._close_server()

    def winEventFilter(self, message):
        """
        Extend the built-in event filtering to handle the
        WM_DWMCOMPOSITIONCHANGED message on Windows.
        """
        if getattr(message, 'message', None) == WM_DWMCOMPOSITIONCHANGED:
            self.composition_changed.emit()
        return QtWidgets.QApplication.winEventFilter(self, message)

    @property
    def already_running(self):
        """ Whether or not the application is already running. """
        if self._already is None:
            # Attempt to acquire a lock.
            self._acquire_lock()

        return self._already

    def ensure_single(self, message=None):
        """
        Ensure that this is the only instance of the application running. If
        a previous instance is detected, send the provided message before
        raising a :class:`SystemExit` exception.

        If ``message`` is None, ``sys.argv[:1]`` will be used instead. Note
        that a false value *other* than None will result in no message being
        sent.
        """
        if self.already_running:
            if message is None:
                message = sys.argv[1:]
            if message:
                self.send_message(message)
            exit()

        # Still here? Keep being awesome.

    def _acquire_lock(self):
        """
        Depending on the OS, either create a lockfile or use Mutex to obtain
        a lock. Also start the socket server.
        """
        if not self._app_id:
            self._build_app_id()

        if os.name == 'nt':
            result = self._create_mutex()
        else:
            result = self._create_lockfile()

        if result:
            self._create_server()
        self._already = not result

    def _build_app_id(self):
        """
        Create a unique application ID if necessary.
        """
        if not self.app_id:
            path, binary = os.path.split(os.path.abspath(sys.argv[0]))

            # Build the first part of the app_id.
            self.app_id = 'qsingleapp-%s-%s' % (binary, path)

        # Now, get the session ID.
        if not self.session:
            if os.name == 'nt':
                try:
                    sid = '%X' % getsid(os.getpid())
                except OSError:
                    sid = os.getenv('USERNAME')
            else:
                sid = os.getenv('USER')

            self.session = sid

        self._app_id = str(uuid.uuid5(uuid.NAMESPACE_OID, self.app_id + self.session))

    def _close_mutex(self, CloseHandle=ctypes.windll.kernel32.CloseHandle):
        """
        If we have a mutex, try to close it.
        """
        if self._mutex:
            CloseHandle(self._mutex)
            self._mutex = None

    def _create_mutex(self):
        """
        Attempt to create a new mutex. Returns True if the mutex was acquired
        successfully, or False if the mutex is already in use.
        """
        mutex_name = ctypes.c_wchar_p(self._app_id[: ctypes.wintypes.MAX_PATH])
        handle = ctypes.windll.kernel32.CreateMutexW(None, ctypes.c_bool(False), mutex_name)
        self._mutex = handle

        return not (not handle or ctypes.GetLastError() == ERROR_ALREADY_EXISTS)

    def _close_lockfile(self, unlink=os.unlink, close=os.close):
        """
        If a lockfile exists, delete it.
        """
        if self._lockfile:
            unlink(self._lockfile)
            close(self._lockfd)
            self._lockfile = None
            self._lockfd = None

    def _create_lockfile(self):
        """
        Attempt to create a lockfile in the user's temporary directory. This is
        one of the few things that doesn't obey the path functions of profile.
        """
        lockfile = os.path.abspath(os.path.join(QtCore.QDir.tempPath(), u'%s.lock' % self._app_id))

        try:
            fd = os.open(lockfile, os.O_TRUNC | os.O_CREAT | os.O_RDWR)
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            os.write(fd, '%d\n' % os.getpid())

        except (OSError, IOError) as error:
            if error.errno in (errno.EACCES, errno.EAGAIN):
                return False
            raise

        # We've got it.
        self._lockfd = fd
        self._lockfile = lockfile
        return True

    def _create_server(self, try_remove=True):
        """
        Attempt to create a new local server and start listening.
        """
        if not self._server:
            self._server = QtNetwork.QLocalServer(self)
            self._server.newConnection.connect(self._new_connection)

        if self._server.isListening():
            return True

        # If desired, remove the old server file.
        if try_remove:
            QtNetwork.QLocalServer.removeServer(self._app_id)

        # Now, attempt to listen and return the success of that.
        return self._server.listen(self._app_id)

    def _close_server(self):
        """
        Close the local server.
        """
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

        # Read the length.
        length = struct.unpack('!I', sock.read(4).data())[0]

        # If we don't have a length, just end now.
        if not length:
            sock.close()
            return

        # Set the next reader.
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
        """
        Accept a connection and read the message from it.
        """
        sock = self._server.nextPendingConnection()
        if not sock:
            return

        sock.readyRead.connect(partial(self._read_length, sock))

    def send_message(self, message, callback=None):
        """
        Attempt to send a message to the previously running instance of the
        application. Returns True if the message is sent successfully, or False
        otherwise.

        Alternatively, if a callback is provided the function will return
        immediately and the boolean will be sent to the callback instead.
        """
        message = json.dumps(message)
        message = struct.pack('!I', len(message)).decode() + message

        # Create a socket.
        sock = QtNetwork.QLocalSocket(self)

        # Build our helper functions.
        def error(*_args):
            """ Return False to the callback. """
            callback(False)

        def connected():
            """ Send our message. """
            sock.writeData(message, len(message))

        def bytesWritten(*_args):
            """ If we've written everything, close and return True. """
            if not sock.bytesToWrite():
                sock.close()
                callback(True)

        if callback:
            sock.error.connect(error)
            sock.connect.connect(connected)
            sock.bytesWritten.connect(bytesWritten)

        # Now connect.
        sock.connectToServer(self._app_id)

        if not callback:
            # Do things synchronously.
            connected = sock.waitForConnected(5000)
            if not connected:
                return False

            # Write it.
            sock.writeData(message, len(message))

            # Wait until we've written everything.
            while sock.bytesToWrite():
                success = sock.waitForBytesWritten(5000)
                if not success:
                    sock.close()
                    return False

            sock.close()
            return True
