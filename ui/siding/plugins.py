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
A plugin system does its best to make no assumptions about the structure of
your application while providing a simple, clean way to easily extend your
application.
"""

###############################################################################
# Imports
###############################################################################

import argparse
import collections
import ConfigParser
import functools
import imp
import inspect
import os
import sys

import PySide
from PySide.QtCore import QCoreApplication, QObject, Signal

from siding import profile
from siding.version import Version, VersionMatch

###############################################################################
# Logging
###############################################################################

import logging
log = logging.getLogger("siding.plugins")

###############################################################################
# Storage, Exceptions, and Other Stuff
###############################################################################

safe_mode = False
version = None

class VersionError(ValueError):
    """
    This exception class is used internally by the :class:`PluginManager` when
    there's a problem related to a plugin's version.
    """
    pass

class DependencyError(VersionError):
    """
    This exception class is used by the :class:`PluginManager` when there is an
    issue loading the dependencies for a plugin, or if those dependencies are
    not acceptable versions.
    """
    pass

if Version(PySide.__version__) < '1.0.6':
    # This is an annoying bug.
    def issignal(signal):
        """ Return True if signal is an instance of QtCore.Signal. """
        return (signal.__class__.__name__ == 'Signal' and
            hasattr(signal, 'emit') and hasattr(signal, 'connect') and
            hasattr(signal, 'disconnect'))
else:
    def issignal(signal):
        """ Return True if signal is an instance of QtCore.Signal. """
        return isinstance(signal, Signal)

###############################################################################
# Helper Functions
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
    if version:
        return version

    ver = QCoreApplication.instance().applicationVersion()
    if ver:
        return ver

    import __main__
    if hasattr(__main__, 'version'):
        return __main__.version
    elif hasattr(__main__, '__version__'):
        return __main__.__version__

    raise RuntimeError("Application version not set.")

def isblacklisted(name):
    """ Return True if the given name is blacklisted, otherwise False. """
    return bool(profile.get('siding/plugins/blacklist/%s' % name))

###############################################################################
# Plugin Interface
###############################################################################

class IPlugin(QObject):
    """
    The most basic plugin interface to be inherited. This class is a subclass
    of :class:`PySide.QtCore.QObject`, and interacts with the rest of the
    application via Slots and Signals.

    Simply define slots and signals in subclasses of IPlugin, and they will
    be automatically connected and disconnected when the plugin is enabled or
    disabled. As a simple example::

        from PySide.QtCore import Signal, Slot
        from siding.plugins import IPlugin

        class Communicate(IPlugin):
            speak = Signal(str)

            @Slot()
            def triggered(self):
                self.speak.emit('Hello, everybody!')

    """

    def __init__(self, manager, name):
        """ Perform minimal plugin initialization. """
        QObject.__init__(self)

        self.manager = manager
        self.name = name
        self._is_active = False

    ##### Plugin Information ##################################################

    @property
    def info(self):
        """ The :class:`PluginInfo` instance representing this plugin. """
        return self.manager._infos.get(self.name)

    ##### Plugin Activation ###################################################

    @property
    def is_active(self):
        """
        Whether or not the plugin is currently active.

        This property performs the brunt of the work involved in activating or
        deactivating a plugin by connecting and disconnecting all signals and
        slots when the plugin is activated or deactivated.
        
        However, manually setting this property outside of :func:`activate` or
        :func:`deactivate` is ill advised, as the plugin manager will not be
        made aware of the change in activation, and no checking will be
        performed to ensure that all of the plugins dependencies have already
        been activated, or that plugins dependant on this plugin have already
        been deactivated.
        """
        return self._is_active

    @is_active.setter
    def is_active(self, val):
        """ Enable or disable the plugin. """
        val = bool(val)
        if val == self._is_active:
            return
        self._is_active = val

        if val:
            # Connect slots and signals.
            for signame in self.manager._signals:
                slot = getattr(self, signame, None)
                if not slot or not hasattr(slot, '_slots'):
                    continue

                for signal in self.manager._signals[signame]:
                    signal.connect(slot)

            for signame in self.manager._slots:
                signal = getattr(self, signame, None)
                if not signal or not issignal(signal):
                    continue

                for slot in self.manager._slots[signame]:
                    signal.connect(slot)

        else:
            # Disconnect slots and signals.
            for signame in self.manager._signals:
                slot = getattr(self, signame, None)
                if not slot or not hasattr(slot, '_slots'):
                    continue

                for signal in self.manager._signals[signame]:
                    signal.disconnect(slot)

            for signame in self.manager._slots:
                signal = getattr(self, signame, None)
                if not signal or not issignal(signal):
                    continue

                for slot in self.manager._slots[signame]:
                    signal.disconnect(slot)

    ##### Public Methods ######################################################

    def activate(self):
        """
        Activate the plugin. By default, this merely sets :attr:`is_active` to
        True.
        """
        self.is_active = True

    def deactivate(self):
        """
        Deactivate the plugin. By default, this merely sets :attr:`is_active`
        to False.
        """
        self.is_active = False

###############################################################################
# PluginInfo Class
###############################################################################

class PluginInfo(object):
    """
    This class loads and stores information on a plugin for use by the plugin
    manager and in the Add-ons GUI.

    If you wish to customize the loading of plugin information beyond altering
    the file extension, you should create a subclass and override the
    :meth:`load` method.
    """

    def __init__(self, manager, name, path, file):
        """ Initialize the PluginInfo. """

        # Store those values.
        self.manager = manager
        self.name = name
        self.path = path
        self.file = file

        # Set a few defaults.
        self.module = None
        self.version = Version('1')

        self.description = {}
        self.requirements = collections.OrderedDict()
        self.required = []

        # Now, load.
        self.load()

    def __repr__(self):
        return '<PluginInfo("%s", version=%s)>' % (self.nice_name,self.version)

    def load(self):
        """ Load the plugin information from file. """
        parser = ConfigParser.SafeConfigParser()

        file = profile.get_file(profile.join(self.path, self.file))
        if not file:
            raise IOError("Can't read plugin information file: %s" %
                          profile.join(self.path, self.file))

        parser.readfp(file)
        file.close()

        if parser.has_section('Plugin'):
            # Read core information.
            pairs = dict(parser.items('Plugin'))
            self.name = pairs.get('name', self.name)
            self.module = pairs.get('module', self.module)
            self.version = Version(pairs.get('version', self.version))

        if parser.has_section('Requires'):
            # Read requirements.
            for key, value in parser.items('Requires'):
                name, match = VersionMatch.from_string(value)
                self.requirements[name] = match

        if parser.has_section('Description'):
            for key, value in parser.items('Description'):
                self.description[key] = value


    @property
    def is_loaded(self):
        """
        Whether or not the plugin this :class:`PluginInfo` instance represents
        is currently loaded.
        """
        return self.name in self.manager._plugins

    @property
    def is_active(self):
        """
        Whether or not the plugin this :class:`PluginInfo` instance represents
        is currently activated.
        """
        plug = self.plugin
        if plug and plug[1]:
            return plug[1][0].is_active
        return False

    @property
    def plugin(self):
        """
        The plugin this :class:`PluginInfo` instance represents, or, if the
        plugin isn't loaded, None.
        """
        return self.manager._plugins.get(self.name)

    @property
    def nice_name(self):
        """
        The formatted name from the description if it exists, or the basic
        name from the file name.
        """
        return self.description.get('name', self.name)

###############################################################################
# Plugin Manager Class
###############################################################################

class PluginManager(QObject):
    """
    This class handles the discovery, loading, and activation of plugins. It
    manages the connection of signals and slots between different plugins and
    the rest of the application, and it provides simple functions to enumerate
    and perform tasks on plugins.
    
    **Note:** An instance of this class is created automatically as
    ``siding.plugins.manager``, and should be sufficient for almost all uses
    of the PluginManager.
    """

    info_class = PluginInfo
    """ The class to use for loading and accessing plugin information. """

    update_class = None
    """ The class to use for finding and downloading plugin updates. """

    info_extension = 'plugin'
    """ The file extension of plugin information files. """

    def __init__(self):
        """ Initialize the PluginManager. """
        QObject.__init__(self)

        self.directories = []

        # Storage
        self._plugins = {}
        self._infos = {}

        # Signal and Slot Storage
        self._signals = {}
        self._slots = {}

    ##### Plugin Enumeration ##################################################

    def list_plugins(self, filter=None):
        """
        Return a list of the names of all the available plugins.

        If a ``filter`` is supplied, it should take one of four possible
        formats.

            1. A string containing the name of a single plugin to list.
               Example::

                    siding.plugins.manager.list_plugins('testplugin')

            2. A string containing the path to a directory of plugins. Note
               that this will only list plugins in that directory that have
               already had their information loaded with
               :func:`discover_plugins`. Example::

                    siding.plugins.manager.list_plugins('/path/to/plugins')

            3. A list containing multiple strings of either type. Example::

                    siding.plugins.manager.list_plugins([
                            'testplugin',
                            'anotherplugin',
                            '/path/to/plugins'
                            ])

            4. A callable that accepts a :class:`PluginInfo` instance and
               returns True if the plugin should be listed. Example::

                    def my_checker(info):
                        return info.description.get('Category') == 'General'

                    siding.plugins.manager.list_plugins(my_checker)

        """
        if not filter:
            return self._infos.keys()

        elif callable(filter):
            return (name for name in self._infos.iterkeys() if filter(name))

        elif isinstance(filter, basestring):
            filter = [filter]

        # Go through the list.
        out = []
        for key in filter:
            if key in self._infos:
                out.append(key)
            elif os.path.exists(key):
                key = os.path.abspath(key)
                for info in self._infos.itervalues():
                    if info.path.startswith(key):
                        out.append(info.name)
        return out

    def get_info(self, name):
        """ Return a :class:`PluginInfo` instance for the named plugin. """
        return self._infos[name]

    def get_plugin(self, name):
        """
        Return a tuple of ``(module, [list, of, plugin, classes])`` for the
        named plugin.
        """
        return self._plugins[name]

    ##### Plugin Discovery and Loading ########################################

    def discover_plugins(self, paths=None):
        """
        Walk through a list of directories and load the information for every
        plugin we encounter. If no ``paths`` are provided, the list of
        directories kept by the PluginManager will be used.

        The actual plugins themselves will *not* be loaded at this point.
        """
        log.debug('Starting plugin discovery.')
        count = len(self._infos.keys())

        # Make sure we've got some paths to use.
        if not paths:
            paths = self.directories

        # Iterate and walk our paths.
        for path in paths:
            if not profile.isdir(path):
                continue
            self._walk_for_plugins(path)

        # Log the number of plugins we found.
        count = len(self._infos.keys()) - count
        log.info('Discovered %d plugins.' % count)

    def _walk_for_plugins(self, path):
        """
        Walk through a directory, reading information on every plugin we run
        across.
        """
        ext = '.%s' % self.info_extension

        for root, dirs, files in profile.walk(path):
            log.debug('Searching in: %s' % root)
            for file in files:
                if not file.endswith(ext):
                    continue
                name = file[:-len(ext)]

                # If we already have information on this plugin, skip it.
                if name in self._infos:
                    continue

                # The only acceptable error from the constructor of a
                # PluginInfo class is an IOError.
                try:
                    info = self.info_class(self, name, root, file)
                except IOError:
                    log.exception("Error loading plugin information for: %s" %
                            file)
                    continue

                # Store the PluginInfo class and log a message.
                self._infos[info.name] = info
                log.debug('Discovered %r at: %s' % (info,
                                                    profile.join(root, file)))

    def load_plugins(self, filter=None, use_blacklist=True):
        """
        Load all the available plugins.

        If a ``filter`` is supplied, it is evaluated with :func:`list_plugins`.

        If ``use_blacklist`` is set to False, plugins will not be checked
        against the current profile's blacklist before being loaded.
        """
        log.debug('Starting plugin loading.')
        count = len(self._plugins.keys())

        # Start loading plugins.
        for name in self.list_plugins(filter):
            # Don't load plugins twice.
            if name in self._plugins:
                continue

            # Get the PluginInfo for this.
            info = self._infos.get(name)
            if not info:
                raise KeyError('Tried to load unknown plugin: %s' % name)

            # If this is blacklisted, and we care, skip it.
            if use_blacklist and isblacklisted(name):
                log.debug('Skipping blacklisted plugin: %s' % info.nice_name)
                continue

            # Try loading it now.
            try:
                self._load_plugin(name, use_blacklist)
            except DependencyError, err:
                log.error('Unable to load plugin: %s\n%s' %
                    (info.nice_name, err))
            except (ImportError, VersionError):
                log.exception('Unable to load plugin: %s' % info.nice_name)

        # Count up and log the number of loaded plugins.
        count = len(self._plugins.keys()) - count
        log.info('Loaded %d plugins.' % count)

    def _load_plugin(self, name, use_blacklist=True, _chain=tuple()):
        """ Load the plugin with the given name. """
        info = self._infos[name]

        # Walk the dependency tree.
        for dname, match in info.requirements.iteritems():
            # Check the name against the blacklist.
            if use_blacklist and isblacklisted(name):
                raise DependencyError("Dependency %r is blacklisted." % dname)

            # Get the version.
            if dname == "__app__":
                version = app_version()
            else:
                dinfo = self._infos.get(dname)
                version = dinfo.version if dinfo else None

            # Test the version.
            if not match.test(version):
                raise DependencyError("Unsatisfied dependency: %s %s" %
                                        (dname, match))

            # If the dependency is __app__, continue.
            if dname == "__app__":
                continue

            # Check for loops.
            new_chain = list(_chain)
            new_chain.append(info.name)
            if dname in new_chain:
                raise DependencyError("Dependency loop: %s" % ", ".join(
                                                                    new_chain))

            # Store reverse requirements.
            if not info.name in dinfo.required:
                dinfo.required.append(info.name)

            # Now, load the plugin.
            try:
                self._load_plugin(dname, use_blacklist, new_chain)
            except DependencyError, err:
                raise DependencyError("Unsatisfied dependency: %s %s\n%s" %
                                        (dname, match, err))
            except (ImportError, VersionError):
                log.exception("Unable to load plugin: %s" % dinfo.nice_name)
                raise DependencyError("Unsatisfied dependency: %s %s" %
                                        (dname, match))

        # Figure out what we're loading.
        modname = info.module if info.module else info.name

        # Now, try determining whether we're loading a single .py file, or an
        # actual module.
        file = None
        if profile.isfile(profile.join(info.path, modname, '__init__.py')):
            # We're doing a whole folder.
            path = profile.get_filename(profile.join(info.path, modname),
                                        False)
            try:
                file, pathname, description = imp.find_module(modname,
                                                    [os.path.join(path, '..')])
                module = imp.load_module(modname, file, pathname, description)
            finally:
                if file:
                    file.close()

        elif profile.isfile(profile.join(info.path, '%s.py' % modname)):
            # We're doing a single file.
            path = profile.join(info.path, '%s.py' % modname)
            file = profile.get_file(path)
            try:
                module = imp.load_module(modname, file, path,
                                         ('.py', 'rb', imp.PY_SOURCE))
            finally:
                if file:
                    file.close()

        else:
            raise ImportError('Unable to find module: %s' % modname)

        # We have our module. Store both it, and any IPlugins it made.
        plugs = []
        for key in dir(module):
            val = getattr(module, key)
            if inspect.isclass(val) and issubclass(val, IPlugin):
                try:
                    plugs.append(val(self, info.name))
                except Exception:
                    log.exception(
                        'Unable to instance plugin class %r for plugin: %s' %
                            (key, info.nice_name))
                    raise ImportError

        # Store it!
        log.info('Loaded plugin: %s' % info.nice_name)
        self._plugins[info.name] = module, plugs
        return module, plugs

    def activate_plugins(self, filter=None):
        """
        Activate all the available plugins.

        If a ``filter`` is supplied, it is evaluated with :func:`list_plugins`.
        """
        log.debug('Starting plugin activation.')

        # Start activating plugins.
        count, classes = 0, 0
        for name in self.list_plugins(filter):
            c_count, c_classes = self._activate_plugin(name)
            count += c_count
            classes += c_classes

        log.info('Activated %d plugins (across %d classes).' % (
            (count, classes)))

    def _activate_plugin(self, name, _chain=tuple()):
        """ Activate the plugin with the given name. """
        info = self._infos[name]
        module, plugins = self._plugins[name]

        # Count how many things we're activating.
        count, classes = 0, 0

        # Ensure all our dependencies are activated.
        for dname in info.requirements.iterkeys():
            if dname == '__app__':
                continue

            new_chain = list(_chain)
            new_chain.append(name)
            if dname in new_chain:
                continue

            c_count, c_classes = self._activate_plugin(dname, new_chain)
            count += c_count
            classes += c_classes

        activated = False
        for plug in plugins:
            if not plug.is_active:
                plug.activate()
                if plug.is_active:
                    activated = True
                    classes += 1

        if activated:
            count += 1
            log.info('Activated plugin: %s' % info.nice_name)

        return count, classes

    def deactivate_plugins(self, filter=None):
        """
        Deactivate all the currently active plugins.

        If a ``filter`` is supplied, it is evaluated with :func:`list_plugins`.
        """
        log.debug('Starting plugin deactivation.')

        # Start deactivating plugins.
        count, classes = 0, 0
        for name in self.list_plugins(filter):
            c_count, c_classes = self._deactivate_plugin(name)
            count += c_count
            classes += c_classes

        log.info('Deactivated %d plugins (across %d classes).' % (
            (count, classes)))

    def _deactivate_plugin(self, name, _chain=tuple()):
        """ Deactivate the plugin with the given name. """
        info = self._infos[name]
        module, plugins = self._plugins[name]

        # Count how many things we're deactivating.
        count, classes = 0, 0

        # Ensure anything depending on us is deactivated.
        for dname in info.required:
            new_chain = list(_chain)
            new_chain.append(name)
            if dname in new_chain:
                continue

            c_count, c_classes = self._deactivate_plugin(dname, new_chain)
            count += c_count
            classes += c_classes

        deactivated = False
        for plug in plugins:
            if plug.is_active:
                plug.deactivate()
                if not plug.is_active:
                    deactivated = True
                    classes += 1

        if deactivated:
            count += 1
            log.info('Deactivated plugin: %s' % info.nice_name)

        return count, classes

    def add_signal(self, name, signal):
        """
        Register a new signal with the plugin manager. All active plugins with
        slots matching the given name will be automatically connected to the
        signal.

        Additionally, this function returns a method that, when called, will
        remove the signal from the system.
        """
        log.debug("add_signal(%r, %r)" % (name, signal))

        if not name in self._signals:
            self._signals[name] = []

        # Build the remover.
        remover = functools.partial(self.remove_signal, name, signal)

        # If we already have it, just return now.
        if signal in self._signals[name]:
            return remover

        # Store the signal in the list.
        self._signals[name].append(signal)

        # Now, iterate through our plugins and connect the signal to every
        # plugin that's currently active.
        for module, plugins in self._plugins.itervalues():
            for plug in plugins:
                slot = getattr(plug, name, None)
                if not plug.is_active or not hasattr(slot, '_slots'):
                    continue
                signal.connect(slot)

        return remover

    def run_signal(self, name, *args):
        """
        Process a signal immediately with all active plugins with slots
        matching the given name. Any provided arguments will be sent along
        to those slots.
        """
        for module, plugins in self._plugins.itervalues():
            for plug in plugins:
                slot = getattr(plug, name, None)
                if not plug.is_active or not hasattr(slot, '_slots'):
                    continue
                try:
                    slot(*args)
                except Exception:
                    log.exception('Error running signal through plugin %r.' %
                            plug.name)

    def remove_signal(self, name, signal=None):
        """
        Remove a signal from the plugin manager and disconnect it from any
        plugins currently connected to it.

        If no ``signal`` is provided, *all* signals with the given name will be
        disconnected and removed from the plugin manager.
        """
        log.debug("remove_signal(%r, %r)" % (name, signal))

        if (not name in self._signals or
                (signal and not signal in self._signals[name])):
            return

        if signal:
            signals = [signal]
        else:
            signals = self._signals[name].values()

        for signal in signals:
            self._signals[name].remove(signal)
            for module, plugins in self._plugins.itervalues():
                for plug in plugins:
                    slot = getattr(plug, name, None)
                    if not plug.is_active or not hasattr(slot, '_slots'):
                        continue
                    signal.disconnect(slot)

    def add_slot(self, name, slot):
        """
        Register a new slot with the plugin manager. All active plugins with
        signals matching the given name will be automatically connected to
        the slot.

        Additionally, this function returns a method that, when called, will
        remove the slot from the system.
        """
        log.debug("add_slot(%r, %r)" % (name, slot))

        if not name in self._slots:
            self._slots[name] = []

        # Build the remover.
        remover = functools.partial(self.remove_slot, name, slot)

        if slot in self._slots[name]:
            return remover
        self._slots[name].append(slot)

        # Now, iterate through our plugins and connect the slot to every
        # plugin that's currently active.
        for module, plugins in self._plugins.itervalues():
            for plug in plugins:
                signal = getattr(plug, name, None)
                if not plug.is_active or not issignal(signal):
                    continue
                signal.connect(slot)

        return remover

    def remove_slot(self, name, slot=None):
        """
        Remove a slot from the plugin manager and disconnect it from any
        plugins currently connected to it.

        If no ``slot`` is provided, *all* slots with the given name will be
        disconnected and removed from the plugin manager.
        """
        log.debug("remove_slot(%r, %r)" % (name, slot))

        if (not name in self._slots or
                (slot and not slot in self._slots[name])):
            return

        if slot:
            slots = [slot]
        else:
            slots = self._slots[name].values()

        for slot in slots:
            self._slots[name].remove(slot)
            for module, plugins in self._plugins.itervalues():
                for plug in plugins:
                    signal = getattr(plug, name, None)
                    if not plug.is_active or not issignal(signal):
                        continue
                    signal.disconnect(slot)

manager = PluginManager()

get_info = manager.get_info
get_plugin = manager.get_plugin

list_plugins = manager.list_plugins
discover_plugins = manager.discover_plugins
load_plugins = manager.load_plugins

activate_plugins = manager.activate_plugins
deactivate_plugins = manager.deactivate_plugins

add_signal = manager.add_signal
remove_signal = manager.remove_signal
add_slot = manager.add_slot
remove_slot = manager.remove_slot

run_signal = manager.run_signal

###############################################################################
# Initialization
###############################################################################

def add_search_path(path, use_profile=False, add_to_start=True):
    """
    Add a new search path to the plugin manager. If ``use_profile`` is True,
    relative paths will be completed by the profile system. Otherwise, they
    will be evaluated based on the working directory when this function is
    called.
    """
    if not os.path.isabs(path):
        if not use_profile:
            path = os.path.abspath(path)

    if add_to_start:
        manager.directories.insert(0, path)
    else:
        manager.directories.append(path)


def initialize(args=None, **kwargs):
    """
    Initialize the plugin manager.

    ==========  =============  ============
    Argument    Default        Description
    ==========  =============  ============
    safe_mode   ``False``      When safe mode is enabled, plugins will be discovered, but they will not be automatically loaded or activated.
    discover    ``True``       If True, discover plugins automatically.
    load        ``True``       If True, load currently discovered plugins automatically.
    activate    ``True``       If True, enable currently loaded plugins automatically.
    paths       ``[]``         A list of paths to search for plugins.
    extension   ``'plugin'``   The file extension of plugin information files. These are just INI files with a unique name by default.
    version                    The application version. This, if set, is used by :func:`app_version`.
    ==========  =============  ============

    **Note**: If you want to keep the default search paths (those being  the
    ``'plugins/'`` subdirectories of both the profile path and the root path),
    use the method :func:`add_search_path` rather than the ``paths``
    argument.

    In addition, you can provide a list of command line arguments to have
    siding load them automatically. Example::

        siding.plugins.initialize(sys.argv[1:])

    The following command line arguments are supported:

    ==================  ============
    Argument            Description
    ==================  ============
    ``--safe-mode``     When safe mode is enabled, plugins will be discovered, but they will not be automatically loaded or activated.
    ``--plugin-path``   Add the given path to the plugin search paths. This may be used more than once. A value of ``-`` will clear the existing list.
    ==================  ============
    """
    global safe_mode
    global version

    # Load the values now.
    safe_mode = kwargs.get('safe_mode', safe_mode)
    version = kwargs.get('version', version)
    manager.info_extension = kwargs.get('extension', manager.info_extension)

    if kwargs.has_key('paths'):
        manager.directories = kwargs.get('paths')
    else:
        # Ensure the profile path and root path are in the directories.
        if not u'plugins' in manager.directories:
            manager.directories.append(u'plugins')

    # Now, parse the options we've got.
    if args:
        if args is True:
            args = sys.argv[1:]

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--safe-mode', action='store_true', default=None)
        parser.add_argument('--plugin-path', action='append')

        options = parser.parse_known_args(args)[0]

        # Do more stuff.
        if options.safe_mode is not None:
            safe_mode = options.safe_mode

        if options.plugin_path:
            for path in options.plugin_path:
                if path == '-':
                    del manager.directories[:]
                if path.startswith(':'):
                    path = path[1:]
                    if not profile.isdir(path):
                        parser.error("No such profile directory: %s" % path)
                else:
                    path = os.path.abspath(path)
                    if not os.path.isdir(path):
                        parser.error("No such directory: %s" % path)
                manager.directories.append(path)

    # Are we supposed to load the plugins?
    if kwargs.get('discover', True):
        manager.discover_plugins()

    if not safe_mode and kwargs.get('load', True):
        manager.load_plugins()

    if not safe_mode and kwargs.get('activate', True):
        manager.activate_plugins()
