import sys

_sout = None
_serr = None

def connect(write_func):
    """Connect to standard output."""
    global _sout
    if _sout is None:
        _sout = _OutputWrangler(sys.stdout)
        sys.stdout = _sout
    _sout.connect(write_func)


def connect_error(write_func):
    """Connect to standard error."""
    global _serr
    if _serr is None:
        _serr = _OutputWrangler(sys.stderr)
        sys.stderr = _serr
    _serr.connect(write_func)


class _OutputWrangler(object):
    def __init__(self, root):
        self._root = root
        self._write_funcs = [self._root.write]

    def write(self, msg):
        for write in self._write_funcs:
            write(msg)
    
    def connect(self, write_func):
        if write_func in self._write_funcs:
            return
        self._write_funcs.append(write_func)

    def disconnect(self, write_func):
        if write_func in self._write_funcs:
            self._write_funcs.remove(write_func)

    def __getattr__(self, attrname):
        """Handle any calls that might be thrown against a root output"""
        return getattr(self._root, attrname)


if __name__ == '__main__':
    bucket = ''
    def test(msg):
        global bucket
        bucket += msg
    connect(test)
    assert(bucket == '')
    print('something')
    assert(bucket != '')
