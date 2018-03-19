import a2ctrl
import a2util
from PySide import QtGui, QtCore
from a2widget import a2module_source_ui


MOD_COUNT_TEXT = '%i modules, %i enabled'


class ModSourceWidget(QtGui.QWidget):
    toggled = QtCore.Signal()

    def __init__(self, mod_source, enabled_list):
        super(ModSourceWidget, self).__init__()
        self.mod_source = mod_source

        a2ctrl.check_ui_module(a2module_source_ui)
        self.ui = a2module_source_ui.Ui_Form()
        self.ui.setupUi(self)

        self.ui.frame.setVisible(False)
        m = 1
        self.ui.modsource_layout.setContentsMargins(m, m, m, m)

        self.ui.check.setText(mod_source.name)
        self.ui.check.setChecked(mod_source.name in enabled_list)
        self.ui.check.clicked[bool].connect(mod_source.toggle)
        self.ui.check.clicked.connect(self.toggled.emit)

        self.ui.mod_count.setText(MOD_COUNT_TEXT % (mod_source.mod_count, mod_source.enabled_count))
        self.ui.tool_button.clicked.connect(self.toggle_details)

        self.ui.version_label.setText(mod_source.config.get('version', 'x.x.x'))
        self.ui.maintainer_label.setText(mod_source.config.get('maintainer', ''))
        self.ui.description_label.setText(mod_source.config.get('description', ''))
        self.ui.local_path.writable = False
        self.ui.local_path.value = mod_source.path

        url = mod_source.config.get('url', '')
        url_label = url
        for url_sceme in ['http://', 'https://']:
            if url_label.startswith(url_sceme):
                url_label = url_label[len(url_sceme):]
                break
        if url_label.startswith('www.'):
            url_label = url_label[4:]
        self.ui.homepage_label.setText('<a href="%s">%s</a>' % (url, url_label))

    def build_menu(self):
        self.menu.clear()
        self.menu.addAction(QtGui.QAction('Details...', self, triggered=self.show_details))
        self.menu.addAction(QtGui.QAction('Explore to ...', self, triggered=self.explore_source))

    def show_details(self):
        raise NotImplementedError('Module Source Dialog tbd...')

    def explore_source(self):
        a2util.explore(self.mod_source.path)

    def toggle_details(self):
        state = self.ui.frame.isVisible()
        self.ui.frame.setVisible(not state)
        a = [QtCore.Qt.DownArrow, QtCore.Qt.RightArrow]
        self.ui.tool_button.setArrowType(a[state])
