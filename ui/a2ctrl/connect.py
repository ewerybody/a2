"""
a2ctrl.connect
"""
import inspect
from functools import partial

from PySide import QtGui

import a2core
from a2widget import A2PathField, TextField_AutoHeight


log = a2core.get_logger(__name__)


def cfg_controls(cfg, ui_object, prefix='cfg_'):
    """
    browses all members of the given ui object to connect ones named with prefix
    ('cfg_' by default) with a config dict and fill it with current value.
    """
    for objname, ctrl in inspect.getmembers(ui_object):
        if not objname.startswith(prefix):
            continue
        name = objname[4:]
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


def control(ctrl, name, cfg, change_signal=None):
    """
    Connects a single control to a name in the given cfg dict
    """
    if isinstance(ctrl, QtGui.QCheckBox):
        # checkBox.clicked doesn't send state, so we put the func to check
        # checkBox.stateChanged does! But sends int: 0, 1, 2 for off, tri, on
        # solution: ctrl.clicked[bool] sends the state already!
        ctrl.clicked[bool].connect(partial(_updateCfgData, cfg, name))
        if change_signal is not None:
            ctrl.clicked[bool].connect(change_signal.emit)
        # set ctrl according to config or set config from ctrl
        if name in cfg:
            ctrl.setChecked(cfg[name])
        else:
            cfg[name] = ctrl.isChecked()

    elif isinstance(ctrl, (QtGui.QLineEdit)):
        ctrl.textChanged.connect(partial(_updateCfgData, cfg, name))
        if change_signal is not None:
            ctrl.textChanged[str].connect(change_signal.emit)
        if name in cfg:
            ctrl.setText(cfg[name])
        else:
            cfg[name] = ctrl.text()

    elif isinstance(ctrl, A2PathField):
        ctrl.changed.connect(partial(_updateCfgData, cfg, name))
        if change_signal is not None:
            ctrl.changed.connect(change_signal.emit)
        if name in cfg:
            ctrl.value = cfg[name]
        else:
            cfg[name] = ctrl.value

    elif isinstance(ctrl, QtGui.QComboBox):
        ctrl.currentIndexChanged.connect(partial(_updateCfgData, cfg, name))
        if change_signal is not None:
            ctrl.currentIndexChanged.connect(change_signal.emit)
        if name in cfg:
            ctrl.setCurrentIndex(cfg[name])
        else:
            cfg[name] = ctrl.currentIndex()

    elif isinstance(ctrl, QtGui.QListWidget):
        # so far only to fill the control
        # since it's not a widget that changes data by default
        # ctrl.itemChanged.connect(partial(_list_widget_test, name))
        if name in cfg:
            ctrl.insertItems(0, cfg[name])
        else:
            items = [ctrl.item(i).text() for i in range(ctrl.count())]
            cfg[name] = items

    elif isinstance(ctrl, (QtGui.QSpinBox, QtGui.QDoubleSpinBox)):
        ctrl.valueChanged.connect(partial(_updateCfgData, cfg, name))
        if change_signal is not None:
            ctrl.valueChanged.connect(change_signal.emit)
        if name in cfg:
            ctrl.setValue(cfg[name])
        else:
            cfg[name] = ctrl.value()

    elif isinstance(ctrl, QtGui.QRadioButton):
        name, value = name.rsplit('_', 1)
        ctrl.toggled.connect(partial(_radio_update, cfg, name, value))
        if change_signal is not None:
            ctrl.toggled.connect(change_signal.emit)
        if name in cfg:
            ctrl.setChecked(cfg[name] == value)
        elif ctrl.isChecked():
            cfg[name] = value

    elif isinstance(ctrl, (QtGui.QTextEdit, TextField_AutoHeight)):
        ctrl.textChanged.connect(partial(_text_edit_update, cfg, name, ctrl))
        if change_signal is not None:
            ctrl.textChanged.connect(partial(change_signal.emit, ctrl))
        if name in cfg:
            ctrl.setText(cfg[name])
        else:
            cfg[name] = ctrl.toPlainText()

    else:
        log.error('Cannot handle widget "%s"!\n  type "%s" NOT covered yet!' %
                  (name, type(ctrl)))


def _updateCfgData(cfg, name, value):
    """
    issued from a control change function this sets an according item in config dict
    """
    cfg[name] = value


def _radio_update(cfg, name, value, state):
    """
    almost same as _updateCfgData but dependent on a state bool arg
    """
    if state:
        cfg[name] = value


def _text_edit_update(cfg, name, ctrl):
    cfg[name] = ctrl.toPlainText()


def _text_edit_send(signal, ctrl):
    signal.emit(ctrl.toPlainText())
