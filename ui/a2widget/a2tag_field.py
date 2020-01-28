from functools import partial

from PySide2 import QtCore, QtWidgets

import a2ctrl
from a2widget.flowlayout import FlowLayout
from a2widget.a2input_dialog import A2InputDialog


class A2TagField(QtWidgets.QWidget):
    changed = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(A2TagField, self).__init__(parent=parent)
        self.main_layout = FlowLayout(self)

        self.plus_button = QtWidgets.QToolButton()
        self.plus_menu = QtWidgets.QMenu(self)
        self.plus_button.setIcon(a2ctrl.Icons.inst().label_plus)
        self.plus_button.clicked.connect(self.build_plus_menu)
        self.main_layout.addWidget(self.plus_button)

        self._tags = []
        self._tags_backup = []
        self._tag_widgets = []
        self._available_tags = None

    def build_plus_menu(self):
        self.plus_menu.clear()
        label_icon = a2ctrl.Icons.inst().label
        self.plus_menu.addAction(a2ctrl.Icons.inst().label_plus, 'New Tag', self.create_tag)
        if self._available_tags:
            self.plus_menu.addSeparator()
            for tag in self._available_tags:
                if tag in self._tags:
                    continue
                self.plus_menu.addAction(label_icon, tag, partial(self.add, tag))

        self.plus_menu.popup(self.cursor().pos())

    def create_tag(self):
        dialog = A2InputDialog(self, 'Create New Tag', self.create_check)
        dialog.okayed.connect(self.add)
        dialog.show()

    def create_check(self, tag_name):
        if self.in_tags_already(tag_name):
            return 'In tags already!'
        return True

    def set_tags(self, these):
        """
        Replaces the saved tags with given ones.

        :param these: Tags to put.
        """
        if isinstance(these, str):
            these = [these]
        elif not isinstance(these, (tuple, list, set)):
            raise RuntimeError('Tag Field needs an iterable as tags')

        self.clear()
        self.add(these)

    def clear(self):
        for widget in self._tag_widgets:
            widget.deleteLater()
        self._tags = []
        self._check_changed()

    @property
    def value(self):
        return self._tags

    @value.setter
    def value(self, these):
        self.set_tags(these)

    def delete(self, tag_name):
        if tag_name not in self._tags:
            return

        i = self._tags.index(tag_name)
        widget = self._tag_widgets.pop(i)
        widget.deleteLater()
        self._tags.remove(tag_name)
        self._check_changed()

    def in_tags_already(self, tag_name):
        return tag_name in self._tags

    def add(self, tag_name, _emit_change=True):
        if self.in_tags_already(tag_name):
            return

        if isinstance(tag_name, (tuple, list, set)):
            for name in tag_name:
                self.add(name, _emit_change=False)
            return
        elif isinstance(tag_name, str):
            self._tags.append(tag_name)
            self._append_to_available(tag_name)

            widget = A2Tag(self, tag_name)
            widget.delete_requested.connect(self.delete)
            self._tag_widgets.append(widget)
            self.main_layout.addWidget(widget)

        self._check_changed()

    def _check_changed(self):
        sorted_tags = sorted(self._tags)
        if sorted_tags != self._tags_backup:
            self._tags_backup = sorted_tags
            self.changed.emit(self._tags)

    @property
    def available_tags(self):
        return self._available_tags

    def set_available_tags(self, these):
        """
        Connects the tag field to an iterable object
        """
        if not isinstance(these, (tuple, list, set, dict)):
            raise AttributeError('Available tags need to be set with an iterable! (list, tuple, set, dict)')

        self._available_tags = these

    def _append_to_available(self, tag_name):
        if tag_name in self._available_tags:
            return

        if isinstance(self._available_tags, list):
            self._available_tags.append(tag_name)
        elif isinstance(self._available_tags, set):
            self._available_tags.add(tag_name)
        elif isinstance(self._available_tags, dict):
            self._available_tags[tag_name] = tag_name.title()
        elif isinstance(self._available_tags, tuple):
            self._available_tags[tag_name] += (tag_name,)


class A2Tag(QtWidgets.QPushButton):
    delete_requested = QtCore.Signal(str)

    def __init__(self, parent, name):
        super(A2Tag, self).__init__(parent)
        self.name = name
        self.setIcon(a2ctrl.Icons.inst().label)
        self.setText(self.name)
        self.button_menu = None
        self.clicked.connect(self.build_menu)

    def build_menu(self):
        if self.button_menu is None:
            self.button_menu = QtWidgets.QMenu()
            self.button_menu.addAction(
                a2ctrl.Icons.inst().delete, 'Delete "%s"' % self.name, self.delete)
        self.button_menu.popup(self.cursor().pos())

    def delete(self):
        self.delete_requested.emit(self.name)


if __name__ == '__main__':
    import a2widget.demo.a2tag_field
    a2widget.demo.a2tag_field.show()
