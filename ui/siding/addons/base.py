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
This module contains :class:`AddonInfo`, the most important class of the
add-on system.
"""

###############################################################################
# Imports
###############################################################################

import errno
import os

from collections import OrderedDict
from ConfigParser import SafeConfigParser

from siding import path, profile
from siding.addons.version import Version, VersionMatch

###############################################################################
# Action Decorator
###############################################################################

def action(text=None, icon=None, status_tip=None, tool_tip=None,
           whats_this=None, default=False, checkable=False, is_checked=None,
           is_enabled=None, is_visible=None):
    """
    This decorator marks a method of an :class:`AddonInfo` subclass as an
    action that should be exposed to the user interface. These actions are
    typically displayed either as a button on the add-on's list entry, or as
    entries of a context menu for the add-on.

    ===========  ============
    Argument     Description
    ===========  ============
    text         The text to display for the action. By default, this is set to the function name after underscores have been converted to spaces and it has been capitalized.
    icon         The icon, if any, to display for the action. See :meth:`PySide.QtGui.QAction.icon() <PySide.QtGui.PySide.QtGui.QAction.icon>`
    status_tip   The status tip for the action. See :meth:`PySide.QtGui.QAction.statusTip <PySide.QtGui.PySide.QtGui.QAction.statusTip>`
    tool_tip     The tool tip for the action. See :meth:`PySide.QtGui.QAction.toolTip  <PySide.QtGui.PySide.QtGui.QAction.toolTip>`
    whats_this   The 'What's This?' text for the action. See :meth:`PySide.QtGui.QAction.whatsThis  <PySide.QtGui.PySide.QtGui.QAction.whatsThis>`
    default      If this is True, this action will be made the default and, if an add-on is double clicked, will be executed.
    checkable    Whether or not the action's state can be toggled.
    is_checked   A function that returns True if the action should be in a checked state.
    is_enabled   A function that returns True if the action should be enabled.
    is_visible   A function that returns True if the action should be visible.
    ===========  ============

    If ``checkable`` is True, you'll have to set an additional function that
    the user interface can use to determine the status of the button. To
    simplify doing so, a decorator named ``is_checked`` is made available as a
    function of the decorated method. Example::

        class MyAddonInfo(AddonInfo):
            debugging = False
            _has_debugger = False

            @action(statusTip='Select this to enable extra logging.')
            def debug(self):
                self.debugging = not self.debugging

            @debug.is_checked
            def is_checked(self):
                # Determine if debug should be checked.
                return self.debugging

    The checked state will be updated after the action method returns, and it
    can be updated at any time by calling :func:`AddonInfo.update_ui` with the
    decorated method. Example::

        class MyAddonInfo(AddonInfo):
            debugging = False
            _has_debugger = False

            @action(statusTip='Select this to enable extra logging.')
            def debug(self):
                self.debugging = not self.debugging

            def some_other_method(self):
                self.update_ui(self.debug)

    Actions may be disabled on a per-add-on basis by defining an additional
    function that the user interface can use to determine the status of the
    button. To do this, an additional decorator named ``is_enabled`` is made
    available as a function of the decorated method. Example::

        class MyAddonInfo(AddonInfo):
            debugging = False
            _has_debugger = False

            @action(statusTip='Select this to enable extra logging.')
            def debug(self):
                self.debugging = not self.debugging

            @debug.is_enabled
            def is_enabled(self):
                # Determine if debug should be enabled.
                return self._has_debugger

    You may also set a function for determining if the action should be
    displayed at all. A decorator named ``is_visible`` is made available as a
    function of the decorated method for this purpose. Example::

        try:
            import some_debugger
            CAN_DEBUG = True
        except ImportError:
            CAN_DEBUG = False

        class MyAddonInfo(AddonInfo):
            debugging = False
            _has_debugger = False

            @action(statusTip='Select this to enable extra logging.')
            def debug(self):
                self.debugging = not self.debugging

            @debug.is_visible
            def is_visible(self):
                return CAN_DEBUG

    You can also set ``text``, ``icon``, ``status_tip``, ``tool_tip``, and
    ``whats_this`` at any time and update the user interface to display the
    new values with by calling :func:`AddonInfo.update_ui` with the decorated
    method. Example::

        class MyAddonInfo(AddonInfo):
            debugging = False
            _has_debugger = False

            @action(statusTip='Select this to enable extra logging.')
            def debug(self):
                self.debugging = not self.debugging

            def some_other_method(self):
                self.debug.icon = siding.style.icon('bug')
                self.update_ui(self.debug)
    """

    def decorator(func):
        # Public things we don't care about.
        func.text = text
        func.icon = icon
        func.status_tip = status_tip
        func.tool_tip = tool_tip
        func.whats_this = whats_this
        func.default = default

        # Private things that shouldn't change.
        func._is_action = True
        func._checkable = checkable
        func._is_checked = is_checked
        func._is_enabled = is_enabled
        func._is_visible = is_visible

        # Decorators.
        def d_is_checked(checker):
            func._is_checked = checker
            return checker
        d_is_checked.__name__ = 'is_checked'
        d_is_checked.__doc__ = (
            "Register a function with the action %s for determining whether "
            "or not the action is currently checked." % func.__name__
            )
        func.is_checked = d_is_checked

        def d_is_enabled(checker):
            func._is_enabled = checker
            return checker
        d_is_enabled.__name__ = 'is_enabled'
        d_is_enabled.__doc__ = (
            "Register a function with the action %s for determining whether "
            "or not the action should be enabled." % func.__name__
            )
        func.is_enabled = d_is_enabled

        def d_is_visible(checker):
            func._is_visible = checker
            return checker
        d_is_visible.__name__ = 'is_visible'
        d_is_visible.__doc__ = (
            "Register a function with the action %s for determining whether "
            "or not the action should be visible." % func.__name__
        )
        func.is_visible = d_is_visible

        # Return our function.
        return func

    return decorator

###############################################################################
# AddonInfo Class
###############################################################################

class AddonInfo(object):
    """
    This class stores all the information available about an add-on, and also
    defines actions that may be performed with the add-on. This class provides
    all the information and functionality required to display an add-on in the
    Add-on Manager. In addition, this class is in charge of loading add-on
    information from file.
    """

    CORE_VALUES = tuple()
    """
    A list of value keys that should be read from the Core section of the
    information file for this type of add-on. Items in this list should be
    names of attributes to be loaded and set to instances.

    If a list or tuple is used in the list of values, they should use the
    format ``(name, format)`` where ``format`` is a callable, such as a class,
    that accepts a single value and returns something. If ``format`` is a
    string, that string will be evaluated as necessary. The result should be
    a callable that can be used to format the value.
    """

    version = Version('1')
    file = None
    path = None
    path_source = None
    _type_name = None

    def __init__(self, name, filename, filedata=None, source=None):
        """
        Initialize the AddonInfo instance for an add-on with the provided name.
        If a filename is provided, store it and attempt to load information
        from that file.
        """

        # Initialize some structures.
        self._ui = []
        self.data = {'name': name}
        self.filedata = filedata
        if filedata:
            if 'name' in filedata:
                del filedata['name']

        self.requires = OrderedDict()
        self.needed_by = []

        # Now, store our information.
        self.name = name

        # Make sure our file exists.
        if not path.exists(filename, source=source):
            raise IOError(errno.ENOENT, 'No such file or directory: %r' %
                                        filename)

        # Store our path for later use.
        self.path_source = path.source(filename, source=source)
        self._path, self.file = os.path.split(filename)

        # Make a PathContext, then go ahead and load.
        self.path = path.PathContext(self._path, self.path_source)

        self.load_information()

    def __repr__(self):
        return '<%s(%r, version=%r)>' % (
            self.__class__.__name__,
            self.data['name'],
            str(self.version)
            )

    ##### Blacklisting ########################################################

    @property
    def is_blacklisted(self):
        """ Whether or not the add-on is blacklisted. """
        return bool(profile.get('siding/addons/blacklist/%s/%s' %
                                (self._type_name, self.name)))

    ##### User Interface Helpers ##############################################

    def _ui_add(self, widget):
        """ Keep a reference to the provided widget. """
        self._ui.append(widget)

    def _ui_remove(self, widget):
        """ Delete the provided widget from our list. """
        if widget in self._ui:
            self._ui.remove(widget)

    def update_ui(self, action=None):
        """
        Update the user interface for this add-on. If an action is provided,
        only update that action. Otherwise, update all actions.
        """
        if action:
            if not isinstance(action, basestring):
                action = action.__name__
            if (not hasattr(self, action) or
                    not getattr(getattr(self, action), '_is_action', False)):
                raise KeyError("%s instance has no action %r." % (
                                self.__class__.__name__, action))

        for ui in self._ui:
            ui.update_actions(action)

    ##### Loading #############################################################

    def load_information(self):
        """ Load the add-on's information from file. """
        parser = SafeConfigParser()
        with self.path.open(self.file) as file:
            parser.readfp(file, self.file)

        # Read the core information.
        if not parser.has_section('Core'):
            raise ValueError(
                "No Core section in the add-on information file for the "
                "add-on %r." % self.name
            )

        for key in self.CORE_VALUES + ('version',):
            if isinstance(key, (list, tuple)):
                key, key_type = key
                if isinstance(key_type, basestring):
                    key_type = eval(key_type)
            else:
                key_type = lambda thing: thing

            # If we don't have that key, and we have a default value, just
            # continue, otherwise raise a ValueError.
            if not parser.has_option('Core', key):
                if not hasattr(self, key):
                    raise ValueError(
                        "Core value %r not defined in the add-on "
                        "information file for the add-on %r." %
                            (key, self.name)
                    )
                continue

            # Load the value and set it as an attribute of self.
            setattr(self, key, key_type(parser.get('Core', key)))

        # Split the inheritance.
        if (hasattr(self, 'inherits') and self.inherits and
                isinstance(self.inherits, basestring)):
            self.inherits = [x.strip() for x in self.inherits.split(',')]

        # Now, read the requirements.
        if parser.has_section('Requires'):
            for key, value in parser.items('Requires'):
                name, match = VersionMatch.from_string(value)
                self.requires[name] = match

        # Finally, read the data section. This generally just contains a nice
        # description of the add-on.
        if parser.has_section('Data'):
            self.data.update(parser.items('Data'))

        if parser.has_section('Description'):
            self.data.update(parser.items('Description'))
