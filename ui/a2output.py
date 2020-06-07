"""Catch standard and error outputs with custom functions."""
import sys

_SOUT = None
_SERR = None


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
        return getattr(self._root, attrname)


if __name__ == '__main__':
    import unittest
    import test.test_output
    unittest.main(test.test_output, verbosity=2)
