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
A profile system that provides both a :class:`PySide.QtCore.QSettings` instance
for storing and retrieving settings values, as well as functions for
determining file locations between the profile directory and the application
root.
"""

###############################################################################
# Imports
###############################################################################

import os
import argparse
import sys

from PySide.QtCore import QCoreApplication, QSettings
from PySide.QtGui import QDesktopServices

try:
    import pkg_resources as pr
except ImportError:
    pr = None

###############################################################################
# Logging
###############################################################################

import logging

log = logging.getLogger("siding.profile")

###############################################################################
# Constants and Storage
###############################################################################

SOURCE_ANY = 0b111
SOURCE_PROFILE = 0b100
SOURCE_PKG_RESOURCES = 0b010
SOURCE_ROOT = 0b001

name = 'default'
settings = None
portable = False

package = None

profile_path = None
root_path = None
cache_path = None

###############################################################################
# Internal Functions
###############################################################################

def assert_profile():
    """ Raise an exception if a profile hasn't been loaded. """
    if settings is None:
        raise RuntimeError("A profile hasn't been loaded.")

##### Path Stuff ##############################################################

def ensure_paths():
    """ Ensure cache_path, profile_path, and root_path are set. """
    global cache_path
    global profile_path
    global root_path

    if not root_path:
        root_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    if not profile_path:
        # The profile path is a bit trickier than the root path, since it can
        # move depending on the portability flag.
        if portable:
            path = root_path
        else:
            path = os.path.abspath(get_data_path())

        # Add the Profiles/<profile> bit to the profile path, and ensure the
        # path actually exists.
        path = os.path.join(path, u'Profiles', name)
        if not os.path.exists(path):
            os.makedirs(path)

        profile_path = path

    if not cache_path:
        # The cache path is like the profile path, in that it varies based on
        # the portability flag.
        if portable:
            path = os.path.join(root_path, u'cache')
        else:
            path = QDesktopServices.storageLocation(
                QDesktopServices.CacheLocation)

        # Add the Profiles/<profile> bit to the cache path, and ensure the path
        # actually exists.
        path = os.path.join(path, u'Profiles', name)
        if not os.path.exists(path):
            os.makedirs(path)

        cache_path = path


def get_home():
    """ Returns the path to the user's home directory. """
    return QDesktopServices.storageLocation(QDesktopServices.HomeLocation)

def get_data_path():
    """
    Returns the path that application data should be stored in. This acts a bit
    special on Windows machines, using the APPDATA environment variable to
    ensure things go to AppData\Roaming and not AppData\Local.
    """
    if os.name == 'nt':
        qapp = QCoreApplication.instance()
        path = os.getenv('APPDATA')

        if qapp.organizationName():
            path = os.path.join(path, qapp.organizationName())

        if qapp.applicationName():
            path = os.path.join(path, qapp.applicationName())

        return path

    return QDesktopServices.storageLocation(QDesktopServices.DataLocation)

###############################################################################
# Settings Getters / Setters
###############################################################################

def contains(key):
    """
    Returns true if key exists in the loaded profile, or false if it does not.
    """
    assert_profile()
    return settings.contains(key)


def keys():
    """ Return a list of all the keys in the loaded profile. """
    assert_profile()
    return settings.allKeys()


def set(key, value):
    """
    Sets the value of key to value in the loaded profile. If the key already
    exists, the existing value is overwritten.
    """
    assert_profile()
    settings.setValue(key, value)


def get(key, default=None):
    """
    Returns the value of key in the loaded profile. If the key doesn't exist,
    the provided default will be returned.
    """
    assert_profile()
    return settings.value(key, default)


def remove(key):
    """ Delete the key from the loaded profile. """
    assert_profile()
    settings.remove(key)

###############################################################################
# Path Manipulation Functions
###############################################################################

def get_file(path, mode='rb', source=SOURCE_ANY):
    """
    Find and open the file at the given ``path``.

    This function first searches in the active profile's directory. If the
    file is not found there, and configuration is available, it attempts to use
    `pkg_resources <http://packages.python.org/distribute/pkg_resources.html>`_
    to locate the file, otherwise it will search the root directory.

    If a file cannot be found, return ``None``.
    
    **Note:** ``mode`` is not used when getting a file from ``pkg_resources``.
    """
    if os.path.isabs(path):
        if os.path.isfile(path):
            return open(path, mode)
        return None

    # Not an absolute path, so process it.
    ensure_paths()

    if source & SOURCE_PROFILE:
        p_path = os.path.join(profile_path, path)
        if os.path.isfile(p_path):
            return open(p_path, mode)

    if source & SOURCE_PKG_RESOURCES:
        if (package and pr and pr.resource_exists(package, path) and
                not pr.resource_isdir(package, path)):
            return pr.resource_stream(package, path)

    if source & SOURCE_ROOT:
        r_path = os.path.join(root_path, path)
        if os.path.isfile(r_path):
            return open(r_path, mode)


def get_source(path, only_files=False, source=SOURCE_ANY):
    """ Return the source that ``path`` is found in. """
    ensure_paths()
    
    if source & SOURCE_PROFILE:
        p_path = os.path.join(profile_path, path)
        if os.path.exists(p_path) and (not only_files or
                                       os.path.isfile(p_path)):
            return SOURCE_PROFILE
    
    if source & SOURCE_PKG_RESOURCES:
        if (package and pr and pr.resource_exists(package, path) and
                (not only_files or not pr.resource_isdir(package, path))):
            return SOURCE_PKG_RESOURCES
    
    if source & SOURCE_ROOT:
        r_path = os.path.join(root_path, path)
        if os.path.exists(r_path) and (not only_files or
                                       os.path.isfile(r_path)):
            return SOURCE_ROOT

    return 0


def get_filename(path, always=True, only_files=False, source=SOURCE_ANY):
    """
    Find the file at the given ``path`` and return the absolute path.

    If ``only_files`` is True, paths will be checked to ensure that they're
    not directories.

    This function first searches in the active profile's directory. If the
    file is not found there, and configuration is available, it attempts to use
    `pkg_resources <http://packages.python.org/distribute/pkg_resources.html>`_
    to locate the file, otherwise it will search the root directory.

    If a file cannot be found, and ``always`` is True, a path to a hypothetical
    file in the active profile's directory will be returned. If ``always`` is
    True and ``only_files`` is also True, and the path in the active profile's
    directory exists and is a directory, returns ``None``. Otherwise, if a file
    cannot be found, returns ``None``.

    **Note:** You should use this function as little as possible, as it may
    require a file to be temporarily written to a cache if the file is found
    with ``pkg_resources``.
    """
    if os.path.isabs(path):
        if only_files and os.path.isdir(path):
            return None
        if always or os.path.exists(path):
            return path

    # Not an absolute path, so process it.
    ensure_paths()

    p_path = os.path.abspath(os.path.join(profile_path, path))
    if source & SOURCE_PROFILE:
        if os.path.exists(p_path) and (not only_files or
                                      (only_files and os.path.isfile(p_path))):
            return p_path

    if source & SOURCE_PKG_RESOURCES:
        if (package and pr and pr.resource_exists(package, path) and
                (not only_files or (only_files and not pr.resource_isdir(
                    package, path)))):
            return pr.resource_filename(package, path)

    if source & SOURCE_ROOT:
        r_path = os.path.abspath(os.path.join(root_path, path))
        if os.path.exists(r_path) and (not only_files or
                                      (only_files and os.path.isfile(r_path))):
            return r_path

    if always and (not only_files or (only_files and not
            os.path.isdir(p_path))):
        return p_path


def join(*parts):
    """ Return a path built from parts, using / as separators. """
    path = os.path.join(*parts)
    if os.name == 'nt':
        path = path.replace('\\', '/')
    return path


def normpath(path):
    """ Return a normalized pathname, using / as separators. """
    path = os.path.normpath(path)
    if os.name == 'nt':
        path = path.replace('\\', '/')
    return path

def listdir(path, source=SOURCE_ANY):
    """
    Returns a list of entries at the given path.

    The list is built using the active profile's directory, ``pkg_resources``
    if available, and the application root directory.
    """
    if os.path.isabs(path):
        return os.listdir(path)

    # Not absolute, so process it.
    ensure_paths()
    output = []

    # Start with the profile.
    if source & SOURCE_PROFILE:
        p_path = os.path.join(profile_path, path)
        if os.path.isdir(p_path):
            for entry in os.listdir(p_path):
                output.append(entry)

    # Now, pkg_resources.
    if source & SOURCE_PKG_RESOURCES:
        if package and pr and pr.resource_isdir(package, path):
            for entry in pr.resource_listdir(package, path):
                if not entry in output:
                    output.append(entry)

    # Finally, root.
    if source & SOURCE_ROOT:
        r_path = os.path.join(root_path, path)
        if os.path.isdir(r_path):
            for entry in os.listdir(r_path):
                if not entry in output:
                    output.append(entry)

    return output


def exists(path, source=SOURCE_ANY):
    """ Returns True if the path exists, otherwise returns False. """
    if os.path.isabs(path):
        return os.path.exists(path)

    # Not absolute, so process it.
    ensure_paths()

    if source & SOURCE_PROFILE:
        if os.path.exists(os.path.join(profile_path, path)):
            return True

    if source & SOURCE_PKG_RESOURCES:
        if package and pr and pr.resource_exists(package, path):
            return True

    if source & SOURCE_ROOT:
        return os.path.exists(os.path.join(root_path, path))

    return False

def isdir(path, source=SOURCE_ANY):
    """ Returns True if the path is a directory, otherwise returns False. """
    if os.path.isabs(path):
        return os.path.isdir(path)

    # Not absolute, so process it.
    ensure_paths()

    if source & SOURCE_PROFILE:
        if os.path.isdir(os.path.join(profile_path, path)):
            return True

    if source & SOURCE_PKG_RESOURCES:
        if package and pr and pr.resource_isdir(package, path):
            return True

    if source & SOURCE_ROOT:
        return os.path.isdir(os.path.join(root_path, path))
    
    return False


def isfile(path, source=SOURCE_ANY):
    """ Returns True if the path is a file, otherwise returns False. """
    if os.path.isabs(path):
        return os.path.isfile(path)

    # Not absolute, so process it.
    ensure_paths()

    if source & SOURCE_PROFILE:
        if os.path.isfile(os.path.join(profile_path, path)):
            return True

    if source & SOURCE_PKG_RESOURCES:
        if (package and pr and pr.resource_exists(package, path) and not
                pr.resource_isdir(package, path)):
            return True

    if source & SOURCE_ROOT:
        return os.path.isfile(os.path.join(root_path, path))

    return False


def walk(top, topdown=True, onerror=None, followlinks=False,
         source=SOURCE_ANY):
    """
    Recursively walk a path, similarly to :func:`os.walk`, but returning a
    combined list of entries in the profile directory, ``pkg_resources``, and
    the application root directory.

    See :func:`os.walk` for more details.
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
        # If it's a link at profile_path or root_path, don't walk it.
        if (followlinks or
                not os.path.islink(os.path.join(profile_path, new_path)) or
                not os.path.islink(os.path.join(root_path, new_path))):
            for x in walk(new_path, topdown, onerror, followlinks, source):
                yield x
    if not topdown:
        yield top, dirs, nondirs

###############################################################################
# Initialization
###############################################################################

def initialize(args=None, **kwargs):
    """
    Initialize the profile system. You may use the following arguments to
    configure the profile system:

    =============  ============  ============
    Argument       Default       Description
    =============  ============  ============
    portable       ``False``     If True, the profile system will attempt to live entirely in the root path.
    profile        ``default``   The name of the profile to load.
    package                      If this is set, and ``pkg_resources`` is available, then attempt to find resources in this package or requirement.
    profile_path                 If this is set, load the profile from this path.
    root_path                    The application root directory. If not set, this will be calculated with ``os.path.abspath(os.path.dirname(sys.argv[0]))``.
    cache_path                   If this is set, this path will be used to cache data rather than a profile-specific path.
    =============  ============  ============

    In addition, you can provide a list of command line arguments to have
    siding load them automatically. Example::

        siding.profile.initialize(sys.argv[1:])

    The following command line arguments are supported:

    ===================  ============
    Argument             Description
    ===================  ============
    ``--portable``       If set, the profile system will attempt to live entirely in the ``root_path``.
    ``--profile``        The name of the profile to load.
    ``--profile-path``   If this is set, load the profile from this path.
    ``--root-path``      The application root directory.
    ``--cache-path``     If this is set, this path will be used to cache data rather than a profile-specific path.
    ``--package``        If this is set, and ``pkg_resources`` is available, then attempt to find resources in this package or requirement.
    ===================  ============
    """
    global name
    global portable
    global package
    global profile_path
    global root_path
    global cache_path
    global settings

    # Set the defaults now.
    portable = kwargs.get('portable', False)
    name = kwargs.get('profile', 'default')

    # And load the paths if we've got them.
    package = kwargs.get('package', package)
    root_path = kwargs.get('root_path', root_path)
    profile_path = kwargs.get('profile_path', profile_path)
    cache_path = kwargs.get('cache_path', cache_path)

    # Now, parse the options we've got.
    if args:
        if args is True:
            args = sys.argv[1:]

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--portable', action='store_true', default=None)
        parser.add_argument('--profile')
        parser.add_argument('--profile-path')
        parser.add_argument('--root-path')
        parser.add_argument('--cache-path')
        parser.add_argument('--package')

        options = parser.parse_known_args(args)[0]

        # Let's set stuff up then.
        if options.portable is not None:
            portable = options.portable

        if options.profile:
            name = options.profile

        if options.package:
            package = package

        if options.profile_path:
            profile_path = options.profile_path
            if not os.path.exists(profile_path):
                os.makedirs(profile_path)

        if options.root_path:
            root_path = options.root_path
            if not os.path.exists(root_path):
                parser.error("The specified root path doesn't exist.")

        if options.cache_path:
            cache_path = options.cache_path
            if not os.path.exists(cache_path):
                os.makedirs(cache_path)

    # Now, open the settings file with QSettings and we're done.
    ensure_paths()
    file = os.path.join(profile_path, u'settings.ini')
    settings = QSettings(file, QSettings.IniFormat)

    log.info(u'Using profile: %s (%s)' % (name, profile_path))
    log.debug(u'settings.ini contains %d keys across %d groups.' % (
        len(settings.allKeys()), len(settings.childGroups())))
