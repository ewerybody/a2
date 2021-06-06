import a2uic
import a2ctrl

from a2qt import QtCore, QtWidgets

from a2widget.a2path_field import A2PathField
from a2element import pathlist_edit_ui, DrawCtrlMixin, EditCtrl


class Draw(QtWidgets.QGroupBox, DrawCtrlMixin):
    def __init__(self, main, cfg, mod, user_cfg):
        super(Draw, self).__init__(main)
        DrawCtrlMixin.__init__(self, main, cfg, mod, user_cfg)

        self.setTitle(self.cfg.get('label', ''))
        self.setCheckable(False)

        self.a2_group_layout = QtWidgets.QVBoxLayout(self)

        self.path_widgets = []
        for path in self.get_user_value(list, default=['']):
            self.add_path(path)

    def add_path(self, path=''):
        """Add a path widget to the list."""
        path_widget = PathEntry(
            self, self.a2_group_layout.count() + 1, self.cfg.get('browse_type', 0), path
        )
        path_widget.changed.connect(self.check)
        path_widget.add_path.connect(self.add_path)
        path_widget.delete_me.connect(self._on_path_removed)
        self.a2_group_layout.addWidget(path_widget)
        self.path_widgets.append(path_widget)

    def _on_path_removed(self):
        del_widget = self.sender()
        self.path_widgets.remove(del_widget)

        # fix index labels
        for index, widget in enumerate(self.path_widgets):
            widget.set_label(index + 1)

        # avoid check when path was empty
        if del_widget.path:
            self.check()

    def check(self, *_args):
        path_list = [w.path for w in self.path_widgets if w.path]
        self.set_user_value(path_list)
        self.change('variables')


class Edit(EditCtrl):
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)

        a2uic.check_module(pathlist_edit_ui)
        self.ui = pathlist_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

    @staticmethod
    def element_name():
        """The elements display name shown in UI"""
        return 'Pathlist'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.check


class PathEntry(QtWidgets.QWidget):
    """A single line widget for each entry in the ui"""

    changed = QtCore.Signal(str)
    delete_me = QtCore.Signal()
    add_path = QtCore.Signal()

    def __init__(self, parent, index, browse_type, path=''):
        super(PathEntry, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._label = QtWidgets.QLabel(str(index))
        layout.addWidget(self._label)
        self._field = A2PathField(self, path, writable=False)
        self._field.browse_type = browse_type
        self._field.changed.connect(self.changed.emit)
        layout.addWidget(self._field)

        button = QtWidgets.QToolButton(self)
        button.setAutoRaise(True)
        if index == 1:
            button.setIcon(a2ctrl.Icons.folder_add)
            button.clicked.connect(self.add_path.emit)
        else:
            button.setIcon(a2ctrl.Icons.clear)
            button.clicked.connect(self.delete)
        layout.addWidget(button)

    @property
    def path(self):
        """
        Holds the path of the widget
        :rtype: str
        """
        return self._field.value

    def set_label(self, value):
        self._label.setText(str(value))

    def delete(self):
        """Tell Qt and parent widget to delete this one."""
        self.deleteLater()
        self.delete_me.emit()

    def __repr__(self, *args, **kwargs):
        return '<PathEntry "%s" at %s>' % (self.path, id(self))


def get_settings(_module_key, cfg, db_dict, user_cfg):
    db_dict.setdefault('variables', {})
    value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=list, default=[])
    db_dict['variables'][cfg['name']] = value
