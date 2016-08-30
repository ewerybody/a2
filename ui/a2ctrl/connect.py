"""
a2ctrl.connect
"""
import inspect
from functools import partial

from PySide import QtGui

import a2core
from a2ctrl.path_field import PathField


log = a2core.get_logger(__name__)


def cfg_controls(cfg, ui_object, prefix='cfg_'):
    """
    browses all members of the given ui object to connect ones named with prefix
    ('cfg_' by default) with a config dict and fill it with current value.
    """
    for objname, control in inspect.getmembers(ui_object):
        if not objname.startswith(prefix):
            continue
        name = objname[4:]
        control(control, name, cfg)


def control_list(controls, cfg, change_signal=None):
    """
    Connects a list of controls to their names in a given cfg dictionary
    """
    for ctrl in controls:
        control(ctrl, ctrl.objectName(), cfg, change_signal)


def control(control, name, cfg, change_signal=None):
    """
    Connects a single control to a name in the given cfg dict
    """
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

    if isinstance(control, QtGui.QCheckBox):
        # checkBox.clicked doesn't send state, so we put the func to check
        # checkBox.stateChanged does! But sends int: 0, 1, 2 for off, tri, on
        # solution: control.clicked[bool] sends the state already!
        control.clicked[bool].connect(partial(_updateCfgData, cfg, name))
        if change_signal is not None:
            control.clicked[bool].connect(change_signal.emit)
        # set ctrl according to config or set config from ctrl
        if name in cfg:
            control.setChecked(cfg[name])
        else:
            cfg[name] = control.isChecked()

    elif isinstance(control, QtGui.QLineEdit):
        control.textChanged.connect(partial(_updateCfgData, cfg, name))
        if change_signal is not None:
            control.textChanged.connect(change_signal.emit)
        if name in cfg:
            control.setText(cfg[name])
        else:
            cfg[name] = control.text()

    elif isinstance(control, PathField):
        control.changed.connect(partial(_updateCfgData, cfg, name))
        if change_signal is not None:
            control.changed.connect(change_signal.emit)
        if name in cfg:
            control.value = cfg[name]
        else:
            cfg[name] = control.value

    elif isinstance(control, QtGui.QComboBox):
        control.currentIndexChanged.connect(partial(_updateCfgData, cfg, name))
        if change_signal is not None:
            control.currentIndexChanged.connect(change_signal.emit)
        if name in cfg:
            control.setCurrentIndex(cfg[name])
        else:
            cfg[name] = control.currentIndex()

    elif isinstance(control, QtGui.QListWidget):
        # so far only to fill the control
        # since it's not a widget that changes data by default
        #control.itemChanged.connect(partial(_list_widget_test, name))
        if name in cfg:
            control.insertItems(0, cfg[name])
        else:
            items = [control.item(i).text() for i in range(control.count())]
            cfg[name] = items

    elif isinstance(control, (QtGui.QSpinBox, QtGui.QDoubleSpinBox)):
        control.valueChanged.connect(partial(_updateCfgData, cfg, name))
        if change_signal is not None:
            control.valueChanged.connect(change_signal.emit)
        if name in cfg:
            control.setValue(cfg[name])
        else:
            cfg[name] = control.value()

    elif isinstance(control, QtGui.QRadioButton):
        name, value = name.rsplit('_', 1)
        control.toggled.connect(partial(_radio_update, cfg, name, value))
        if change_signal is not None:
            control.toggled.connect(change_signal.emit)
        if name in cfg:
            control.setChecked(cfg[name] == value)
        elif control.isChecked():
            cfg[name] = value

    else:
        log.error('Cannot handle widget "%s"!\n  type "%s" NOT covered yet!' %
                  (name, type(control)))

