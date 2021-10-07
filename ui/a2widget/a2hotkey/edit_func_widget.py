import os
import a2core
import a2util
from a2qt import QtGui, QtCore, QtWidgets
from a2widget.a2hotkey import edit_func_widget_ui
from a2widget.a2hotkey.hotkey_common import Vars, MOD_KEYS, SEND_MODES, strip_mode


class HelpLabels:
    cmds = 'Help on Autohotkey commands'
    run = 'Help on Autohotkey "Run"'
    send = 'Help on Autohotkey "Send"'
    vars = 'Help on Autohotkey Built-in Variables'


class FuncTypes:
    code = 'Run code'
    open = 'Open file/url'
    send = 'Send keystroke'


FUNCTIONS = {
    FuncTypes.code: Vars.function_code,
    FuncTypes.open: Vars.function_url,
    FuncTypes.send: Vars.function_send,
}


class FuncWidget(QtWidgets.QWidget):
    changed = QtCore.Signal()

    def __init__(self, parent):
        super(FuncWidget, self).__init__(parent)
        self._config_dict = None

        # update check done in parent widget for proper order
        self.ui = edit_func_widget_ui.Ui_FuncWidget()
        self.ui.setupUi(self)

        self.ui.function_text.text_changed.connect(self.on_input)
        self.ui.run_url.changed.connect(self.on_input)
        self.ui.function_send_mode.currentIndexChanged.connect(self.on_send_mode_change)

        self.ui.a2option_button.menu_called.connect(self.build_menu)

        self.a2 = None
        self.help_map = None

    def set_config(self, config_dict):
        self._config_dict = config_dict

    def build_menu(self, menu):
        self._build_help_map()

        index = self.ui.cfg_functionMode.currentIndex()
        if index == 0:
            # fsubmenu1 = self.menu.addMenu('local functions')
            # fsubmenu2 = self.menu.addMenu('built-in functions')
            menu.addAction(HelpLabels.cmds, self.surf_to_help)

        elif index == 1:
            for label, func in [
                ('Insert directory...', self.insert_dir),
                ('Insert file...', self.insert_file),
                (HelpLabels.run, self.surf_to_help),
            ]:
                menu.addAction(label, func)

        else:
            fsubmenu1 = menu.addMenu('Insert modifier key')
            for label in MOD_KEYS:
                fsubmenu1.addAction(label, self.insert_mod_key)

                # fsubmenu2 = self.menu.addMenu('built-in variables')
                # for var in []:
                #    action = QtGui.QAction(var, fsubmenu2, triggered=partial(self.set_sendmode, var))
                #    fsubmenu2.addAction(action)
            for label, func in [
                (HelpLabels.send, self.surf_to_help),
                (HelpLabels.vars, self.surf_to_help),
            ]:
                menu.addAction(label, func)

        menu.popup(QtGui.QCursor.pos())

    def insert_mod_key(self):
        key = self.sender().text()[0]
        self.ui.function_text.insertPlainText(key)

    def _build_help_map(self):
        if self.help_map is None:
            self.a2 = a2core.A2Obj.inst()
            urls = self.a2.urls
            self.help_map = {
                HelpLabels.cmds: urls.ahk_commands,
                HelpLabels.run: urls.ahk_run,
                HelpLabels.send: urls.ahk_send,
                HelpLabels.vars: urls.ahk_builtin_vars,
            }

    def surf_to_help(self):
        label = self.sender().text()
        url = self.help_map[label]
        a2util.surf_to(url)

    def insert_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Browsing for a directory ...')
        if directory:
            self.ui.run_url.insert(directory)

    def insert_file(self):
        # options = QtGui.QFileDialog.Options() | QtGui.QFileDialog.DontConfirmOverwrite
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Browsing for a file ...')
        if file_name:
            self.ui.run_url.insert(os.path.normpath(file_name))

    def on_send_mode_change(self):
        code = self.ui.function_text.text()
        self.on_input(code)

    def on_input(self, code):
        current = self.ui.cfg_functionMode.currentText()
        if current == FuncTypes.open:
            code = 'Run, ' + code

        elif current == FuncTypes.send:
            # If `code` is empty we SHOULD strip the whole thing but we also
            # detect the Send mode from it :/ This has to happen somewhere else!
            send_mode = self.ui.function_send_mode.currentText()
            code = '%s, %s' % (send_mode, code)

        self._config_dict[FUNCTIONS[current]] = code
        self.changed.emit()

    def set_function_text(self, current=None):
        if current is None:
            current = self.ui.cfg_functionMode.currentText()

        self.ui.run_label.setVisible(current == FuncTypes.open)
        self.ui.function_send_mode.setVisible(current == FuncTypes.send)
        self.ui.run_url.setVisible(current == FuncTypes.open)
        self.ui.function_text.setVisible(current != FuncTypes.open)

        text = self._config_dict.get(FUNCTIONS[current], '')
        text = self._strip_mode(text, current)
        if current == FuncTypes.open:
            self.ui.run_url.setText(text)
        else:
            self.ui.function_text.setText(text)

    def _strip_mode(self, text, current):
        """
        Remove `Run, ` or `Send*, ` to put it into the input field.
        """
        modes = {
            FuncTypes.open: ('run',),
            FuncTypes.send: SEND_MODES,
        }

        if current in (FuncTypes.open, FuncTypes.send):
            text, mode = strip_mode(text, modes[current])

            # set the send mode combobox
            if current == FuncTypes.send:
                for i in range(self.ui.function_send_mode.count()):
                    if self.ui.function_send_mode.itemText(i).lower() == mode:
                        self.ui.function_send_mode.setCurrentIndex(i)
                        break
        return text

    def showEvent(self, *args, **kwargs):
        self.set_function_text()
        self.ui.cfg_functionMode.currentTextChanged.connect(self.set_function_text)

        return QtWidgets.QWidget.showEvent(self, *args, **kwargs)


if __name__ == '__main__':
    import a2widget.demo.hotkey_func_demo

    a2widget.demo.hotkey_func_demo.show()
