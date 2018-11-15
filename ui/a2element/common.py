import os
import time
from copy import deepcopy
from functools import partial

from PySide2 import QtGui, QtCore, QtWidgets

import a2core
import a2util
import a2ctrl
from a2ctrl import Icons


LOCAL_MENU_PREFIX = 'local: '


class DrawCtrlMixin(object):
    """
    Display widget to host everything that you want to show to the
    user for him to set up on your module.
    """
    def __init__(self, main, cfg, mod, user_cfg=None):
        """"
        :param bool _init_ctrl: Set False when using multiple inheritance
        to keep it from calling super() again.
        """
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self.cfg = cfg
        self.mod = mod

        self.check_delay = 250
        self._check_scheduled = False
        self.is_expandable_widget = False
        self._check_timer = QtCore.QTimer()
        self._check_timer.setInterval(self.check_delay)
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
        Gets an element configuration PLUS anything set from the user.
        :return: Dictionary with user values inserted.
        """
        user_dict = {}
        for key in set(list(self.user_cfg) + list(self.cfg)):
            try:
                user_dict[key] = self.user_cfg[key]
            except (TypeError, KeyError):
                user_dict[key] = self.cfg[key]
        return user_dict

    def set_user_value(self, this, name=None):
        """
        Set a user value in the module config.
        Name is None by by default so you can just set the default value by ... well:
        passing the value. Voila!
        """
        try:
            self.mod.set_user_cfg(self.cfg, this, name)
        except AttributeError:
            # cannot set config if no module given
            pass

    def has_user_cfg(self):
        """
        Tells you if the element has user data saved.
        :rtype: bool
        """
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

        index = self.parent_cfg.index(self.cfg)
        maxIndex = len(self.parent_cfg) - 1
        if isinstance(value, bool):
            if value:
                newindex = top_index
                # self.main.ui.scrollArea.scrollToTop()
                # self.main.ui.scrollArea
            else:
                newindex = maxIndex
                # TODO: scrolling should be done in module_view
                # self.scroll_to_bottom()
        else:
            newindex = index + value
        # hop out if already at start or end
        if index == newindex or newindex < top_index or newindex > maxIndex:
            # print('returning from move! curr/new/max: %s/%s/%s' % (index, newindex, maxIndex))
            return

        # cfg = self.parent_cfg.pop(index)
        self.parent_cfg.pop(index)
        self.parent_cfg.insert(newindex, self.cfg)
        self.main.edit_mod(keep_scroll=True)

    def delete(self):
        if self.cfg in self.parent_cfg:
            self.parent_cfg.remove(self.cfg)
            self.main.edit_mod(keep_scroll=True)

    def duplicate(self):
        newCfg = deepcopy(self.cfg)
        self.parent_cfg.append(newCfg)
        self.main.edit_mod()
        self.scroll_to_bottom()

    def cut(self):
        self.main.edit_clipboard.append(deepcopy(self.cfg))
        self.delete()

    def help(self):
        a2util.surf_to(self.helpUrl)

    def _setup_ui(self, add_layout):
        # self.setTitle(self.cfg['typ'])
        self.setTitle(self.element_name())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Maximum)
        self.setSizePolicy(sizePolicy)

        self._ctrl_layout = QtWidgets.QGridLayout(self)
        self._ctrl_layout.setContentsMargins(0, 0, 0, 0)
        self._sub_layout = QtWidgets.QHBoxLayout()

        try:
            margin = self.main.style.get('margin')
            self._sub_layout.setContentsMargins(margin, margin, margin, margin)
        except AttributeError:
            pass

        self.mainWidget = QtWidgets.QWidget(self)
        self._sub_layout.addWidget(self.mainWidget)
        self._ctrl_layout.addLayout(self._sub_layout, 0, 0, 1, 1)

        if add_layout:
            self.mainLayout = QtWidgets.QVBoxLayout()
            self.mainLayout.setContentsMargins(5, 5, 5, 5)
            self.mainWidget.setLayout(self.mainLayout)

        self._ctrl_button_layout = QtWidgets.QVBoxLayout()
        self._ctrl_button_layout.setSpacing(0)
        self._ctrl_button_layout.setContentsMargins(0, 0, 0, 0)

        self._ctrl_button = QtWidgets.QToolButton(self)
        self._ctrl_button.setIcon(Icons.inst().more)
        button_size = 32
        self._ctrl_button.setMinimumSize(QtCore.QSize(button_size, button_size))
        self._ctrl_button.setMaximumSize(QtCore.QSize(button_size, button_size))
        self._ctrl_button.setIconSize(QtCore.QSize(button_size, button_size))
        self._ctrl_button.setAutoRaise(True)
        self._ctrl_button_layout.addWidget(self._ctrl_button)

        self._ctrl_button_layout.setAlignment(
            self._ctrl_button, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

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
        menu_items = [('Up', partial(self.move, -1), icons.up),
                      ('Down', partial(self.move, 1), icons.down),
                      ('To Top', partial(self.move, True), icons.up_align),
                      ('To Bottom', partial(self.move, False), icons.down_align),
                      ('Delete', self.delete, icons.delete),
                      ('Duplicate', self.duplicate, icons.copy),
                      ('Help on %s' % self.element_name(), self.help, icons.help)]

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

            # find biggest number
            this_type = self.cfg['typ']
            controls = [cfg.get('name', '') for cfg in self.main.temp_config
                        if cfg.get('typ') == this_type]

            new_name = a2util.get_next_free_number(new_name, controls)
            self.cfg['name'] = new_name

    def scroll_to_bottom(self):
        # self._scrollValB4 = self.main.ui.scrollBar.value()
        # self._scrollMaxB4 = self.main.ui.scrollBar.maximum()
        # print('scroll_to_bottom...')
        # QtCore.QTimer.singleShot(300, self._scroll_to_bottom)
        pass

    def _scroll_to_bottom(self, *args):
        # print('scrollValB4: %s' % self._scrollValB4)
        time.sleep(0.1)
        tmax = 0.3
        curve = QtCore.QEasingCurve(QtCore.QEasingCurve.OutQuad)
        res = 0.01
        steps = tmax / res
        tsteps = 1 / steps
        t = 0.0
        # this = self.main.ui.scrollBar.value()
        scrollEnd = self.main.ui.scrollBar.maximum()
        if not scrollEnd:
            scrollEnd = self._scrollMaxB4 + 100
        r = scrollEnd - self._scrollValB4
        self.main.ui.scrollBar.setValue(self._scrollValB4)
        while t <= 1.0:
            time.sleep(res)
            t += tsteps
            v = curve.valueForProgress(t)
            scrollval = self._scrollValB4 + (v * r)
            self.main.ui.scrollBar.setValue(scrollval)

    def enterEvent(self, event):
        self._ctrl_button.setVisible(True)
        return QtWidgets.QGroupBox.enterEvent(self, event)

    def leaveEvent(self, event):
        self._ctrl_button.setVisible(False)
        return QtWidgets.QGroupBox.leaveEvent(self, event)


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
        self.menu_include = BrowseScriptsMenu(self.main)
        self.menu_include.script_selected.connect(self._add_element)
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
        if name:
            cfg['name'] = name
        if typ == 'include':
            cfg['file'] = name

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
            name = base[len(a2ctrl.LOCAL_ELEMENT_ID) + 1:]
            action = self.menu.addAction(LOCAL_MENU_PREFIX + display_name, self._on_add_element_action)
            action.setData((a2ctrl.LOCAL_ELEMENT_ID, name))
            if icon:
                action.setIcon(icon)


class BrowseScriptsMenu(QtWidgets.QMenu):
    script_selected = QtCore.Signal(tuple)

    def __init__(self, main):
        super(BrowseScriptsMenu, self).__init__()
        self.main = main
        self.setIcon(Icons.inst().code)
        self.setTitle('Include Script')
        self.aboutToShow.connect(self.build_menu)

    def build_menu(self):
        self.clear()
        scripts_in_use = set()
        for cfg in self.main.temp_config:
            if cfg['typ'] == 'include':
                scripts_in_use.add(cfg['file'])

        icons = Icons.inst()
        scripts_unused = set(self.main.mod.scripts) - scripts_in_use

        for script_name in scripts_unused:
            action = self.addAction(icons.code, script_name, self._on_action_click)
            action.setData(script_name)

        if scripts_unused:
            self.addSeparator()

        self.addAction(icons.code, 'Create New Script', self.set_script)

    def _on_action_click(self):
        self.script_selected.emit(('include', self.sender().data()))

    def set_script(self):
        from a2widget.a2input_dialog import A2InputDialog
        dialog = A2InputDialog(
            self.main, 'New Script',
            self.main.mod.check_create_script,
            text='awesomeScript',
            msg='Give a name for the new script file:')
        # dialog.okayed.connect(partial(self.set_script, create=True))
        dialog.exec_()
        if not dialog.output:
            return

        name = self.main.mod.create_script(dialog.output, self.main.devset.author_name)
        self.script_selected.emit(('include', name))
