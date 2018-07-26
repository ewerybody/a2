from copy import deepcopy

from PySide2 import QtCore, QtWidgets

import a2core
import a2ctrl
import a2util
from a2element.common import EditAddElem
from a2widget import a2settings_view
from a2widget import a2module_view_ui
import traceback


log = a2core.get_logger(__name__)
NEW_MODULE_DESC = ('Because none existed before this temporary description was created '
                   'for "%s". Change it to describe what it does with a couple of words.')
NEW_MODULE_CFG = {'typ': 'nfo',
                  'version': '0.1'}


class A2ModuleView(QtWidgets.QWidget):

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
        self.settings_widget = self.ui.scroll_area_contents

        self.ui.modCheck.clicked[bool].connect(self.main.mod_enable)
        self.ui.a2help_button.clicked.connect(self.mod_info)

        self.ui.a2ok_button.clicked.connect(self.main.edit_submit)
        self.ui.a2cancel_button.clicked.connect(self.draw_mod)
        self.toggle_edit(False)

        margin = self.main.style.get('margin')
        self.ui.a2edit_okcancel_layout.setContentsMargins(margin, margin, margin, margin)

    def draw_mod(self):
        """
        from the modules config creates the usual display controls and
        fills them with the saved settings from the database.
        On change they trigger writing to the db, collect all include info
        and restart a2.
        """
        self.toggle_edit(False)

        if self.main.mod is None:
            if not self.main.num_selected:
                self.controls = [a2settings_view.A2Settings(self.main)]
                self.update_header()
                self.draw_ui()
                return

            else:
                config = [{'typ': 'nfo', 'author': '', 'version': '',
                           'description': 'Multiple modules selected. Here goes some '
                                          'useful info in the future...'}]
        else:
            config = self.main.mod.config
            self.main.temp_config = None

        if len(config):
            if config[0].get('typ') != 'nfo':
                log.error('First element of config is not typ nfo! %s' % self.main.mod.name)
        else:
            config = [{'typ': 'nfo', 'author': '', 'version': '',
                       'description': 'Module Config is currently empty! imagine awesome layout here ...'}]

        nfo = config[0]
        self.update_header(nfo.get('author', ''), nfo.get('version', ''))

        self.controls = []
        self.menu_items = []
        for element_cfg in config:
            element_widget = a2ctrl.draw(self.main, element_cfg, self.main.mod)
            if isinstance(element_widget, QtWidgets.QWidget):
                self.controls.append(element_widget)
            elif isinstance(element_widget, QtWidgets.QAction):
                print('element_widget: %s' % element_widget)
                self.menu_items.append(element_widget)
            elif element_widget is not None:
                log.error('What is element "%s"?!' % element_widget)

        self.ui.head_widget.setVisible(True)
        self.toggle_edit(False)
        self.draw_ui()

    def update_header(self, author='', version=''):
        """
        Updates the module settings view to the right of the UI
        when something different is elected in the module list
        """
        self.ui.modCheck.setTristate(False)
        self.ui.modAuthor.setText(author)
        self.ui.modVersion.setText(version)

        if self.main.mod is None:
            self.ui.a2mod_view_source_label.setText('')

            if not self.main.num_selected:
                self.ui.head_widget.setVisible(False)

            else:
                self.ui.head_widget.setVisible(True)
                self.ui.modName.setText('%i modules' % self.main.num_selected)
                num_enabled = sum([mod.enabled for mod in self.main.selected])
                if num_enabled == 0:
                    self.ui.modCheck.setChecked(False)
                elif num_enabled == self.main.num_selected:
                    self.ui.modCheck.setChecked(True)
                else:
                    self.ui.modCheck.setTristate(True)
                    self.ui.modCheck.setCheckState(QtCore.Qt.PartiallyChecked)
        else:
            self.ui.head_widget.setVisible(True)
            self.ui.a2mod_view_source_label.setText(self.main.mod.source.name)
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
        self.menu_items = []
        if self.main.temp_config is None:
            self.main.temp_config = deepcopy(self.main.mod.config)

        if not len(self.main.temp_config):
            new_cfg = deepcopy(NEW_MODULE_CFG)
            new_cfg.update({
                'description': NEW_MODULE_DESC % self.main.mod.name,
                'date': a2util.get_date(),
                'author': self.main.devset.author_name})
            self.main.temp_config.insert(0, new_cfg)

        for cfg in self.main.temp_config:
            self.controls.append(a2ctrl.edit(cfg, self.main, self.main.temp_config))

        edit_select = EditAddElem(self.main, self.main.temp_config)
        self.controls.append(edit_select)

        self.draw_ui(keep_scroll)
        self.toggle_edit(True)
        self.settings_widget.setFocus()

    def draw_ui(self, keep_scroll=False):
        """
        takes list of controls and arranges them in the scroll layout

        1. I tried to just create layouts for each module unhook them from the
        scroll layout on demand and hook up another one but Qt is smart so it
        deletes the invisible layout which cannot be hooked up again.
        2. I tried to brute force delete everything and building it over again each
        time something else is selected in the left list but Qt refuses to
        delete anything visually with destroy() or removeWidget()
        3. We probably need an actual tab layout to do this but I can't find how to
        make the tabs invisible...
        4. I'll try to create an all new layout,
            fill it and switch away from the old one:
        """
        # to refill the scroll layout:
        # create widget to host the module's new layout
        new_widget = QtWidgets.QWidget(self)
        policy = QtWidgets.QSizePolicy

        if keep_scroll:
            current_height = self.settings_widget.height()
            current_scroll_value = self.ui.scrollBar.value()
            new_widget.setSizePolicy(policy(policy.Preferred, policy.Fixed))
            new_widget.setMinimumHeight(current_height)

        # create new column layout for the module controls
        new_layout = QtWidgets.QVBoxLayout(new_widget)

        # turn scroll layout content to new host widget
        self.ui.a2scroll_area.setWidget(new_widget)

        # make the new inner layout the mainLayout
        # add the controls to it
        has_expandable_widget = False
        for ctrl in self.controls:
            if ctrl is None:
                continue

            try:
                new_layout.addWidget(ctrl)
                if ctrl.is_expandable_widget:
                    has_expandable_widget = True
            except RuntimeError as error:
                log.error(traceback.format_exc().strip())
                raise error
            except AttributeError as error:
                log.debug('Error drawing widget: %s' % ctrl)
                log.error(traceback.format_exc().strip())
                raise error

        # amend a spacer
        spacer = QtWidgets.QSpacerItem(0, 0, policy.Minimum, policy.Minimum)
        new_layout.addItem(spacer)

        vertical_policy = policy.Minimum if has_expandable_widget else policy.Maximum
        new_widget.setSizePolicy(policy(policy.Preferred, vertical_policy))

        if keep_scroll:
            self.ui.scrollBar.setValue(current_scroll_value)

        self.settings_widget = new_widget

    def toggle_edit(self, state):
        self.editing = state
        self.ui.a2edit_okcancel_widget.setVisible(state)
        for button in [self.ui.a2cancel_button, self.ui.a2ok_button]:
            button.setEnabled(state)

    def mod_info(self):
        """
        Open help of the selected module or a2 help
        """
        if self.main.mod is None:
            a2util.surf_to(self.a2.urls.help)
        else:
            self.main.mod.help()

    def scroll_to(self):
        # TODO:
        # if self.ui.module_view.ui.scrollArea.hasFocus():
        # print('self.ui.scrollArea.hasFocus(): %s' % self.ui.scrollArea.hasFocus())
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
