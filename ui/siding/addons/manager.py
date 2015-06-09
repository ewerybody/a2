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
This module contains the core of the add-ons system. It handles discovery,
dependencies, keeping track of available add-ons, and querying the system to
get :class:`AddonInfo` instances.
"""

###############################################################################
# Imports
###############################################################################

import re

from PySide.QtCore import QCoreApplication

from siding.addons.base import AddonInfo
from siding import path

###############################################################################
# Log
###############################################################################

import logging
log = logging.getLogger('siding.addons')

###############################################################################
# Constants and Exceptions
###############################################################################

INFO_FILE_MATCH = re.compile(r"({.*?})")

class DependencyError(ValueError):
    """
    This exception is used by the :class:`AddonManager` when there's an issue
    with the dependencies for a plugin either being missing or being an invalid
    version.
    """
    pass

###############################################################################
# Internal Helper Functions
###############################################################################

def app_version():
    """
    Detect and return the application version for the running application. The
    following locations are searched, in this order, for a version string:

        1. ``siding.plugins.version``
        2. :func:`PySide.QtCore.QCoreApplication.applicationVersion`
        3. ``__main__.version``
        4. ``__main__.__version__``

    If the version is not found in one of those locations, a
    :class:`RuntimeError` will be raised.
    """
    ver = QCoreApplication.instance().applicationVersion()
    if ver:
        return ver

    import __main__
    if hasattr(__main__, 'version'):
        return __main__.version
    elif hasattr(__main__, '__version__'):
        return __main__.__version__

    raise RuntimeError("Application version not set.")

def parse_info_file(filename, type_name):
    """
    Build a regular expression from the provided filename pattern for matching
    when we're discovering add-ons.
    """
    if not '{name}' in filename.lower():
        raise ValueError("info_file must contain {name}")

    output = r""
    expect_var = None
    for part in INFO_FILE_MATCH.split(filename):
        if not part:
            continue
        if not part.startswith('{') or not part.endswith('}'):
            output += re.escape(part)
            expect_var = True
        elif part.lower() == '{type}':
            output += re.escape(type_name)
            expect_var = True
        else:
            if expect_var is None:
                output += r"/"
            elif not expect_var:
                raise ValueError("info_file cannot contain two variables back "
                                 "to back.")
            output += r"(?P<%s>.+?)" % re.escape(part[1:-1])
            expect_var = False

    output += r"$"
    return re.compile(output)

###############################################################################
# The Add-on Manager
###############################################################################

class AddonManager(object):
    """
    This class is in charge of the entire add-on system. It discovers add-ons,
    handles dependencies and inheritance, loads add-ons, stores references to
    all the loaded add-ons, and allows you to easily fetch an add-on's info
    instance if you know its type and name.
    """

    def __init__(self):
        super(AddonManager, self).__init__()

        # Set up the storage tables.
        self._addons = {}
        self._types = {}

    ##### Query Functions #####################################################

    def get(self, type, name):
        """
        Return the add-on of the given type and name. If there isn't one,
        KeyError is raised.
        """
        return self._addons[type][name]

    def find(self, type=None, filter=None):
        """
        Generate a list of all add-ons of the given type that match the
        filter. ``filter`` should be a callable that accepts :class:`AddonInfo`
        instances and returns True if the add-on should be included. Example::

            for x in siding.addons.find('plugin', lambda info: info.is_active):
                print 'The plugin %r is active.' % x
        """
        if isinstance(type, (tuple, list)):
            types = type
        else:
            types = [type] if type else self._types.keys()

        for type in types:
            for addon in self._addons[type].itervalues():
                if filter and not filter(addon):
                    continue
                yield addon

    ##### Add-on Registration #################################################

    def add_type(self, name, info_class, info_file="{name}.{type}",
                 search_paths=None, text=None, icon=None):
        """
        Register a new add-on type with the Add-on Manager.

        =============  ============
        Argument       Description
        =============  ============
        name           The name of the add-on type. This is for internal use and won't necessarily be used for the user interface.
        info_class     The :class:`AddonInfo` subclass to use for add-ons of this type.
        info_file      The information filename pattern to search for. See below for more information.
        search_paths   A list of paths to search for available add-ons of this type.
        text           The text to display for the add-on type in the user interface. If this isn't set, the name will have underscores converted to spaces and undergo capitalization for this string.
        icon           The icon, if any, to display for the add-on type. See :meth:`PySide.QtGui.QAction.icon() <PySide.QtGui.PySide.QtGui.QAction.icon>`
        =============  ============

        ``info_file`` is a somewhat special variable and entirely responsible
        for discovering what files are actually add-ons and should be loaded.
        By default, the value of info_file is ``"{name}.{type}"``. This
        pattern matches all files with an extension matching the registered
        type name. For example, if you register a type named ``"plugin"``, then
        the file ``"test.plugin"`` would match, resulting in an add-on called
        ``"test"``. ``{name}`` and ``{type}`` are the only special variables
        at this time.

        In addition, you may use paths separators in ``info_file``. As an
        example, siding's style system uses the value ``"{name}/style.ini"``
        to match style folders containing ``style.ini`` files.

        ``search_paths`` should be a list of relative paths for use with the
        path module. If not set, the default list has a single entry, that
        being the name of the type. So, a type called ``"plugins`` will
        automatically search in the ``plugins/`` folder.
        """
        if name in self._types:
            raise KeyError("There's already an add-on type named %r." % name)

        # Process info_file
        info_regex = parse_info_file(info_file, name)

        # Make sure we've got search paths.
        if not search_paths:
            search_paths = [name]

        # While we're at it, make sure we have an AddonInfo subclass.
        if not issubclass(info_class, AddonInfo):
            raise TypeError("info_class must be an AddonInfo subclass.")

        # Store it.
        self._types[name] = info_class, info_regex, search_paths, text, icon
        info_class._type_name = name

    ##### Add-on Discovery ####################################################

    def discover(self, type=None, source=None):
        """
        Discover any available add-ons in the known search paths. If ``type``
        is specified, only discover add-ons of that type or types. Returns a
        list of discovered add-ons.

        This is probably the most important single function of the Add-on
        Manager, as it must be called before you can access your add-ons.
        """
        if isinstance(type, (tuple, list)):
            types = type
        else:
            types = [type] if type else self._types.keys()

        output = []

        # Iterate over the type list, and walk for each type.
        for type in types:
            log.info('Discovering add-ons of type %r.' % type)
            if not type in self._addons:
                self._addons[type] = {}

            info_class, info_regex, search_paths = self._types[type][:3]
            for spath in search_paths:
                log.debug('Searching path: %s' % spath)
                for root, dirs, files in path.walk(spath, source=source):
                    for file in files:
                        filepath = path.join(root, file)
                        match = info_regex.search(filepath)
                        if not match:
                            continue

                        # If we've already got an add-on with this name, just
                        # continue.
                        name = match.group('name')
                        if name in self._addons[type]:
                            continue

                        # We've got an add-on. Build the info instance.
                        try:
                            addon = info_class(name, filepath,
                                            match.groupdict(), source=source)
                        except (IOError, ValueError):
                            log.exception(
                                'Problem loading add-on information for the '
                                'add-on %r (%r).' % (name, filepath))
                            continue

                        # Store it!
                        log.info('Found %s: %s' % (type, addon.data['name']))
                        self._addons[type][name] = addon
                        output.append(addon)

        log.info('Discovery finished.')
        return output

    ##### Dependency and Inheritance Checking #################################

    def check_dependencies(self, addon, _chain=tuple()):
        """
        Verify that the dependencies of the given addon are available and that
        their own dependencies are available, ensuring that it will be possible
        to load an addon, or any other action that requires dependencies.
        """
        type = getattr(addon, '_type_name', None)
        if not type in self._types:
            raise TypeError("Invalid add-on type %r." % addon.__class__)

        # Update the chain.
        new_chain = _chain + (addon.name,)

        # Iterate the requirements.
        for dname, match in addon.requires:
            if dname in new_chain:
                raise DependencyError('Dependency loop: %r' % new_chain)

            if dname == '__app__':
                version = app_version()
            else:
                d_type, _, name = dname.rpartition(':')
                if not d_type:
                    d_type = type
                if not d_type in self._types:
                    raise DependencyError(
                        'Invalid add-on type %r in dependency %r of add-on %r.'
                            % (d_type, dname, addon.data['name']))

                # Get the dependency.
                try:
                    dinfo = self.get(d_type, name)
                    if dinfo.is_blacklisted:
                        raise DependencyError(
                                'Dependency %r is blacklisted.' % dname)

                    # Walk the dependency tree.
                    self.check_dependencies(dinfo)
                    version = dinfo.version
                except KeyError:
                    version = None

            # Check the version.
            if not match.test(version):
                raise DependencyError(
                    'Unsatisfied dependency: %s %s' % (dname, match))

    def check_inheritance(self, addon, _chain=tuple()):
        """
        Verify that the inherited add-ons are available, and that there aren't
        any repeating inheritance chains. If there is an inheritance issue, and
        the add-on has an ``on_inheritance_issue`` function, it will be called
        to determine how to handle the issue. That function can raise its own
        exception or modify the add-on's inheritance list. If the function
        returns, the inheritance calculation will be restarted.
        """
        type = addon._type_name

        # Make sure we actually have something to inherit.
        if not getattr(addon, 'inherits', None):
            return

        # Update the chain.
        new_chain = _chain + (addon.name,)

        # Iterate the inheritance list.
        for name in addon.inherits:
            if name in new_chain:
                if hasattr(addon, 'on_inheritance_issue'):
                    addon.on_inheritance_issue()
                    return self.check_inheritance(addon, _chain)
                raise DependencyError('Inheritance loop: %r' % new_chain)
            
            try:
                new_one = self.get(type, name)
            except KeyError:
                if hasattr(addon, 'on_inheritance_issue'):
                    addon.on_inheritance_issue()
                    return self.check_inheritance(addon, _chain)
                raise DependencyError('Inheriting non-existent %s %r.' %
                                        (type, name))
            
            self.check_inheritance(new_one, new_chain)

# Now, instance the manager.
manager = AddonManager()