from copy import deepcopy
from a2ctrl import connect

import a2mod
import a2core
import a2util
import a2ctrl
import a2element.common
import a2element._edit
import a2element.group
from a2ctrl import Icons

from a2qt import QtWidgets, QtGui


class EditView(QtWidgets.QWidget):
    def __init__(self, parent, config_list):
        super(EditView, self).__init__(parent)
        self.elements = []
        self.config_list = config_list
        self.main = parent

        if not config_list:
            new_cfg = a2mod.NEW_MODULE_CFG.copy()
            new_cfg['description'] = a2mod.NEW_MODULE_DESC % self.main.mod.name
            new_cfg['date'] = a2util.get_date()
            new_cfg['author'] = self.main.devset.author_name
            config_list.insert(0, new_cfg)

        self.edit_layout = QtWidgets.QVBoxLayout(self)
        self._elemenu = QtWidgets.QMenu(self)

        self._draw()

    def _draw(self):
        for element in self.elements:
            element.deleteLater()
        self.elements.clear()

        for cfg in self.config_list:
            element = self._build_element(cfg, self.config_list)
            if element is None:
                continue

            if cfg.get('typ', '') == 'group':
                sub_elements = []
                for sub_cfg in cfg['children']:
                    sub_element = self._build_element(sub_cfg, cfg['children'])
                    if sub_element is None:
                        continue
                    sub_elements.append(sub_element)
                element.fill_elements(sub_elements)

            self.edit_layout.addWidget(element)
            self.elements.append(element)

        # amend a spacer
        policy = QtWidgets.QSizePolicy
        spacer = QtWidgets.QSpacerItem(10, 60, policy.Minimum, policy.Minimum)
        self.edit_layout.addItem(spacer)

        self.setSizePolicy(policy(policy.Preferred, policy.Maximum))

    def _build_element(self, cfg, parent_cfg):
        element = a2ctrl.edit(cfg, self.main, parent_cfg)
        new_name = self._check_new_name(cfg)
        if new_name and element is not None:
            if hasattr(element, 'ui') and hasattr(element.ui, 'cfg_name'):
                name_widget = getattr(element.ui, 'cfg_name')
                name_widget.setText(new_name)

        if isinstance(element, a2element.common.EditCtrl):
            element.menu_requested.connect(self._build_elemenu)
            element.changed.connect(self._draw)
        return element

    def _build_elemenu(self):
        element, index, parent = self._element_index()
        self._elemenu.clear()

        menu_items = []
        if (parent.max_index - parent.top_index):
            if index != parent.top_index:
                menu_items.append(('Up', self.move_up, Icons.up))
            if index != parent.max_index:
                menu_items.append(('Down', self.move_down, Icons.down))
            if index != parent.top_index:
                menu_items.append(('To Top', self.move_top, Icons.up_align))
            if index != parent.max_index:
                menu_items.append(('To Bottom', self.move_bottom, Icons.down_align))
        menu_items.extend(
            [
                ('Delete', self.delete_element, Icons.delete),
                ('Duplicate', self.duplicate, Icons.copy),
                ('Help on %s' % element.element_name(), self.help, Icons.help),
            ]
        )

        clipboard_count = ''
        if self.main.edit_clipboard:
            clipboard_count = ' (%i)' % len(self.main.edit_clipboard)

        if element.cfg.get('typ') == 'group':
            menu_items.insert(-1, ('Paste' + clipboard_count, self.paste, Icons.paste))
        else:
            menu_items.insert(-1, ('Cut' + clipboard_count, self.cut, Icons.cut))

        action = None
        for label, func, icon in menu_items:
            action = self._elemenu.addAction(icon, label, func)
            action.setData(element)

        if action is not None:
            self._elemenu.insertSeparator(action)
        self._elemenu.popup(QtGui.QCursor.pos())

    @property
    def max_index(self):
        """Give index of the last element config."""
        return len(self.config_list) - 1

    @property
    def top_index(self):
        """Give index of the first element config."""
        if self.config_list and self.config_list[0].get('typ', '') == 'nfo':
            return 1
        return 0

    def get_cfg_copy(self) -> list:
        return deepcopy(self.config_list)

    def add_element(self, config):
        self.config_list.append(config)
        self._draw()

    def _element_index(self):
        sender = self.sender()
        if isinstance(sender, QtGui.QAction):
            element = sender.data()
        else:
            element = sender

        if not isinstance(element, a2element.common.EditCtrl):
            raise TypeError('Not an EditCtrl type!')

        try:
            return element, self.elements.index(element), self
        except ValueError:
            for other in self.elements:
                if not isinstance(other, a2element.group.Edit):
                    continue
                try:
                    return element, self.elements[6].get_child_index(element), other
                except ValueError:
                    continue
        raise RuntimeError(f'Element could not be found! {element}')

    def move_up(self):
        element, index, parent = self._element_index()
        self._move_to(element, index, max(index - 1, parent.top_index), parent)

    def move_top(self):
        element, index, parent = self._element_index()
        self._move_to(element, index, parent.top_index, parent)

    def move_down(self):
        element, index, parent = self._element_index()
        self._move_to(element, index, min(index + 1, parent.max_index), parent)

    def move_bottom(self):
        element, index, parent = self._element_index()
        self._move_to(element, index, parent.max_index, parent)

    def _move_to(self, element: a2element.common.EditCtrl, from_index: int, to_index: int, parent):
        parent.config_list.pop(from_index)
        parent.config_list.insert(to_index, element.cfg)
        self._draw()

    def duplicate(self):
        element, index, parent = self._element_index()
        new_cfg = deepcopy(element.cfg)
        if 'name' in new_cfg:
            new_cfg['name'] = self._increase_name_number(new_cfg['name'])
        parent.config_list.insert(index + 1, new_cfg)
        self._draw()

    def _increase_name_number(self, name):
        names = [e.get('name') for e in a2ctrl.iter_element_cfg_type(self.config_list)]
        names = [n for n in names if n is not None]
        new_name = a2util.get_next_free_number(name, names)
        return new_name

    def help(self):
        element, _, _ = self._element_index()
        if element.help_url:
            url = element.help_url
        else:
            a2 = a2core.A2Obj.inst()
            url = a2.urls.wiki + element.element_name() + '-element'
        a2util.surf_to(url)

    def paste(self):
        """
        Amends child list with cfgs from the main edit_clipboard
        and flushes it afterwards.
        """
        group, index, parent = self._element_index()
        group.config_list.extend(self.main.edit_clipboard)
        self.main.edit_clipboard.clear()
        self._draw()

    def cut(self):
        element, index, parent = self._element_index()

        self.main.edit_clipboard.append(deepcopy(element.cfg))
        parent.config_list.pop(index)
        self._draw()

    def delete_element(self):
        element, index, parent = self._element_index()
        parent.config_list.pop(index)
        self._draw()

    def _check_new_name(self, config):
        """
        If no name set yet, like on new controls this creates a new unique
        name for the control from the module name + control type + incremental number
        """
        if 'name' not in config or config['name'] != '':
            return
        new_name = '%s_%s' % (self.main.mod.name, config['typ'].title())
        new_name = new_name.replace(' ', '_')
        config['name'] = self._increase_name_number(new_name)
        return new_name

    def on_menu_button_clicked(self):
        pass