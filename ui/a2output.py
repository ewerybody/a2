"""Catch standard and error outputs with custom functions."""
import os
import sys
import time

_SOUT = None
_SERR = None
LOG_STD_NAME = 'a2.log'
LOG_ERR_NAME = 'a2_errors.log'


def connect(write_func):
    """Connect a function to standard output."""
    global _SOUT
    if _SOUT is None:
        _SOUT = _OutputWrangler(sys.stdout)
        sys.stdout = _SOUT
    _SOUT.connect(write_func)


def connect_error(write_func):
    """Connect a function to standard error."""
    global _SERR
    if _SERR is None:
        _SERR = _OutputWrangler(sys.stderr)
        sys.stderr = _SERR
    _SERR.connect(write_func)


class _OutputWrangler(object):
    """Mimic standard output object but connected to multiple target functions."""
    def __init__(self, root):
        self._root = root
        if self._root is None:
            self._write_funcs = []
        else:
            self._write_funcs = [self._root.write]

    def write(self, msg):
        """Write incoming message to all writer functions."""
        for writer in self._write_funcs:
            writer(msg)

    def connect(self, write_func):
        """Enlist another writer function to be triggered on write."""
        if write_func in self._write_funcs:
            return
        self._write_funcs.append(write_func)

    def disconnect(self, write_func):
        """Remove a writer function from our list."""
        if write_func in self._write_funcs:
            self._write_funcs.remove(write_func)

    def __getattr__(self, attrname):
        """Handle any calls that might be thrown against the root output."""
        if self._root is None:
            return self._pass
        return getattr(self._root, attrname)

    def _pass(self, *args):
        pass


class A2Logger(object):
    _instance = None

    @classmethod
    def inst(cls):
        """
        Return the singleton instance of A2Logger.

        :rtype: A2Obj
        """
        if A2Logger._instance is None:
            A2Logger._instance = A2Logger()
        return A2Logger._instance

    def __init__(self):
        if A2Logger._instance is not None:
            raise RuntimeError('Singleton A2Logger has already been initialized!\n'
                               '  Use A2Logger.inst() to get the instance!')

        self._data_path = None
        self._std_path = None
        self._err_path = None
        connect(self._write_std)
        connect_error(self._write_err)

    @staticmethod
    def _now():
        return round(time.time(), 2)

    def _write_msg(self, log_path, msg):
        if not msg.strip():
            return

        if not msg.endswith('\n'):
            msg += '\n'

        with open(log_path, 'a', encoding='utf8') as file_obj:
            file_obj.write(f'{self._now()} - {msg}')

    def _write_std(self, msg):
        self._write_msg(self.std_path, msg)

    def _write_err(self, msg):
        self._write_msg(self.err_path, msg)

    def set_data_path(self, data_path):
        """
        Route the logging to a given directory.
        """
        self._data_path = data_path
        self._std_path = os.path.join(self._data_path, LOG_STD_NAME)
        self._err_path = os.path.join(self._data_path, LOG_ERR_NAME)

    @property
    def data_path(self):
        """Path to the directory with log files."""
        if self._data_path is None:
            return os.path.join(os.getenv('LOCALAPPDATA'), 'a2', 'data')
        return self._data_path

    @property
    def std_path(self):
        """Path to the standard log file."""
        if self._std_path is None:
            return os.path.join(self.data_path, LOG_STD_NAME)
        return self._std_path

    @property
    def err_path(self):
        """Path to the error log file."""
        if self._err_path is None:
            return os.path.join(self.data_path, LOG_ERR_NAME)
        return self._err_path


def get_logger():
    """
    Return the singleton logger object.
    :rtype: A2Logger
    """
    return A2Logger.inst()


if __name__ == '__main__':
    import unittest
    import test.test_output
    unittest.main(test.test_output, verbosity=2)
