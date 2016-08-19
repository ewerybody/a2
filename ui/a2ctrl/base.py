"""
a2ctrl.base

@created: Aug 3, 2016
@author: eRiC
"""
import time
import inspect
import threading
import logging
from copy import deepcopy
from functools import partial
from os.path import exists, join
from PySide import QtGui, QtCore, QtSvg

import a2core
from a2ctrl import PathField


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

ICO_PATH = None


class EditCtrl(QtGui.QGroupBox):
    """
    frame widget for an edit control which enables basic arrangement of the
    control up & down as well as deleting the control.

    It's made to work with handwritten and compiled Uis right away.
    To embedd a compiled ui tell it so addLayout=False in the super()-statement:
        super(MyNewCtrl, self).__init__(addLayout=False)
    state the mainWidget in setupUi:
        self.ui.setupUi(self.mainWidget)
    and then set the self.mainWidget-layout to your top layout in the compiled ui:
        self.mainWidget.setLayout(self.ui.mytoplayout)

    TODO: currently this is embedded as menuitems on a button which is pretty shitty.
        I'd like to have some actual up/down buttons and an x to indicate delete
        functionality
    """
    ctrlType = 'EditCtrl'

    def __init__(self, cfg, main, parentCfg, addLayout=True):
        super(EditCtrl, self).__init__()
        self.a2 = a2core.A2Obj.inst()
        self.cfg = cfg
        self.main = main
        self.parentCfg = parentCfg
        self._setupUi(addLayout)
        self.helpUrl = self.a2.urls.helpEditCtrl

    def move(self, value, *args):
        if self.parentCfg and self.parentCfg[0].get('typ', '') == 'nfo':
            top_index = 1
        else:
            top_index = 0

        index = self.parentCfg.index(self.cfg)
        maxIndex = len(self.parentCfg) - 1
        if isinstance(value, bool):
            if value:
                newindex = top_index
                #self.main.ui.scrollArea.scrollToTop()
                #self.main.ui.scrollArea
            else:
                newindex = maxIndex
                self.scroll_to_bottom()
        else:
            newindex = index + value
        # hop out if already at start or end
        if index == newindex or newindex < top_index or newindex > maxIndex:
            #print('returning from move! curr/new/max: %s/%s/%s' % (index, newindex, maxIndex))
            return

        #cfg = self.parentCfg.pop(index)
        self.parentCfg.pop(index)
        self.parentCfg.insert(newindex, self.cfg)
        self.main.editMod(keep_scroll=True)

    def delete(self):
        if self.cfg in self.parentCfg:
            self.parentCfg.remove(self.cfg)
            self.main.editMod(keep_scroll=True)

    def duplicate(self):
        newCfg = deepcopy(self.cfg)
        self.parentCfg.append(newCfg)
        self.main.editMod()
        self.scroll_to_bottom()

    def cut(self):
        self.main.edit_clipboard.append(deepcopy(self.cfg))
        self.delete()

    def help(self):
        a2core.surfTo(self.helpUrl)

    def _setupUi(self, addLayout):
        self.setTitle(self.cfg['typ'])
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        self.setSizePolicy(sizePolicy)
        self._ctrlLayout = QtGui.QHBoxLayout(self)
        self._ctrlLayout.setSpacing(0)
        self._ctrlLayout.setContentsMargins(0, 0, 0, 0)
        self.mainWidget = QtGui.QWidget(self)
        if addLayout:
            self.mainLayout = QtGui.QVBoxLayout()
            self.mainLayout.setContentsMargins(5, 5, 5, 5)
            self.mainWidget.setLayout(self.mainLayout)
        self._ctrlLayout.addWidget(self.mainWidget)

        self._ctrlButtonLayout = QtGui.QVBoxLayout()
        self._ctrlButtonLayout.setSpacing(0)
        self._ctrlButtonLayout.setContentsMargins(5, 0, 5, 5)
        self._ctrlButtonLayout.setObjectName("ctrlButtonLayout")

        self._ctrlButton = QtGui.QPushButton(self)
        self._ctrlButton.setMinimumSize(QtCore.QSize(40, 40))
        self._ctrlButton.setMaximumSize(QtCore.QSize(40, 40))
        self._ctrlButton.setText("...")
        self._ctrlButton.setFlat(True)
        self._ctrlButton.setObjectName("ctrlButton")
        self._ctrlButtonLayout.addWidget(self._ctrlButton)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Expanding)
        self._ctrlButtonLayout.addItem(spacerItem)
        self._ctrlLayout.addLayout(self._ctrlButtonLayout)
        self._ctrlLayout.setStretch(0, 1)

        self._ctrlMenu = QtGui.QMenu(self)
        self._ctrlMenu.aboutToShow.connect(self.buildMenu)
        self._ctrlButton.setMenu(self._ctrlMenu)

    def buildMenu(self):
        """
        TODO: don't show top/to top, bottom/to bottom when already at top/bottom
        """
        self._ctrlMenu.clear()
        icons = Icons.inst()
        menu_items = [('Up', partial(self.move, -1), icons.up),
                      ('Down', partial(self.move, 1), icons.down),
                      ('To Top', partial(self.move, True), icons.up_align),
                      ('To Bottom', partial(self.move, False), icons.down_align),
                      ('Delete', self.delete, icons.delete),
                      ('Duplicate', self.duplicate, icons.copy),
                      ('Help on %s' % self.ctrlType, self.help, icons.help)]

        clipboard_count = ''
        if self.main.edit_clipboard:
            clipboard_count = ' (%i)' % len(self.main.edit_clipboard)

        if self.ctrlType == 'Groupbox':
            menu_items.insert(-1, ('Paste' + clipboard_count, self.paste, icons.paste))
        else:
            menu_items.insert(-1, ('Cut' + clipboard_count, self.cut, icons.cut))

        for item in menu_items:
            if icons and len(item) == 3:
                action = QtGui.QAction(item[2], item[0], self._ctrlMenu, triggered=item[1])
            else:
                action = QtGui.QAction(item[0], self._ctrlMenu, triggered=item[1])
            self._ctrlMenu.addAction(action)

    def check_new_name(self):
        """
        If no name set yet, like on new controls this creates a new unique
        name for the control from the module name + control type + incremental number
        """
        if 'name' not in self.cfg:
            #build the base control name
            new_name = '%s_%s' % (self.main.mod.name, self.ctrlType)
            # find biggest number
            this_type = self.cfg['typ']
            controls = [cfg.get('name', '') for cfg in self.main.tempConfig
                        if cfg.get('typ') == this_type]
            number = len(controls)
            try_name = new_name + str(number)
            while try_name in controls:
                number += 1
                try_name = new_name + str(number)
            self.cfg['name'] = try_name

    def scroll_to_bottom(self):
        self._scrollValB4 = self.main.ui.scrollBar.value()
        self._scrollMaxB4 = self.main.ui.scrollBar.maximum()
        print('scroll_to_bottom...')
        #QtCore.QTimer.singleShot(300, self._scroll_to_bottom)
        threading.Thread(target=self._scroll_to_bottom).start()

    def _scroll_to_bottom(self, *args):
        print('scrollValB4: %s' % self._scrollValB4)
        time.sleep(0.1)
        tmax = 0.3
        curve = QtCore.QEasingCurve(QtCore.QEasingCurve.OutQuad)
        res = 0.01
        steps = tmax / res
        tsteps = 1 / steps
        t = 0.0
        #this = self.main.ui.scrollBar.value()
        scrollEnd = self.main.ui.scrollBar.maximum()
        print('scrollEnd: %s' % scrollEnd)
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


class Ico(QtGui.QIcon):
    def __init__(self, ico_name, px=512, scale=1.0, color=None):
        super(Ico, self).__init__()
        if exists(ico_name):
            self.path = ico_name
        else:
            global ICO_PATH
            if ICO_PATH is None:
                ICO_PATH = join(a2core.A2Obj.inst().paths.a2, 'ui', 'res', '%s.svg')
            self.path = ICO_PATH % ico_name
            if not exists(self.path):
                log.error('SVG_icon: could not find path to "%s"!' % ico_name)
                return

        renderer = QtSvg.QSvgRenderer(self.path)
        image = QtGui.QImage(QtCore.QSize(px, px), QtGui.QImage.Format_ARGB32)
        painter = QtGui.QPainter(image)

        if scale != 1.0:
            t = (px / 2) * (1 - scale)
            painter.translate(t, t)
            painter.scale(scale, scale)

        renderer.render(painter)

        if color:
            if isinstance(color, (int, float)):
                color = [int(color)] * 3
            if isinstance(color, (tuple, list)):
                color = QtGui.QColor(color[0], color[1], color[2])
            if isinstance(color, QtGui.QColor):
                painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
                painter.fillRect(image.rect(), color)
            else:
                log.error('Cannot use color: "%s"' % str(color))

        pixmap = QtGui.QPixmap.fromImage(image)
        self.addPixmap(pixmap)
        painter.end()


class Icons(object):
    _instance = None

    @staticmethod
    def inst():
        """
        :rtype: Icons
        """
        if Icons._instance is None:
            Icons._instance = Icons()
        return Icons._instance

    def __init__(self):
        self.a2 = Ico('a2')
        self.a2close = Ico('a2x')
        self.a2reload = Ico('a2reload')
        self.a2help = Ico('a2help')
        self.autohotkey = Ico('autohotkey')
        self.check = Ico('check')
        self.code = Ico('code')
        self.copy = Ico('copy')
        self.combo = Ico('combo')
        self.cut = Ico('cut')
        self.delete = Ico('delete')
        self.down = Ico('down')
        self.down_align = Ico('down_align')
        self.folder = Ico('folder')
        self.group = Ico('group')
        self.help = Ico('help')
        self.hotkey = Ico('keyboard')
        self.number = Ico('number')
        self.paste = Ico('paste')
        self.string = Ico('string')
        self.up = Ico('up')
        self.up_align = Ico('up_align')


def connect_cfg_controls(cfg, object_collection):
    """
    browses all members of the ui object to connect ones named 'cfg_'
    with the EditCtrls current cfg dict and fill it with current value.
    """
    for objname, control in inspect.getmembers(object_collection):
        if not objname.startswith('cfg_'):
            continue
        name = objname[4:]
        connect_control(control, name, cfg)


def connect_control(control, name, cfg, change_signal=None):
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
        # set ctrl according to config or set config from ctrl
        if name in cfg:
            control.setChecked(cfg[name])
        else:
            cfg[name] = control.isChecked()

    elif isinstance(control, QtGui.QLineEdit):
        control.textChanged.connect(partial(_updateCfgData, cfg, name))
        if name in cfg:
            control.setText(cfg[name])
        else:
            cfg[name] = control.text()

    elif isinstance(control, PathField):
        control.changed.connect(partial(_updateCfgData, cfg, name))
        if name in cfg:
            control.value = cfg[name]
        else:
            cfg[name] = control.value

    elif isinstance(control, QtGui.QComboBox):
        control.currentIndexChanged.connect(partial(_updateCfgData, cfg, name))
        if name in cfg:
            control.setCurrentIndex(cfg[name])
        else:
            cfg[name] = control.currentIndex()

    elif isinstance(control, QtGui.QListWidget):
        # so far only to fill the control
        #QtGui.QListWidget.c
        #control.itemChanged.connect(partial(_list_widget_test, name))
        if name in cfg:
            control.insertItems(0, cfg[name])
        else:
            items = [control.item(i).text() for i in range(control.count())]
            cfg[name] = items

    elif isinstance(control, (QtGui.QSpinBox, QtGui.QDoubleSpinBox)):
        control.valueChanged.connect(partial(_updateCfgData, cfg, name))
        if name in cfg:
            control.setValue(cfg[name])
        else:
            cfg[name] = control.value()

    elif isinstance(control, QtGui.QRadioButton):
        name, value = name.rsplit('_', 1)

        control.toggled.connect(partial(_radio_update, cfg, name, value))
        if name in cfg:
            control.setChecked(cfg[name] == value)
        elif control.isChecked():
            cfg[name] = value

    else:
        log.error('Cannot handle widget "%s"!\n  type "%s" NOT covered yet!' %
                  (name, type(control)))
