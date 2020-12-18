"""
Home of the A2ItemEditor Lister widget.
"""
from collections import OrderedDict

from PySide6 import QtCore, QtWidgets

import a2core
import a2ctrl.connect
import a2ctrl.icons
from a2widget import a2item_editor_ui


log = a2core.get_logger(__name__)
#: Minimum number of to automatically show the search field.
SEARCH_FIELD_MIN_ITEMS = 10
DEFAULT_ITEM_FLAGS = (
    QtCore.Qt.ItemIsSelectable
    | QtCore.Qt.ItemIsEditable
    | QtCore.Qt.ItemIsDragEnabled
    | QtCore.Qt.ItemIsEnabled
)


class A2ItemEditor(QtWidgets.QWidget):
    """A lister widget for editing complex data dictionaries."""

    selected_name_changed = QtCore.Signal(str)
    selection_changed = QtCore.Signal(list)
    item_changed = QtCore.Signal(tuple)
    item_deleted = QtCore.Signal(str)
    data_changed = QtCore.Signal()
    _value_changed = QtCore.Signal(str)
    list_menu_called = QtCore.Signal(QtWidgets.QMenu)

    data = {}

    def __init__(self, *args, **kwargs):
        super(A2ItemEditor, self).__init__(*args, **kwargs)
        a2ctrl.check_ui_module(a2item_editor_ui)
        self._drawing = True
        self.ui = a2item_editor_ui.Ui_A2ItemEditor()
        self.ui.setupUi(self)

        self.ui.config_layout = QtWidgets.QFormLayout(self.ui.config_widget)
        self.ui.config_layout.setContentsMargins(0, 0, 0, 0)

        self._data_widgets = OrderedDict()

        self.search_field_min_items = SEARCH_FIELD_MIN_ITEMS
        self.item_flags = DEFAULT_ITEM_FLAGS
        self.fill_item_list()

        self._selected_name = None

        icons = a2ctrl.icons.Icons.inst()
        self.ui.item_list.itemChanged.connect(self.check_item_change)
        self.ui.item_list.context_menu_requested.connect(self.list_menu_called.emit)
        self.ui.item_list.items_removed.connect(self._on_items_removed)
        self.ui.item_list.items_selected.connect(self._on_selection_change)

        self.ui.a2item_editor_add_button.clicked.connect(self.add_item)
        self.ui.a2item_editor_add_button.setIcon(icons.list_add)

        self.ui.a2item_editor_remove_button.setIcon(icons.clear)
        self.ui.a2item_editor_remove_button.clicked.connect(self.ui.item_list.remove_selected)

        self._drawing = False
        self._current_data = {}
        self.selected_name_changed.connect(self.draw_data)

        self._value_changed.connect(self.update_data)

        self.ui.search_field.textChanged.connect(self.update_filter)
        self.ui.a2search_x_button.clicked.connect(self.reset_filter)
        self.ui.a2search_x_button.setIcon(icons.clear)
        self.update_filter()

    def set_data(self, data):
        """Fill in some data."""
        self.data = data
        self.fill_item_list()

    def add_data_label_widget(
        self, value_name, widget, set_function, change_signal=None, default_value=None, label=None
    ):
        """
        :param str value_name: Name of the data item to control.
        :param QtWidgets.QWidget widget: The QWidget object to put into the layout.
        :param function set_function: Widget member function to display its current data.
        :param QtCore.Signal change_signal: Optional signal to use for data change notification.
        :param * default_value: Fallback and reference value to check against.
        :param str label: Optional string to put into the Label Field of a FormLayout.
        """
        label = label if label is not None else value_name.title()
        # self.ui.config_layout.addRow(label, widget)
        self.add_row(label, widget)
        self._add_data_widget(value_name, widget, set_function, change_signal, default_value)

    def add_data_widget(
        self, value_name, widget, set_function, change_signal=None, default_value=None
    ):
        """
        Fills the config_layout with a control and connects it to the data.

        :param str value_name: Name of the data item to control.
        :param QtWidgets.QWidget widget: The QWidget object to put into the layout.
        :param function set_function: Function object of widget to use to display the current data.
        :param QtCore.Signal change_signal: Optional signal to use for data change notification.
        :param * default_value: Fallback and reference value to check against.
        """
        self.add_row(widget)
        self._add_data_widget(value_name, widget, set_function, change_signal, default_value)

    def add_row(self, *args):
        self.ui.config_layout.addRow(*args)

    def _add_data_widget(self, value_name, widget, set_function, change_signal, default_value):
        self._drawing = True
        self._data_widgets[value_name] = {
            'widget': widget,
            'set_function': set_function,
            'change_signal': change_signal,
            'default_value': default_value,
        }

        a2ctrl.connect.control(
            widget, value_name, self._current_data, self._value_changed, change_signal
        )

        self._drawing = False

    def draw_data(self, item_name):
        """Fill the ui with the data from selected item."""
        self._drawing = True
        for value_name, widget_dict in self._data_widgets.items():
            value = self.data.get(item_name, {}).get(value_name, widget_dict['default_value'])
            widget_dict['set_function'](value)
            self._current_data[value_name] = value

        self._drawing = False

    def update_data(self):
        """
        Shall always update the config but not trigger change if there was no text set
        and text was not deleted.
        """
        if self._drawing:
            return

        diff_dict = {}
        for value_name, widget_dict in self._data_widgets.items():
            value = self._current_data.get(value_name)
            if value != widget_dict['default_value']:
                diff_dict[value_name] = value

        if self.data[self.selected_name] != diff_dict:
            self.data[self.selected_name] = diff_dict
            self.data_changed.emit()

    def check_item_change(self, item):
        """Detect name changes and handle data move."""
        new_name = item.text()
        old_name = self._selected_name
        if new_name != old_name:
            self._selected_name = new_name
            data = self.data.pop(old_name) if old_name else {}

            self.data[new_name] = data
            self.draw_data(new_name)

            self.data_changed.emit()
            self.item_changed.emit((old_name, new_name, item))

    @property
    def item_names(self):
        """Return list of all items."""
        return self.ui.item_list.get_names()

    def fill_item_list(self):
        """Put available keys from data to the item list."""
        self.ui.item_list.clear()
        for item_name in sorted(self.data.keys(), key=str.lower):
            self._add_and_setup_item(item_name)
        # enable search field only when there are more than x enties
        self.enable_search_field(len(self.data) > self.search_field_min_items)

    @property
    def selected_name(self):
        """String name of currently selected item."""
        return self._selected_name

    def _on_selection_change(self, item_objs):
        self.selection_changed.emit(item_objs)

        text = item_objs[0].text() if item_objs else ''
        if text != self._selected_name:
            self._selected_name = text
            self.selected_name_changed.emit(text)

        self.ui.config_widget.setEnabled(item_objs != [])
        self.ui.a2item_editor_remove_button.setEnabled(item_objs != [])

    def _add_and_setup_item(self, name):
        item = QtWidgets.QListWidgetItem(name)
        item.setFlags(self.item_flags)
        self.ui.item_list.addItem(item)
        return item

    def add_item(self):
        """Add empty entry to the list and enable edit mode for user to type."""
        self.ui.item_list.editItem(self.add_named_item())

    def add_named_item(self, name=''):
        """Add and select a new item with a given or empty string name."""
        item = self._add_and_setup_item(name)
        self.ui.item_list.select_items([item])
        return item

    def _on_items_removed(self, item_objs):
        for item in item_objs:
            item_name = item.text()
            try:
                self.data.pop(item_name)
                self.data_changed.emit()
                self.item_deleted.emit(item_name)
            except KeyError:
                pass

    def update_filter(self, text=None):
        """
        Hides or shows all the items according to the filter.
        :param text:
        :return:
        """
        if not text:
            self.ui.a2search_x_button.setVisible(False)
            for item in self.ui.item_list.iter_items():
                item.setHidden(False)
        else:
            self.ui.a2search_x_button.setVisible(True)
            items = self.ui.item_list.findItems(text, QtCore.Qt.MatchContains)
            item_ids = [id(i) for i in items]
            for item in self.ui.item_list.iter_items():
                item.setHidden(id(item) not in item_ids)

    def reset_filter(self):
        """Reset Search filter so all entries are shown."""
        self.ui.search_field.setText('')

    def enable_search_field(self, state):
        """Set the visible state of the field."""
        self.ui.search_field.setVisible(state)

    def delete_item(self):
        """Delete selected items from the list."""
        self.ui.item_list.remove_selected()
