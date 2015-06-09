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
A flexible add-ons system that's easy to extend with new types of add-ons,
provides a nice pre-built user interface for use in your applications, and that
has an easy-to-customize in-app update system.
"""

###############################################################################
# Imports
###############################################################################

from siding.addons.base import action, AddonInfo
from siding.addons.manager import DependencyError, manager
from siding.addons.version import Version, VersionMatch

safe_mode = False

###############################################################################
# Shortcuts
###############################################################################

add_type = manager.add_type
discover = manager.discover
find = manager.find
get = manager.get

check_inheritance = manager.check_inheritance
check_dependencies = manager.check_dependencies

###############################################################################
# The UI Helper
###############################################################################

def show():
    """ Show the Add-on Manager's user interface. """
    from siding.addons import ui
    ui.show()

###############################################################################
# Exports
###############################################################################

__all__ = [
    manager,  # The All Powerful

    add_type, discover, get, find,  # Manager Functions
    check_dependencies, check_inheritance,

    action,  # Decorators

    AddonInfo, DependencyError,  # Classes
    Version, VersionMatch,

    ##### UI Stuff ############################################################

    show,

]
