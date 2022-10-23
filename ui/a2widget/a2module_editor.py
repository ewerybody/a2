from copy import deepcopy

import a2mod
import a2core
import a2util
import a2ctrl
import a2element.common
import a2element._edit
import a2element.group
from a2ctrl import Icons

from a2qt import QtCore, QtWidgets, QtGui

ISSUE_DOUBLE = (
    'Double name! Variable "<b>%s</b>" already defined<br>'
    'in other element "<b>%s</b>" at position %i'
)
ISSUE_TAKEN = 'Name taken! Variable "<b>%s</b>" already defined<br>in other module <b>%s</b>'
_EDIT_CACHE = []


class EditView(QtWidgets.QWidget):
    scroll_request = QtCore.Signal(int)

    def __init__(self, parent, config_list):
        super(EditView, self).__init__(parent)
        self.elements = []  # type: list[QtWidgets.QWidget]
        self._indexed_elements = []  # type: list[a2element.common.EditCtrl]
        self.config_list = config_list  # type: list[dict]
        self.main = parent

        if not config_list:
            new_cfg = a2mod.NEW_MODULE_CFG.copy()
            new_cfg['description'] = a2mod.NEW_MODULE_DESC % self.main.mod.name
            new_cfg['date'] = a2util.get_date()
            new_cfg['author'] = self.main.devset.author_name
            config_list.insert(0, new_cfg)

        self.edit_layout = QtWidgets.QVBoxLayout(self)
        self._elemenu = QtWidgets.QMenu(self)
        self._spacer = None
        self._draw()

    def _draw(self):
        for element in self.elements:
            element.deleteLater()
        self.elements.clear()
        self._indexed_elements.clear()

        for cfg in self.config_list:
            element = self._build_element(cfg, self.config_list)
            self._indexed_elements.append(element)
            if element is None:
                continue

            if isinstance(element, a2element.group.Edit):
                sub_elements = []
                for sub_cfg in cfg['children']:
                    sub_element = self._build_element(sub_cfg, cfg['children'])
                    self._indexed_elements.append(sub_element)
                    if sub_element is None:
                        continue
                    sub_elements.append(sub_element)
                element.fill_elements(sub_elements)

            self.edit_layout.addWidget(element)
            self.elements.append(element)

        # amend a spacer
        if self._spacer is None:
            policy = QtWidgets.QSizePolicy
            self._spacer = QtWidgets.QSpacerItem(10, 60, policy.Minimum, policy.Minimum)
            self.setSizePolicy(policy(policy.Preferred, policy.Maximum))
        else:
            self.edit_layout.removeItem(self._spacer)
        self.edit_layout.addItem(self._spacer)

    def _build_element(self, cfg, parent_cfg):
        element = a2ctrl.edit(cfg, self.main, parent_cfg)
        new_name = self._check_new_name(cfg)
        if new_name and element is not None:
            try:
                ui = getattr(element, 'ui')
                name_widget = getattr(ui, 'cfg_name')
                name_widget.setText(new_name)
            except AttributeError:
                pass

        if isinstance(element, a2element.common.EditCtrl):
            element.menu_requested.connect(self._build_elemenu)
            element.changed.connect(self._draw)
        return element

    def _build_elemenu(self):
        element, index, parent = self._element_index()
        self._elemenu.clear()

        menu_items = []
        if parent.max_index - parent.top_index:
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
        if _EDIT_CACHE:
            clipboard_count = ' (%i)' % len(_EDIT_CACHE)

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
                    return element, other.get_child_index(element), other
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
        if isinstance(group, a2element.group.Edit):
            group.config_list.extend(_EDIT_CACHE)
            _EDIT_CACHE.clear()
            self._draw()

    def cut(self):
        element, index, parent = self._element_index()

        _EDIT_CACHE.append(deepcopy(element.cfg))
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

    def check_issues(self):
        """Do some tests to check the validity of all elements in the editor.
        Return `True` if there is nothing to report.
        """
        import a2ahk, a2runtime

        variables = a2runtime.collect_variables()
        this_key = self.main.mod.key
        other_vars = {}
        for mod_key, var_name, _ in variables.iter_mod_variables():
            if mod_key == this_key:
                continue
            other_vars[var_name.lower()] = mod_key

        names = {}
        issues = {}
        for i, cfg in enumerate(a2ctrl.iter_element_cfg_type(self.config_list)):
            if 'name' not in cfg:
                continue
            name = cfg['name']
            _name = name.lower()

            if _name in names:
                pos = names[_name]
                other = self._indexed_elements[names[_name]].element_name()
                issues.setdefault(i, []).append(ISSUE_DOUBLE % (name, other, pos))
            else:
                names[_name] = i

            if _name in other_vars:
                issues.setdefault(i, []).append(ISSUE_TAKEN % (name, other_vars[_name]))

            result = a2ahk.check_variable_name(name)
            if result:
                issues.setdefault(i, []).append(result)

        for index, element in enumerate(self._indexed_elements):
            element_issue = element.check_issues()
            if element_issue:
                issues.setdefault(index, []).append(element_issue)

            if index in issues:
                element.setStyleSheet('QGroupBox {border-color: "red";}')
                element.setToolTip('\n'.join(issues[index]))
            else:
                element.setStyleSheet('QGroupBox {border-color: "#DDD";}')
                element.setToolTip('')

        if issues:
            first_index = sorted(issues)[0]
            element = self._indexed_elements[first_index]
            self.scroll_request.emit(element.geometry().top())

        return bool(issues)
