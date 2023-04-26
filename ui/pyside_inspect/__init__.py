import os
import sys
import inspect
import logging
from .pyside import QtWidgets, QtCore, QtGui, qt_docs_url

WA_TRANSP4MOUSE = QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
log = logging.getLogger(__name__)


class InspectMode(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self._last_widget = None
        self._widget = None  # type: None | QtWidgets.QWidget
        self._last_cursor_pos = None
        self._app = parent.a2.app
        self._ui_map = {}
        self._stack = []

        self.setGeometry(parent.geometry())
        # self.setStyleSheet('border: 2px dashed white;' 'background-color: transparent;')
        # self.setAttribute(WA_TRANSP4MOUSE, True)
        flags = self.windowFlags()
        # flags |= QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
        flags |= QtCore.Qt.WindowType.FramelessWindowHint
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.highlight = Highlight(self)
        self.highlight.clicked.connect(self.highlight_click)
        self.highlight.hide()
        # self.highlight.under_cursor.connect(self._on_highlighter_update)

        # self.escape_shortcut = QtGui.QShortcut(
        #     QtGui.QKeySequence(QtCore.Qt.Key_Dow), self, self.close
        # )
        # self.escape_shortcut.setContext(QtCore.Qt.ApplicationShortcut)
        shortcut = QtGui.QShortcut(self)
        shortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key.Key_Escape))
        shortcut.activated.connect(self.close)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.check)
        self.timer.start()
        self.installEventFilter(self)
        self.show()

        self.enable_timer = QtCore.QTimer(self)
        self.enable_timer.timeout.connect(self.enable_click)
        self.enable_timer.setInterval(500)
        self._enabled = True

        # thread = UiCrawler(self)
        # thread.finished.connect(self.update_ui_map)
        # thread.finished.connect(thread.deleteLater)
        # thread.start()
        self._ui_map = get_ui_map()
        self._ui_map

    def disable_click(self):
        if self._enabled:
            self._enabled = False
            self.setAttribute(WA_TRANSP4MOUSE, True)
            self.highlight.set_highlighted(False)

    def enable_click(self):
        if not self._enabled:
            self._enabled = True
            self.setAttribute(WA_TRANSP4MOUSE, False)
            self.highlight.set_highlighted(True)
            self.activateWindow()

            test = self.testAttribute(WA_TRANSP4MOUSE)
            print('WA_TRANSP4MOUSE: %s' % test)

            print(
                'highlight under cursor: %s'
                % (self._app.widgetAt(QtGui.QCursor.pos()) is self.highlight)
            )

    # def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
    #     print('event.pos(): %s' % event.pos())
    #     self.disable_click()
    #     self.enable_timer.start()
    #     return super().mouseMoveEvent(event)

    # def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
    #     return super().mousePressEvent(event)

    def check(self):
        cursor_pos = QtGui.QCursor.pos()
        if cursor_pos == self._last_cursor_pos:
            self.setAttribute(WA_TRANSP4MOUSE, False)
            self.highlight.setAttribute(WA_TRANSP4MOUSE, False)
            self.enable_click()
            self.enable_timer.stop()
            return

        self._last_cursor_pos = cursor_pos
        widget = self._app.widgetAt(cursor_pos)
        if widget is self or widget is self.highlight:
            print('widget is self')
            self.setAttribute(WA_TRANSP4MOUSE, True)
            return
        if widget is None:
            # print('widget is None')
            return
        if widget == self._widget:
            print('widget is OLD widget')
            return
        self.enable_timer.start()
        self.disable_click()

        self._widget = widget
        # print('self._widget: %s' % self._widget)

        geometry = widget.geometry()
        geometry.moveTopLeft(self.mapFromGlobal(widget.mapToGlobal(QtCore.QPoint(0, 0))))
        self.highlight.set_geo(geometry)

    def close(self):
        self._enabled = False
        self.timer.stop()
        self.highlight.deleteLater()
        super().close()

    def highlight_click(self):
        if self._widget is None:
            return

        self._enabled = False
        self.timer.stop()
        menu = QtWidgets.QMenu(self)

        self._stack.clear()
        depth = 0
        obj = self._widget
        name = self._widget.objectName()
        qt_classes = []

        while obj is not None:
            print('widget: %s' % obj)
            print('  class: %s' % obj.__class__)
            mod_name = obj.__class__.__module__
            obj_class = obj.__class__.__name__
            print('  module: %s' % mod_name)
            mod = sys.modules[mod_name]
            if mod.__file__ is not None and not mod.__file__.endswith('.pyd'):
                self._scan_file(mod.__file__, obj)
            if mod in (QtWidgets, QtGui):
                class_name = '%s.%s' % (mod.__name__.split('.')[-1], obj_class)
                if class_name not in qt_classes:
                    qt_classes.append(class_name)

            self._stack.append(obj)
            obj = obj.parent()

            depth += 1
            if depth > 100:
                break

        for class_name in qt_classes:
            module_short_name, obj_class = class_name.split('.', 1)
            action = menu.addAction(f'Browse "{obj_class}" Qt for Python docs', self._browse_qt_docs)
            action.setData((module_short_name, obj_class))

        if menu.isEmpty():
            log.error('Nothing in the highligter menu!')
            return

        self.close()
        menu.popup(QtGui.QCursor.pos())

    def _scan_file(self, path, obj):
        print(f'scanning: {path}...')

        with open(path) as file_obj:
            mod_lines = file_obj.read().split('\n')

        search_var = ''
        name = obj.objectName()

        for i, line in enumerate(mod_lines):
            if name:
                if name not in line or line in ('"""', "'''") or line.lstrip().startswith('#'):
                    continue
                pos = line.find(name)
                quote = line[pos - 1]
                if not quote in '\'"' or line[pos + len(name)] != quote:
                    continue

                if 'setObjectName' in line:
                    opos = line.find('setObjectName')
                else:
                    left = line[: pos - 1].strip()
                    if left[-1] != '=':
                        continue
                    left = left[:-1].rstrip()

        # with open(mod.__file__) as fobj:
        #     content = fobj.read()

    def update_ui_map(self):
        thread = self.sender()
        if not isinstance(thread, UiCrawler):
            return
        self._ui_map.clear()
        self._ui_map.update(thread.get_ui_map())

    def _browse_qt_docs(self):
        action = self.sender()
        if not isinstance(action, QtGui.QAction):
            return
        import webbrowser

        module_name, class_name = action.data()
        webbrowser.open(qt_docs_url.format(mod=module_name, cls=class_name))

    # def _on_highlighter_update(self, under_cursor: bool):
    #     print('under_cursor: %s' % under_cursor)
    #     self.setAttribute(WA_TRANSP4MOUSE, not under_cursor)
    #     # self.setAttribute(WA_TRANSP4MOUSE, False)


class Highlight(QtWidgets.QPushButton):
    under_cursor = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.highlight.setAttribute(WA_TRANSP4MOUSE)
        self.setStyleSheet(
            'border: 2px dashed red; border-radius: 5px; background-color: transparent;'
        )
        flags = self.windowFlags()
        flags |= QtCore.Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        # self.setText('Press me!')

    def set_geo(self, geometry):
        self.show()
        # geometry = widget.geometry()
        # geometry.moveTopLeft(self.mapFromGlobal(widget.mapToGlobal(QtCore.QPoint(0, 0))))
        self.setGeometry(geometry)

    def set_highlighted(self, state):
        if state:
            self.setStyleSheet(
                'border: 2px dashed red; border-radius: 5px; background-color: rgba(50,0,0,40)'
            )
            self.setFocus()
        else:
            self.setStyleSheet(
                'border: 2px dashed red; border-radius: 5px; background-color: transparent;'
            )

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self.under_cursor.emit(False)
        return super().leaveEvent(event)

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:
        self.under_cursor.emit(True)
        return super().enterEvent(event)


class UiCrawler(QtCore.QThread):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._ui_map = {}

    def get_ui_map(self):
        return self._ui_map

    def run(self):
        self._ui_map = get_ui_map()


def get_ui_map():
    from . import pyside

    layouts_mods = {}
    side_mod_names = [pyside.NAME + '.' + mod for mod in pyside.__all__]
    stdlib = os.path.normcase(os.path.join(os.path.dirname(sys.executable), 'lib'))

    # loop over list to prevent RuntimeError: dictionary changed size during iteration
    for mod in list(sys.modules.values()):
        if not hasattr(mod, '__spec__'):
            continue
        if mod.__spec__ is None or mod.__spec__.origin in ('built-in', 'frozen'):
            continue
        if mod.__spec__.origin is None or os.path.normcase(mod.__spec__.origin).startswith(stdlib):
            continue
        if mod.__spec__.origin.endswith('.pyd'):
            continue
        for name, member in inspect.getmembers(mod, inspect.isclass):
            if not hasattr(member, 'setupUi'):
                continue
            layouts_mods.setdefault(mod, []).append(member)
    return layouts_mods


if __name__ == '__main__':
    pass
