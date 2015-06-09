###############################################################################
#
# Copyright 2012 Siding Developers (see AUTHORS.txt)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################
"""
A path manipulation module that remains aware of multiple file sources,
allowing an application to transparently load files from both a profile
specific location and the application root.

This module has support for the use of
`pkg_resources <http://packages.python.org/distribute/pkg_resources.html>`_,
though it doesn't require it.

Initialization of the path system is handled by the profile system, though it
isn't strictly necessary. You could use this module by itself as long as you
populate the sources list with :func:`add_source`.
"""

###############################################################################
# Imports
###############################################################################

import errno
import imp
import os
import sys
import types

try:
    import pkg_resources
    _Requirement = pkg_resources.Requirement
except ImportError:
    pkg_resources = None
    # Make a unique _Requirement so nothing will ever be an instance of it.
    class _Requirement(object):
        """ Don't use this. """
        pass

from PySide.QtCore import QCoreApplication
from PySide.QtGui import QDesktopServices

###############################################################################
# Settings
###############################################################################

_sources = []

###############################################################################
# Internal Helpers
###############################################################################

def assert_pkg_resources():
    """ Ensure that ``pkg_resources`` is available. """
    if not pkg_resources:
        raise ImportError('No module named pkg_resources')

def _is_frozen():
    """ Try to determine if the application is frozen. """
    return (
        hasattr(sys, 'frozen') or
        hasattr(sys, 'importers') or
        imp.is_frozen('__main__')
    )

###############################################################################
# Source Manipulation
###############################################################################

def add_source(source, add_to_start=False):
    """
    Add a new source to the path system. You can use this to add custom paths
    to the system, as well as ``pkg_resource`` packages and/or requirements.

    If you provide a string for ``source``, it will first be checked for a
    ``"py:`` prefix. If such a prefix exists, the string will be treated as a
    package for ``pkg_resource``. Otherwise, the string will be checked with
    :func:`os.path.exists` to determine if it's a valid location. If it *is*,
    it will be processed with :func:`os.path.abspath` and used as a normal
    folder. Otherwise, it will be assumed to be a package and we'll attempt to
    find it. It's recommended to prefix your packages with ``"py:"`` to prevent
    any chance of confusion.

    If you provide a module for ``source``, we'll use ``source.__name__`` to
    get its name and store that.

    If ``add_to_start`` is True, the source will be added to the beginning of
    the list rather than the end.

    .. note::
        If the profile system is in use, the profile specific path will
        *always* be at the beginning of the source list, regardless of the use
        of ``add_to_start``. If you absolutely must add a source to be checked
        before the profile path, modify ``siding.path._sources`` directly.
        Additionally, the root path, if set, will *always* be at the end of
        source list unless you modify the source list directly.
    """
    from siding import profile

    if profile.profile_path:
        if not profile.profile_path in _sources:
            _sources.insert(0, profile.profile_path)
        start_ind = _sources.index(profile.profile_path) + 1
    else:
        start_ind = 0

    if profile.root_path:
        if not profile.root_path in _sources:
            _sources.append(profile.root_path)
        end_ind = _sources.index(profile.root_path)
    else:
        end_ind = len(_sources)

    # If the source is already there, just return.
    if source in _sources:
        return

    if isinstance(source, basestring) and not source.startswith('py:'):
        if os.path.exists(source):
            source = os.path.abspath(source)
        else:
            file = None
            try:
                file, path, desc = imp.find_module(source)

                assert_pkg_resources()
                source = 'py:%s' % source

            except ImportError:
                raise IOError(errno.ENOENT,
                    'No such file or directory or package: %r' % source)
            finally:
                if file:
                    file.close()

    elif isinstance(source, types.ModuleType):
        assert_pkg_resources()
        source = 'py:%s' % source.__name__

    elif not isinstance(source, _Requirement):
        assert_pkg_resources()
        raise TypeError('source must be a string or pkg_resources.Requirement')

    if add_to_start:
        _sources.insert(start_ind, source)
    else:
        _sources.insert(end_ind, source)

###############################################################################
# Special Paths
###############################################################################

def appdata():
    """
    Return the path that application data should be stored in. This acts a bit
    special on Windows machines as Qt doesn't return the right path itself.
    """
    if os.name == 'nt':
        path = os.getenv('APPDATA')
        app = QCoreApplication.instance()
        if app:
            if app.organizationName():
                path = os.path.join(path, app.organizationName())
            if app.applicationName():
                path = os.path.join(path, app.applicationName())
        return path

    return QDesktopServices.storageLocation(QDesktopServices.DataLocation)

def cache():
    """ Return a path for writing temporary files. """
    return QDesktopServices.storageLocation(QDesktopServices.CacheLocation)

def home():
    """ Return the path to the user's home directory. """
    return QDesktopServices.storageLocation(QDesktopServices.HomeLocation)

def root():
    """ Return a guess of the application root. """
    if _is_frozen():
        # We're finding the executable.
        return os.path.abspath(os.path.dirname(unicode(sys.executable,
                                    sys.getfilesystemencoding())))

    # Not frozen, so get sys.argv[0]
    return os.path.abspath(os.path.dirname(sys.argv[0]))

###############################################################################
# Path Manipulation Functions
###############################################################################

def join(*parts):
    """
    Join two or more path components, using ``"/"`` as the path separator, even
    when running on Windows, to ensure compatibility with ``pkg_resources``.
    """
    path = os.path.join(*parts)
    if os.name == 'nt':
        path = path.replace('\\', '/')
    return path

def normpath(name):
    """
    Normalize path, and use ``"/"`` as the path separator, even when running on
    Windows, to ensure compatibility with ``pkg_resources``.
    """
    name = os.path.normpath(name)
    if os.name == 'nt':
        name = name.replace('\\', '/')
    return name

###############################################################################
# File Access Functions
###############################################################################

# Store the builtin open.
_open = open

def open(name, mode='rb', source=None):
    """
    Open a file, returning a file-like object. If the file cannot be opened,
    :class:`IOError` is raised. This function call works similarly to the
    built-in ``open``.

    When the file is opened in write-mode, and no source is specified, the
    file will be created in the first source that has the directory that the
    file exists in. If no such source exists, IOError is raised.

    .. warning::
        Files returned by ``pkg_resources`` are always read as ``rb``,
        regardless of the specified mode. Additionally, attempting to open a
        file from ``pkg_resources`` for writing will cause a ValueError to be
        raised. This only happens when the source has been set directly, and
        will not cause issue if a source using ``pkg_resources`` is in the
        list.
    """
    if os.path.isabs(name):
        return _open(name, mode)

    # Iterate through our sources until we can find it.
    if isinstance(source, (tuple, list)):
        sources = list(source)
        source = None
    else:
        sources = [source] if source else _sources

    for src in sources:
        # Are we dealing with a directory name?
        if isinstance(src, basestring) and not src.startswith('py:'):
            path = os.path.join(src, name)
            if os.path.exists(path):
                return _open(path, mode)
            elif (os.path.exists(os.path.dirname(path)) and
                    mode.startswith('w')):
                return _open(path, mode)
            continue

        # Must be a ``pkg_resources`` thing.
        assert_pkg_resources()
        if isinstance(src, basestring):
            src = src[3:]

        # Make sure we're not opening a resource file for write access.
        if mode[0] in 'wa' or '+' in mode:
            if not source:
                continue
            raise ValueError('pkg_resource sources are read only.')

        # If the resource doesn't exist, skip this source.
        if not pkg_resources.resource_exists(src, name):
            continue

        # If the resource is a directory, raise an IOError.
        if pkg_resources.resource_isdir(src, name):
            raise IOError(errno.EACCES, 'Cannot open directory: %r' % name)

        return pkg_resources.resource_stream(src, name)

    # Still here? Guess we didn't find it.
    if mode.startswith('a'):
        # We're dealing with append access, so iterate again, trying to open
        # such a file.
        for src in sources:
            # Not interested in pkg_resources now.
            if not isinstance(src, basestring) or src.startswith('py:'):
                continue

            path = os.path.join(src, name)
            if os.path.exists(os.path.dirname(path)):
                return _open(path, mode)

    # Still here? Guess we couldn't find what we're looking for.
    raise IOError(errno.ENOENT, 'No such file or directory: %r' % name)

def source(name, source=None):
    """
    Find the first source that contains the given path, and return it. If no
    source contains the path, return None. This is useful for locking something
    to a certain source, which you may want to do in certain situations, such
    as ensuring all of an add-ons files will be loaded from one and only one
    source.

    .. note::
        Python modules for use with ``pkg_resources`` are returned as strings
        prefixed with ``"py:"``. This happens internally to easily
        differentiate between Python modules and directories.
    """
    if os.path.isabs(name):
        return name

    # Iterate through the sources.
    if isinstance(source, (tuple, list)):
        sources = list(source)
    else:
        sources = [source] if source else _sources

    for src in sources:
        if isinstance(src, basestring) and not src.startswith('py:'):
            if os.path.exists(os.path.join(src, name)):
                return src
            continue

        # Must be a ``pkg_resources`` thing.
        assert_pkg_resources()
        _src = src
        if isinstance(_src, basestring):
            _src = _src[3:]

        if pkg_resources.resource_exists(_src, name):
            return src

def abspath(name, creating=False, source=None):
    """
    Find the given path and return the absolute path to that path. This is
    useful if you *have* to have a filename for an external library that can't
    make use of :func:`open`.

    If ``creating`` is True, the very first path will be returned. There is
    no guarantee that it exists. Additionally, any source using
    ``pkg_resources`` will be skipped automatically when ``creating`` is True
    as those sources are read only.

    If the path cannot be found, and ``creating`` is False, raise an IOError.
    """
    if os.path.isabs(name):
        return name

    # Iterate through our sources until we can find it.
    if isinstance(source, (tuple, list)):
        sources = list(source)
        source = None
    else:
        sources = [source] if source else _sources

    for src in sources:
        # Are we dealing with a directory name?
        if isinstance(src, basestring) and not src.startswith('py:'):
            path = os.path.join(src, name)
            if creating or os.path.exists(path):
                return path
            continue

        # Must be a ``pkg_resources`` thing.
        assert_pkg_resources()
        if isinstance(src, basestring):
            src = src[3:]

        # Make sure we're not opening a resource file for write access.
        if creating:
            if not source:
                continue
            raise ValueError('pkg_resource sources are read only.')

        # If the resource doesn't exist, skip this source.
        if not pkg_resources.resource_exists(src, name):
            continue

        # Extract the resource and return the path.
        return pkg_resources.resource_filename(src, name)

    # Still here? Guess we didn't find it.
    raise IOError(errno.ENOENT, 'No such file or directory: %r' % name)

###############################################################################
# Path Enumeration Functions
###############################################################################

def listdir(name, source=None):
    """ Generate the entries at a given path. """
    if os.path.isabs(name):
        for entry in os.listdir(name):
            yield entry
        return

    # Figure out what we're iterating.
    if isinstance(source, (tuple, list)):
        sources = list(source)
    else:
        sources = [source] if source else _sources

    # Now, build it.
    for src in sources:
        if isinstance(src, basestring) and not src.startswith('py:'):
            path = os.path.join(src, name)
            if not os.path.isdir(path):
                continue
            this_src = os.listdir(path)
        else:
            if isinstance(src, basestring) and src.startswith('py:'):
                src = src[3:]
            if not pkg_resources.resource_isdir(src, name):
                continue
            this_src = pkg_resources.resource_listdir(src, name)
        for entry in this_src:
            yield entry

def exists(name, source=None):
    """  Returns True if the path exists, False otherwise. """
    if os.path.isabs(name):
        return os.path.exists(name)

    # Iterate to find the path.
    if isinstance(source, (tuple, list)):
        sources = list(source)
    else:
        sources = [source] if source else _sources

    for src in sources:
        if isinstance(src, basestring) and not src.startswith('py:'):
            if os.path.exists(os.path.join(src, name)):
                return True
            continue

        # Must be a ``pkg_resources`` thing.
        assert_pkg_resources()
        if isinstance(src, basestring):
            src = src[3:]

        # Does it exist?
        if pkg_resources.resource_exists(src, name):
            return True

    return False

def isdir(name, source=None):
    """ Return True if the path is a directory, False otherwise. """
    if os.path.isabs(name):
        return os.path.isdir(name)

    # Iterate to find the path.
    if isinstance(source, (tuple, list)):
        sources = list(source)
    else:
        sources = [source] if source else _sources

    for src in sources:
        if isinstance(src, basestring) and not src.startswith('py:'):
            if os.path.isdir(os.path.join(src, name)):
                return True
            continue

        # Must be a ``pkg_resources`` thing.
        assert_pkg_resources()
        if isinstance(src, basestring):
            src = src[3:]

        # Is it a directory?
        if pkg_resources.resource_isdir(src, name):
            return True

    return False

def isfile(name, source=None):
    """ Return True if the path is a file, False otherwise. """
    if os.path.isabs(name):
        return os.path.isfile(name)

    # Iterate to find the path.
    if isinstance(source, (tuple, list)):
        sources = list(source)
    else:
        sources = [source] if source else _sources

    for src in sources:
        if isinstance(src, basestring) and not src.startswith('py:'):
            if os.path.isfile(os.path.join(src, name)):
                return True
            continue

        # Must be a ``pkg_resources`` thing.
        assert_pkg_resources()
        if isinstance(src, basestring):
            src = src[3:]

        # Is it a file?
        if pkg_resources.resource_exists(src, name) and not \
                pkg_resources.resource_isdir(src, name):
            return True

    return False

def islink(name, source):
    """
    Return True if the path is a link, False otherwise. This only works on
    specific sources.
    """
    if not isinstance(source, basestring) or source.startswith('py:'):
        return False
    return os.path.islink(join(source, name))

def walk(top, topdown=True, onerror=None, followlinks=False, source=None):
    """
    Recursively walk a path, similarly to :func:`os.walk`, but returning a
    combined list of entries in all the available sources, or the given
    source.

    .. seealso:: :func:`os.walk`
    """
    try:
        names = listdir(top, source)
    except OSError, err:
        if onerror is not None:
            onerror(err)
        return

    dirs, nondirs = [], []
    for name in names:
        entry = join(top, name)
        if isdir(entry, source):
            dirs.append(name)
        if isfile(entry, source) or not isdir(entry, source):
            nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs

    for name in dirs:
        new_path = join(top, name)
        new_source = source

        if not followlinks:
            new_source = source[:] if source else _sources[:]
            new_source = [src for src in new_source if not islink(name, src)]
            if not new_source:
                continue

        # Walk it.
        for x in walk(new_path, topdown, onerror, followlinks, new_source):
            yield x

    if not topdown:
        yield top, dirs, nondirs

###############################################################################
# PathContext Class
###############################################################################

class PathContext(object):
    """
    The path context class is a special class that makes it easy to perform
    multiple path commands working with a preset source. This is useful so that
    add-ons can only locate and open files in the source the add-on information
    files was found in.

    Every path manipulation function available in ``siding.path`` is available
    with a PathContext.
    """

    def __init__(self, path, source):
        super(PathContext, self).__init__()
        self.path = path
        self._source = source

    def add_source(self, source, add_to_start=False):
        """ Add the given source to the PathContext's internal source list. """
        if source in _sources:
            return

        # Make sure _source is a list.
        if isinstance(self._source, (tuple, list)):
            self._source = list(self._source)
        else:
            self._source = [self._source] if self._source else []

        # Determine what indices to use.
        start_ind = 0
        end_ind = len(self._source)

        from siding import profile
        if profile.profile_path in self._source:
            start_ind = self._source.index(profile.profile_path) + 1
        if profile.root_path in self._source:
            end_ind = self._source.index(profile.root_path)

        # Sanitize our input.
        if isinstance(source, basestring) and not source.startswith('py:'):
            if os.path.exists(source):
                source = os.path.abspath(source)
            else:
                file = None
                try:
                    file, path, desc = imp.find_module(source)

                    assert_pkg_resources()
                    source = 'py:%s' % source

                except ImportError:
                    raise IOError(errno.ENOENT,
                        'No such file or directory or package: %r' % source)
                finally:
                    if file:
                        file.close()

        elif isinstance(source, types.ModuleType):
            assert_pkg_resources()
            source = 'py:%s' % source.__name__

        elif not isinstance(source, _Requirement):
            assert_pkg_resources()
            raise TypeError('source must be a string or '
                            'pkg_resources.Requirement')

        # Now, add it.
        if add_to_start:
            self._source.insert(start_ind, source)
        else:
            self._source.insert(end_ind, source)

    @staticmethod
    def join(*parts):
        return join(*parts)

    @staticmethod
    def normpath(name):
        return normpath(name)

    def open(self, name, mode='rb'):
        if os.path.isabs(name):
            return open(name, mode)
        return open(join(self.path, name), mode, source=self._source)

    def source(self, name):
        if os.path.isabs(name):
            return name
        return source(name, source=self._source)

    def abspath(self, name, creating=False):
        if os.path.isabs(name):
            return name
        return abspath(join(self.path, name), creating, source=self._source)

    def listdir(self, name):
        if not os.path.isabs(name):
            name = join(self.path, name)
        return listdir(name, source=self._source)

    def exists(self, name):
        if os.path.isabs(name):
            return os.path.exists(name)
        return exists(join(self.path, name), source=self._source)

    def isdir(self, name):
        if os.path.isabs(name):
            return os.path.isdir(name)
        return isdir(join(self.path, name), source=self._source)

    def isfile(self, name):
        if os.path.isabs(name):
            return os.path.isfile(name)
        return isfile(join(self.path, name), source=self._source)

    def islink(self, name):
        if os.path.isabs(name):
            return os.path.islink(name)
        return islink(join(self.path, name), self._source)

    def walk(self,top, topdown=True, onerror=None, followlinks=False):
        if not os.path.isabs(top):
            top = join(self.path, top)
        return walk(top, topdown, onerror, followlinks, source=self._source)
