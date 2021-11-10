import traceback

from a2qt import QtCore, QtWidgets, QtGui

import a2mod
import a2uic
import a2core
import a2ctrl
import a2util
import a2path


log = a2core.get_logger(__name__)
MULTI_MODULE_DESC = 'Multiple modules selected. Here goes some useful info in the future...'
EMPTY_MODULE_DESC = 'Module Config is currently empty! imagine awesome layout here ...'


class A2ModuleView(QtWidgets.QWidget):
    reload_requested = QtCore.Signal()
    enable_request = QtCore.Signal(bool)
    edit_mode = QtCore.Signal(bool)
    okayed = QtCore.Signal()

    def __init__(self, parent):
        super(A2ModuleView, self).__init__(parent)
        self.main = None
        self.editing = False
        self.controls = []
        self.menu_items = []
        self.a2 = a2core.A2Obj.inst()
        self._editor = None

    def setup_ui(self, main):
        self.main = main
        from a2widget import a2module_view_ui

        a2uic.check_module(a2module_view_ui)
        self.ui = a2module_view_ui.Ui_A2ModuleView()
        self.ui.setupUi(self)
        self.update_header()

        self.ui.scrollBar = self.ui.a2scroll_area.verticalScrollBar()
        self.settings_widget = self.ui.scroll_area_contents

        self.ui.mod_check.clicked[bool].connect(self.toggle_state)
        self.ui.a2help_button.clicked.connect(self.help)

        self.ui.a2ok_button.clicked.connect(self.okayed.emit)
        self.ui.a2cancel_button.clicked.connect(self.draw_mod)
        self.add_button = None
        self.add_button_layer = None
        self._set_editing(False)
        icon_size = self.main.style.get('icon_size')
        self.ui.icon_label.setMinimumSize(icon_size, icon_size)
        self.ui.icon_label.setMaximumSize(icon_size, icon_size)

        margin = self.main.style.get('margin', 0)
        self.ui.a2edit_okcancel_layout.setContentsMargins(margin, margin, margin, margin)

    def draw_mod(self):
        """
        from the modules config creates the usual display controls and
        fills them with the saved settings from the database.
        On change they trigger writing to the db, collect all include info
        and restart a2.
        """
        self._set_editing(False)

        if self.main.mod is None:
            if not self.main.num_selected:
                self.draw_settings()
                return
            else:
                config = [a2mod.NEW_MODULE_CFG.copy()]
                config[0]['description'] = MULTI_MODULE_DESC

            module_user_cfg = {}
            self.ui.icon_label.hide()

        else:
            config = self.main.mod.config
            module_user_cfg = self.main.mod.get_user_cfg()
            self.ui.icon_label.show()
            self.ui.icon_label.setPixmap(
                self.main.mod.icon.pixmap(self.main.style.get('icon_size'))
            )

        if config:
            if config[0].get('typ') != 'nfo':
                log.error('First element of config is not typ nfo! %s' % self.main.mod.name)
        else:
            config = [a2mod.NEW_MODULE_CFG.copy()]
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
            self.ui.a2_mod_name.setText(self.main.mod.display_name)
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

        from copy import deepcopy
        from a2widget import a2module_editor
        import a2element._edit

        self.controls.clear()
        self.menu_items.clear()

        config_copy = deepcopy(self.main.mod.config)
        self._editor = a2module_editor.EditView(self.main, config_copy)
        self.ui.a2edit_tool_button.clicked.connect(self._editor.on_menu_button_clicked)

        self.add_button = a2element._edit.EditAddElem(self.main, config_copy)
        self.add_button.add_request.connect(self._editor.add_element)
        self.add_button_layer = QtWidgets.QVBoxLayout()
        spacing = self.main.style.get('spacing')
        self.add_button_layer.setContentsMargins(spacing, 0, 0, 0)
        self.add_button_layer.addWidget(self.add_button)
        self.ui.mod_view_grid.addLayout(self.add_button_layer, 1, 0, 1, 1)
        self.add_button_layer.setAlignment(
            self.add_button, QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft
        )

        self._set_widget(self._editor)
        self._set_editing(True)
        self.settings_widget.setFocus()

    def draw_ui(self):
        """
        Take list of controls and arrange them in scroll layout.

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
        # to refill the scroll layout: create widget to host the module's new layout
        new_widget = QtWidgets.QWidget(self.main)
        # create new column layout for the module controls
        new_layout = QtWidgets.QVBoxLayout(new_widget)

        # make the new inner layout the mainLayout add the controls to it
        has_expandable_widget = False
        for ctrl in self.controls:
            if ctrl is None:
                continue

            try:
                new_layout.addWidget(ctrl)
                if ctrl.is_expandable_widget:
                    has_expandable_widget = True

            # TODO: draw an error-widget instead!
            except RuntimeError as error:
                log.error(traceback.format_exc().strip())
                raise error

            except AttributeError as error:
                log.debug('Error drawing widget: %s', ctrl)
                log.error(traceback.format_exc().strip())
                raise error

        # amend a spacer
        QSizePolicy = QtWidgets.QSizePolicy
        spacer = QtWidgets.QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        new_layout.addItem(spacer)

        vertical_policy = QSizePolicy.Minimum if has_expandable_widget else QSizePolicy.Maximum
        new_widget.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, vertical_policy))
        self._set_widget(new_widget)

    def _set_widget(self, new_widget):
        """Turn scroll layout content to new host widget."""
        _current_widget = self.ui.a2scroll_area.takeWidget()
        _current_widget.deleteLater()
        self.ui.a2scroll_area.setWidget(new_widget)
        self.settings_widget = new_widget

    def _set_editing(self, state):
        self.editing = state
        self.edit_mode.emit(state)
        self.ui.a2edit_okcancel_widget.setVisible(state)
        for button in [self.ui.a2cancel_button, self.ui.a2ok_button]:
            button.setEnabled(state)
        if not state:
            if self.add_button_layer is None and self.add_button is None:
                return
            self.ui.mod_view_grid.removeItem(self.add_button_layer)
            self.add_button.deleteLater()
            self.add_button_layer = None
            self.add_button = None

    def help(self):
        """
        Open help of the selected module or a2 help
        """
        if self.main.mod is None:
            a2util.surf_to(self.a2.urls.help)
        else:
            self.main.mod.help()

    def check_element(self, name):
        """Find a named element and call its `check` method."""
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

    def toggle_state(self, state):
        """Get the top checkbox state and emit according request."""
        state = not self.ui.mod_check.isTristate() and state
        self.enable_request.emit(state)

    @property
    def _tmp_cfg(self):
        # TODO: The editor should handle all by itself and not pass that config
        return self.editor.get_cfg_copy()

    def cfg_different(self):
        """Shallow difference check between temp and current module config.

        Could have been done with deepdiff, but we want to treat empty string values
        equal to None or even key missing."""
        tmp_cfg = self.editor.get_cfg_copy()
        if tmp_cfg == self.main.mod.config:
            return False

        if len(tmp_cfg) != len(self.main.mod.config):
            return True

        for cfg0, cfg1 in zip(self.main.mod.config, tmp_cfg):
            for key in set(cfg0).intersection(cfg1):
                if cfg0.get(key) != cfg1.get(key):
                    return True
            for key in set(cfg0).difference(cfg1):
                if cfg0[key] != '':
                    return True
            for key in set(cfg1).difference(cfg0):
                if cfg1[key] != '':
                    return True
        return False

    def user_cancels(self):
        """Popup dialog to ask about discarding changes.
        Return `True` if user clicks **Cancel** to keep editing."""
        import a2dev

        msg = (
            'The module configuration appears to have changed!\n'
            'Do you really want to exit and discard the changes?\n\n'
            'You can also have a look at the differences...'
        )
        dialog = a2dev.OkDiffDialog(
            self.main, 'Config Changed!', msg, self.main.mod.config_file, None
        )
        dialog.diff_requested.connect(self._on_diff_requested)
        dialog.exec_()
        dialog.remove_temp_files()
        return dialog.result is False

    def _on_diff_requested(self):
        dialog = self.sender()
        tmp_path = a2path.temp_path(f'temp_{self.main.mod.name}_', 'json')
        a2util.json_write(tmp_path, self._tmp_cfg)
        dialog.file_path2 = tmp_path

    @property
    def editor(self):
        if self._editor is None:
            RuntimeError('No editor built!')
        return self._editor