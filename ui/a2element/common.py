"""
The a2 element foundations.
"""
import os
from functools import partial

from a2qt import QtCore, QtGui, QtWidgets

import a2core
import a2ctrl
import a2util
from a2ctrl import Icons
from a2widget import local_script

LOCAL_MENU_PREFIX = 'local: '
DELAYED_CHECK_DELAY = 250


class DrawCtrlMixin:
    """
    Display widget to host everything that you want to show to the
    user for him to set up on your module.
    """

    def __init__(self, main, cfg, mod, user_cfg=None):
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self.cfg = cfg
        self.mod = mod

        self._check_scheduled = False
        self.is_expandable_widget = False
        self._check_timer = QtCore.QTimer()
        self._check_timer.setInterval(DELAYED_CHECK_DELAY)
        self._check_timer.timeout.connect(self._check)
        self._check_args = None
        self.user_cfg = user_cfg or {}

    def get_user_value(self, typ, name=None, default=None):
        """
        Get a user value. 'value'
        Name is 'value' by default so you can just get the default value by stating the type. Voila!
        """
        return a2ctrl.get_cfg_value(self.cfg, self.user_cfg, name, typ, default)

    def get_user_dict(self):
        """
        Get element configuration PLUS anything set from the user.
        :return: Dictionary with user values inserted.
        """
        user_dict = {}
        for key in set(list(self.user_cfg) + list(self.cfg)):
            try:
                user_dict[key] = self.user_cfg[key]
            except (TypeError, KeyError):
                user_dict[key] = self.cfg[key]
        return user_dict

    def set_user_value(self, value, name=None):
        """
        Set a user value in the module config.
        Name is None by by default so you can just set the default value by ... well:
        passing the value. Voila!
        """
        try:
            self.mod.set_user_cfg(self.cfg, value, name)
        except AttributeError:
            # cannot set config if no module given
            pass

    def has_user_cfg(self):
        """
        Tell if the element has user data saved.
        :rtype: bool
        """
        if self.mod is None:
            return False
        name = a2util.get_cfg_default_name(self.cfg)
        return self.mod.is_in_user_cfg(name)

    def clear_user_cfg(self):
        name = a2util.get_cfg_default_name(self.cfg)
        self.mod.clear_user_cfg_name(name)
        self.main.load_runtime_and_ui()

    def change(self, specific=None):
        """
        Triggers the module to save it's settings to the database and
        a2 include rewrite and restart if the module is enabled.
        """
        if self.mod is None:
            return

        self.mod.change()
        if self.mod.enabled:
            self.main.settings_changed(specific)

    def delayed_check(self, *args):
        """
        Calls the check method with a little delay to prevent spamming reload.
        """
        self._check_args = args
        self._check_timer.start()

    def _check(self):
        if self._check_timer.isActive():
            self._check_timer.stop()
        self.check(*self._check_args)

    def check(self, *args):
        """
        For the element to gather data from the widgets and call change on demand.
        To be re-implemented when subclassing DrawCtrl.
        """
        pass

    def get_ui_value(self):
        raise NotImplementedError('get_ui_value Implementation Missing!')

    def default_check(self, *args):
        if args:
            value = args[0]
        else:
            value = self.get_ui_value()

        # prevent being called double
        if self.value == value:
            return

        self.value = value
        self.set_user_value(value)
        self.change('variables')


class DrawCtrl(QtWidgets.QWidget, DrawCtrlMixin):
    """
    Display widget to host everything that you want to show to the
    user for him to set up on your module.
    """

    def __init__(self, main, cfg, mod, user_cfg=None):
        super(DrawCtrl, self).__init__(parent=main)
        DrawCtrlMixin.__init__(self, main, cfg, mod, user_cfg)


class EditCtrl(QtWidgets.QGroupBox):
    """
    frame widget for an edit control which enables basic arrangement of the
    control up & down as well as deleting the control.

    It's made to work with handwritten and compiled Uis right away.
    To embedd a compiled ui tell it so add_layout=False in the super()-statement:
        super(MyNewCtrl, self).__init__(add_layout=False)
    state the mainWidget in setupUi:
        self.ui.setupUi(self.mainWidget)
    and then set the self.mainWidget-layout to your top layout in the compiled ui:
        self.mainWidget.setLayout(self.ui.mytoplayout)

    TODO: currently this is embedded as menuitems on a button which is pretty shitty.
        I'd like to have some actual up/down buttons and an x to indicate delete
        functionality
    """

    delete_requested = QtCore.Signal()
    move_rel_requested = QtCore.Signal(int)
    move_abs_requested = QtCore.Signal(bool)
    duplicate_requested = QtCore.Signal()
    cut_requested = QtCore.Signal()

    def __init__(self, cfg, main, parent_cfg, add_layout=True):
        super(EditCtrl, self).__init__()
        self.a2 = a2core.A2Obj.inst()
        self.cfg = cfg
        self.main = main
        self.parent_cfg = parent_cfg

        self._setup_ui(add_layout)
        self.helpUrl = self.a2.urls.helpEditCtrl
        self.is_expandable_widget = False

    @staticmethod
    def element_name():
        return 'EditCtrl'

    @staticmethod
    def element_icon():
        return None

    def move(self, value, *args):
        if self.parent_cfg and self.parent_cfg[0].get('typ', '') == 'nfo':
            top_index = 1
        else:
            top_index = 0

        index = None
        for i, cfg in enumerate(self.parent_cfg):
            if self.cfg is cfg:
                index = i
                break
        if index is None:
            index = self.parent_cfg.index(self.cfg)

        max_index = len(self.parent_cfg) - 1
        if isinstance(value, bool):
            if value:
                newindex = top_index
            else:
                newindex = max_index
        else:
            newindex = index + value
        # hop out if already at start or end
        if index == newindex or newindex < top_index or newindex > max_index:
            # print('returning from move! curr/new/max: %s/%s/%s' % (index, newindex, max_index))
            return

        # cfg = self.parent_cfg.pop(index)
        self.parent_cfg.pop(index)
        self.parent_cfg.insert(newindex, self.cfg)
        self.main.edit_mod()

    def delete(self):
        self.delete_requested.emit()

        if self.cfg in self.parent_cfg:
            self.parent_cfg.remove(self.cfg)
            self.main.edit_mod()

    def duplicate(self):
        from copy import deepcopy

        new_cfg = deepcopy(self.cfg)
        if 'name' in new_cfg:
            new_cfg['name'] = self.increase_name_number(new_cfg['name'])
        self.parent_cfg.append(new_cfg)
        self.main.edit_mod()

    def cut(self):
        from copy import deepcopy

        self.main.edit_clipboard.append(deepcopy(self.cfg))
        self.delete()

    def help(self):
        a2util.surf_to(self.helpUrl)

    def _setup_ui(self, add_layout):
        # self.setTitle(self.cfg['typ'])
        self.setTitle(self.element_name())
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
        )
        self.setSizePolicy(size_policy)

        self._ctrl_layout = QtWidgets.QGridLayout(self)
        self._ctrl_layout.setContentsMargins(0, 0, 0, 0)
        self._sub_layout = QtWidgets.QHBoxLayout()

        margin = self.get_style_value('margin', 8)
        self._sub_layout.setContentsMargins(margin, margin, margin, margin)

        self.mainWidget = QtWidgets.QWidget(self)
        self._sub_layout.addWidget(self.mainWidget)
        self._ctrl_layout.addLayout(self._sub_layout, 0, 0, 1, 1)

        if add_layout:
            self.mainLayout = QtWidgets.QVBoxLayout()
            spacing = self.get_style_value('small_spacing', 5)
            self.mainLayout.setContentsMargins(spacing, spacing, spacing, spacing)
            self.mainWidget.setLayout(self.mainLayout)

        self._ctrl_button_layout = QtWidgets.QVBoxLayout()
        self._ctrl_button_layout.setSpacing(0)
        self._ctrl_button_layout.setContentsMargins(0, 0, 0, 0)

        self._ctrl_button = QtWidgets.QToolButton(self)
        self._ctrl_button.setIcon(Icons.inst().more)
        button_size = self.get_style_value('icon_size', 32)
        self._ctrl_button.setMinimumSize(QtCore.QSize(button_size, button_size))
        self._ctrl_button.setMaximumSize(QtCore.QSize(button_size, button_size))
        self._ctrl_button.setIconSize(QtCore.QSize(button_size, button_size))
        self._ctrl_button.setAutoRaise(True)
        self._ctrl_button_layout.addWidget(self._ctrl_button)

        self._ctrl_button_layout.setAlignment(
            self._ctrl_button, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight
        )

        self._ctrl_layout.addLayout(self._ctrl_button_layout, 0, 0, 1, 1)

        self._ctrl_menu = QtWidgets.QMenu(self)
        self._ctrl_button.clicked.connect(self._build_menu)
        self._ctrl_button.setVisible(False)

    def _build_menu(self):
        """
        TODO: don't show top/to top, bottom/to bottom when already at top/bottom
        """
        self._ctrl_menu.clear()
        icons = Icons.inst()
        menu_items = [
            ('Up', partial(self.move, -1), icons.up),
            ('Down', partial(self.move, 1), icons.down),
            ('To Top', partial(self.move, True), icons.up_align),
            ('To Bottom', partial(self.move, False), icons.down_align),
            ('Delete', self.delete, icons.delete),
            ('Duplicate', self.duplicate, icons.copy),
            ('Help on %s' % self.element_name(), self.help, icons.help),
        ]

        clipboard_count = ''
        if self.main.edit_clipboard:
            clipboard_count = ' (%i)' % len(self.main.edit_clipboard)

        if self.cfg.get('typ') == 'group':
            menu_items.insert(-1, ('Paste' + clipboard_count, self.paste, icons.paste))
        else:
            menu_items.insert(-1, ('Cut' + clipboard_count, self.cut, icons.cut))

        for label, func, icon in menu_items:
            action = self._ctrl_menu.addAction(icon, label, func)
        self._ctrl_menu.insertSeparator(action)
        self._ctrl_menu.popup(QtGui.QCursor.pos())

    def check_new_name(self):
        """
        If no name set yet, like on new controls this creates a new unique
        name for the control from the module name + control type + incremental number
        """
        if 'name' not in self.cfg:
            # build the base control name
            new_name = '%s_%s' % (self.main.mod.name, self.element_name())
            new_name = new_name.replace(' ', '_')
            self.cfg['name'] = self.increase_name_number(new_name)

    def increase_name_number(self, name):
        """
        Look up the current controls to find a free number for given name.
        """
        names = [e.get('name') for e in a2ctrl.iter_element_cfg_type(self.main.temp_config)]
        names = [n for n in names if n is not None]
        new_name = a2util.get_next_free_number(name, names)
        return new_name

    def enterEvent(self, event):
        self._ctrl_button.setVisible(True)
        return QtWidgets.QGroupBox.enterEvent(self, event)

    def leaveEvent(self, event):
        self._ctrl_button.setVisible(False)
        return QtWidgets.QGroupBox.leaveEvent(self, event)

    def get_style_value(self, value_name, default=None):
        """Retrieve a value from the main style builder."""
        try:
            return self.main.style.get(value_name, default)
        except AttributeError:
            return default


class EditAddElem(QtWidgets.QWidget):
    """
    to add a control to a module setup. This will probably go into some popup
    later. This way its a little too clunky I think.

        * include > script1.ahk
                    script2.ahk
                    create new script
        * hotkey
        * checkBox
        * ...

    TIL: if you don't make this a widget and just a object Qt will forget about
    any connections you make!
    """

    def __init__(self, main, config, name=None):
        super(EditAddElem, self).__init__()
        self.main = main
        self.config = config

        self.base_layout = QtWidgets.QHBoxLayout(self)
        self.base_layout.setSpacing(5)

        name = 'Add Element' if name is None else name
        self.a2add_button = QtWidgets.QPushButton(name)
        self.a2add_button.setObjectName('a2add_button')
        self.a2add_button.clicked.connect(self.build_menu)
        self.a2add_button.setIcon(Icons.inst().list_add)
        self.base_layout.addWidget(self.a2add_button)

        self.menu = QtWidgets.QMenu(self)
        self.menu_include = None
        self.base_layout.setAlignment(self.a2add_button, QtCore.Qt.AlignLeft)
        self.is_expandable_widget = False

    def build_menu(self):
        self.menu.clear()
        self.menu_include = LocalAHKScriptsMenu(self, self.main)
        self.menu_include.script_selected.connect(self._on_add_include)
        self.menu.addMenu(self.menu_include)

        import a2element

        for name, display_name, icon in a2element.get_list():
            action = self.menu.addAction(display_name, self._on_add_element_action)
            action.setData((name, None))
            if icon:
                action.setIcon(icon)

        self.menu.addSeparator()
        self.menu.addAction(self.main.ui.actionCreate_New_Element)
        self._check_for_local_element_mods()
        self.menu.popup(QtGui.QCursor.pos())

    def _on_add_include(self, file_name, _name):
        self._add_element('include', file_name)

    def _on_add_element_action(self):
        typ, name = self.sender().data()
        self._add_element(typ, name)

    def _add_element(self, typ, name=None):
        """
        Just adds a new dict with the according typ value to the temp_config.
        Only if it's an include we already enter the file selected.
        Every other default value will be handled by the very control element.
        """
        cfg = {'typ': typ}
        if typ == 'include':
            cfg['file'] = name
        elif name:
            cfg['name'] = name

        self.config.append(cfg)
        self.main.edit_mod()

    def _check_for_local_element_mods(self):
        if self.main.mod is None:
            return

        for item in os.scandir(self.main.mod.path):
            if not item.is_file():
                continue
            base, ext = os.path.splitext(item.name)
            if not base.startswith(a2ctrl.LOCAL_ELEMENT_ID) or ext.lower() != '.py':
                continue

            element_module = a2ctrl.get_local_element(item.path)
            if element_module is None:
                continue

            edit_class = getattr(element_module, 'Edit')
            display_name = edit_class.element_name()
            icon = edit_class.element_icon()
            name = base[len(a2ctrl.LOCAL_ELEMENT_ID) + 1 :]
            action = self.menu.addAction(
                LOCAL_MENU_PREFIX + display_name, self._on_add_element_action
            )
            action.setData((a2ctrl.LOCAL_ELEMENT_ID, name))
            if icon:
                action.setIcon(icon)


class LocalAHKScriptsMenu(local_script.BrowseScriptsMenu):
    """Selection menu for module-local Autohotkey scripts."""

    # script_selected = QtCore.Signal(tuple)

    def __init__(self, parent, main):
        super(LocalAHKScriptsMenu, self).__init__(parent, main)
        import a2ahk

        self.setTitle('Include Script')
        self.dialog_title = 'New Autohotkey Script'
        self.dialog_msg = 'Give a name for the new Autohotkety script:'
        self.extension = a2ahk.EXTENSION
        self.on_create_name_check = self.main.mod.check_create_script

    def get_available_scripts(self):
        scripts_used = set()
        for cfg in a2ctrl.iter_element_cfg_type(self.main.temp_config, 'include'):
            scripts_used.add(cfg['file'].lower())

        available = [name for name in self.main.mod.scripts if name.lower() not in scripts_used]
        return available

    def create_script(self, file_name):
        self.main.mod.create_script(file_name, self.main.devset.author_name)
