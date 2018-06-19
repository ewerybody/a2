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
The user interface code for the add-ons system.
"""

###############################################################################
# Imports
###############################################################################

from PySide2.QtWidgets import QMainWindow, QTabWidget, QWidget

from siding import addons, style, plugins

###############################################################################
# Constants and Storage
###############################################################################

_manager_window = None

###############################################################################
# The AddonTypeTab Class (with a horrible name)
###############################################################################

class AddonTypeTab(QWidget):
    """
    An instance of this class is created for each type of add-on registered
    with the system.
    """

    def __init__(self, type, parent=None):
        QWidget.__init__(self, parent)

        # Get our info.
        self.name = type
        text, self.icon = addons.manager._types[type][-2:]
        if text:
            self.text = text
        else:
            self.text = ' '.join(x.capitalize() for x in
                                 self.name.replace('_').split(' '))

        if not self.icon:
            self.icon = ''

        # Set some stuff.
        self.setWindowTitle(self.text)
        self.setWindowIcon(style.icon(self.icon))

###############################################################################
# The ManagerWindow Class
###############################################################################

class ManagerWindow(QMainWindow):
    """
    This is the Add-on Manager's custom window. Not much else to say, really.
    """

    def __init__(self, parent=None):
        super(ManagerWindow, self).__init__(parent)

        # Set the window title and size.
        self.setWindowTitle(self.tr("Add-on Manager"))
        self.setMinimumSize(400, 300)

        # Build the main widget.
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Load up all our tabs.
        for addon_type in sorted(addons.manager._types.keys()):
            tab = AddonTypeTab(addon_type)
            self.tabs.addTab(tab, tab.windowIcon(), tab.windowTitle())

        # Let plugins get in on this.
        plugins.run_signal('opened_addon_manager', self)

        # Icons and Style!
        #style.enable_aero(self)
        self.reload_icons()
        style.style_reloaded.connect(self.reload_icons)
        

    def reload_icons(self):
        """ Reload all of our icons. Which is... one icon. """
        self.setWindowIcon(style.icon('addon-manager'))

    def showRaise(self):
        """ Show and raise the window. """
        self.show()
        self.raise_()
        self.setFocus()

    ##### The Close Event #####################################################

    def closeEvent(self, event):
        """ Disconnect any signals and remove our reference. """
        global _manager_window
        if _manager_window is self:
            _manager_window = None

        style.style_reloaded.disconnect(self.reload_icons)
        plugins.run_signal('closed_addon_manager', self)

###############################################################################
# The Starting Point
###############################################################################

def show():
    """ Show the Add-on Manager's user interface. """
    global _manager_window

    if not _manager_window:
        _manager_window = ManagerWindow()

    # Show the manager.
    _manager_window.showRaise()