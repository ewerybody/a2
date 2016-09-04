"""
a2element.nfo

@created: Sep 3, 2016
@author: eRiC
"""
from PySide import QtGui, QtCore


class Draw(QtGui.QWidget):
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__()
        self.layout = QtGui.QVBoxLayout(self)
        self.label = QtGui.QLabel(self)
        self.label.setText(cfg.get('description') or '')
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)


class Edit(QtGui.QGroupBox):
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__()
        self.cfg = cfg
        self.typ = cfg['typ']
        self.setTitle('module information:')
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                             QtGui.QSizePolicy.Maximum))
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(5, 5, 5, 10)
        self.description = EditText('description', cfg.get('description'), self.layout, self.getCfg)
        self.author = EditLine('author', cfg.get('author'), self.layout, self.getCfg)
        self.version = EditLine('version', cfg.get('version'), self.layout, self.getCfg)
        self.date = EditLine('date', cfg.get('date'), self.layout, self.getCfg)
        self.url = EditLine('url', cfg.get('url') or '', self.layout, self.getCfg)

    def getCfg(self):
        self.cfg['description'] = self.description.value
        self.cfg['author'] = self.author.value
        self.cfg['version'] = self.version.value
        self.cfg['date'] = self.date.value
        self.cfg['url'] = self.url.value
        return self.cfg


class EditLine(QtGui.QWidget):
    def __init__(self, name, text, parentLayout=None, updatefunc=None):
        super(EditLine, self).__init__()
        global labelW
        self.name = name
        self.updatefunc = updatefunc
        self.parentLayout = parentLayout
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setSpacing(5)
        self.labelCtrl = QtGui.QLabel('%s:' % name)
        self.labelCtrl.setAlignment(QtCore.Qt.AlignRight)
        self.layout.addWidget(self.labelCtrl)
        self.inputCtrl = QtGui.QLineEdit()
        self.inputCtrl.setText(str(text))
        self.inputCtrl.textChanged.connect(self.update)
        self.layout.addWidget(self.inputCtrl)
        if parentLayout:
            parentLayout.addWidget(self)

    def update(self):
        if self.updatefunc:
            self.updatefunc()

    @property
    def value(self):
        return self.inputCtrl.text()


class EditText(QtGui.QWidget):
    def __init__(self, name, text, parent=None, updatefunc=None):
        super(EditText, self).__init__()
        global labelW, lenL
        self.name = name
        self.parent = parent
        self.updatefunc = updatefunc
        self.baselayout = QtGui.QVBoxLayout(self)
        self.baselayout.setSpacing(5)
        #self.labelCtrl = QtGui.QLabel('%s:' % name)
        #self.baselayout.addWidget(self.labelCtrl)
        self.inputCtrl = QtGui.QPlainTextEdit()
        self.inputCtrl.setPlainText(str(text))
        self.inputCtrl.setTabChangesFocus(True)
        self.inputCtrl.textChanged.connect(self.update)
        self.baselayout.addWidget(self.inputCtrl)
        if parent:
            parent.addWidget(self)

    def update(self):
        if self.updatefunc:
            self.updatefunc()

    @property
    def value(self):
        return self.inputCtrl.toPlainText()


def get_settings(module_key, cfg, db_dict, user_cfg):
    raise NotImplementedError('Settings for nfo are never fetched!')
