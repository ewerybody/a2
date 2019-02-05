import inspect
from functools import partial

from PySide2 import QtWidgets

import a2core
import a2widget


log = a2core.get_logger(__name__)


def cfg_controls(cfg, ui_object, prefix='cfg_'):
    """
    browses all members of the given ui object to connect ones named with prefix
    ('cfg_' by default) with a config dict and fill it with current value.
    """
    for name, ctrl in [(objname[len(prefix):], ctrl) for objname, ctrl
                       in inspect.getmembers(ui_object)
                       if objname.startswith(prefix)]:
        control(ctrl, name, cfg)


def control_list(controls, cfg, change_signal=None):
    """
    Connects a list of controls to their names in a given cfg dictionary
    """
    for ctrl in controls:
        object_name = ctrl.objectName()
        if not object_name:
            raise RuntimeError('Cannot connect widget without objectName!\n  '
                               'Please do "widget.setObjectName(\'attribname\')"')
        control(ctrl, ctrl.objectName(), cfg, change_signal)


def control(ctrl, name, cfg, change_signal=None, trigger_signal=None):
    """
    Connects a single control to a name in the given cfg dict

    :param QWidget ctrl: The Qt object to work on.
    :param str name: The key name to look for in the dict.
    :param dict cfg: The whole config dictionary object to connect to.
    :param QtCore.Signal change_signal: Optional. A signal to emit on change.
    :param QtCore.Signal trigger_signal: Optional. The signal get the change event from.
    """
    if isinstance(ctrl, QtWidgets.QCheckBox):
        # checkBox.clicked doesn't send state, so we put the func to check
        # checkBox.stateChanged does! But sends int: 0, 1, 2 for off, tri, on
        # solution: ctrl.clicked[bool] sends the state already!
        ctrl.clicked[bool].connect(partial(_update_cfg_data, cfg, name))
        if change_signal is not None:
            ctrl.clicked[bool].connect(change_signal.emit)
        # set ctrl according to config or set config from ctrl
        if name in cfg:
            ctrl.setChecked(cfg[name])
        else:
            cfg[name] = ctrl.isChecked()

    elif isinstance(ctrl, (QtWidgets.QLineEdit, a2widget.A2ButtonField)):
        ctrl.textChanged.connect(partial(_update_cfg_data, cfg, name))
        if change_signal is not None:
            ctrl.textChanged[str].connect(change_signal.emit)
        if name in cfg:
            ctrl.setText(cfg[name])
        else:
            cfg[name] = ctrl.text()

    elif isinstance(ctrl, (a2widget.A2CoordsField,
                           a2widget.A2TagField,
                           a2widget.A2PathField)):
        ctrl.changed.connect(partial(_update_cfg_data, cfg, name))
        if change_signal is not None:
            ctrl.changed.connect(change_signal.emit)
        if name in cfg:
            ctrl.value = cfg[name]
        else:
            cfg[name] = ctrl.value

    elif isinstance(ctrl, QtWidgets.QComboBox):
        ctrl.currentIndexChanged.connect(partial(_update_cfg_data, cfg, name))
        if change_signal is not None:
            ctrl.currentIndexChanged.connect(change_signal.emit)
        if name in cfg:
            ctrl.setCurrentIndex(cfg[name])
        else:
            cfg[name] = ctrl.currentIndex()

    elif isinstance(ctrl, QtWidgets.QListWidget):
        # so far only to fill the control
        # since it's not a widget that changes data by default
        # ctrl.itemChanged.connect(partial(_list_widget_test, name))
        if name in cfg:
            ctrl.insertItems(0, cfg[name])
        else:
            items = [ctrl.item(i).text() for i in range(ctrl.count())]
            cfg[name] = items

    elif isinstance(ctrl, (QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox)):
        ctrl.valueChanged.connect(partial(_update_cfg_data, cfg, name))
        if change_signal is not None:
            ctrl.valueChanged.connect(change_signal.emit)
        if name in cfg:
            ctrl.setValue(cfg[name])
        else:
            cfg[name] = ctrl.value()

    elif isinstance(ctrl, QtWidgets.QRadioButton):
        name, value = name.rsplit('_', 1)
        # try to cast the value to int like its commonly used in the configs
        try:
            value = int(value)
        except ValueError:
            pass

        ctrl.toggled.connect(partial(_radio_update, cfg, name, value))
        if change_signal is not None:
            ctrl.clicked[bool].connect(change_signal.emit)
        if name in cfg:
            ctrl.setChecked(cfg[name] == value)
        elif ctrl.isChecked():
            cfg[name] = value

    elif isinstance(ctrl, (QtWidgets.QTextEdit, a2widget.A2TextField, a2widget.A2CodeField)):
        # For if a not immediate change signal is wanted
        # TODO: Do this for the other ctrl types
        if trigger_signal is None:
            trigger_signal = ctrl.textChanged

        trigger_signal.connect(partial(_text_edit_update, cfg, name, ctrl))
        if change_signal is not None:
            trigger_signal.connect(partial(change_signal.emit, ctrl))
        if name in cfg:
            ctrl.setText(cfg[name])
        else:
            cfg[name] = ctrl.toPlainText()

    else:
        log.error('Cannot handle widget "%s"!\n  type "%s" NOT covered yet!' %
                  (name, type(ctrl)))


def _update_cfg_data(cfg, name, value):
    """
    issued from a control change function this sets an according item in config dict
    """
    cfg[name] = value


def _radio_update(cfg, name, value, state):
    """
    almost same as _update_cfg_data but dependent on a state bool arg
    """
    if state:
        cfg[name] = value


def _text_edit_update(cfg, name, ctrl):
    cfg[name] = ctrl.toPlainText()


def _text_edit_send(signal, ctrl):
    signal.emit(ctrl.toPlainText())


def control_to_db(widget, db, key, default_value=None):
    """
    Only for direct connections to the default db table.

    :param QtWidgets.QWidget widget: Some Qt Widget to connect to.
    """
    if isinstance(widget, QtWidgets.QCheckBox):
        _connect_checkbox_to_db(widget, db, key, default_value)


def _connect_checkbox_to_db(widget, db, key, default_value):
    if default_value is None:
        default_value = False

    def _db_setter(value, db_object=db, setting_key=key, *args):
        db_object.set(setting_key, value)
        value = db_object.get(setting_key)

    widget.setChecked(db.get(key) or default_value)
    widget.clicked[bool].connect(_db_setter)
