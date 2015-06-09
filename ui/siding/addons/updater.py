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
A basic interface for a class to allow add-ons to be updated automatically and
entirely within the application.
"""

###############################################################################
# Imports
###############################################################################

from PySide.QtCore import QObject, Signal

from siding.addons.base import AddonInfo

###############################################################################
# IUpdater Class
###############################################################################

class IUpdater(QObject):
    """
    This class is in charge of checking for add-on updates and, when updates
    are found, downloading and installing them to a location provided by the
    Add-on Manager.

    This class *must* be subclassed and installed into the Add-on Manager for
    the built-in update system to function properly.

    A basic :class:`HTTPUpdater` subclass has been provided that should suit
    very basic needs, and serve as an example of how to properly subclass this
    class.
    """

    ##### Signals #############################################################

    update_progress = Signal((AddonInfo, int, str), (AddonInfo, int))
    """
    This signal is emitted whenever progress is made, either checking for
    updates for an add-on or downloading and installing those updates. It's
    used by user interfaces to show progress to the end user.

    The arguments to this signal are
    ``(addon_info, percent_complete, message)``. If there is no message, that
    argument may be omitted.

    The Add-on Manager itself doesn't care about progress, and will only take
    action when the ``update_finished`` or ``update_error`` signals are
    emitted.
    """

    update_finished = Signal(AddonInfo, bool)
    """
    This signal is emitted after an add-on has been updated, or at least been
    checked and determined to be the latest version.

    The arguments to this signal are ``(addon_info, updated)`. If the add-on
    was updated, ``updated`` should be set to True. Otherwise, it should be
    False.

    The user interface will be updated after this signal is received, disabling
    the progress display used while waiting for the update to complete. If the
    add-on *was* updated, a message will most likely be displayed, telling the
    user that their add-on will be updated when the application is restarted.
    """

    update_error = Signal((AddonInfo, object), (AddonInfo, str))
    """
    This signal is emitted whenever an error occurs while waiting for an
    update to finish.

    The arguments to this signal are either ``(addon_info, error)`` or
    ``(addon_info, error_message)``. If an exception is provided, suitable
    information will be extracted from it. Otherwise, the provided string will
    be displayed.

    The user interface will be updated after this signal is received, disabling
    the progress display used while waiting for the update to complete. An
    error message will be displayed, either as a message box or as a message
    attached to the add-on information widget.
    """

    ##### Initialization ######################################################

    def __init__(self, manager):
        super(IUpdater, self).__init__()

        # Store the reference to the manager.
        self.manager = manager


    ##### Methods #############################################################

    def can_update(self, addon):
        """
        Begin a check to see if the provided add-on can be updated. This method
        is not expected to return any information. Instead, the Add-on Manager
        will await either an ``update_finished`` or ``update_error`` signal.

        =========  ============
        Argument   Description
        =========  ============
        addon     A :class:`AddonInfo` instance for the add-on in question.
        =========  ============
        """
        self.update_error.emit(
                addon,
                NotImplementedError('An updater is not installed.')
            )

    def do_update(self, addon):
        """
        Begin downloading and installing an update for the provided add-on.
        This method is not expected to return any information. Instead, the
        Add-on Manager will await either an ``update_finished`` or
        ``update_error`` signal.

        =========  ============
        Argument   Description
        =========  ============
        addon     A :class:`AddonInfo` instance for the add-on in question.
        =========  ============
        """
        self.update_error.emit(
                addon,
                NotImplementedError('An updater is not installed.')
            )
