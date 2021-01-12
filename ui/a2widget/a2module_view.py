import traceback

from a2qt import QtCore, QtWidgets, QtGui

import a2uic
import a2core
import a2ctrl
import a2util


log = a2core.get_logger(__name__)
NEW_MODULE_DESC = (
    'Because none existed before this temporary description was created '
    'for "%s". Change it to describe what it does with a couple of words.'
)
NEW_MODULE_CFG = {'typ': 'nfo', 'version': '0.1', 'author': ''}
MULTI_MODULE_DESC = 'Multiple modules selected. Here goes some useful info in the future...'
EMPTY_MODULE_DESC = 'Module Config is currently empty! imagine awesome layout here ...'


class A2ModuleView(QtWidgets.QWidget):
    reload_requested = QtCore.Signal()

    def __init__(self, parent):
        super(A2ModuleView, self).__init__(parent)
        self.main = None
        self.editing = False
        self.controls = []
        self.menu_items = []
        self.a2 = a2core.A2Obj.inst()

    def setup_ui(self, main):
        self.main = main
        from a2widget import a2module_view_ui

        a2uic.check_module(a2module_view_ui)
        self.ui = a2module_view_ui.Ui_A2ModuleView()
        self.ui.setupUi(self)
        self.update_header()

        self.ui.scrollBar = self.ui.a2scroll_area.verticalScrollBar()
        self.settings_widget = self.ui.scroll_area_contents

        self.ui.mod_check.clicked[bool].connect(self.main.mod_enable)
        self.ui.a2help_button.clicked.connect(self.help)

        self.ui.a2ok_button.clicked.connect(self.main.edit_submit)
        self.ui.a2cancel_button.clicked.connect(self.draw_mod)
        self.toggle_edit(False)

        margin = self.main.style.get('margin', 0)
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
                self.draw_settings()
                return
            else:
                config = [NEW_MODULE_CFG.copy()]
                config[0]['description'] = MULTI_MODULE_DESC

            module_user_cfg = {}

        else:
            config = self.main.mod.config
            module_user_cfg = self.main.mod.get_user_cfg()
            self.main.temp_config = None

        if config:
            if config[0].get('typ') != 'nfo':
                log.error('First element of config is not typ nfo! %s' % self.main.mod.name)
        else:
            config = [NEW_MODULE_CFG.copy()]
            config[0]['description'] = EMPTY_MODULE_DESC

        nfo = config[0]
        self.update_header(nfo.get('author', ''), nfo.get('version', ''))

        self.controls.clear()
        self.menu_items.clear()

        for element_cfg in config:
            cfg_name = a2util.get_cfg_default_name(element_cfg)
            user_cfg = module_user_cfg.get(cfg_name, {})
            element_widget = a2ctrl.draw(self.main, element_cfg, self.main.mod, user_cfg)

            if isinstance(element_widget, QtWidgets.QWidget):
                self.controls.append(element_widget)
            elif isinstance(element_widget, QtGui.QAction):
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
        self.ui.mod_check.setTristate(False)
        self.ui.mod_author.setText(author)
        self.ui.mod_version.setText(version)

        if self.main.mod is None:
            self.ui.a2mod_view_source_label.setText('')

            if not self.main.num_selected:
                self.ui.head_widget.setVisible(False)

            else:
                self.ui.head_widget.setVisible(True)
                self.ui.a2_mod_name.setText('%i modules' % self.main.num_selected)
                num_enabled = sum([mod.enabled for mod in self.main.selected])
                if num_enabled == 0:
                    self.ui.mod_check.setChecked(False)
                elif num_enabled == self.main.num_selected:
                    self.ui.mod_check.setChecked(True)
                else:
                    self.ui.mod_check.setTristate(True)
                    self.ui.mod_check.setCheckState(QtCore.Qt.PartiallyChecked)
        else:
            self.ui.head_widget.setVisible(True)
            self.ui.a2mod_view_source_label.setText(self.main.mod.source.name)
            self.ui.a2_mod_name.setText(self.main.mod.name)
            # weird.. need to set false first to fix tristate effect
            self.ui.mod_check.setChecked(False)
            self.ui.mod_check.setChecked(self.main.mod.enabled)

    def edit_mod(self):
        """
        From the modules config creates controls to edit the config itself.
        If a header is not found one will be added to the in-edit config.
        On "OK" the config data is collected from the UI and written back to the json.
        On Cancel the in-edit config is discarded and drawMod called which draws the
        UI unchanged.
        """
        if self.main.mod is None:
            return

        import a2element.common
        from copy import deepcopy

        self.controls.clear()
        self.menu_items.clear()
        if self.main.temp_config is None:
            self.main.temp_config = deepcopy(self.main.mod.config)

        if not self.main.temp_config:
            new_cfg = NEW_MODULE_CFG.copy()
            new_cfg.update(
                {
                    'description': NEW_MODULE_DESC % self.main.mod.name,
                    'date': a2util.get_date(),
                    'author': self.main.devset.author_name,
                }
            )
            self.main.temp_config.insert(0, new_cfg)

        for cfg in self.main.temp_config:
            self.controls.append(a2ctrl.edit(cfg, self.main, self.main.temp_config))

        edit_select = a2element.common.EditAddElem(self.main, self.main.temp_config)
        self.controls.append(edit_select)

        self.draw_ui()

        # new_widget = EditView(self, self.controls, self.main.temp_config)

        # # turn scroll layout content to new host widget
        # _current_widget = self.ui.a2scroll_area.takeWidget()
        # _current_widget.deleteLater()
        # self.ui.a2scroll_area.setWidget(new_widget)
        # self.settings_widget = new_widget

        self.toggle_edit(True)
        self.settings_widget.setFocus()

    def draw_ui(self):
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
        new_widget = QtWidgets.QWidget(self.main)

        # create new column layout for the module controls
        new_layout = QtWidgets.QVBoxLayout(new_widget)

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
                log.debug('Error drawing widget: %s', ctrl)
                log.error(traceback.format_exc().strip())
                raise error

        policy = QtWidgets.QSizePolicy
        # amend a spacer
        spacer = QtWidgets.QSpacerItem(0, 0, policy.Minimum, policy.Minimum)
        new_layout.addItem(spacer)

        vertical_policy = policy.Minimum if has_expandable_widget else policy.Maximum
        new_widget.setSizePolicy(policy(policy.Preferred, vertical_policy))

        # turn scroll layout content to new host widget
        _current_widget = self.ui.a2scroll_area.takeWidget()
        _current_widget.deleteLater()
        self.ui.a2scroll_area.setWidget(new_widget)
        self.settings_widget = new_widget

    def toggle_edit(self, state):
        self.editing = state
        self.ui.a2edit_okcancel_widget.setVisible(state)
        for button in [self.ui.a2cancel_button, self.ui.a2ok_button]:
            button.setEnabled(state)

    def help(self):
        """
        Open help of the selected module or a2 help
        """
        if self.main.mod is None:
            a2util.surf_to(self.a2.urls.help)
        else:
            self.main.mod.help()

    def check_element(self, name):
        """
        Finds a named element and calls its check func.
        """
        for widget in self.controls:
            try:
                if widget.cfg['name'] == name:
                    widget.check()
                    return
            except (AttributeError, KeyError):
                pass

    def draw_settings(self):
        from a2widget import a2settings_view

        # remember tab if already a settings tab
        if len(self.controls) == 1 and isinstance(self.controls[0], a2settings_view.A2Settings):
            settings_widget = a2settings_view.A2Settings(self.main, self.controls[0].tab_index)
        else:
            settings_widget = a2settings_view.A2Settings(self.main)

        settings_widget.reload_requested.connect(self.reload_requested.emit)
        self.controls[:] = [settings_widget]
        self.update_header()
        self.draw_ui()


class EditView(QtWidgets.QWidget):
    def __init__(self, parent, controls, config_list):
        super(EditView, self).__init__(parent)
        self.edit_layout = QtWidgets.QVBoxLayout(self)
        self.controls = controls
        self.config_list = config_list

        import a2element.common

        for ctrl in controls:
            if ctrl is None:
                continue

            self.edit_layout.addWidget(ctrl)

            if isinstance(ctrl, a2element.common.EditCtrl):
                ctrl.delete_requested.connect(self.delete_element)
                ctrl.move_abs_requested.connect(self.move_absolute)
                ctrl.move_rel_requested.connect(self.move_relative)

        # amend a spacer
        policy = QtWidgets.QSizePolicy
        spacer = QtWidgets.QSpacerItem(10, 10, policy.Minimum, policy.Minimum)
        self.edit_layout.addItem(spacer)

        self.setSizePolicy(policy(policy.Preferred, policy.Maximum))

    def delete_element(self):
        sender = self.sender()
        print('delete_element', sender)

    def move_relative(self, value):
        sender = self.sender()
        print('move_relative', sender, value)

    def move_absolute(self, value):
        sender = self.sender()
        print('move_absolute', sender, value)
