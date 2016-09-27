"""
a2ctrl.a2module_view

@created: Aug 14, 2016
@author: eRiC
"""
from copy import deepcopy

from PySide import QtGui, QtCore

import a2core
import a2ctrl
from a2widget import a2settings_view
from a2widget import a2module_view_ui


log = a2core.get_logger(__name__)


class A2ModuleView(QtGui.QWidget):

    def __init__(self, parent):
        super(A2ModuleView, self).__init__(parent)
        self.main = None
        self.editing = False
        self.controls = []
        self.a2 = a2core.A2Obj.inst()

    def setup_ui(self, main):
        self.main = main
        a2ctrl.check_ui_module(a2module_view_ui)
        self.ui = a2module_view_ui.Ui_A2ModuleView()
        self.ui.setupUi(self)

        self.ui.scrollBar = self.ui.a2scroll_area.verticalScrollBar()

        self.mainlayout = self.ui.scroll_area_contents.layout()
        self.ui.spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum,
                                           QtGui.QSizePolicy.Expanding)
        self.mainlayout.addItem(self.ui.spacer)
        self.settings_widget = self.ui.scroll_area_contents

        self.ui.modCheck.clicked[bool].connect(self.main.mod_enable)
        self.ui.a2help_button.clicked.connect(self.mod_info)

        self.ui.a2ok_button.clicked.connect(self.main.edit_submit)
        self.ui.a2cancel_button.clicked.connect(self.draw_mod)
        self.toggle_edit(False)

    def draw_mod(self):
        """
        from the modules config creates the usual display controls and
        fills them with the saved settings from the database.
        On change they trigger writing to the db, collect all include info
        and restart a2.
        """
        self.controls = []

        if self.main.mod is None:
            if not self.main.num_selected:
                self.controls.append(a2settings_view.A2Settings(self.main))
                config = [{'typ': 'nfo', 'author': '', 'version': 'v0.1'}]
            else:
                config = [{'typ': 'nfo', 'author': '', 'version': '',
                           'description': 'Multiple modules selected. Here goes some '
                                          'useful info in the future...'}]
        else:
            config = self.main.mod.config

            self.main.tempConfig = None

        if len(config):
            if config[0].get('typ') != 'nfo':
                log.error('First element of config is not typ nfo! %s' % self.main.mod.name)
        else:
            config = [{'typ': 'nfo', 'author': '', 'version': '',
                       'description': 'Module Config is currently empty! imagine awesome layout here ...'}]

        self.ui.modAuthor.setText(config[0].get('author', ''))
        self.ui.modVersion.setText(config[0].get('version', ''))
        self.update_header()

        for cfg in config:
            self.controls.append(a2ctrl.draw(self.main, cfg, self.main.mod))

        self.toggle_edit(False)
        self.drawUI()

    def update_header(self):
        """
        Updates the module settings view to the right of the UI
        when something different is elected in the module list
        """
        self.ui.modCheck.setTristate(False)

        if self.main.mod is None:
            self.ui.a2mod_view_source_label.setText('')

            if not self.main.num_selected:
                self.ui.modCheck.setVisible(False)
                self.ui.modName.setText('a2')
            else:
                self.ui.modCheck.setVisible(True)
                self.ui.modName.setText('%i modules' % self.main.num_selected)
                numenabled = sum([mod.enabled for mod in self.main.selected])
                if numenabled == 0:
                    self.ui.modCheck.setChecked(False)
                elif numenabled == self.main.num_selected:
                    self.ui.modCheck.setChecked(True)
                else:
                    self.ui.modCheck.setTristate(True)
                    self.ui.modCheck.setCheckState(QtCore.Qt.PartiallyChecked)
        else:
            self.ui.a2mod_view_source_label.setText(self.main.mod.source.name)
            self.ui.modCheck.setVisible(True)
            self.ui.modName.setText(self.main.mod.name)
            # weird.. need to set false first to fix tristate effect
            self.ui.modCheck.setChecked(False)
            self.ui.modCheck.setChecked(self.main.mod.enabled)

    def edit_mod(self, keep_scroll=False):
        """
        From the modules config creates controls to edit the config itself.
        If a header is not found one will be added to the in-edit config.
        On "OK" the config data is collected from the UI and written back to the json.
        On Cancel the in-edit config is discarded and drawMod called which draws the
        UI unchanged.
        """
        if self.main.mod is None:
            return

        self.controls = []
        if self.main.tempConfig is None:
            self.main.tempConfig = deepcopy(self.main.mod.config)

        #if not mod.config: is None or mod.config is []
        if not len(self.main.tempConfig):
            newNfo = {'typ': 'nfo',
                      'description': 'Because none existed before this temporary description was '
                                     'created for "%s". Change it to describe what it does with a '
                                     'couple of words.' % self.main.mod.name,
                      'author': self.main.devset.author_name,
                      'version': '0.1',
                      'date': a2core.get_date()}
            self.main.tempConfig.insert(0, newNfo)

        for cfg in self.main.tempConfig:
            self.controls.append(a2ctrl.edit(cfg, self.main, self.main.tempConfig))

        editSelect = a2ctrl.EditAddElem(self.main, self.main.tempConfig)
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
        # turn scroll layout content to new host widget
        self.ui.a2scroll_area.setWidget(new_widget)

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
        for button in [self.ui.a2cancel_button, self.ui.a2ok_button]:
            button.setEnabled(state)
            button.setMaximumSize(QtCore.QSize(16777215, 150 if state else 0))
            self.ui.a2edit_okcancel_widget.setMaximumSize(QtCore.QSize(16777215, 150 if state else 0))

    def mod_info(self):
        """
        Open help of the selected module or a2 help
        """
        if self.main.mod is None:
            a2core.surfTo(self.a2.urls.help)
        else:
            self.main.mod.help()

    def scroll_to(self):
        # TODO:
        #if self.ui.module_view.ui.scrollArea.hasFocus():
        #print('self.ui.scrollArea.hasFocus(): %s' % self.ui.scrollArea.hasFocus())
        #    current = self.ui.scrollBar.value()
        #    scroll_end = self.ui.scrollBar.maximum()
        #    if isinstance(value, bool):
        #        value = 0 if value else self.ui.scrollBar.maximum()
        #    if value == current or scroll_end == 0:
        #        return
        #    if not smooth:
        #        self.ui.scrollBar.setValue(value)
        pass
    #             tmax = 0.3
    #             curve = QtCore.QEasingCurve(QtCore.QEasingCurve.OutQuad)
    #             res = 0.01
    #             steps = tmax / res
    #             tsteps = 1 / steps
    #             t = 0.0
    #
    #             rng = value - current
    #             while t <= 1.0:
    #                 time.sleep(res)
    #                 t += tsteps
    #                 v = curve.valueForProgress(t)
    #                 scrollval = current + (v * rng)
    #                 self.ui.scrollBar.setValue(scrollval)
