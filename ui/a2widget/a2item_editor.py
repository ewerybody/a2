"""
a2widget.a2item_editor

@created: Sep 26, 2016
@author: eRiC
"""
import a2ctrl.qlist
import a2ctrl.connect
from PySide2 import QtCore, QtWidgets
from a2widget import a2item_editor_ui
from collections import OrderedDict


class A2ItemEditor(QtWidgets.QWidget):
    selected_name_changed = QtCore.Signal(str)
    selection_changed = QtCore.Signal(list)
    item_changed = QtCore.Signal(tuple)
    item_deleted = QtCore.Signal(str)
    data_changed = QtCore.Signal()
    _value_changed = QtCore.Signal(str)

    data = {}
    draw_labels = True

    def __init__(self, *args, **kwargs):
        super(A2ItemEditor, self).__init__(*args, **kwargs)
        a2ctrl.check_ui_module(a2item_editor_ui)
        self._drawing = True
        self.ui = a2item_editor_ui.Ui_A2ItemEditor()
        self.ui.setupUi(self)

        if self.draw_labels:
            self.ui.config_layout = QtWidgets.QFormLayout(self.ui.config_widget)
        else:
            self.ui.config_layout = QtWidgets.QVBoxLayout(self.ui.config_widget)

        contents_margins = self.ui.config_layout.contentsMargins()
        contents_margins.setTop(0)
        self.ui.config_layout.setContentsMargins(contents_margins)

        self.ui.config_widget.setLayout(self.ui.config_layout)
        self._data_widgets = OrderedDict()

        self.fill_item_list()

        self._selected_name = None

        self.ui.item_list.itemChanged.connect(self.check_item_change)
        self.ui.item_list.keyPressEvent = self.item_list_keyPressEvent
        self.ui.add_entry_button.clicked.connect(self.add_item)
        self.ui.del_entry_button.clicked.connect(self.delete_item)

        self.ui.item_list.itemSelectionChanged.connect(self.selection_change)
        self._drawing = False
        self._current_data = {}
        self.selected_name_changed.connect(self.draw_data)

        self._value_changed.connect(self.update_data)

        self.ui.search_field.textChanged.connect(self.update_filter)
        self.ui.a2search_x_button.clicked.connect(self.reset_filter)
        self.ui.a2search_x_button.setIcon(a2ctrl.Icons.inst().clear)
        self.update_filter()

    def add_data_widget(self, value_name, widget, set_function, change_signal=None,
                        default_value=None, label=None):
        """
        Fills the config_layout with a control and connects it to the data.

        :param str value_name: Name of the data item to control.
        :param QtWidgets.QWidget widget: The QWidget object to put into the layout.
        :param function set_function: Function object of the widget to use to display the current data.
        :param QtCore.Signal change_signal: Optional signal to use for data change notification.
        :param * default_value: Fallback and reference value to check against.
        :param str label: Optional string to put into the Label Field of a FormLayout.
        """
        self._drawing = True
        if self.draw_labels:
            this_label = label if label is not None else value_name.title()
            row_index = self.ui.config_layout.rowCount()
            self.ui.config_layout.setWidget(row_index, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel(this_label))
            self.ui.config_layout.setWidget(row_index, QtWidgets.QFormLayout.FieldRole, widget)
        else:
            self.ui.config_layout.addWidget(widget)

        self._data_widgets[value_name] = {'widget': widget,
                                          'set_function': set_function,
                                          'change_signal': change_signal,
                                          'default_value': default_value}

        a2ctrl.connect.control(widget, value_name, self._current_data, self._value_changed, change_signal)

        self._drawing = False

    def draw_data(self, item_name):
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
        return a2ctrl.qlist.get_items_as_text(self.ui.item_list)

    def fill_item_list(self):
        self.ui.item_list.clear()
        for item_name in sorted(self.data.keys(), key=str.lower):
            self._add_and_setup_item(item_name)

    @property
    def selected_name(self):
        return self._selected_name

    def selection_change(self):
        item_objs = self.ui.item_list.selectedItems()
        self.selection_changed.emit(item_objs)

        text = item_objs[0].text() if item_objs else ''
        if text != self._selected_name:
            self._selected_name = text
            self.selected_name_changed.emit(text)

        self.ui.config_widget.setEnabled(item_objs != [])
        self.ui.del_entry_button.setEnabled(item_objs != [])

    def item_list_keyPressEvent(self, event):
        """
        Capture delete key to remove entries
        """
        if event.key() == QtCore.Qt.Key_Delete:
            self.delete_item()
        return QtWidgets.QListWidget.keyPressEvent(self.ui.item_list, event)

    def _add_and_setup_item(self, name):
        item = QtWidgets.QListWidgetItem(name)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable |
                      QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
        self.ui.item_list.addItem(item)
        return item

    def add_item(self):
        new_item_name = ''
        item = self._add_and_setup_item(new_item_name)
        self.ui.item_list.editItem(item)
        a2ctrl.qlist.select_items(self.ui.item_list, item)

    def delete_item(self):
        item_objs = self.ui.item_list.selectedItems()
        for item in item_objs:
            item_row = self.ui.item_list.row(item)
            self.ui.item_list.takeItem(item_row)
        item_name = item_objs[0].text()
        try:
            self.data.pop(item_name)
            self.data_changed.emit()
            self.item_deleted.emit(item_name)
        except KeyError:
            pass

    def update_filter(self, text=None):
        all_items = a2ctrl.qlist.get_all_items(self.ui.item_list)
        if not text:
            self.ui.a2search_x_button.setVisible(False)
            [i.setHidden(False) for i in all_items]
        else:
            self.ui.a2search_x_button.setVisible(True)
            items = self.ui.item_list.findItems(text, QtCore.Qt.MatchContains)
            item_ids = [id(i) for i in items]
            for item in all_items:
                item.setHidden(id(item) not in item_ids)

    def reset_filter(self):
        self.ui.search_field.setText('')
