"""
a2ctrl.a2module_view

@created: Aug 14, 2016
@author: eRiC
"""
import logging
from copy import deepcopy

from PySide import QtGui, QtCore

import a2core
import a2ctrl
from a2ctrl import a2module_view_ui

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class ModuleView(QtGui.QWidget):

    def __init__(self, parent):
        super(ModuleView, self).__init__(parent)
        self.main = None
        self.editing = False
        self.controls = []
        self.a2 = a2core.A2Obj.inst()
        # since the view can only display one module at a time
        # this is set to the module on change
        self.mod = None

    def setup_ui(self, main):
        self.main = main
        self.ui = a2module_view_ui.Ui_ModuleView()
        self.ui.setupUi(self)

        #self.setLayout(self.ui.module_list_layout)
        self.ui.scrollArea.setFont(a2ctrl.fontL)
        self.ui.scrollBar = self.ui.scrollArea.verticalScrollBar()

        self.mainlayout = self.ui.scrollAreaContents.layout()
        self.ui.spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum,
                                           QtGui.QSizePolicy.Expanding)
        self.mainlayout.addItem(self.ui.spacer)
        self.settings_widget = self.ui.scrollAreaContents

        self.ui.modCheck.setVisible(False)
        self.ui.modName.setText('a2')
        self.ui.modVersion.setText('v0.1')
        self.ui.modAuthor.setText('')

        self.ui.modCheck.clicked.connect(self.main.mod_enable)
        self.ui.modInfoButton.clicked.connect(self.mod_info)

        self.ui.editOKButton.released.connect(self.main.editSubmit)
        self.ui.editCancelButton.released.connect(self.draw_mod)
        self.toggle_edit(False)

    def draw_mod(self):
        """
        from the modules config creates the usual display controls and
        fills them with the saved settings from the database.
        On change they trigger writing to the db, collect all include info
        and restart a2.
        """
        self.controls = []

        if self.main.selected == []:
            self.mod = None
            self.controls.append(a2ctrl.a2settings.A2Settings(self.main))
            config = [{'typ': 'nfo', 'author': '', 'version': 'v0.1'}]
        else:
            if len(self.main.selected) > 1:
                config = [{'typ': 'nfo', 'author': '', 'version': '',
                           'description': 'Multiple modules selected. Here goes some '
                                          'useful info in the future...'}]
                self.mod = None
            else:
                self.mod = self.main.selected[0]
                print('self.mod.name: %s' % self.mod.name)
                config = self.mod.config
                print('config: %s' % config)

            self.main.tempConfig = None

        if len(config):
            if config[0].get('typ') != 'nfo':
                log.error('First element of config is not typ nfo! %s' % self.mod.name)
        else:
            config = [{'typ': 'nfo', 'author': '', 'version': '',
                       'description': 'Module Config is currently empty! imagine awesome layout here ...'}]

        self.ui.modAuthor.setText(config[0].get('author', ''))
        self.ui.modVersion.setText(config[0].get('version', ''))

        for cfg in config:
            self.controls.append(a2ctrl.draw(self, cfg, self.mod))

        self.toggle_edit(False)
        self.drawUI()

    def mod_select(self):
        """
        Updates the module settings view to the right of the UI
        when something different is elected in the module list
        """
        if self._draw_phase:
            return

        sel = self.ui.modList.selectedItems()
        numsel = len(sel)
        self.ui.modCheck.setTristate(False)

        if not numsel:
            self.ui.modCheck.setVisible(False)
            self.mod = None
            self.selected_mod = []
            self.ui.modName.setText('a2')

        elif numsel == 1:
            name = sel[0].text()
            # break if sel == previous sel
            if name in self.selected_mod and len(self.selected_mod) == 1 and force is False:
                return
            self.ui.modCheck.setVisible(True)
            self.ui.modName.setText(name)
            enabled = name in self.a2.enabled
            # weird.. need to set false first to fix tristate effect
            self.ui.modCheck.setChecked(False)
            self.ui.modCheck.setChecked(enabled)

            self.mod = self.a2.modules[name]
            self.selected_mod = [name]

        else:
            names = [s.text() for s in sel]
            self.selected_mod = names
            self.ui.modCheck.setVisible(True)
            self.ui.modName.setText('%i modules' % numsel)
            numenabled = len([n for n in names if n in self.a2.enabled])
            if numenabled == 0:
                self.ui.modCheck.setChecked(False)
            elif numenabled == numsel:
                self.ui.modCheck.setChecked(True)
            else:
                self.ui.modCheck.setTristate(True)
                self.ui.modCheck.setCheckState(QtCore.Qt.PartiallyChecked)

        self.drawMod()

    def edit_mod(self, keep_scroll=False):
        """
        From the modules config creates controls to edit the config itself.
        If a header is not found one will be added to the in-edit config.
        On "OK" the config data is collected from the UI and written back to the json.
        On Cancel the in-edit config is discarded and drawMod called which draws the
        UI unchanged.
        """
        if len(self.main.selected) != 1 or self.main.selected[0] == 'a2':
            return
        self.mod = self.main.selected[0]

        self.controls = []
        if self.main.tempConfig is None:
            self.main.tempConfig = deepcopy(self.mod.config)

        #if not mod.config: is None or mod.config is []
        if not len(self.main.tempConfig):
            newNfo = {'typ': 'nfo',
                      'description': 'Because none existed before this temporary description was '
                                     'created for "%s". Change it to describe what it does with a '
                                     'couple of words.' % self.mod.name,
                      'author': a2core.get_author(),
                      'version': '0.1',
                      'date': a2core.get_date()}
            self.main.tempConfig.insert(0, newNfo)

        for cfg in self.main.tempConfig:
            self.controls.append(a2ctrl.edit(cfg, self, self.main.tempConfig))

        editSelect = a2ctrl.EditAddElem(self, self.main.tempConfig)
        self.controls.append(editSelect)

        self.drawUI(keep_scroll)
        self.toggle_edit(True)
        self.settings_widget.setFocus()

    def drawUI(self, keep_scroll=False):
        """
        takes list of controls and arranges them in the scroll layout

        1. I tried to just create layouts for each module unhook them from the
        scroll layout on demand and hook up another one but Qt is spart so it
        deletes the invisible layout which cannot be hooked up again.
        2. I tried to brute force delete everything and building it over again each
        time something else is seleceted in the left list but Qt refuses to
        delete anything visually with destroy() or removeWidget()
        3. We probably need an actual tab layout to do this but I can't find how to
        make the tabs invisible...
        4. I'll try to create an all new layout,
            fill it and switch away from the old one:
        """
        # to refill the scoll layout:
        # take away the spacer from 'mainLayout'
        self.mainlayout.removeItem(self.ui.spacer)
        # create widget to host the module's new layout
        current_height = self.settings_widget.height()
        new_widget = QtGui.QWidget(self)
        if keep_scroll:
            current_scroll_value = self.ui.scrollBar.value()
            new_widget.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                                       QtGui.QSizePolicy.Fixed))
            new_widget.setMinimumHeight(current_height)

        # create new column layout for the module controls
        newLayout = QtGui.QVBoxLayout(new_widget)
        newLayout.setContentsMargins(5, 5, 5, 5)
        newLayout.setSpacing(a2ctrl.UIValues.spacing)
        # turn scroll layout content to new host widget
        self.ui.scrollArea.setWidget(new_widget)

        # make the new inner layout the mainLayout
        # add the controls to it
        for ctrl in self.controls:
            if ctrl:
                newLayout.addWidget(ctrl)
        # amend the spacer
        newLayout.addItem(self.ui.spacer)

        new_widget.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                                   QtGui.QSizePolicy.Maximum))
        if keep_scroll:
            self.ui.scrollBar.setValue(current_scroll_value)

        self.mainlayout = newLayout
        self.settings_widget = new_widget

    def toggle_edit(self, state):
        self.editing = state
        for button in [self.ui.editCancelButton, self.ui.editOKButton]:
            button.setEnabled(state)
            button.setMaximumSize(QtCore.QSize(16777215, 50 if state else 0))
            self.ui.editOKCancelWidget.setMaximumSize(QtCore.QSize(16777215, 50 if state else 0))

    def mod_info(self):
        """
        Open help of the selected module or a2 help
        """
        if self.mod is None:
            a2core.surfTo(self.a2.urls.help)
        else:
            self.mod.help()
